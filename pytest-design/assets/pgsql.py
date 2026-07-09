"""Copy-ready surrogate `tests/conftest.py` for a `SQLAlchemy 2.0` + `psycopg` async `PostgreSQL` stack.

Copy this file to `tests/conftest.py` and adapt the `app.*` imports and the `Faker`
locale list. Import-time patches MUST stay at the top, before any model module is
imported. This is a template, not a drop-in module; tune paths and seeds locally.
"""

import gc
import logging
import os
import random
import sqlite3
import uuid
from collections.abc import AsyncGenerator
from typing import Any

import pytest
import pytest_asyncio
import sqlalchemy as sa
import sqlalchemy.dialects.postgresql as pg_dialect
from faker import Faker
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.sql import sqltypes

# ── 1. Import-time patches (save originals) ─────────────────
_ORIG_JSONB = pg_dialect.JSONB
pg_dialect.JSONB = sa.JSON

_ORIG_UUID_BIND_PROCESSOR = sqltypes.Uuid.bind_processor


def _patched_uuid_bind_processor(self, dialect):
    def process(value):
        if value is None:
            return None
        if isinstance(value, str):
            return value
        if isinstance(value, uuid.UUID):
            return str(value)
        return value
    return process


sqltypes.Uuid.bind_processor = _patched_uuid_bind_processor

try:
    import psycopg.errors
    _ORIG_PSYCOPG_UNIQUE_VIOLATION = psycopg.errors.UniqueViolation
    psycopg.errors.UniqueViolation = sqlite3.IntegrityError
except Exception:
    _ORIG_PSYCOPG_UNIQUE_VIOLATION = None


def _restore_import_time_patches() -> None:
    pg_dialect.JSONB = _ORIG_JSONB
    sqltypes.Uuid.bind_processor = _ORIG_UUID_BIND_PROCESSOR
    if _ORIG_PSYCOPG_UNIQUE_VIOLATION is not None:
        psycopg.errors.UniqueViolation = _ORIG_PSYCOPG_UNIQUE_VIOLATION


@pytest.fixture(scope="session", autouse=True)
def _restore_patches_after_session() -> None:
    yield
    _restore_import_time_patches()


# ── 2. Imports that may load models (after patches) ─────────
from app import storages
from app.storages import sqlalchemy_postgres
from app.storages.sqlalchemy_postgres import db


# ── 3. Seeded fake fixture ──────────────────────────────────
@pytest.fixture(scope="session")
def fake(pytestconfig: pytest.Config) -> Faker:
    fake = Faker(["en_US", "ja_JP", "de_DE"])
    seed = getattr(pytestconfig.option, "randomly_seed", None)
    if seed is None:
        seed = int(os.environ.get("PYTEST_FAKER_SEED", random.randint(0, 2**32)))
        logging.getLogger("faker").info("Faker seed: %s", seed)
    fake.seed_instance(seed)
    return fake


# ── 4. db_session fixture ───────────────────────────────────
@pytest_asyncio.fixture(scope="function")
async def db_session(tmp_path: Any) -> AsyncGenerator[AsyncSession, None]:
    db_path = tmp_path / "test.db"
    dsn = f"sqlite+aiosqlite:///{db_path}"
    engine = create_async_engine(dsn, poolclass=sa.pool.NullPool)

    orig_get_dsn = db.get_dsn
    orig_get_ssl = db.get_ssl_options
    orig_session = db.Session
    orig_tr_manager = storages.StorageFactory.tr_manager

    db.get_dsn = lambda: dsn
    db.get_ssl_options = dict

    from app.storages.sqlalchemy_postgres.transaction_manager import TransactionManager
    storages.StorageFactory.tr_manager = TransactionManager()

    stripped_indexes: list[tuple[Any, Any]] = []
    for table in sqlalchemy_postgres.BaseModel.metadata.tables.values():
        for idx in list(table.indexes):
            if idx.dialect_options.get("postgresql", {}).get("where") is not None:
                stripped_indexes.append((table, idx))
                table.indexes.discard(idx)

    async with engine.begin() as conn:
        await conn.run_sync(sqlalchemy_postgres.BaseModel.metadata.create_all)
        nested_trans = await conn.begin_nested()
        session_maker = async_sessionmaker(bind=conn, expire_on_commit=False)
        session = session_maker()
        db.Session = lambda: session

        try:
            yield session
        finally:
            await nested_trans.rollback()
            await session.close()
            await engine.dispose()

            db.Session = orig_session
            db.get_dsn = orig_get_dsn
            db.get_ssl_options = orig_get_ssl
            storages.StorageFactory.tr_manager = orig_tr_manager

            for table, idx in stripped_indexes:
                table.indexes.add(idx)

            gc.collect()


# ── 5. add_item helper (flush + refresh, no commit) ─────────
@pytest_asyncio.fixture
def add_item(db_session: AsyncSession):
    async def _factory(item):
        db_session.add(item)
        await db_session.flush()
        await db_session.refresh(item)
        return item
    return _factory

---
---

# Collections

Keep dict, set, and sequence operations idiomatic: direct membership, sensible defaults, literal construction, and intentional commas.

## Rule of thumb

1. Let the dict do the work: use `get`, `items`, and direct membership; avoid manual key checks, `.keys()`, and `zip(dict.keys(), dict.values())`.
2. Remove keys safely with `pop(key, None)` and drop truthiness checks around `get()` when the default `None` is enough.
3. Build collections idiomatically: unpack iterables into literals, use `defaultdict(factory)`, and pass only meaningful arguments to `deque`.
4. Match the iteration type to the intent: sequences for ordered literals, `items()` for key-value pairs, and never iterate over a literal set.
5. Keep trailing commas intentional: add them on the last multiline item, remove them from single-line literals and bare tuple expressions.
6. Avoid runtime work for constant data: write list/set/dict literals directly and do not split static strings.
7. Slice once: use `maxsplit=1` or `rsplit` when only one end of a string is needed, and mutate `os.environ` item-by-item rather than reassigning it.

## Example: Config loader

A configuration helper that manually probes the dict, mis-slices the endpoint, and reassigns `os.environ`.

### Bad

```python
import os


def build_config():
    os.environ = {"APP_MODE": "prod"}  # B003

    config = {"debug": True, "timeout": 30, "log_level": "INFO", "retry": True, "feature": False}
    endpoint = "api.example.com"

    debug = "debug" in config.keys()  # SIM118

    timeout = config["timeout"] if "timeout" in config else 60  # SIM401

    host = endpoint.split(".")[0]  # PLC0207
    tld = endpoint.split(".")[-1]  # PLC0207

    if "retry" in config and config["retry"]:  # RUF019
        retry = True

    level = config.get("log_level", None)  # SIM910

    pairs = []
    for key, value in zip(config.keys(), config.values()):  # SIM911
        pairs.append(f"{key}={value}")

    if "old_key" in config:
        del config["old_key"]  # RUF051

    if config.get("feature", False):  # RUF056
        feature = True

    return {
        "debug": debug,
        "timeout": timeout,
        "host": host,
        "tld": tld,
        "retry": retry,
        "level": level,
        "pairs": pairs,
        "feature": feature,
    }
```

### Good

```python
import os


def build_config():
    os.environ.clear()
    os.environ["APP_MODE"] = "prod"

    config = {"debug": True, "timeout": 30, "log_level": "INFO", "retry": True, "feature": False}
    endpoint = "api.example.com"

    debug = "debug" in config

    timeout = config.get("timeout", 60)

    host = endpoint.split(".", maxsplit=1)[0]
    tld = endpoint.rsplit(".", maxsplit=1)[-1]

    if config.get("retry"):
        retry = True

    level = config.get("log_level")

    pairs = [f"{key}={value}" for key, value in config.items()]

    config.pop("old_key", None)

    if config.get("feature"):
        feature = True

    return {
        "debug": debug,
        "timeout": timeout,
        "host": host,
        "tld": tld,
        "retry": retry,
        "level": level,
        "pairs": pairs,
        "feature": feature,
    }
```

### Violations

1. **B003** — `os.environ = {"APP_MODE": "prod"}`; reassigning `os.environ` does not clear the inherited environment.
2. **PLC0207** — `endpoint.split(".")[0]` and `endpoint.split(".")[-1]`; splitting the whole string is wasteful when only one end is used.
3. **RUF019** — `if "retry" in config and config["retry"]; use `config.get("retry")` to test safely.
4. **RUF051** — `del config["old_key"]; use config.pop("old_key", None) instead.
5. **RUF056** — `if config.get("feature", False)`; the default fallback `None` is already falsy.
6. **SIM118** — `"debug" in config.keys()`; `.keys()` is redundant for membership tests.
7. **SIM401** — `config["timeout"] if "timeout" in config else 60`; the ternary key-check collapses into `config.get("timeout", 60)`.
8. **SIM910** — `config.get("log_level", None)`; `None` is already the default fallback.
9. **SIM911** — `zip(config.keys(), config.values())`; iterate with `config.items()` instead.

## Example: Event builder

An event processor that builds collections the hard way and sprinkles trailing commas everywhere.

### Bad

```python
from collections import defaultdict, deque


def prepare_event(event):
    raw_tags = "urgent,review,draft".split(",")  # SIM905

    tags = {"urgent", "review", "draft", "urgent"}  # B033

    for category in {"urgent", "review", "draft"}:  # PLC0208
        print(category)

    counts = defaultdict(default_factory=int)  # RUF026

    queue = deque([], 100)  # RUF037

    meta = {
        "id": event["id"],
        "type": event["type"]  # COM812
    }

    label = event.get("label"),  # COM818

    buckets = (1, 2, 3,)  # COM819

    alias_map = {"alias": value.lower() for value in raw_tags}  # B035

    if "unknown" not in []:  # RUF060
        handle = "unknown"

    header = [event["id"]] + raw_tags + ["end"]  # RUF005

    return tags, counts, queue, meta, label, buckets, alias_map, handle, header
```

### Good

```python
from collections import defaultdict, deque


def prepare_event(event):
    raw_tags = ["urgent", "review", "draft"]

    tags = {"urgent", "review", "draft"}

    for category in ("urgent", "review", "draft"):
        print(category)

    counts = defaultdict(int)

    queue = deque(maxlen=100)

    meta = {
        "id": event["id"],
        "type": event["type"],
    }

    label = event.get("label")

    buckets = (1, 2, 3)

    alias_map = {value: value.lower() for value in raw_tags}

    handle = "unknown"

    header = [event["id"], *raw_tags, "end"]

    return tags, counts, queue, meta, label, buckets, alias_map, handle, header
```

### Violations

1. **B033** — `{"urgent", "review", "draft", "urgent"}`; duplicate items in a set literal are silently collapsed.
2. **B035** — `{"alias": value.lower() for value in raw_tags}`; a static key overwrites on every iteration.
3. **COM812** — `"type": event["type"]`; missing trailing comma on the last multiline item.
4. **COM818** — `label = event.get("label"),`; trailing comma turns the expression into a one-tuple.
5. **COM819** — `(1, 2, 3,)`; prohibited trailing comma in a single-line tuple.
6. **PLC0208** — `for category in {"urgent", "review", "draft"}`; iterate over a sequence instead of a literal set.
7. **RUF005** — `[event["id"]] + raw_tags + ["end"]; prefer iterable unpacking over concatenation.
8. **RUF026** — `defaultdict(default_factory=int)`; `default_factory` is a positional-only argument.
9. **RUF037** — `deque([], 100)`; an empty iterable is unnecessary when creating a deque.
10. **RUF060** — `"unknown" not in []`; membership test against an always-empty collection is a no-op.
11. **SIM905** — `"urgent,review,draft".split(",")`; replace a static split with a list literal.

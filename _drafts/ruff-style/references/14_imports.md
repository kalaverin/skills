---
---

# Imports

Keep import blocks sorted, absolute, conventional, and minimal; manage aliases, lazy imports, and banned APIs.

## Rule of thumb

1. Place every import at module scope, at the very top of the file: future imports first, then one name per line, grouped and sorted by stdlib / third-party / first-party.
2. Import only what you use; never star-import, never import the module itself, and re-export intentionally with `__all__` or a redundant alias.
3. Prefer absolute imports and public APIs; add `__init__.py` to regular packages and avoid private names from external modules.
4. Use community aliases and avoid redundant aliases; access members through the module alias when that is the project convention.
5. Add `from __future__ import annotations` when you use modern type syntax or typing imports that can be simplified under PEP 563.
6. Honor project policy on banned and heavy imports: avoid banned APIs, keep configured heavy imports out of module scope, and do not resolve lazy imports immediately.

## Example: Module header

**Target:** `py39`
**Config:** pair1

A junior's first utility module in a project still targeting Python 3.9, tangled at the top of the file.

### Bad

```python
# File: shop/prices.py  # I002
from pathlib import Path  # F401,I001

import json, decimal  # E401,F401

from pandas import DataFrame
from typing import Dict, Optional
from __future__ import time_travel  # F404,F407

import shop.prices  # F401,PLW0406

DISCOUNT = decimal.Decimal(0.1)
import os  # E402,F401


def load_prices(path):
    return DataFrame([{"value": 1}])


def maybe_process(items: dict[str, int | None]) -> Dict[str, Optional[int]]:  # FA100,FA102
    return items
```

### Good

```python
# File: shop/prices.py
"""Price utilities."""

from __future__ import annotations

import decimal
from pathlib import Path
from typing import Dict, Optional

import pandas as pd

DISCOUNT = decimal.Decimal("0.1")


def load_prices(path: Path) -> pd.DataFrame:
    return pd.DataFrame([{"value": 1}])


def maybe_process(items: dict[str, int | None]) -> Dict[str, Optional[int]]:
    return items
```

### Violations

1. **E401** — `import json, decimal`; two imports share one line.
2. **E402** — `import os`; module-level import appears after runtime code.
3. **F401** — `from pathlib import Path`; imported name is never referenced.
4. **F404** — `from __future__ import time_travel`; future imports must be at the beginning of the file.
5. **F407** — `from __future__ import time_travel`; `time_travel` is not a defined future feature.
6. **FA100** — `from typing import Dict, Optional`; rewriteable annotations need future annotations to unlock the simplification.
7. **FA102** — `items: dict[str, int | None]`; PEP 585/604 syntax needs future annotations for older targets.
8. **I001** — the whole import block is unsorted and ungrouped.
9. **I002** — missing required import `from __future__ import annotations`.
10. **PLW0406** — `import shop.prices`; the module imports itself by its qualified name.

## Example: Alias conventions

**Config:** pair2

A data-pipeline helper that ignores project alias conventions and hides a dependency inside a function.

### Bad

```python
"""Data pipeline helpers."""

import numpy as numpy  # ICN001,PLC0414
import pandas  # F401,ICN001
import tensorflow.keras.backend as K  # ICN002
from pandas import Series  # ICN003


def summarize(frame):
    arr = numpy.array(frame)
    return Series(arr).mean()


def build_kernel():
    import torch  # PLC0415
    return torch.ones((3, 3)) + K.ones((3, 3))
```

### Good

```python
"""Data pipeline helpers."""

import numpy as np
import pandas as pd
import tensorflow as tf
import torch


def summarize(frame):
    arr = np.array(frame)
    return pd.Series(arr).mean()


def build_kernel():
    return torch.ones((3, 3)) + tf.keras.backend.ones((3, 3))
```

### Violations

1. **ICN001** — `import pandas`; pandas is conventionally imported as `pd`.
2. **ICN002** — `import tensorflow.keras.backend as K`; the single-capital alias is banned.
3. **ICN003** — `from pandas import Series`; pandas members should be accessed through `pd`.
4. **PLC0414** — `import numpy as numpy`; the alias does not rename the package.
5. **PLC0415** — `import torch` inside `build_kernel`; imports belong at module level unless deliberately lazy.

## Example: Star imports and package boundaries

**Config:** pair3

A report builder inside an incomplete package that reaches up to parents, imports private internals, and star-imports to save typing.

### Bad

```python
# File: analytics/reports/builder.py (analytics/reports/ has no __init__.py)  # INP001

"""Build reports."""

from .. import shared  # I001,TID252
from thirdparty import _internals  # PLC2701
from math import *  # F403


def build_report(data):
    from .helpers import *  # F403,F406,PLC0415
    normalized = _internals.normalize(data)
    return sqrt(normalized) + shared.base  # F405
```

### Good

```python
# File: analytics/reports/builder.py (analytics/reports/__init__.py exists)

"""Build reports."""

from math import mean, sqrt

from thirdparty import public_api

from analytics.reports.helpers import fetch
from analytics.shared import base


def build_report(data):
    normalized = public_api.normalize(data)
    fetched = fetch(normalized)
    return sqrt(mean(fetched)) + base
```

### Violations

1. **F403** — `from math import *`; wildcard import pollutes the namespace.
2. **F405** — `sqrt(normalized)`; the name may be undefined or may come from a star import.
3. **F406** — `from .helpers import *`; wildcard import used inside a function.
4. **INP001** — `analytics/reports/builder.py`; the directory is an implicit namespace package because `__init__.py` is missing.
5. **PLC2701** — `from thirdparty import _internals`; private name imported from an external module.
6. **TID252** — `from .. import shared`; relative import from a parent module.

## Example: Banned and lazy imports

**Target:** `py315`
**Config:** pair4

A network client on Python 3.15 that mixes banned APIs, heavy module-level imports, and a lazy import that is resolved immediately.

### Bad

```python
"""Network client."""

import typing  # I001,TID254
import urllib3  # F401,TID251
import tensorflow as tf  # TID253

lazy import marshmallow


class Loader(marshmallow.Schema):  # TID255
    def show(self) -> typing.Any:
        return tf.__version__
```

### Good

```python
"""Network client."""

from __future__ import annotations

lazy import typing


class Loader:
    def show(self) -> typing.Any:
        import tensorflow as tf
        return tf.__version__
```

### Violations

1. **TID251** — `import urllib3`; this module is banned by project policy.
2. **TID253** — `import tensorflow as tf`; tensorflow is banned at module level.
3. **TID254** — `import typing`; project policy requires `typing` to be imported lazily.
4. **TID255** — `class Loader(marshmallow.Schema)`; the lazy import of `marshmallow` is resolved immediately by the class base.

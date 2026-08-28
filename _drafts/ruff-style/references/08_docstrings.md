---
---

# Docstrings

Write complete, well-formatted docstrings that mirror the signature: coverage, layout, voice, sections, and contract fidelity (pydocstyle `D`, pydoclint `DOC`, pycodestyle `W505`).

## Rule of thumb

1. Document every public face: module, package `__init__.py`, class, method, `__init__`, magic method, nested class, and function — with purposeful text, not filler.
2. Pin one convention per project (this corpus uses `google`); never mix Google `Name:` headers with NumPy dashed underlines, and leave the rebel rules (`D203`, `D213`, `D413`) off unless the project explicitly opts in.
3. Keep one-liners on one line, hugging the `def`, with `"""` quotes, no padding spaces, and an `r"""` prefix whenever the text contains a backslash.
4. Shape multi-line docstrings as summary on the opening line, one blank line, body flush at the quote indent in spaces (never tabs), closing quotes alone on the last line.
5. Write the summary as one capitalized sentence ending in a period: imperative where the convention demands it, never an echoed signature, never opening with `This`; property docstrings read as attributes (`The bar.`).
6. Let sections breathe: capitalized headers flush at the quote indent, one blank line before and after each section, none between a header and its body, no empty sections, canonical order `Args` → `Returns`/`Yields` → `Raises`.
7. Treat the docstring as a contract: every parameter, `return`, `yield`, and explicit `raise` documented exactly once and nothing phantom; `@overload` stubs carry no docstring; no empty docstrings survive; doc lines wrap under `lint.pycodestyle.max-doc-length`.

## Example: Public API coverage

**Config:** pair1

A junior's game module that ships a full public API surface without a single docstring.

### Bad

```python
# File: game/player.py  # D100


class Player:  # D101
    def __init__(self, name: str, points: int = 0) -> None:  # D107
        self.name = name
        self.points = points

    def add_points(self, points: int) -> None:  # D102
        self.points += points

    def __str__(self) -> str:  # D105
        return f"Player: {self.name}"

    class Stats:  # D106
        ...


def rank(players: list[Player]) -> list[Player]:  # D103
    return sorted(players, key=lambda p: p.points, reverse=True)
```

### Good

```python
# File: game/player.py
"""Player model and ranking helpers."""


class Player:
    """A player in the game.

    Attributes:
        name: The name of the player.
        points: The number of points the player has.

    """

    def __init__(self, name: str, points: int = 0) -> None:
        """Initialize a player with a name and starting points."""
        self.name = name
        self.points = points

    def add_points(self, points: int) -> None:
        """Add points to the player's score.

        Args:
            points: The number of points to add.

        """
        self.points += points

    def __str__(self) -> str:
        """Return a string representation of the player."""
        return f"Player: {self.name}"

    class Stats:
        """Statistics for a player."""


def rank(players: list[Player]) -> list[Player]:
    """Return players sorted by points, highest first.

    Args:
        players: The players to rank.

    Returns:
        The players sorted by descending points.

    """
    return sorted(players, key=lambda p: p.points, reverse=True)
```

### Violations

1. **D100** — `# File: game/player.py`; the module has no docstring at all.
2. **D101** — `class Player:`; public class without a docstring.
3. **D102** — `def add_points(...)`; public method without a docstring.
4. **D103** — `def rank(...)`; public function without a docstring.
5. **D105** — `def __str__(...)`; magic method without a docstring.
6. **D106** — `class Stats:` nested in `Player`; nested classes do not inherit the enclosing docstring.
7. **D107** — `def __init__(...)`; the constructor is the class's creation contract and needs its own docstring.

## Example: Package docstring

**Config:** pair2

The package's entry point re-exports its modules but stays invisible to `help()` and doc generators.

### Bad

```python
# File: game/__init__.py  # D104

__all__ = ["player", "stats"]
```

### Good

```python
# File: game/__init__.py
"""Game and player management package."""

__all__ = ["player", "stats"]
```

### Violations

1. **D104** — `# File: game/__init__.py`; a public package's `__init__.py` needs a docstring listing what it exports.

## Example: Function docstring whitespace

**Config:** pair3

A list-utils module where every docstring exists but its vertical shape is wrong.

### Bad

```python
"""List utilities."""


def mean(values: list[float]) -> float:
    """Return the mean of the given values.
    """  # D200
    return sum(values) / len(values)


def median(values: list[float]) -> float:

    """Return the median of the given values."""  # D201
    return sorted(values)[len(values) // 2]


def total(values: list[float]) -> float:
    """Return the sum of the given values."""  # D202

    return sum(values)


def sort_list(items: list[int]) -> list[int]:
    """Return a sorted copy of the list.
    Sort the list in ascending order and return a copy of the result.
    """  # D205
    return sorted(items)


def unique(items: list[int]) -> list[int]:
    """Return the unique items of the list.

    Keep the first occurrence of each item and drop the rest."""  # D209
    return list(dict.fromkeys(items))


def factorial(n: int) -> int:
    """ Return the factorial of n. """  # D210
    ...


def describe(items: list[int]) -> str:
    """
    Describe the list.

    Return a human-readable summary of the list contents.
    """  # D212
    ...
```

### Good

```python
"""List utilities."""


def mean(values: list[float]) -> float:
    """Return the mean of the given values."""
    return sum(values) / len(values)


def median(values: list[float]) -> float:
    """Return the median of the given values."""
    return sorted(values)[len(values) // 2]


def total(values: list[float]) -> float:
    """Return the sum of the given values."""
    return sum(values)


def sort_list(items: list[int]) -> list[int]:
    """Return a sorted copy of the list.

    Sort the list in ascending order and return a copy of the result.
    """
    return sorted(items)


def unique(items: list[int]) -> list[int]:
    """Return the unique items of the list.

    Keep the first occurrence of each item and drop the rest.
    """
    return list(dict.fromkeys(items))


def factorial(n: int) -> int:
    """Return the factorial of n."""
    ...


def describe(items: list[int]) -> str:
    """Describe the list.

    Return a human-readable summary of the list contents.
    """
    ...
```

### Violations

1. **D200** — mean's docstring spills onto a second physical line; the content fits on one line with the quotes.
2. **D201** — blank line between `def median(...)` and its docstring.
3. **D202** — blank line between total's docstring and the function body.
4. **D205** — sort_list's summary is followed by the description with no blank line between them.
5. **D209** — unique's closing quotes share a line with the last paragraph instead of sitting on their own line.
6. **D210** — `""" Return the factorial of n. """`; whitespace padding between the quotes and the text.
7. **D212** — describe's summary is pushed to the second physical line by a blank first line.

## Example: Indentation and quotes

**Config:** pair4

A path-helpers module with tab damage, ragged continuation lines, wrong quotes, and an escape-eaten Windows path.

### Bad

```python
"""Path helpers."""


def sort_list(items: list[int]) -> list[int]:
    """Return a sorted copy of the list.

	Sort the list in ascending order and return a copy of the result.
    """  # D206,D207
    return sorted(items)


def dedent_case(items: list[int]) -> list[int]:
    """Return a sorted copy of the list.

Sort the list in ascending order and return a copy of the result.
    """  # D207
    return sorted(items)


def indent_case(items: list[int]) -> list[int]:
    """Return a sorted copy of the list.

        Sort the list in ascending order and return a copy of the result.
    """  # D208
    return sorted(items)


def kos_root() -> str:
    '''Return the pathname of the KOS root directory.'''  # D300
    ...


def config_dir() -> str:
    """Return the config directory, e.g. C:\new\app."""  # D301
    ...
```

### Good

```python
"""Path helpers."""


def sort_list(items: list[int]) -> list[int]:
    """Return a sorted copy of the list.

    Sort the list in ascending order and return a copy of the result.
    """
    return sorted(items)


def dedent_case(items: list[int]) -> list[int]:
    """Return a sorted copy of the list.

    Sort the list in ascending order and return a copy of the result.
    """
    return sorted(items)


def indent_case(items: list[int]) -> list[int]:
    """Return a sorted copy of the list.

    Sort the list in ascending order and return a copy of the result.
    """
    return sorted(items)


def kos_root() -> str:
    """Return the pathname of the KOS root directory."""
    ...


def config_dir() -> str:
    r"""Return the config directory, e.g. C:\new\app."""
    ...
```

### Violations

1. **D206** — the body line of sort_list's docstring is tab-indented; docstrings use spaces.
2. **D207** — dedent_case's body line starts at column 0; continuation lines align with the opening quotes.
3. **D208** — indent_case's body line is indented 8 spaces; free text sits flush with the quotes, only section bodies go deeper.
4. **D300** — `'''Return the pathname of the KOS root directory.'''`; PEP 257 standardizes on `"""`.
5. **D301** — `C:\new\app` in a plain docstring; backslashes are escape sequences (`\n` becomes a newline) unless the docstring is `r"""`.

## Example: Class docstring spacing

**Config:** pair5

A metadata class whose docstring is detached from the `class` line and glued to its first method (NumPy/`pep257` convention: no blank line before, exactly one after).

### Bad

```python
"""Photo metadata helpers."""


class PhotoMetadata:

    """Metadata about a photo."""  # D204,D211
    def __init__(self, file: str) -> None:
        """Initialize photo metadata for a file."""
        self.file = file
```

### Good

```python
"""Photo metadata helpers."""


class PhotoMetadata:
    """Metadata about a photo."""

    def __init__(self, file: str) -> None:
        """Initialize photo metadata for a file."""
        self.file = file
```

### Violations

1. **D204** — `def __init__` follows the class docstring with no blank line; PEP 257 wants exactly one.
2. **D211** — blank line between `class PhotoMetadata:` and its docstring; under `google`/`numpy`/`pep257` the class docstring hugs the `class` line (rival of D203 — never enable both).

## Example: Summary-line voice

**Config:** pair6

A statistics module whose one-line summaries misread in every way: no period, indicative mood, echoed signature, lowercase opener, leading `This`. The pair's ruff.toml sets no `lint.pydocstyle.convention` so both the `numpy`/`pep257` rules (`D400`, `D401`, `D404`) and the `google` rule (`D415`) fire.

### Bad

```python
"""Statistics helpers."""


def mean(values: list[float]) -> float:
    """Return the mean of the given values"""  # D400,D415
    return sum(values) / len(values)


def median(values: list[float]) -> float:
    """Returns the median of the given values."""  # D401
    return sorted(values)[len(values) // 2]


def combine(a: int, b: int) -> list[int]:
    """combine(a: int, b: int) -> list[int]"""  # D400,D402,D415
    return [a, b]


def total(values: list[float]) -> float:
    """return the sum of the given values."""  # D403
    return sum(values)


def maximum(values: list[float]) -> float:
    """This function returns the maximum of the given values."""  # D401,D404
    return max(values)
```

### Good

```python
"""Statistics helpers."""


def mean(values: list[float]) -> float:
    """Return the mean of the given values."""
    return sum(values) / len(values)


def median(values: list[float]) -> float:
    """Return the median of the given values."""
    return sorted(values)[len(values) // 2]


def combine(a: int, b: int) -> list[int]:
    """Return a list with a and b."""
    return [a, b]


def total(values: list[float]) -> float:
    """Return the sum of the given values."""
    return sum(values)


def maximum(values: list[float]) -> float:
    """Return the maximum of the given values."""
    return max(values)
```

### Violations

1. **D400** — `"""Return the mean of the given values"""`; the first line does not end with a period (`numpy`/`pep257` variant of D415).
2. **D401** — `"""Returns the median..."""` and `"""This function returns..."""`; the summary is not phrased as a command.
3. **D402** — `"""combine(a: int, b: int) -> list[int]"""`; the first line echoes the signature, which type annotations already carry.
4. **D403** — `"""return the sum..."""`; the first word is not capitalized.
5. **D404** — `"""This function returns..."""`; leading `This` is filler, start with the verb.
6. **D415** — `"""Return the mean of the given values"""`; the first line ends with no `.`, `?`, or `!` (`google` variant of D400).

## Example: Google-style sections

**Config:** pair7

A speed module whose `Args`/`Returns`/`Raises` blocks are ragged, squashed, hollow, and scrambled.

### Bad

```python
"""Speed calculations."""


def calculate_speed(distance: float, time: float) -> float:
    """Calculate speed as distance divided by time.

        Args:
            distance: Distance traveled.
            time: Time spent traveling.

    Returns:
        Speed as distance divided by time.
    """  # D214,D413
    return distance / time


def convert(speed: float) -> float:
    """Convert speed to parsecs per hour.

    Args:

        speed: Speed in km/h.
    Returns:
        Speed in parsecs per hour.

    Raises:
    """  # D410,D411,D412,D413,D414
    ...


def describe(distance: float, time: float) -> str:
    """Describe a trip.

    returns:
        A human-readable summary.

    args
        distance: Distance traveled.
        time: Time spent traveling.
    """  # D405,D413,D416,D420
    ...
```

### Good

```python
"""Speed calculations."""


def calculate_speed(distance: float, time: float) -> float:
    """Calculate speed as distance divided by time.

    Args:
        distance: Distance traveled.
        time: Time spent traveling.

    Returns:
        Speed as distance divided by time.

    """
    return distance / time


def convert(speed: float) -> float:
    """Convert speed to parsecs per hour.

    Args:
        speed: Speed in km/h.

    Returns:
        Speed in parsecs per hour.

    """
    return speed * 1.05e-13


def describe(distance: float, time: float) -> str:
    """Describe a trip.

    Args:
        distance: Distance traveled.
        time: Time spent traveling.

    Returns:
        A human-readable summary.

    """
    return f"{distance} km in {time} h"
```

### Violations

1. **D214** — `        Args:` is over-indented; section headers align with the opening quotes, only bodies go one level deeper.
2. **D405** — `returns:` and `args`; section names are proper nouns and must be capitalized.
3. **D410** — `Returns:` immediately follows the `Args` body; one blank line separates a section from the next header.
4. **D411** — `Returns:` has no blank line before it; the mirror of D410, fired from the header's side.
5. **D412** — blank line between `Args:` and its own body; gaps detach entries from their header.
6. **D414** — `Raises:` with an empty body; fill the section or delete it.
7. **D416** — `args` ends without a colon; Google-style headers are `Name:` (the `google` counterpart of D406).
8. **D420** — `returns` appears before `args`; canonical Google order is `Args` → `Returns`/`Yields` → `Raises`.

## Example: NumPy-style sections

**Config:** pair8

The same speed module rewritten by a NumPy-native junior whose dashed underlines are colon-crested, missing, orphaned, stunted, and shifted (`convention = "numpy"`).

### Bad

```python
"""Speed calculations."""


def calculate_speed(distance: float, time: float) -> float:
    """Calculate speed as distance divided by time.

    Parameters:
    ----------
    distance : float
        Distance traveled.
    time : float
        Time spent traveling.
    """  # D406,D413,DOC201
    return distance / time


def convert(speed: float) -> float:
    """Convert speed to parsecs per hour.

    Parameters

    speed : float
        Speed in km/h.
    """  # D407,D412,D413
    ...


def describe(distance: float) -> str:
    """Describe a trip.

    Parameters

    ----------
    distance : float
        Distance traveled.
    """  # D408,D413
    ...


def shorten(distance: float) -> float:
    """Shorten a distance.

    Parameters
    ---
    distance : float
        Distance traveled.
    """  # D409,D413
    ...


def widen(distance: float) -> float:
    """Widen a distance.

    Parameters
        ----------
    distance : float
        Distance traveled.
    """  # D215,D413
    ...
```

### Good

```python
"""Speed calculations."""


def calculate_speed(distance: float, time: float) -> float:
    """Calculate speed as distance divided by time.

    Parameters
    ----------
    distance : float
        Distance traveled.
    time : float
        Time spent traveling.

    Returns
    -------
    float
        Speed as distance divided by time.

    """
    return distance / time


def convert(speed: float) -> float:
    """Convert speed to parsecs per hour.

    Parameters
    ----------
    speed : float
        Speed in km/h.

    """
    ...


def describe(distance: float) -> str:
    """Describe a trip.

    Parameters
    ----------
    distance : float
        Distance traveled.

    """
    ...


def shorten(distance: float) -> float:
    """Shorten a distance.

    Parameters
    ----------
    distance : float
        Distance traveled.

    """
    ...


def widen(distance: float) -> float:
    """Widen a distance.

    Parameters
    ----------
    distance : float
        Distance traveled.

    """
    ...
```

### Violations

1. **D215** — `        ----------` is indented past its `Parameters` header; a NumPy underline sits flush with the header.
2. **D406** — `Parameters:` ends with a colon; NumPy headers are bare words followed by a newline (rival of the Google-side D416).
3. **D407** — `Parameters` has no dashed underline at all; without it the header is just a paragraph.
4. **D408** — the `----------` underline is separated from `Parameters` by a blank line; it belongs on the immediately following line.
5. **D409** — `---` under `Parameters`; the underline length must match the header length exactly.

## Example: Args contract

**Config:** pair9

A refactor dropped `time` from the docstring and left a phantom `unit` behind; the signatures moved on, the text did not.

### Bad

```python
"""Speed calculations."""


def calculate_speed(distance: float, time: float) -> float:  # D417
    """Calculate speed as distance divided by time.

    Args:
        distance: Distance traveled.

    Returns:
        Speed as distance divided by time.
    """  # D413
    return distance / time


def convert(speed: float, precision: int) -> float:
    """Convert speed to parsecs per hour.

    Args:
        speed: Speed in km/h.
        precision: Decimal places to keep.
        unit: Output unit.

    Returns:
        Speed in parsecs per hour.
    """  # D413,DOC102
    return round(speed * 1.05e-13, precision)
```

### Good

```python
"""Speed calculations."""


def calculate_speed(distance: float, time: float) -> float:
    """Calculate speed as distance divided by time.

    Args:
        distance: Distance traveled.
        time: Time spent traveling.

    Returns:
        Speed as distance divided by time.

    """
    return distance / time


def convert(speed: float, precision: int) -> float:
    """Convert speed to parsecs per hour.

    Args:
        speed: Speed in km/h.
        precision: Decimal places to keep.

    Returns:
        Speed in parsecs per hour.

    """
    return round(speed * 1.05e-13, precision)
```

### Violations

1. **D417** — `time` is missing from calculate_speed's `Args:`; once an Args section exists it must cover every parameter.
2. **DOC102** — `unit: Output unit.` is documented but not in the signature; phantom parameters are refactor residue.

## Example: Returns, yields, and raises contract

**Config:** pair10

A helper module whose docstrings lie about what comes back and what blows up.

### Bad

```python
"""Greeting and counting helpers."""


class FasterThanLightError(ArithmeticError):
    """Raised when the calculated speed exceeds the speed of light."""


def calculate_speed(distance: float, time: float) -> float:
    """Calculate speed as distance divided by time.

    Args:
        distance: Distance traveled.
        time: Time spent traveling.
    """  # D413,DOC201,DOC501
    try:
        return distance / time
    except ZeroDivisionError as exc:
        raise FasterThanLightError from exc


def say_hello(n: int) -> None:
    """Say hello to the user.

    Args:
        n: Number of times to say hello.

    Returns:
        Doesn't return anything.
    """  # D413,DOC202
    for _ in range(n):
        print("Hello!")


def count_to_n(n: int) -> int:
    """Generate integers up to n.

    Args:
        n: The number at which to stop counting.
    """  # D413,DOC402
    for i in range(1, n + 1):
        yield i


def describe(n: int) -> None:
    """Describe the counting.

    Args:
        n: The number at which to stop counting.

    Yields:
        Doesn't yield anything.
    """  # D413,DOC403
    for _ in range(n):
        print("Counting")


def divide(distance: float, time: float) -> float:
    """Divide distance by time.

    Args:
        distance: Distance traveled.
        time: Time spent traveling.

    Returns:
        Speed as distance divided by time.

    Raises:
        ZeroDivisionError: If time is zero.
    """  # D413,DOC502
    return distance / time
```

### Good

```python
"""Greeting and counting helpers."""


class FasterThanLightError(ArithmeticError):
    """Raised when the calculated speed exceeds the speed of light."""


def calculate_speed(distance: float, time: float) -> float:
    """Calculate speed as distance divided by time.

    Args:
        distance: Distance traveled.
        time: Time spent traveling.

    Returns:
        Speed as distance divided by time.

    Raises:
        FasterThanLightError: If the calculated speed exceeds the speed of light.

    """
    try:
        return distance / time
    except ZeroDivisionError as exc:
        raise FasterThanLightError from exc


def say_hello(n: int) -> None:
    """Say hello to the user.

    Args:
        n: Number of times to say hello.

    """
    for _ in range(n):
        print("Hello!")


def count_to_n(n: int) -> int:
    """Generate integers up to n.

    Args:
        n: The number at which to stop counting.

    Yields:
        The current number in the count.

    """
    for i in range(1, n + 1):
        yield i


def describe(n: int) -> None:
    """Describe the counting.

    Args:
        n: The number at which to stop counting.

    """
    for _ in range(n):
        print("Counting")


def divide(distance: float, time: float) -> float:
    """Divide distance by time.

    Args:
        distance: Distance traveled.
        time: Time spent traveling.

    Returns:
        Speed as distance divided by time.

    """
    return distance / time
```

### Violations

1. **DOC201** — calculate_speed returns a value but its docstring has no `Returns:` section.
2. **DOC202** — say_hello documents `Returns:` for a `-> None` function; no `return` statement means no Returns section.
3. **DOC402** — count_to_n yields items but its docstring has no `Yields:` section.
4. **DOC403** — describe documents `Yields:` but never yields; a phantom section misleads callers into iterating a plain function.
5. **DOC501** — `raise FasterThanLightError from exc` is not documented in `Raises:`; every explicit raise is part of the contract.
6. **DOC502** — `ZeroDivisionError` is documented but never explicitly raised in the body; it merely propagates from `/`.

## Example: Rebel conventions

**Config:** pair11

A project that deliberately opts into the rules every standard convention disables: blank line before class docstrings (D203), summaries on the second line (D213), breathing room before the closing quotes (D413). The pair's ruff.toml selects exactly these three codes — their rivals (D211, D212) would otherwise fire on the Good listing, since no `lint.pydocstyle.convention` enables D203/D213/D413.

### Bad

```python
"""Trip reporting."""


class TripReport:
    """A trip report."""  # D203

    def render(self) -> str:
        """Render the report.

        Returns:
            The rendered report.
        """  # D213,D413
        return "report"
```

### Good

```python
"""Trip reporting."""


class TripReport:

    """A trip report."""

    def render(self) -> str:
        """
        Render the report.

        Returns:
            The rendered report.

        """
        return "report"
```

### Violations

1. **D203** — `"""A trip report."""` hugs the `class` line; this convention requires one blank line before a class docstring (rival of D211).
2. **D213** — the summary sits on the first physical line; this convention requires it on the second line (rival of D212).
3. **D413** — no blank line between the last section and the closing quotes.

## Example: Overloads, empty docstrings, and doc line width

**Config:** pair12

A number module with typing text duplicated onto `@overload` stubs, an empty-docstring placeholder, a property documented like a function, and a doc line that runs past the configured `lint.pycodestyle.max-doc-length = 72`.

### Bad

```python
"""Number helpers."""

from typing import overload


@overload
def factorial(n: int) -> int:  # D418
    """Return the factorial of n."""
    ...


@overload
def factorial(n: float) -> float:  # D418
    """Return the factorial of n."""
    ...


def factorial(n):
    """Return the factorial of n."""
    if n <= 1:
        return 1
    return n * factorial(n - 1)


def mean(values: list[float]) -> float:
    """"""  # D419
    return sum(values) / len(values)


class Cache:
    """A tiny cache."""

    @property
    def size(self) -> int:
        """Returns the size of the cache."""  # D421
        return len(self._items)


def configure(path: str) -> None:
    """Configure the loader from a path that points at the shared configuration file."""  # W505
    ...
```

### Good

```python
"""Number helpers."""

from typing import overload


@overload
def factorial(n: int) -> int: ...


@overload
def factorial(n: float) -> float: ...


def factorial(n):
    """Return the factorial of n."""
    if n <= 1:
        return 1
    return n * factorial(n - 1)


def mean(values: list[float]) -> float:
    """Return the mean of the given values."""
    return sum(values) / len(values)


class Cache:
    """A tiny cache."""

    @property
    def size(self) -> int:
        """The size of the cache."""
        return len(self._items)


def configure(path: str) -> None:
    """Configure the loader from a shared config path."""
    ...
```

### Violations

1. **D418** — docstrings on the `@overload` stubs; overloads are type-checker phantoms, the implementation owns the docstring.
2. **D419** — `""""""` on mean; an empty docstring is scaffolding — fill it or delete it.
3. **D421** — `"""Returns the size of the cache."""`; a property is consumed as an attribute, so document it as `The size of the cache.`
4. **W505** — configure's summary line exceeds `lint.pycodestyle.max-doc-length`; the rule is inert unless that setting is set.

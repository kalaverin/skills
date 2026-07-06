## 1. Python Language Rules

### 1.1 Lint
[ref: #s1.1-lint]
**1.1.1 Definition**
[ref: #s1.1.1-definition]
Run `pylint` over your code using the Google `pylintrc`. `pylint` finds bugs and style problems. Because Python is dynamic, some warnings may be spurious, but they should be infrequent.

**1.1.2 Pros**
[ref: #s1.1.2-pros]
Catches easy-to-miss errors like typos and using-vars-before-assignment.

**1.1.3 Cons**
[ref: #s1.1.3-cons]
`pylint` is not perfect; sometimes you must write around it, suppress warnings, or fix it.

**1.1.4 Decision**
[ref: #s1.1.4-decision]
- Run `pylint` on all code.
- Suppress inappropriate warnings with a line-level comment so other issues are not hidden.
- Use the symbolic name in suppressions (e.g., `# pylint: disable=invalid-name`). Google-specific warnings start with `g-`.
- If the reason for suppression is not clear from the symbolic name, add an explanation.
- Prefer `pylint: disable` over the deprecated `pylint: disable-msg`.
- Unused argument warnings can be suppressed by deleting the variables at the beginning of the function with a comment (e.g., `del beans, eggs  # Unused by vikings.`).
- Other allowed but no-longer-encouraged forms: using `_` as the identifier, prefixing with `unused_`, or assigning to `_`. These break callers that pass arguments by name and do not enforce that the arguments are actually unused.

```python
# Yes
def viking_cafe_order(spam: str, beans: str, eggs: str | None = None) -> str:
    del beans, eggs  # Unused by vikings.
    return spam + spam + spam
```

---

### 1.2 Imports
[ref: #s1.2-imports]
Use `import` statements for packages and modules only, not for individual types, classes, or functions.

**1.2.1 Definition**
[ref: #s1.2.1-definition]
Imports are a reusability mechanism for sharing code between modules.

**1.2.2 Pros**
[ref: #s1.2.2-pros]
Simple namespace management; `x.Obj` indicates `Obj` is defined in module `x`.

**1.2.3 Cons**
[ref: #s1.2.3-cons]
Module names can collide; some are inconveniently long.

**1.2.4 Decision**
[ref: #s1.2.4-decision]
- Use `import x` for importing packages and modules.
- Use `from x import y` where `x` is the package prefix and `y` is the module name with no prefix.
- Use `from x import y as z` when:
  - Two modules named `y` are to be imported.
  - `y` conflicts with a top-level name in the current module.
  - `y` conflicts with a common parameter name in the public API (e.g., `features`).
  - `y` is inconveniently long.
  - `y` is too generic (e.g., `from storage.file_system import options as fs_options`).
- Use `import y as z` only when `z` is a standard abbreviation (e.g., `import numpy as np`).

```python
# Yes
from sound.effects import echo
...
echo.EchoFilter(input, output, delay=0.7, atten=4)
```

- Do NOT use relative names in imports. Even within the same package, use the full package name to prevent unintentionally importing a package twice.

**1.2.4.1 Exemptions**
[ref: #imports-exemptions]
- Symbols from `typing`, `collections.abc`, and `typing_extensions` may be imported directly to support static analysis and type checking.
- Redirects from `six.moves` are exempt.

---

### 1.3 Packages
[ref: #s1.3-packages]
Import each module using the full pathname location of the module.

**1.3.1 Pros**
[ref: #s1.3.1-pros]
Avoids conflicts and incorrect imports due to unexpected `sys.path`.

**1.3.2 Cons**
[ref: #s1.3.2-cons]
Harder to deploy if you must replicate the package hierarchy (not a problem with modern deployment).

**1.3.3 Decision**
[ref: #s1.3.3-decision]
- All new code must import each module by its full package name.
- The directory of the main binary should NOT be assumed to be in `sys.path`.
- Code should assume `import jodie` refers to a third-party or top-level package, not a local `jodie.py`.

```python
# Yes
import absl.flags
from doctor.who import jodie
_FOO = absl.flags.DEFINE_string(...)

# Yes
from absl import flags
from doctor.who import jodie
_FOO = flags.DEFINE_string(...)

# No
import jodie  # Unclear intent; depends on sys.path
```

---

### 1.4 Exceptions
[ref: #s1.4-exceptions]
Exceptions are allowed but must be used carefully.

**1.4.1 Definition**
[ref: #s1.4.1-definition]
Exceptions break normal control flow to handle errors or exceptional conditions.

**1.4.2 Pros**
[ref: #s1.4.2-pros]
Normal control flow is not cluttered by error-handling code; allows skipping multiple frames.

**1.4.3 Cons**
[ref: #s1.4.3-cons]
May confuse control flow; easy to miss error cases when calling libraries.

**1.4.4 Decision**
[ref: #s1.4.4-decision]
- Make use of built-in exception classes when it makes sense. Raise `ValueError` for programming mistakes like violated preconditions.
- Do NOT use `assert` statements in place of conditionals or for validating preconditions. `assert` must not be critical to application logic. A litmus test: the `assert` could be removed without breaking the code. `assert` conditionals are not guaranteed to be evaluated. For `pytest` based tests, `assert` is okay and expected.
- Libraries or packages may define their own exceptions. They must inherit from an existing exception class. Exception names should end in `Error` and must not introduce repetition (`foo.FooError`).
- NEVER use catch-all `except:` statements, or catch `Exception` or `BaseException`, unless you are re-raising the exception, or creating an isolation point where exceptions are recorded and suppressed (e.g., protecting a thread's outermost block).
- Minimize the amount of code in a `try`/`except` block. The larger the `try` body, the more likely an unexpected exception will be raised and hidden.
- Use the `finally` clause for cleanup (e.g., closing a file).

```python
# Yes
def connect_to_next_port(self, minimum: int) -> int:
    """Connects to the next available port.

    Args:
      minimum: A port value greater or equal to 1024.

    Returns:
      The new minimum port.

    Raises:
      ConnectionError: If no available port is found.
    """
    if minimum < 1024:
        # Note: ValueError not listed in Raises because it is a reaction to API misuse.
        raise ValueError(f'Min. port must be at least 1024, not {minimum}.')
    port = self._find_next_open_port(minimum)
    if port is None:
        raise ConnectionError(
            f'Could not connect to service on port {minimum} or higher.')
    # The code does not depend on the result of this assert.
    assert port >= minimum, (
        f'Unexpected port {port} when minimum was {minimum}.')
    return port

# No
def connect_to_next_port(self, minimum: int) -> int:
    """..."""
    assert minimum >= 1024, 'Minimum port must be at least 1024.'
    port = self._find_next_open_port(minimum)
    assert port is not None
    return port
```

---

### 1.5 Mutable Global State
[ref: #s1.5-global-variables]
Avoid mutable global state.

**1.5.1 Definition**
[ref: #s1.5.1-definition]
Module-level values or class attributes that can be mutated during program execution.

**1.5.2 Pros**
[ref: #s1.5.2-pros]
Occasionally useful.

**1.5.3 Cons**
[ref: #s1.5.3-cons]
Breaks encapsulation; may change module behavior during import.

**1.5.4 Decision**
[ref: #s1.5.4-decision]
- Avoid mutable global state.
- If warranted, declare mutable global entities at module level or as class attributes, make them internal by prepending `_`, and expose access through public functions or class methods.
- Explain the design reasons in a comment or linked doc.
- Module-level constants are permitted and encouraged. Name them with ALL_CAPS and underscores (e.g., `_MAX_HOLY_HANDGRENADE_COUNT = 3` for internal, `SIR_LANCELOTS_FAVORITE_COLOR = "blue"` for public).

---

### 1.6 Nested/Local/Inner Classes and Functions
[ref: #s1.6-nested]
Nested local functions or classes are fine when used to close over a local variable. Inner classes are fine.

**1.6.1 Definition**
[ref: #s1.6.1-definition]
A class can be defined inside a method, function, or class. A function can be defined inside a method or function. Nested functions have read-only access to enclosing scope variables.

**1.6.2 Pros**
[ref: #s1.6.2-pros]
Allows utility classes/functions limited to a small scope; ADT-style; commonly used for decorators.

**1.6.3 Cons**
[ref: #s1.6.3-cons]
Cannot be directly tested; can make the outer function longer and less readable.

**1.6.4 Decision**
[ref: #s1.6.4-decision]
- Avoid nested functions or classes except when closing over a local value other than `self` or `cls`.
- Do NOT nest a function just to hide it from module users. Instead, prefix its name with `_` at the module level so it can still be accessed by tests.

---

### 1.7 Comprehensions & Generator Expressions
[ref: #s1.7-comprehensions]
Okay to use for simple cases.

**1.7.1 Definition**
[ref: #s1.7.1-definition]
List, Dict, and Set comprehensions and generator expressions create containers and iterators without traditional loops, `map()`, `filter()`, or `lambda`.

**1.7.2 Pros**
[ref: #s1.7.2-pros]
Simple comprehensions can be clearer; generator expressions avoid list creation.

**1.7.3 Cons**
[ref: #s1.7.3-cons]
Complicated comprehensions can be hard to read.

**1.7.4 Decision**
[ref: #s1.7.4-decision]
- Comprehensions are allowed.
- Multiple `for` clauses or filter expressions are NOT permitted.
- Optimize for readability, not conciseness.

```python
# Yes
result = [mapping_expr for value in iterable if filter_expr]

result = [
    is_valid(metric={'key': value})
    for value in interesting_iterable
    if a_longer_filter_expression(value)
]

descriptive_name = [
    transform({'key': key, 'value': value}, color='black')
    for key, value in generate_iterable(some_input)
    if complicated_condition_is_met(key, value)
]

result = []
for x in range(10):
    for y in range(5):
        if x * y > 10:
            result.append((x, y))

return {
    x: complicated_transform(x)
    for x in long_generator_function(parameter)
    if x is not None
}

return (x**2 for x in range(10))
unique_names = {user.name for user in users if user is not None}

# No
result = [(x, y) for x in range(10) for y in range(5) if x * y > 10]

return (
    (x, y, z)
    for x in range(5)
    for y in range(5)
    if x != y
    for z in range(5)
    if y != z
)
```

---

### 1.8 Default Iterators and Operators
[ref: #s1.8-default-iterators-and-operators]
Use default iterators and operators for types that support them (lists, dictionaries, files).

**1.8.1 Definition**
[ref: #s1.8.1-definition]
Container types define default iterators and membership test operators (`in`, `not in`).

**1.8.2 Pros**
[ref: #s1.8.2-pros]
Simple, efficient, direct, generic.

**1.8.3 Cons**
[ref: #s1.8.3-cons]
You cannot tell the type by reading method names (also an advantage).

**1.8.4 Decision**
[ref: #s1.8.4-decision]
- Use default iterators and operators for types that support them.
- Prefer built-in iterator methods to methods that return lists.
- Do NOT mutate a container while iterating over it.

```python
# Yes
for key in adict: ...
if obj in alist: ...
for line in afile: ...
for k, v in adict.items(): ...

# No
for key in adict.keys(): ...
for line in afile.readlines(): ...
```

---

### 1.9 Generators
[ref: #s1.9-generators]
Use generators as needed.

**1.9.1 Definition**
[ref: #s1.9.1-definition]
A generator function returns an iterator that yields a value each time it executes `yield`. Runtime state is suspended until the next value is needed.

**1.9.2 Pros**
[ref: #s1.9.2-pros]
Simpler code; local variables and control flow are preserved; uses less memory than creating a full list.

**1.9.3 Cons**
[ref: #s1.9.3-cons]
Local variables in the generator are not garbage collected until the generator is consumed to exhaustion or itself garbage collected.

**1.9.4 Decision**
[ref: #s1.9.4-decision]
- Generators are fine.
- Use "Yields:" rather than "Returns:" in the docstring for generator functions.
- If the generator manages an expensive resource, force cleanup by wrapping the generator with a context manager (PEP-0533).

---

### 1.10 Lambda Functions
[ref: #s1.10-lambda-functions]
Okay for one-liners. Prefer generator expressions over `map()` or `filter()` with a `lambda`.

**1.10.1 Definition**
[ref: #s1.10.1-definition]
Lambdas define anonymous functions in an expression.

**1.10.2 Pros**
[ref: #s1.10.2-pros]
Convenient.

**1.10.3 Cons**
[ref: #s1.10.3-cons]
Harder to read and debug than local functions; lack of names makes stack traces difficult; expressiveness limited to a single expression.

**1.10.4 Decision**
[ref: #s1.10.4-decision]
- Lambdas are allowed.
- If the lambda body spans multiple lines or exceeds 60-80 chars, define it as a regular nested function instead.
- For common operations (e.g., multiplication), use functions from the `operator` module instead of lambdas (prefer `operator.mul` over `lambda x, y: x * y`).

---

### 1.11 Conditional Expressions
[ref: #s1.11-conditional-expressions]
Okay for simple cases.

**1.11.1 Definition**
[ref: #s1.11.1-definition]
Conditional expressions provide shorter syntax for if statements: `x = 1 if cond else 2`.

**1.11.2 Pros**
[ref: #s1.11.2-pros]
Shorter and more convenient than an if statement.

**1.11.3 Cons**
[ref: #s1.11.3-cons]
May be harder to read; condition may be difficult to locate if the expression is long.

**1.11.4 Decision**
[ref: #s1.11.4-decision]
- Okay to use for simple cases.
- Each portion must fit on one line: true-expression, if-expression, else-expression.
- Use a complete if statement when things get more complicated.

```python
# Yes
one_line = 'yes' if predicate(value) else 'no'
slightly_split = ('yes' if predicate(value)
                  else 'no, nein, nyet')
the_longest_ternary_style_that_can_be_done = (
    'yes, true, affirmative, confirmed, correct'
    if predicate(value)
    else 'no, false, negative, nay')

# No
bad_line_breaking = ('yes' if predicate(value) else
                     'no')
portion_too_long = ('yes'
                    if some_long_module.some_long_predicate_function(
                        really_long_variable_name)
                    else 'no, false, negative, nay')
```

---

### 1.12 Default Argument Values
[ref: #s1.12-default-argument-values]
Okay in most cases.

**1.12.1 Definition**
[ref: #s1.12.1-definition]
Values specified at the end of a parameter list: `def foo(a, b=0):`.

**1.12.2 Pros**
[ref: #s1.12.2-pros]
Easy way to override defaults without defining many functions.

**1.12.3 Cons**
[ref: #s1.12.3-cons]
Default arguments are evaluated once at module load time. Mutable objects as defaults cause shared state bugs.

**1.12.4 Decision**
[ref: #s1.12.4-decision]
- Do NOT use mutable objects as default values in function or method definitions.

```python
# Yes
def foo(a, b=None):
    if b is None:
        b = []

def foo(a, b: Sequence | None = None):
    if b is None:
        b = []

def foo(a, b: Sequence = ()):  # Empty tuple OK (immutable)
    ...

# No
def foo(a, b=[]):
    ...

def foo(a, b=time.time()):  # Represents module load time, not call time
    ...

def foo(a, b=_FOO.value):  # sys.argv not yet parsed
    ...

def foo(a, b: Mapping = {}):  # Mutable default
    ...
```

---

### 1.13 Properties
[ref: #s1.13-properties]
Properties may be used to control getting or setting attributes that require trivial computations or logic. Property implementations must match the general expectations of regular attribute access: cheap, straightforward, and unsurprising.

**1.13.1 Definition**
[ref: #s1.13.1-definition]
Wrap method calls for getting/setting an attribute as standard attribute access.

**1.13.2 Pros**
[ref: #s1.13.2-pros]
- Attribute access/assignment API rather than getter/setter method calls.
- Can make an attribute read-only.
- Allows lazy calculations.
- Maintains public interface when internals evolve.

**1.13.3 Cons**
[ref: #s1.13.3-cons]
- Can hide side-effects like operator overloading.
- Can be confusing for subclasses.

**1.13.4 Decision**
[ref: #s1.13.4-decision]
- Properties are allowed, but only when necessary and matching expectations of typical attribute access; otherwise follow getter/setter rules.
- Do NOT use a property to simply get and set an internal attribute with no computation (make the attribute public instead).
- Using a property to control access or calculate a trivially derived value is allowed.
- Create properties with the `@property` decorator. Manually implementing a property descriptor is a power feature (avoid).
- Do NOT use properties for computations a subclass may want to override and extend.

---

### 1.14 True/False Evaluations
[ref: #s1.14-truefalse-evaluations]
Use the "implicit" false if at all possible (with caveats).

**1.14.1 Definition**
[ref: #s1.14.1-definition]
"Empty" values are false: `0, None, [], {}, ''`.

**1.14.2 Pros**
[ref: #s1.14.2-pros]
Easier to read, less error-prone, usually faster.

**1.14.3 Cons**
[ref: #s1.14.3-cons]
May look strange to C/C++ developers.

**1.14.4 Decision**
[ref: #s1.14.4-decision]
- Use implicit false: `if foo:` rather than `if foo != []:`.
- ALWAYS use `if foo is None:` (or `is not None`) to check for `None`.
- NEVER compare a boolean variable to `False` using `==`. Use `if not x:`. If you need to distinguish `False` from `None`, chain expressions: `if not x and x is not None:`.
- For sequences (strings, lists, tuples), use the fact that empty sequences are false: `if seq:` and `if not seq:` are preferable to `if len(seq):` and `if not len(seq):`.
- When handling integers, implicit false may involve more risk (accidentally handling `None` as 0). You may compare a known integer against 0 (unless it is the result of `len()`).
- Note that `'0'` (string) evaluates to true.
- Numpy arrays may raise an exception in implicit boolean context. Prefer `.size` when testing emptiness (e.g., `if not users.size`).

```python
# Yes
if not users:
    print('no users')

if i % 10 == 0:
    self.handle_multiple_of_ten()

def f(x=None):
    if x is None:
        x = []

# No
if len(users) == 0:
    print('no users')

if not i % 10:
    self.handle_multiple_of_ten()

def f(x=None):
    x = x or []
```

---

### 1.16 Lexical Scoping
[ref: #s1.16-lexical-scoping]
Okay to use.

**1.16.1 Definition**
[ref: #s1.16.1-definition]
A nested Python function can refer to variables defined in enclosing functions but cannot assign to them. Variable bindings are resolved using lexical scoping.

**1.16.2 Pros**
[ref: #s1.16.2-pros]
Clearer, more elegant code.

**1.16.3 Cons**
[ref: #s1.16.3-cons]
Can lead to confusing bugs (see PEP-0227 example).

```python
i = 4
def foo(x: Iterable[int]):
    def bar():
        print(i, end='')
    # ...
    # A bunch of code here
    # ...
    for i in x:  # Ah, i *is* local to foo, so this is what bar sees
        print(i, end='')
    bar()

# So `foo([1, 2, 3])` will print `1 2 3 3`, not `1 2 3 4`.
```

**1.16.4 Decision**
[ref: #s1.16.4-decision]
Okay to use.

```python
def get_adder(summand1: float) -> Callable[[float], float]:
    """Returns a function that adds numbers to a given number."""
    def adder(summand2: float) -> float:
        return summand1 + summand2

    return adder
```

---

### 1.17 Function and Method Decorators
[ref: #s1.17-function-and-method-decorators]
Use decorators judiciously when there is a clear advantage. Avoid `staticmethod` and limit use of `classmethod`.

**1.17.1 Definition**
[ref: #s1.17.1-definition]
Decorators (the `@` notation) transform functions/methods. `@property` converts methods into dynamically computed attributes.

```python
class C:
    @my_decorator
    def method(self):
        # method body ...
        pass

# Is equivalent to:

class C:
    def method(self):
        # method body ...
        pass
    method = my_decorator(method)
```

**1.17.2 Pros**
[ref: #s1.17.2-pros]
Elegantly specifies transformations; eliminates repetitive code; enforces invariants.

**1.17.3 Cons**
[ref: #s1.17.3-cons]
Can perform arbitrary operations, resulting in surprising implicit behavior. Decorators execute at object definition time; failures are hard to recover from.

**1.17.4 Decision**
[ref: #s1.17.4-decision]
- Use decorators judiciously when there is a clear advantage.
- Decorators must follow the same import and naming guidelines as functions.
- A decorator docstring must clearly state that the function is a decorator.
- Write unit tests for decorators.
- Avoid external dependencies in the decorator itself (files, sockets, DB connections), since they might not be available at import time.
- A decorator called with valid parameters should be guaranteed to succeed in all cases.
- NEVER use `staticmethod` unless forced to integrate with an existing library API. Write a module-level function instead.
- Use `classmethod` only when writing a named constructor, or a class-specific routine that modifies necessary global state such as a process-wide cache.

---

### 1.18 Threading
[ref: #s1.18-threading]
Do not rely on the atomicity of built-in types. While Python's built-in data types such as dictionaries appear to have atomic operations, there are corner cases where they aren't atomic (e.g., if `__hash__` or `__eq__` are implemented as Python methods), and their atomicity should not be relied upon. Neither should you rely on atomic variable assignment (since this depends on dictionaries).

- Use the `queue` module's `Queue` data type as the preferred way to communicate data between threads.
- Otherwise, use the `threading` module and its locking primitives.
- Prefer condition variables and `threading.Condition` instead of using lower-level locks.

---

### 1.19 Power Features
[ref: #s1.19-power-features]
Avoid these features.

**1.19.1 Definition**
[ref: #s1.19.1-definition]
Custom metaclasses, bytecode access, on-the-fly compilation, dynamic inheritance, object reparenting, import hacks, reflection (some uses of `getattr()`), modification of system internals, `__del__` methods implementing customized cleanup, etc.

**1.19.2 Pros**
[ref: #s1.19.2-pros]
Powerful; can make code more compact.

**1.19.3 Cons**
[ref: #s1.19.3-cons]
Harder to read, understand, and debug.

**1.19.4 Decision**
[ref: #s1.19.4-decision]
- Avoid these features in your code.
- Standard library modules and classes that internally use these features are okay (e.g., `abc.ABCMeta`, `dataclasses`, `enum`).

---

### 1.20 Modern Python: from __future__ imports
[ref: #s1.20-modern-python]
**1.20.1 Definition**
[ref: #s1.20.1-definition]
`from __future__ import` statements enable modern features on a per-file basis.

**1.20.2 Pros**
[ref: #s1.20.2-pros]
Smoother runtime version upgrades; modern code is more maintainable.

**1.20.3 Cons**
[ref: #s1.20.3-cons]
May not work on very old interpreter versions.

**1.20.4 Decision**
[ref: #s1.20.4-decision]
- Use of `from __future__ import` statements is encouraged.
- Once you no longer need to run on a version where the features are hidden behind `__future__`, feel free to remove those lines.
- In code that may execute on versions as old as 3.5 rather than >= 3.7, import:
  ```python
  from __future__ import generator_stop
  ```
- Do not remove `__future__` imports until you are confident the code is only used in a sufficiently modern environment.
- Even if you do not currently use the feature a specific future import enables, keeping it prevents later modifications from inadvertently depending on older behavior.

---

### 1.21 Type Annotated Code
[ref: #s1.21-type-annotated-code]
You can annotate Python code with type hints. Type-check the code at build time with a type checking tool like `pytype`. In most cases, when feasible, type annotations are in source files. For third-party or extension modules, annotations can be in stub `.pyi` files.

**1.21.1 Definition**
[ref: #s1.21.1-definition]
```python
def func(a: int) -> list[int]:
    ...

a: SomeType = some_func()
```

**1.21.2 Pros**
[ref: #s1.21.2-pros]
Improves readability and maintainability; converts many runtime errors to build-time errors.

**1.21.3 Cons**
[ref: #s1.21.3-cons]
Type declarations must be kept up to date; may see type errors on code you think is valid; may reduce ability to use Power Features.

**1.21.4 Decision**
[ref: #s1.21.4-decision]
- You are strongly encouraged to enable Python type analysis when updating code.
- When adding or modifying public APIs, include type annotations and enable checking via `pytype` in the build system.
- If undesired side-effects prevent adoption, add a comment with a TODO or link to a bug describing the issue.

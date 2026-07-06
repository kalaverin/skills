## 2. Python Style Rules

### 2.1 Semicolons
[ref: #s2.1-semicolons]
- Do NOT terminate lines with semicolons.
- Do NOT use semicolons to put two statements on the same line.

---

### 2.2 Line Length
[ref: #s2.2-line-length]
- Maximum line length is **80 characters**.
- Explicit exceptions:
  - Long import statements.
  - URLs, pathnames, or long flags in comments.
  - Long string module-level constants not containing whitespace (e.g., URLs or pathnames) that would be inconvenient to split.
  - Pylint disable comments (e.g., `# pylint: disable=invalid-name`).
- Do NOT use a backslash for explicit line continuation. Use Python's implicit line joining inside parentheses, brackets, and braces. If necessary, add an extra pair of parentheses around an expression.
- Backslash-escaped newlines within strings are allowed.
- When a literal string won't fit on one line, use parentheses for implicit line joining.
- Prefer to break lines at the highest possible syntactic level. If you must break a line twice, break it at the same syntactic level both times.
- Within comments, put long URLs on their own line if necessary.
- Docstring summary lines must remain within the 80 character limit.
- If Black or Pyink cannot bring a line below 80, the line may exceed the limit; authors should manually break the line when sensible.

```python
# Yes
foo_bar(self, width, height, color='black', design=None, x='foo',
        emphasis=None, highlight=0)

if (width == 0 and height == 0 and
        color == 'red' and emphasis == 'strong'):

    (bridge_questions.clarification_on
     .average_airspeed_of.unladen_swallow) = 'African or European?'

    with (
        very_long_first_expression_function() as spam,
        very_long_second_expression_function() as beans,
        third_thing() as eggs,
    ):
        place_order(eggs, beans, spam, beans)

# No
if width == 0 and height == 0 and \
        color == 'red' and emphasis == 'strong':

    bridge_questions.clarification_on \
        .average_airspeed_of.unladen_swallow = 'African or European?'

    with very_long_first_expression_function() as spam, \
          very_long_second_expression_function() as beans, \
          third_thing() as eggs:
        place_order(eggs, beans, spam, beans)
```

Prefer to break lines at the highest possible syntactic level. If you must break a line twice, break it at the same syntactic level both times.

```python
# Yes
bridgekeeper.answer(
    name="Arthur", quest=questlib.find(owner="Arthur", perilous=True))

answer = (a_long_line().of_chained_methods()
          .that_eventually_provides().an_answer())

if (
    config is None
    or 'editor.language' not in config
    or config['editor.language'].use_spaces is False
):
    use_tabs()

# No
bridgekeeper.answer(name="Arthur", quest=questlib.find(
        owner="Arthur", perilous=True))

answer = a_long_line().of_chained_methods().that_eventually_provides(
    ).an_answer()

if (config is None or 'editor.language' not in config or config[
    'editor.language'].use_spaces is False):
    use_tabs()
```

Within comments, put long URLs on their own line if necessary.

```python
# Yes
# See details at
# http://www.example.com/us/developer/documentation/api/content/v2.0/csv_file_name_extension_full_specification.html

# No
# See details at
# http://www.example.com/us/developer/documentation/api/content/\
# v2.0/csv_file_name_extension_full_specification.html
```

---

### 2.3 Parentheses
[ref: #s2.3-parentheses]
- Use parentheses sparingly.
- It is fine, though not required, to use parentheses around tuples.
- Do NOT use them in return statements or conditional statements unless using parentheses for implied line continuation or to indicate a tuple.

```python
# Yes
if foo:
    bar()
while x:
    x = bar()
if x and y:
    bar()
if not x:
    bar()
onesie = (foo,)
return foo
return spam, beans
return (spam, beans)
for (x, y) in dict.items(): ...

# No
if (x):
    bar()
if not(x):
    bar()
return (foo)
```

---

### 2.4 Indentation
[ref: #s2.4-indentation]
- Indent code blocks with **4 spaces**.
- Never use tabs.
- Implied line continuation should align wrapped elements vertically, or use a hanging 4-space indent.
- Closing brackets can be placed at the end of the expression or on separate lines, but if on separate lines they should be indented the same as the line with the corresponding opening bracket.

```python
# Yes — Aligned with opening delimiter
foo = long_function_name(var_one, var_two,
                         var_three, var_four)
meal = (spam,
        beans)

foo = {
    'long_dictionary_key': value1 +
                           value2,
    ...
}

# Yes — 4-space hanging indent; nothing on first line
foo = long_function_name(
    var_one, var_two, var_three,
    var_four)
meal = (
    spam,
    beans)

# Yes — 4-space hanging indent; closing parenthesis on new line
foo = long_function_name(
    var_one, var_two, var_three,
    var_four
)
meal = (
    spam,
    beans,
)

# Yes — 4-space hanging indent in dictionary
foo = {
    'long_dictionary_key':
        long_dictionary_value,
    ...
}

# No — Stuff on first line forbidden
foo = long_function_name(var_one, var_two,
    var_three, var_four)
meal = (spam,
    beans)

# No — 2-space hanging indent forbidden
foo = long_function_name(
  var_one, var_two, var_three,
  var_four)

# No — No hanging indent in dictionary
foo = {
    'long_dictionary_key':
    long_dictionary_value,
    ...
}
```

#### 2.4.1 Trailing Commas in Sequences of Items
[ref: #s2.4.1-trailing-commas]
- Trailing commas are recommended only when the closing container token `]`, `)`, or `}` does not appear on the same line as the final element, as well as for tuples with a single element.
- The presence of a trailing comma is also used as a hint to auto-formatters (Black/Pyink) to format the container to one item per line.

```python
# Yes
golomb3 = [0, 1, 3]
golomb4 = [
    0,
    1,
    4,
    6,
]

# No
golomb4 = [
    0,
    1,
    4,
    6,]
```

---

### 2.5 Blank Lines
[ref: #s2.5-blank-lines]
- Two blank lines between top-level definitions (function or class).
- One blank line between method definitions and between the docstring of a `class` and the first method.
- No blank line following a `def` line.
- Use single blank lines as appropriate within functions or methods.
- Blank lines need not be anchored to the definition. Related comments immediately preceding definitions can make sense; consider if the comment might be more useful as part of the docstring.

---

### 2.6 Whitespace
[ref: #s2.6-whitespace]
Follow standard typographic rules for spaces around punctuation.

- No whitespace inside parentheses, brackets, or braces.
- No whitespace before a comma, semicolon, or colon.
- Do use whitespace after a comma, semicolon, or colon, except at the end of a line.
- No whitespace before the open paren/bracket that starts an argument list, indexing, or slicing.
- No trailing whitespace.
- Surround binary operators with a single space on either side for assignment (`=`), comparisons (`==`, `<`, `>`, `!=`, `<=`, `>=`, `in`, `not in`, `is`, `is not`), and Booleans (`and`, `or`, `not`).
- Use judgment for arithmetic operators (`+`, `-`, `*`, `/`, `//`, `%`, `**`, `@`).
- NEVER use spaces around `=` when passing keyword arguments or defining a default parameter value, **except** when a type annotation is present — then DO use spaces around the `=` for the default parameter value.
- Do NOT use spaces to vertically align tokens on consecutive lines (applies to `:`, `#`, `=`, etc.).

```python
# Yes
spam(ham[1], {'eggs': 2}, [])

if x == 4:
    print(x, y)
x, y = y, x

spam(1)
dict['key'] = list[index]

x == 1

def complex(real, imag=0.0): return Magic(r=real, i=imag)
def complex(real, imag: float = 0.0): return Magic(r=real, i=imag)

foo = 1000  # comment
long_name = 2  # comment that should not be aligned

dictionary = {
    'foo': 1,
    'long_name': 2,
}

# No
spam( ham[ 1 ], { 'eggs': 2 }, [ ] )

if x == 4 :
    print(x , y)
x , y = y , x

spam (1)
dict ['key'] = list [index]

x<1

def complex(real, imag = 0.0): return Magic(r = real, i = imag)
def complex(real, imag: float=0.0): return Magic(r = real, i = imag)

foo       = 1000  # comment
long_name = 2     # comment that should not be aligned

dictionary = {
    'foo'      : 1,
    'long_name': 2,
}
```

---

### 2.7 Shebang Line
[ref: #s2.7-shebang-line]
- Most `.py` files do not need a `#!` line.
- Start the main file of a program with `#!/usr/bin/env python3` (supports virtualenvs) or `#!/usr/bin/python3` per PEP-394.
- This line is ignored by Python when importing modules. It is only necessary on a file intended to be executed directly.

---

### 2.8 Comments and Docstrings
[ref: #s2.8-comments-and-docstrings]
Use the right style for module, function, method docstrings, and inline comments.

#### 2.8.1 Docstrings
[ref: #s2.8.1-comments-in-doc-strings]
- Python uses docstrings to document code. A docstring is the first statement in a package, module, class, or function.
- Always use the three-double-quote `"""` format (PEP 257).
- A docstring should be organized as:
  1. Summary line (one physical line, not exceeding 80 characters), terminated by a period, question mark, or exclamation point.
  2. Blank line.
  3. Rest of the docstring starting at the same cursor position as the first quote of the first line.
- There are more formatting guidelines below.

#### 2.8.2 Modules
[ref: #s2.8.2-comments-in-modules]
- Every file should contain license boilerplate appropriate for the project license.
- Files should start with a docstring describing the contents and usage of the module.

```python
"""A one-line summary of the module or program, terminated by a period.

Leave one blank line.  The rest of this docstring should contain an
overall description of the module or program.  Optionally, it may also
contain a brief description of exported classes and functions and/or usage
examples.

Typical usage example:

  foo = ClassFoo()
  bar = foo.function_bar()
"""
```

##### 2.8.2.1 Test Modules
[ref: #s2.8.2.1-test-modules]
- Module-level docstrings for test files are not required.
- Include them only when there is additional information (how to run the test, unusual setup, external environment dependencies, etc.).
- Docstrings that do not provide any new information should not be used.

```python
"""Tests for foo.bar."""
```

#### 2.8.3 Functions and Methods
[ref: #s2.8.3-functions-and-methods]
In this section, "function" means method, function, generator, or property.

- A docstring is **mandatory** for every function that has one or more of:
  - being part of the public API
  - nontrivial size
  - non-obvious logic
- The docstring must give enough information to write a call to the function without reading its code.
- Describe calling syntax and semantics, not implementation details, unless those details are relevant to usage (e.g., side effects on arguments).
- The docstring may be descriptive-style (`"""Fetches rows from a Bigtable."""`) or imperative-style (`"""Fetch rows from a Bigtable."""`), but the style must be consistent within a file.
- The docstring for a `@property` data descriptor should use the same style as for an attribute or function argument (`"""The Bigtable path."""`, not `"""Returns the Bigtable path."""`).
- Special sections (Args, Returns, Raises, Yields, etc.) begin with a heading line ending with a colon.
- All sections other than the heading should maintain a hanging indent of two or four spaces (be consistent within a file).
- These sections can be omitted when the function's name and signature are informative enough.

**Args:**
[ref: #doc-function-args]
- List each parameter by name. A description follows the name, separated by a colon and space or newline.
- If the description is too long for an 80-character line, use a hanging indent of 2 or 4 spaces more than the parameter name (be consistent with the rest of the file).
- Include required type(s) if the code does not contain a corresponding type annotation.
- If a function accepts `*foo` (variable length argument lists) or `**bar`, document those as `*foo` and `**bar`.

**Returns:** (or **Yields:** for generators)

- Describe the type and semantics of the return value.
- Must not be present if the function only returns `None`.
- May be omitted if the docstring starts with "Returns" or "Yields" (e.g., `"""Returns the row from the dataset."""`).
- For complex return types, describe the structure if not obvious.

**Raises:**

- List all exceptions that are relevant to the interface and that the caller should be aware of.
- Do NOT document `ValueError` raised on invalid API usage if that is a programming error; only document exceptions that are part of the contract.

```python
def fetch_smalltable_rows(
    table_handle: smalltable.Table,
    keys: Sequence[bytes | str],
    require_all_keys: bool = False,
) -> Mapping[bytes, tuple[str, ...]]:
    """Fetches rows from a Smalltable.

    Retrieves rows pertaining to the given keys from the Table instance
    represented by table_handle.  String keys will be UTF-8 encoded.

    Args:
        table_handle: An open smalltable.Table instance.
        keys: A sequence of strings representing the key of each table
          row to fetch.  String keys will be UTF-8 encoded.
        require_all_keys: If True only rows with values set for all keys will be
          returned.

    Returns:
        A dict mapping keys to the corresponding table row data
        fetched. Each row is represented as a tuple of strings. For
        example:

        {b'Serak': ('Rigel VII', 'Preparer'),
         b'Zim': ('Irk', 'Invader'),
         b'Lrrr': ('Omicron Persei 8', 'Emperor')}

        Returned keys are always bytes.  If a key from the keys argument is
        missing from the dictionary, then that row was not found in the
        table (and require_all_keys must have been False).

    Raises:
        IOError: An error occurred accessing the smalltable.
    """
```

##### 2.8.3.1 Overridden Methods
[ref: #s2.8.3.1-overridden-methods]
- A method that overrides a base class method does **not** need a docstring if it is explicitly decorated with `@override` (from `typing_extensions` or `typing`), **unless** the overriding method's behavior materially refines the base method's contract or additional details are needed (e.g., side effects).
- If the overriding method is not decorated with `@override`, a docstring is required.
- A trivial docstring like `"""See base class."""` is acceptable when `@override` is present but not sufficient on its own without `@override`.

```python
from typing_extensions import override

class Parent:
    def do_something(self):
        """Parent method, includes docstring."""

class Child(Parent):
    @override
    def do_something(self):
        pass

# Child class, but without @override decorator, a docstring is required.
class Child(Parent):
    def do_something(self):
        pass

# Docstring is trivial; @override is sufficient to indicate that docs can be
# found in the base class.
class Child(Parent):
    @override
    def do_something(self):
        """See base class."""
```

#### 2.8.4 Classes
[ref: #s2.8.4-comments-in-classes]
- Classes should have a docstring below the class definition describing the class.
- Public attributes (excluding properties) should be documented in an `Attributes` section, following the same formatting as a function's `Args`.
- All class docstrings should start with a one-line summary describing what the class instance represents.
- Subclasses of `Exception` should describe what the exception represents, not the context in which it might occur.
- Do NOT repeat unnecessary information (e.g., "class that describes...").

```python
class SampleClass:
    """Summary of class here.

    Longer class information...
    Longer class information...

    Attributes:
        likes_spam: A boolean indicating if we like SPAM or not.
        eggs: An integer count of the eggs we have laid.
    """

    def __init__(self, likes_spam: bool = False):
        """Initializes the instance based on spam preference.

        Args:
          likes_spam: Defines if instance exhibits this preference.
        """
        self.likes_spam = likes_spam
        self.eggs = 0

    @property
    def butter_sticks(self) -> int:
        """The number of butter sticks we have."""

# Yes
class CheeseShopAddress:
    """The address of a cheese shop.

    ...
    """

class OutOfCheeseError(Exception):
    """No more cheese is available."""

# No
class CheeseShopAddress:
    """Class that describes the address of a cheese shop.

    ...
    """

class OutOfCheeseError(Exception):
    """Raised when no more cheese is available."""
```

#### 2.8.5 Block and Inline Comments
[ref: #s2.8.5-block-and-inline-comments]
- Add comments to tricky parts of the code. If you will have to explain it at the next code review, comment it now.
- Complicated operations get a few lines of comments before they commence.
- Non-obvious operations get comments at the end of the line.
- Comments should start at least 2 spaces away from the code, with `#` followed by at least one space.
- NEVER describe the code. Assume the reader knows Python better than you do.

```python
# We use a weighted dictionary search to find out where i is in
# the array.  We extrapolate position based on the largest num
# in the array and the array size and then do binary search to
# get the exact number.

if i & (i-1) == 0:  # True if i is 0 or a power of 2.
```

```python
# BAD COMMENT: Now go through the b array and make sure whenever i occurs
# the next element is i+1
```

#### 2.8.6 Punctuation, Spelling, and Grammar
[ref: #s2.8.6-punctuation-spelling-and-grammar]
- Pay attention to punctuation, spelling, and grammar.
- Comments should be as readable as narrative text, with proper capitalization and punctuation.
- Complete sentences are more readable than sentence fragments.
- Shorter end-of-line comments can be less formal, but be consistent.
- Source code must maintain a high level of clarity and readability.

---

### 2.10 Strings
[ref: #s2.10-strings]
- Use an f-string, the `%` operator, or the `format` method for formatting strings, even when the parameters are all strings.
- Use your best judgment to decide between formatting options.
- A single join with `+` is okay, but do NOT format with `+`.
- Avoid using `+` and `+=` to accumulate a string within a loop. Use a list and `''.join`, or an `io.StringIO` buffer.
- Be consistent with your choice of string quote character within a file. Pick `'` or `"` and stick with it.
- It is okay to use the other quote character to avoid backslash-escaping quotes within the string.
- Prefer `"""` for multi-line strings rather than `'''`. Projects may choose to use `'''` for all non-docstring multi-line strings if and only if they also use `'` for regular strings.
- Docstrings MUST use `"""` regardless.
- Multi-line strings do not flow with the indentation of the rest of the program. If you need to avoid embedding extra space, use concatenated single-line strings or a multi-line string with `textwrap.dedent()`.
- Note that using a backslash inside string literals to escape newlines does not violate the prohibition against explicit line continuation.

```python
# Yes
x = f'name: {name}; score: {n}'
x = '%s, %s!' % (imperative, expletive)
x = '{}, {}'.format(first, second)
x = 'name: %s; score: %d' % (name, n)
x = 'name: %(name)s; score: %(score)d' % {'name': name, 'score': n}
x = 'name: {}; score: {}'.format(name, n)
x = a + b

items = ['<table>']
for last_name, first_name in employee_list:
    items.append('<tr><td>%s, %s</td></tr>' % (last_name, first_name))
items.append('</table>')
employee_table = ''.join(items)

Python('Why are you hiding your eyes?')
Gollum("I'm scared of lint errors.")
Narrator('"Good!" thought a happy Python reviewer.')

long_string = """This is fine if your use case can accept
    extraneous leading spaces."""

long_string = ("And this is fine if you cannot accept\n" +
               "extraneous leading spaces.")

long_string = ("And this too is fine if you cannot accept\n"
               "extraneous leading spaces.")

import textwrap
long_string = textwrap.dedent("""\
    This is also fine, because textwrap.dedent()
    will collapse common leading spaces in each line.""")

# No
x = first + ', ' + second
x = 'name: ' + name + '; score: ' + str(n)

employee_table = '<table>'
for last_name, first_name in employee_list:
    employee_table += '<tr><td>%s, %s</td></tr>' % (last_name, first_name)
employee_table += '</table>'

Python("Why are you hiding your eyes?")
Gollum('The lint. It burns. It burns us.')
Gollum("Always the great lint. Watching. Watching.")

long_string = """This is pretty ugly.
Don't do this.
"""
```

#### 2.10.1 Logging
[ref: #s2.10.1-logging]
- For logging functions that expect a pattern-string (with `%-placeholders`) as their first argument: ALWAYS call them with a string literal (NOT an f-string!) as the first argument, with pattern-parameters as subsequent arguments.
- Some logging implementations collect the unexpanded pattern-string as a queryable field.
- This prevents rendering a message that no logger is configured to output.

```python
# Yes
import tensorflow as tf
logger = tf.get_logger()
logger.info('TensorFlow Version is: %s', tf.__version__)

import os
from absl import logging
logging.info('Current $PAGER is: %s', os.getenv('PAGER', default=''))

homedir = os.getenv('HOME')
if homedir is None or not os.access(homedir, os.W_OK):
    logging.error('Cannot write to home directory, $HOME=%r', homedir)

# No
import os
from absl import logging
logging.info('Current $PAGER is:')
logging.info(os.getenv('PAGER', default=''))

homedir = os.getenv('HOME')
if homedir is None or not os.access(homedir, os.W_OK):
    logging.error(f'Cannot write to home directory, $HOME={homedir!r}')
```

#### 2.10.2 Error Messages
[ref: #s2.10.2-error-messages]
Error messages (e.g., on exceptions like `ValueError`, or messages shown to the user) must follow three guidelines:

1. The message needs to precisely match the actual error condition.
2. Interpolated pieces need to always be clearly identifiable as such.
3. They should allow simple automated processing (e.g., grepping).

```python
# Yes
if not 0 <= p <= 1:
    raise ValueError(f'Not a probability: {p=}')

try:
    os.rmdir(workdir)
except OSError as error:
    logging.warning('Could not remove directory (reason: %r): %r',
                    error, workdir)

# No
if p < 0 or p > 1:  # PROBLEM: also false for float('nan')!
    raise ValueError(f'Not a probability: {p=}')

try:
    os.rmdir(workdir)
except OSError:
    # PROBLEM: Message makes an assumption that might not be true:
    # Deletion might have failed for some other reason, misleading
    # whoever has to debug this.
    logging.warning('Directory already was deleted: %s', workdir)

try:
    os.rmdir(workdir)
except OSError:
    # PROBLEM: The message is harder to grep for than necessary, and
    # not universally non-confusing for all possible values of `workdir`.
    # Imagine someone calling a library function with such code
    # using a name such as workdir = 'deleted'. The warning would read:
    # "The deleted directory could not be deleted."
    logging.warning('The %s directory could not be deleted.', workdir)
```

---

### 2.11 Files, Sockets, and Similar Stateful Resources
[ref: #s2.11-files-sockets-closeables]
- Explicitly close files and sockets when done.
- This extends to closeable resources that internally use sockets (DB connections) and other resources needing similar shutdown (mmap mappings, h5py File objects, matplotlib.pyplot figure windows).
- Do NOT rely on `__del__` for cleanup:
  - No guarantee when `__del__` is invoked.
  - Different Python implementations use different memory management.
  - Unexpected references may keep objects alive longer than intended.
- The preferred way is using the `with` statement.
- For file-like objects that do not support `with`, use `contextlib.closing()`.
- In rare cases where context-based resource management is infeasible, document clearly how resource lifetime is managed.

```python
with open("hello.txt") as hello_file:
    for line in hello_file:
        print(line)

import contextlib
with contextlib.closing(urllib.urlopen("http://www.python.org/")) as front_page:
    for line in front_page:
        print(line)
```

---

### 2.12 TODO Comments
[ref: #s2.12-todo-comments]
- Use `TODO` comments for temporary code, short-term solutions, or good-enough-but-not-perfect code.
- A `TODO` comment begins with `TODO` in all caps, a following colon, and a link to a resource containing context (ideally a bug reference).
- Follow the context with an explanatory string introduced with a hyphen `-`.
- Purpose: consistent `TODO` format searchable for more details.

```python
# TODO: crbug.com/192795 - Investigate cpufreq optimizations.
```

- Old style (formerly recommended, now discouraged for new code):
  ```python
  # TODO(crbug.com/192795): Investigate cpufreq optimizations.
  # TODO(yourusername): Use a "*" here for concatenation operator.
  ```
- Avoid TODOs that refer to an individual or team as the context.
- If the TODO is of the form "At a future date do something", include a very specific date or a very specific event that future maintainers will comprehend. Issues are ideal for tracking this.

---

### 2.13 Imports Formatting
[ref: #s2.13-imports-formatting]
- Imports should be on separate lines; exceptions for `typing` and `collections.abc` imports are allowed.
- Imports are always put at the top of the file, just after any module comments and docstrings, and before module globals and constants.
- Group imports from most generic to least generic:
  1. Python future import statements (e.g., `from __future__ import annotations`).
  2. Python standard library imports (e.g., `import sys`).
  3. Third-party module or package imports (e.g., `import tensorflow as tf`).
  4. Code repository sub-package imports (e.g., `from otherproject.ai import mind`).
  5. Deprecated: application-specific imports that are part of the same top-level sub-package as this file. New code is encouraged not to bother with this; treat application-specific sub-package imports the same as other sub-package imports.
- Within each grouping, imports should be sorted lexicographically, ignoring case, according to each module's full package path.
- Code may optionally place a blank line between import sections.

```python
# Yes
from collections.abc import Mapping, Sequence
import os
import sys
from typing import Any, NewType

# No
import os, sys
```

```python
import collections
import queue
import sys

from absl import app
from absl import flags
import bs4
import cryptography
import tensorflow as tf

from book.genres import scifi
from myproject.backend import huxley
from myproject.backend.hgwells import time_machine
from myproject.backend.state_machine import main_loop
from otherproject.ai import body
from otherproject.ai import mind
from otherproject.ai import soul
```

---

### 2.14 Statements
[ref: #s2.14-statements]
- Generally only one statement per line.
- You may put the result of a test on the same line as the test only if the entire statement fits on one line.
- You can NEVER do so with `try`/`except` since `try` and `except` can't both fit on the same line.
- You can only do so with an `if` if there is no `else`.

```python
# Yes
if foo: bar(foo)

# No
if foo: bar(foo)
else:   baz(foo)

try:               bar(foo)
except ValueError: baz(foo)

try:
    bar(foo)
except ValueError: baz(foo)
```

---

### 2.15 Accessors (Getters and Setters)
[ref: #s2.15-accessors]
- Getter and setter functions should be used when they provide a meaningful role or behavior for getting or setting a variable's value.
- Use them when getting or setting is complex or the cost is significant.
- If a pair simply reads and writes an internal attribute, make the internal attribute public instead.
- If setting a variable invalidates or rebuilds state, it should be a setter function.
- Alternatively, properties may be an option when simple logic is needed.
- Getters and setters should follow Naming guidelines: `get_foo()` and `set_foo()`.
- If past behavior allowed access through a property, do NOT bind the new getter/setter functions to the property. Any code still attempting to access by the old method should break visibly.

---

### 2.16 Naming
[ref: #s2.16-naming]
Names should be descriptive. Avoid abbreviation. Do not use abbreviations that are ambiguous or unfamiliar to readers outside your project, and do not abbreviate by deleting letters within a word. Always use a `.py` filename extension. Never use dashes.

Format examples: `module_name`, `package_name`, `ClassName`, `method_name`, `ExceptionName`, `function_name`, `GLOBAL_CONSTANT_NAME`, `global_var_name`, `instance_var_name`, `function_parameter_name`, `local_var_name`, `query_proper_noun_for_thing`, `send_acronym_via_https`.

#### 2.16.1 Names to Avoid
[ref: #s2.16.1-names-to-avoid]
- Single character names, EXCEPT for specifically allowed cases:
  - Counters or iterators (e.g., `i`, `j`, `k`, `v`, et al.)
  - `e` as an exception identifier in `try/except` statements.
  - `f` as a file handle in `with` statements.
  - Private type variables with no constraints (e.g., `_T = TypeVar("_T")`, `_P = ParamSpec("_P")`).
  - Names matching established notation in a reference paper or algorithm.
  - Be mindful not to abuse single-character naming. Descriptiveness should be proportional to the name's scope of visibility.
- Dashes (`-`) in any package/module name.
- `__double_leading_and_trailing_underscore__` names (reserved by Python).
- Offensive terms.
- Names that needlessly include the type of the variable (e.g., `id_to_name_dict`).

#### 2.16.2 Naming Conventions
[ref: #s2.16.2-naming-conventions]
- "Internal" means internal to a module, or protected or private within a class.
- Prepending a single underscore (`_`) has some support for protecting module variables and functions (linters will flag protected member access). It is okay for unit tests to access protected constants from modules under test.
- Prepending a double underscore (`__` aka "dunder") to an instance variable or method effectively makes it private (name mangling); discourage its use as it impacts readability and testability. Prefer a single underscore.
- Place related classes and top-level functions together in a module. Unlike Java, there is no need to limit yourself to one class per module.
- Use `CapWords` for class names, but `lower_with_under.py` for module names. Old `CapWords.py` modules exist but are now discouraged.
- New unit test files follow PEP 8 compliant `lower_with_under` method names: `test_<method_under_test>_<state>`. For consistency with legacy modules using `CapWords` function names, underscores may appear in method names starting with `test` to separate logical components (e.g., `test<MethodUnderTest>_<state>`).

#### 2.16.3 File Naming
[ref: #s2.16.3-file-naming]
- Python filenames must have a `.py` extension and must not contain dashes (`-`).
- This allows them to be imported and unittested.
- If you want an executable accessible without the extension, use a symbolic link or a simple bash wrapper containing `exec "$0.py" "$@"`.

#### 2.16.4 Guidelines Derived from Guido's Recommendations
[ref: #s2.16.4-guidelines-derived-from-guidos-recommendations]
| Type | Public | Internal |
|---|---|---|
| Packages | `lower_with_under` | |
| Modules | `lower_with_under` | `_lower_with_under` |
| Classes | `CapWords` | `_CapWords` |
| Exceptions | `CapWords` | |
| Functions | `lower_with_under()` | `_lower_with_under()` |
| Global/Class Constants | `CAPS_WITH_UNDER` | `_CAPS_WITH_UNDER` |
| Global/Class Variables | `lower_with_under` | `_lower_with_under` |
| Instance Variables | `lower_with_under` | `_lower_with_under` (protected) |
| Method Names | `lower_with_under()` | `_lower_with_under()` (protected) |
| Function/Method Parameters | `lower_with_under` | |
| Local Variables | `lower_with_under` | |

#### 2.16.5 Mathematical Notation
[ref: #math-notation]
- For mathematically-heavy code, short variable names that would otherwise violate the style guide are preferred when they match established notation in a reference paper or algorithm.
- Cite the source of naming conventions, preferably with a hyperlink, in a comment or docstring.
- Prefer PEP8-compliant `descriptive_names` for public APIs.
- Use a narrowly-scoped `pylint: disable=invalid-name` directive to silence warnings.

---

### 2.17 Main
[ref: #s2.17-main]
- `pydoc` and unit tests require modules to be importable.
- If a file is meant to be used as an executable, its main functionality should be in a `main()` function.
- Always check `if __name__ == '__main__':` before executing the main program.
- When using `absl`, use `app.run`:

```python
from absl import app
...

def main(argv: Sequence[str]):
    # process non-flag arguments
    ...

if __name__ == '__main__':
    app.run(main)
```

- Otherwise:

```python
def main():
    ...

if __name__ == '__main__':
    main()
```

- Be careful not to call functions, create objects, or perform other operations at the top level that should not execute when the file is being `pydoc`ed.

---

### 2.18 Function Length
[ref: #s2.18-function-length]
- Prefer small and focused functions.
- No hard limit on function length.
- If a function exceeds about 40 lines, think about whether it can be broken up without harming program structure.
- Keeping functions short and simple makes them easier to read and modify.
- Do not be intimidated by modifying existing long functions; if working with such a function proves difficult, consider breaking it into smaller pieces.

---

### 2.19 Type Annotations
[ref: #s2.19-type-annotations]
#### 2.19.1 General Rules
[ref: #s2.19.1-general-rules]
- Familiarize yourself with type hints.
- Annotating `self` or `cls` is generally not necessary. `Self` can be used if necessary for proper type information.
- Do NOT feel compelled to annotate the return value of `__init__` (where `None` is the only valid option).
- If any other variable or returned type should not be expressed, use `Any`.
- You are not required to annotate all functions in a module.
  - At least annotate your public APIs.
  - Use judgment to balance safety/clarity vs. flexibility.
  - Annotate code prone to type-related errors (previous bugs or complexity).
  - Annotate code that is hard to understand.
  - Annotate code as it becomes stable from a types perspective.

```python
from typing import Self

class BaseClass:
    @classmethod
    def create(cls) -> Self:
        ...

    def difference(self, other: Self) -> float:
        ...
```

#### 2.19.2 Line Breaking
[ref: #s2.19.2-line-breaking]
- Follow existing indentation rules.
- After annotating, many function signatures become "one parameter per line".
- To ensure the return type gets its own line, place a comma after the last parameter.
- Always prefer breaking between variables, not between variable names and type annotations.
- If everything fits on one line, keep it on one line.
- If the combination of function name, last parameter, and return type is too long, indent by 4 in a new line.
- When using line breaks, prefer putting each parameter and the return type on their own lines, aligning the closing parenthesis with `def`.
- Optionally, the return type may be put on the same line as the last parameter.
- `pylint` allows moving the closing parenthesis to a new line and aligning with the opening one, but this is less readable.
- Prefer not to break types. If they are too long, keep sub-types unbroken.
- If a single name and type is too long, consider using a type alias. The last resort is to break after the colon and indent by 4.

```python
# Yes
def my_method(
    self,
    first_var: int,
    second_var: Foo,
    third_var: Bar | None,
) -> int:
    ...

# Yes (fits on one line)
def my_method(self, first_var: int) -> int:
    ...

# Yes
def my_method(
    self,
    other_arg: MyLongType | None,
) -> tuple[MyLongType1, MyLongType1]:
    ...

# Okay
def my_method(
    self,
    first_var: int,
    second_var: int) -> dict[OtherLongType, MyLongType]:
    ...

# No
def my_method(self,
              other_arg: MyLongType | None,
             ) -> dict[OtherLongType, MyLongType]:
    ...

# Yes (type too long, break after colon)
def my_function(
    long_variable_name:
        long_module_name.LongTypeName,
) -> None:
    ...

# No
def my_function(
    long_variable_name: long_module_name.
        LongTypeName,
) -> None:
    ...
```

As in the examples above, prefer not to break types. However, sometimes they are too long to be on a single line (try to keep sub-types unbroken).

```python
def my_method(
    self,
    first_var: tuple[list[MyLongType1],
                     list[MyLongType2]],
    second_var: list[dict[
        MyLongType3, MyLongType4]],
) -> None:
    ...
```

#### 2.19.3 Forward Declarations
[ref: #s2.19.3-forward-declarations]
- If you need to use a class name from the same module that is not yet defined, either use `from __future__ import annotations` or use a string for the class name.

```python
# Yes
from __future__ import annotations

class MyClass:
    def __init__(self, stack: Sequence[MyClass], item: OtherClass) -> None:
        ...

class OtherClass:
    ...

# Yes
class MyClass:
    def __init__(self, stack: Sequence['MyClass'], item: 'OtherClass') -> None:
        ...

class OtherClass:
    ...
```

#### 2.19.4 Default Values
[ref: #s2.19.4-default-values]
- As per PEP-008, use spaces around the `=` only for arguments that have both a type annotation and a default value.

```python
# Yes
def func(a: int = 0) -> int:
    ...

# No
def func(a:int=0) -> int:
    ...
```

#### 2.19.5 NoneType
[ref: #s2.19.5-nonetype]
- `NoneType` is a first-class type. For typing purposes, `None` is an alias for `NoneType`.
- If an argument can be `None`, it MUST be declared.
- Use `|` union type expressions (recommended in Python 3.10+), or older `Optional` and `Union` syntaxes.
- Use explicit `X | None` instead of implicit.
- Earlier type checkers allowed `a: str = None` to mean `a: str | None = None`; this is no longer preferred.

```python
# Yes
def modern_or_union(a: str | int | None, b: str | None = None) -> str:
    ...

def union_optional(a: Union[str, int, None], b: Optional[str] = None) -> str:
    ...

# No
def nullable_union(a: Union[None, str]) -> str:
    ...

def implicit_optional(a: str = None) -> str:
    ...
```

#### 2.19.6 Type Aliases
[ref: #s2.19.6-type-aliases]
- You can declare aliases of complex types.
- The name of an alias should be `CapWorded`.
- If the alias is used only in this module, it should be `_Private`.
- Note that `: TypeAlias` annotation is only supported in Python 3.10+.

```python
from typing import TypeAlias

_LossAndGradient: TypeAlias = tuple[tf.Tensor, tf.Tensor]
ComplexTFMap: TypeAlias = Mapping[str, _LossAndGradient]
```

#### 2.19.7 Ignoring Types
[ref: #s2.19.7-ignoring-types]
- You can disable type checking on a line with `# type: ignore`.
- `pytype` has a disable option for specific errors (similar to lint):
  ```python
  # pytype: disable=attribute-error
  ```

#### 2.19.8 Typing Variables
[ref: #s2.19.8-typing-variables]
**Annotated Assignments**
[ref: #annotated-assignments]
- If an internal variable has a type that is hard or impossible to infer, specify its type with an annotated assignment: a colon and type between the variable name and value.

```python
a: Foo = SomeUndecoratedFunction()
```

**Type Comments**
[ref: #type-comments]
- Do NOT add new uses of `# type: <type name>` comments. They were necessary before Python 3.6.

```python
# Do not add new instances of this:
a = SomeUndecoratedFunction()  # type: Foo
```

#### 2.19.9 Tuples vs Lists
[ref: #s2.19.9-tuples-vs-lists]
- Typed lists can only contain objects of a single type.
- Typed tuples can either have a single repeated type or a set number of elements with different types. The latter is commonly used as the return type from a function.

```python
a: list[int] = [1, 2, 3]
b: tuple[int, ...] = (1, 2, 3)
c: tuple[int, str, float] = (1, "2", 3.5)
```

#### 2.19.10 Type Variables
[ref: #s2.19.10-typevars]
- Use `TypeVar` and `ParamSpec` for generics.
- A `TypeVar` can be constrained.
- Use `AnyStr` for multiple annotations that can be `bytes` or `str` and must all be the same type.
- A type variable must have a descriptive name, UNLESS it meets ALL of the following:
  - not externally visible
  - not constrained

```python
from collections.abc import Callable
from typing import ParamSpec, TypeVar

_P = ParamSpec("_P")
_T = TypeVar("_T")

def next(l: list[_T]) -> _T:
    return l.pop()

def print_when_called(f: Callable[_P, _T]) -> Callable[_P, _T]:
    def inner(*args: _P.args, **kwargs: _P.kwargs) -> _T:
        print("Function was called")
        return f(*args, **kwargs)
    return inner

# Constrained
AddableType = TypeVar("AddableType", int, float, str)
def add(a: AddableType, b: AddableType) -> AddableType:
    return a + b

# AnyStr
from typing import AnyStr
def check_length(x: AnyStr) -> AnyStr:
    if len(x) <= 42:
        return x
    raise ValueError()

# Yes
_T = TypeVar("_T")
_P = ParamSpec("_P")
AddableType = TypeVar("AddableType", int, float, str)
AnyFunction = TypeVar("AnyFunction", bound=Callable)

# No
T = TypeVar("T")
P = ParamSpec("P")
_T = TypeVar("_T", int, float, str)  # constrained must be descriptive
_F = TypeVar("_F", bound=Callable)
```

#### 2.19.11 String Types
[ref: #s2.19.11-string-types]
- Do NOT use `typing.Text` in new code. It is only for Python 2/3 compatibility.
- Use `str` for string/text data.
- Use `bytes` for binary data.
- If all string types of a function are always the same, use `AnyStr`.

```python
def deals_with_text_data(x: str) -> str:
    ...

def deals_with_binary_data(x: bytes) -> bytes:
    ...
```

#### 2.19.12 Imports For Typing
[ref: #s2.19.12-imports-for-typing]
- For symbols from `typing` or `collections.abc` used to support static analysis and type checking, always import the symbol itself.
- You are explicitly allowed to import multiple specific symbols on one line from `typing` and `collections.abc`.
- Treat names from `typing` or `collections.abc` similarly to keywords; do not define them in your Python code.
- If there is a collision between a type and an existing name, import it using `import x as y`.
- When annotating function signatures, prefer abstract container types like `collections.abc.Sequence` over concrete types like `list`.
- If you need a concrete type (e.g., a tuple of typed elements), prefer built-in types like `tuple` over parametric type aliases from `typing` (e.g., `typing.Tuple`).

```python
from collections.abc import Mapping, Sequence
from typing import Any, Generic, cast, TYPE_CHECKING

from typing import Any as AnyType

# Prefer abstract containers
def transform_coordinates(original: Sequence[tuple[float, float]]) -> Sequence[tuple[float, float]]:
    ...
```

```python
# No — prefer built-in generic types over typing module aliases
from typing import List, Tuple

def transform_coordinates(original: List[Tuple[float, float]]) -> List[Tuple[float, float]]:
    ...
```

#### 2.19.13 Conditional Imports
[ref: #s2.19.13-conditional-imports]
- Use conditional imports only in exceptional cases where additional imports needed for type checking must be avoided at runtime.
- This pattern is discouraged; prefer refactoring to allow top-level imports.
- Imports needed only for type annotations can be placed within `if TYPE_CHECKING:`.
- Conditionally imported types need to be referenced as strings, to be forward compatible with Python 3.6 where annotation expressions are evaluated.
- Only entities used solely for typing should be defined here (including aliases).
- The block should be right after all normal imports.
- There should be no empty lines in the typing imports list.
- Sort this list as if it were a regular imports list.

```python
import typing
if typing.TYPE_CHECKING:
    import sketch

def f(x: "sketch.Sketch"): ...
```

#### 2.19.14 Circular Dependencies
[ref: #s2.19.14-circular-dependencies]
- Circular dependencies caused by typing are code smells. Refactor if possible.
- If technically necessary but build systems prevent it, replace the module with `Any`.
- Set a meaningful alias and use the real type name from this module (any attribute of `Any` is `Any`).
- Alias definitions should be separated from the last import by one line.

```python
from typing import Any

some_mod = Any  # some_mod.py imports this module.
...

def my_method(self, var: "some_mod.SomeType") -> None:
    ...
```

#### 2.19.15 Generics
[ref: #s2.19.15-generics]
- When annotating, prefer to specify type parameters for generic types in a parameter list; otherwise parameters will be assumed to be `Any`.
- If the best type parameter for a generic is `Any`, make it explicit, but consider whether `TypeVar` might be more appropriate.

```python
# Yes
def get_names(employee_ids: Sequence[int]) -> Mapping[int, str]:
    ...

# No — interpreted as Sequence[Any] -> Mapping[Any, Any]
def get_names(employee_ids: Sequence) -> Mapping:
    ...

# No — Any is explicit but TypeVar is better
def get_names(employee_ids: Sequence[Any]) -> Mapping[Any, str]:
    """Returns a mapping from employee ID to employee name for given IDs."""

# Yes
_T = TypeVar('_T')
def get_names(employee_ids: Sequence[_T]) -> Mapping[_T, str]:
    """Returns a mapping from employee ID to employee name for given IDs."""
```

#### 2.19.16 Build Dependencies
[ref: #s2.19.16-build-dependencies]
- Type annotations can be placed in stub `.pyi` files for third-party or extension modules.
- For code within the same repository, prefer inline annotations.

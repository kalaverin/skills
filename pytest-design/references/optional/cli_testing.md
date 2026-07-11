---
subject: "Exercise command-line interfaces in-process and reserve subprocess for installed binaries: design `argparse` as `main(arg_list)` with `shlex.split`+`capsys`, drive `click` via `CliRunner`, drive `typer` via its runner, and smoke-test entry points with `subprocess.run`; parametrize missing/invalid/unknown args, `--help`, `--version`, and error paths."
index:
  - anchor: cli-testing-argparse
    what: "Designing an `argparse` entry point as `main(arg_list)` that accepts an optional argument list so tests call it directly in-process and assert on `SystemExit.code` and captured output."
    problem: "Mutating global `sys.argv` and spawning subprocesses makes CLI test nondeterministic, so entry point must run in-process with captured streams; in-process invocation, argument list, exit code assert, no global state, flag variants, deterministic output."
    use_when: "CLI entry point can run in process through argument list, global `sys.argv` mutation is unnecessary, and exit code plus captured streams define behavior; in process invocation, argument list, exit code assert, no global state, flag variants, deterministic output, shlex split."
    avoid_when: "Do not patch `sys.argv` directly instead of designing `main(arg_list)`, do not run pytest with `-s` to see output (use `capsys` or `capfd`), do not assert equality against the full output string, and do not ignore `SystemExit.code` (verify it via `exc_info.value.code`)."
    expected: "The CLI runs in-process with no global-state mutation, exit codes and output substrings are asserted deterministically, and harmless message changes do not break tests."
  - anchor: cli-testing-click
    what: "Driving `click` commands with `click.testing.CliRunner` and asserting on structured `result` fields (`exit_code`, `output`, `exception`) instead of global capture fixtures."
    problem: "Click command with prompts, file-system side effects, or subcommands must run isolated without process-wide capture, asserting structured result fields; isolated filesystem, prompt input, subcommand routing, result exit code, result output, runner invoke."
    use_when: "Click command includes prompts, filesystem side effects, or subcommands, and structured runner result gives stronger assertion than global capture; isolated filesystem, prompt input, subcommand routing, result exit code, result output, runner invoke, command result."
    avoid_when: "Do not run pytest with `-s` to observe output (use the runner's result fields), do not assert equality against the entire output string, and do not ignore the exit code (verify `result.exit_code`); use `catch_exceptions=False` and `mix_stderr=False` only to target specific error-formatting or stderr-only behavior."
    expected: "Commands run through `CliRunner` with isolated side effects, and assertions read `result.exit_code`, `result.output`, and `result.exception` rather than global streams."
  - anchor: cli-testing-typer
    what: "Using `typer.testing.CliRunner` exactly like Click's runner, and wrapping plain functions in a temporary `typer.Typer()` app to test them as commands."
    problem: "Typer application or Typer-annotated function must run as command with same structured-result assertions, covering routing and option aliases; ad-hoc command, temporary app, runner invoke, alias behavior, exit code, consistent routing."
    use_when: "Typer app or Typer annotated function must run as command, with same runner semantics as Click and alias behavior under assertion; ad hoc command, temporary app, runner invoke, alias behavior, exit code, consistent routing, typed command."
    avoid_when: "Do not run pytest with `-s` to see output (use the runner's result fields), do not assert equality against the entire output string, and do not ignore the exit code (verify `result.exit_code`)."
    expected: "Typer apps and ad-hoc commands run through `CliRunner` with consistent routing and alias behavior, asserted via `result.exit_code` and `result.output`."
  - anchor: cli-testing-subprocess
    what: "Shelling out with `subprocess.run(shlex.split(cmd), capture_output=True, text=True)` to verify an installed entry point as a user would run it, asserting only `returncode` and salient output fragments."
    problem: "Installed entry point runs as real process that in-process runners cannot reach, yet asserting whole output strings makes test brittle; packaged binary, console script, executable smoke test, end-to-end invocation, deployment artifact, fragment assertion."
    use_when: "Installed entry point cannot be imported, packaging smoke test needs real process, and only return code plus salient fragments matter; packaged binary, console script, executable smoke test, end to end invocation, deployment artifact, fragment assertion, return code."
    avoid_when: "Do not shell out when an in-process invocation would exercise the same behavior, and do not assert equality against the entire output string."
    expected: "The installed entry point is verified end-to-end with `returncode` and fragment assertions, while in-process runners remain the default for importable CLIs."
  - anchor: cli-testing-common-cases
    what: "A framework-independent checklist of invariant categories (valid arguments, missing required argument, invalid value or wrong type, unknown flag, `--help`/`--version`, error path) and what to assert for each."
    problem: "CLI behavior drifts across refactors unless every framework shares one invariant sweep over valid, missing, invalid, unknown, help, version, and error paths; invariant categories, parametrized matrix, flag coverage, error path, help version, refactor safety."
    use_when: "CLI behavior must stay stable across refactors, valid missing invalid unknown help version and error paths form one matrix; invariant categories, parametrized matrix, flag coverage, error path, help version, refactor safety, cli contract."
    avoid_when: "Do not write a separate test per flag or argument — collapse the categories into one `@pytest.mark.parametrize` invariant sweep."
    expected: "Every CLI is covered across all invariant categories with a single parametrized matrix."
libraries:
  - click>=8.4
  - typer
---

# CLI TESTING

## argparse CLIs
[ref: #cli-testing-argparse]

Design the entry point to accept an optional argument list so tests can call it directly instead of mutating global state.

Use this approach for `argparse`-based CLIs or any thin wrapper around them.

```python
import shlex

import pytest
from faker import Faker
from pytest import CaptureFixture

from mypackage import cli


def test_main_prints_version_and_exits(
    capsys: CaptureFixture[str],
    monkey: pytest.MonkeyPatch,
    fake: Faker,
) -> None:
    """
    Given: a CLI version patched to a generated value.
    When: the CLI is invoked with --version.
    Then: it exits with code 0 and prints the version.
    """
    # --- Arrange ---
    version = fake.numerify("%#.%#.%#")
    monkey.setattr(cli, "__version__", version)

    # --- Act ---
    with pytest.raises(SystemExit) as exc_info:
        cli.main([fake.word(), "--version"])
    captured = capsys.readouterr()

    # --- Assert ---
    assert exc_info.value.code == 0
    assert version in captured.out
```

Prefer `shlex.split()` to turn readable command-line strings into argument lists.

```python
def test_main_greets_by_name(
    capsys: CaptureFixture[str],
    fake: Faker,
) -> None:
    """
    Given: a generated name.
    When: the CLI is invoked with --name.
    Then: the captured output contains the name.
    """
    # --- Arrange ---
    name = fake.first_name()
    args = shlex.split(f"--name {name}")

    # --- Act ---
    cli.main(args)
    captured = capsys.readouterr()

    # --- Assert ---
    assert name in captured.out
```

**Variety booster:** parametrize over short and long flag forms, then assert that `SystemExit.code` and captured substrings match for both valid and invalid inputs.

## click CLIs
[ref: #cli-testing-click]

Drive `click` commands with `click.testing.CliRunner` and assert on structured result fields instead of global capture fixtures.

Use this approach for `click` commands, especially when testing prompts, file-system side effects, or `click.Group` subcommands.

```python
from pathlib import Path

from click.testing import CliRunner
from faker import Faker

from mypackage.cli import create_file, greet


def test_click_greet_outputs_name(fake: Faker) -> None:
    """
    Given: a generated name.
    When: the click greet command is invoked.
    Then: it exits cleanly and the output contains the name.
    """
    # --- Arrange ---
    runner = CliRunner()
    name = fake.first_name()

    # --- Act ---
    result = runner.invoke(greet, ["--name", name])

    # --- Assert ---
    assert result.exit_code == 0
    assert name in result.output
    assert result.exception is None


def test_click_prompt_writes_file(fake: Faker) -> None:
    """
    Given: a filename and content supplied via prompt.
    When: the click create_file command is invoked.
    Then: the file is created with the expected content.
    """
    # --- Arrange ---
    runner = CliRunner()
    filename = fake.file_name(extension="txt")
    content = fake.sentence()

    # --- Act ---
    with runner.isolated_filesystem():
        result = runner.invoke(
            create_file,
            ["--name", filename],
            input=f"{content}\n",
        )

        # --- Assert ---
        assert result.exit_code == 0
        path = Path(filename)
        assert path.exists()
        assert content in path.read_text()
```

On Click 8.4+, you can pass `capture="fd"` for file-descriptor-level capture when the CLI writes directly to file descriptors rather than standard streams.

**Variety booster:** combine `input=`, `catch_exceptions=False`, and `mix_stderr=False` to exercise error formatting, prompt cancellation, and stderr-only messages.

## typer CLIs
[ref: #cli-testing-typer]

Use `typer.testing.CliRunner` exactly like `click.testing.CliRunner`, and wrap plain functions in a temporary `typer.Typer()` app when you want to test them as commands.

Use this approach for `typer` applications and for testing functions that Typer annotates as commands.

```python
import typer
from typer.testing import CliRunner
from faker import Faker

from mypackage.cli import app, greet_user


def test_typer_app_greets_by_name(fake: Faker) -> None:
    """
    Given: a generated name.
    When: the typer app greet subcommand is invoked.
    Then: it exits cleanly and the output contains the name.
    """
    # --- Arrange ---
    runner = CliRunner()
    name = fake.first_name()

    # --- Act ---
    result = runner.invoke(app, ["greet", "--name", name])

    # --- Assert ---
    assert result.exit_code == 0
    assert name in result.output


def test_plain_function_as_typer_command(fake: Faker) -> None:
    """
    Given: a plain function registered as a temporary typer command.
    When: the temporary app is invoked with --name.
    Then: it exits cleanly and the output contains the name.
    """
    # --- Arrange ---
    runner = CliRunner()
    temp_app = typer.Typer()
    temp_app.command()(greet_user)
    name = fake.first_name()

    # --- Act ---
    result = runner.invoke(temp_app, ["--name", name])

    # --- Assert ---
    assert result.exit_code == 0
    assert name in result.output
```

**Variety booster:** register the same function under multiple command names in the test app to verify that Typer routing and option aliases behave consistently.

## subprocess smoke tests
[ref: #cli-testing-subprocess]

Reserve shelling out for installed entry points, packaging smoke tests, or when the CLI cannot be imported, and assert only on exit code and salient output fragments.

Use this approach when you need to verify the executable as a user would run it.

```python
import shlex
import subprocess

from faker import Faker


def test_installed_entrypoint_shows_help(fake: Faker) -> None:
    """
    Given: an installed CLI entry point name.
    When: it is invoked with --help via subprocess.
    Then: it exits with code 0 and prints a usage line.
    """
    # --- Arrange ---
    entry_point = fake.word()

    # --- Act ---
    result = subprocess.run(
        shlex.split(f"{entry_point} --help"),
        capture_output=True,
        text=True,
    )

    # --- Assert ---
    assert result.returncode == 0
    assert "usage:" in result.stdout.lower()
```

Replace `entry_point` with the actual installed command name in your project.

**Variety booster:** run the same scenario through both the in-process runner and a subprocess invocation, and assert that both produce the same exit code.

## Common test cases
[ref: #cli-testing-common-cases]

Cover the same invariant categories regardless of framework so that CLI behavior stays predictable across refactors.

| Scenario | What to assert |
|---|---|
| Valid arguments | Exit code `0`, expected output substrings present, no unhandled exception. |
| Missing required argument | Non-zero exit code and a usage or help hint in `stdout` or `stderr`. |
| Invalid value or wrong type | Non-zero exit code and a clear error substring that explains the failure. |
| Unknown flag | Non-zero exit code and a usage or help hint. |
| `--help` / `--version` | Exit code `0`, expected metadata substrings, not an exact full-string match. |
| Error path | Non-zero exit code; the expected exception type when invoked in-process. |

Use `@pytest.mark.parametrize` to combine flag variants and expected outcomes without multiplying boilerplate.

**Variety booster:** for each error path, assert both the exit code and that the message contains the offending value, so the test guards against generic error placeholders.

## Anti-patterns
[ref: #cli-testing-anti-patterns]

Avoid brittle global state, leaked output, and exact-string assertions that break on harmless message changes.

**Variety booster:** add a focused regression test for every anti-pattern you remove from an existing suite.

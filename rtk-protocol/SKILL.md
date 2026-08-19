---
name: rtk-protocol
description: "Token-optimized command execution via RTK (Rust Token Killer). Activates automatically when the `rtk` binary is detected in PATH. Governs the always-prefix golden rule (including inside && chains), the full dedicated-filter command inventory (files, search, git/forges, cloud/DB, language toolchains, infrastructure, network, meta/ops) pinned to the installed rtk version, and the precedence contract with mandatory-tools tool selection and the MCP tool layer."
triggers:
  files: "command -v rtk >/dev/null 2>&1"
  reason: "The skill activates only where the rtk binary actually exists; without it the instructions would be dead weight."
requires:
  - mandatory-tools
version: 0.1.0
---

# SKILL: RTK (Rust Token Killer) — Token-Optimized Commands

RTK is a high-performance CLI proxy that filters and summarizes command output before it reaches the agent's context: when it has a dedicated filter for a command, it compacts the output (typically 60–90% token reduction); when it does not, it passes the command through unchanged — so prefixing is always safe. This skill owns when and how the agent prefixes commands with `rtk`.

## 1. The Golden Rule

[ref: #rtk-golden-rule]

**Always prefix commands with `rtk`.** If RTK has a dedicated filter, it uses it; if not, the command passes through unchanged. This holds even inside command chains with `&&`:

```bash
# ❌ Wrong
git add . && git commit -m "msg" && git push

# ✅ Correct
rtk git add . && rtk git commit -m "msg" && rtk git push
```

## 2. Version Pin (refresh trigger)

[ref: #rtk-version-pin]

- The §3 inventory is generated from `rtk --help` of **rtk 0.42.4** (captured 2026-08-03).
- On ANY rtk upgrade: run `rtk --help`, diff the command list against §3, update the inventory, and bump the pin. An installed rtk NEWER than the pin means this skill may be incomplete — treat the mismatch as a refresh trigger and tell the user.

## 3. Command Inventory

[ref: #rtk-command-inventory]

### Files & Reading

```bash
rtk ls <path>           # Directory listing, token-optimized (native ls proxy)
rtk tree <path>         # Directory tree, token-optimized (native tree proxy)
rtk read <file>         # File reading with intelligent filtering
rtk smart <file>        # 2-line technical summary (heuristic-based)
rtk find <pattern>      # File find, compact tree output (native find flags: -name, -type)
rtk wc <file>           # Word/line/byte count, compact (strips paths and padding)
```

### Search & Analysis

```bash
rtk grep <pattern>      # Compact grep — strips whitespace, truncates, groups by file
rtk rg <pattern>        # Compact ripgrep — runs rg NATIVELY, same output filter as grep
rtk err <cmd>           # Errors/warnings only from any command
rtk log <file>          # Filter and deduplicate log output
rtk json <file>         # JSON compact values by default, or keys-only (--keys-only)
rtk deps                # Project dependency summary
rtk env                 # Environment variables (filtered)
rtk diff                # Ultra-condensed diff (only changed lines)
rtk summary <cmd>       # Heuristic summary of command output
rtk test <cmd>          # Run tests, show only failures
```

### Git & Forges

```bash
rtk git <args>          # Compact git output (works with ALL subcommands and flags)
rtk gh <args>           # GitHub CLI, token-optimized
rtk glab <args>         # GitLab CLI, token-optimized
rtk gt <args>           # Graphite stacked-PR commands, compact
```

### Cloud & Databases

```bash
rtk aws <args>          # AWS CLI, compact (forced JSON, compressed)
rtk psql <args>         # PostgreSQL client, compact (borders stripped, tables compressed)
```

### Python

```bash
rtk ruff <args>         # Ruff linter/formatter, compact
rtk pytest <args>       # Pytest, failures only (90%)
rtk mypy <args>         # Mypy type checker, grouped errors
rtk pip <args>          # Pip, compact (auto-detects uv)
rtk uv run <cmd>        # uv run, compact (preserves uv-managed environment semantics)
```

### JavaScript / TypeScript

```bash
rtk pnpm <args>         # pnpm, ultra-compact
rtk npm run <script>    # npm run, filtered (strips boilerplate)
rtk npx <cmd>           # npx with intelligent routing (tsc, eslint, prisma → specialized filters)
rtk jest                # Jest, failures only (99.5%)
rtk vitest              # Vitest, failures only (99.5%)
rtk playwright test     # Playwright E2E, failures only (94%)
rtk prisma              # Prisma without ASCII art (88%)
rtk tsc                 # TypeScript errors grouped by file/code (83%)
rtk next build          # Next.js build with route metrics (87%)
rtk lint                # ESLint, grouped rule violations (84%)
rtk prettier --check    # Files needing format only (70%)
rtk format              # Universal format checker (prettier, black, ruff format)
```

### Rust / Go / JVM / .NET

```bash
rtk cargo <args>        # Cargo (build/check/clippy/test), compact — clippy grouped by file (80%), test failures only (90%)
rtk go <args>           # Go commands, compact (test failures only, 90%)
rtk golangci-lint       # golangci-lint, compact `run` support, passthrough otherwise
rtk dotnet <args>       # .NET (build/test/restore/format), compact
rtk sbt <args>          # SBT (Scala), compact
rtk gradlew <args>      # Android Gradle wrapper (build/test/lint), compact
rtk mvn <args>          # Maven (test/integration-test/compile/package/install/verify/deploy), compact
```

### PHP

```bash
rtk php <args>          # PHP runner, compact (artisan, syntax checks)
rtk phpunit             # PHPUnit, compact
rtk phpstan             # PHPStan analyzer, compact
rtk pest                # Pest test runner, compact
rtk paratest            # ParaTest parallel runner, compact
rtk ecs                 # EasyCodingStandard fixer, compact
rtk pint                # Laravel Pint (PHP-CS-Fixer), compact
```

### Ruby

```bash
rtk rake test           # Rake/Rails test, compact Minitest output (90%)
rtk rubocop             # RuboCop linter, compact
rtk rspec               # RSpec test runner, compact (60%)
```

### Infrastructure

```bash
rtk docker <args>       # Docker, compact (ps/images/logs deduplicated, 85%)
rtk kubectl <args>      # Kubectl, compact (get/logs deduplicated, 85%)
rtk oc <args>           # OpenShift CLI, compact
```

### Network (raw-fetch cases only, per `kagi-search` §1.1)

```bash
rtk curl <url>          # Curl with auto-JSON detection and schema output (70%)
rtk wget <url>          # Download, compact (strips progress bars, 65%)
```

### Meta & Operations

```bash
rtk gain [--history]    # Token savings summary and history
rtk cc-economics        # Claude Code economics: spending (ccusage) vs savings (rtk)
rtk config              # Show or create configuration file
rtk discover            # Discover missed RTK savings from session history
rtk session             # RTK adoption across sessions
rtk telemetry           # Manage telemetry consent and data (RGPD/GDPR)
rtk learn               # Learn CLI corrections from error history
rtk run <cmd>           # Execute via sh -c, raw (no filtering, no tracking)
rtk proxy <cmd>         # Execute without filtering, but track usage
rtk pipe                # Read stdin, apply filter, print (Unix pipe mode)
rtk trust / untrust     # Trust/revoke project-local TOML filters in current directory
rtk verify              # Verify hook integrity, run TOML filter inline tests
rtk hook-audit          # Hook rewrite audit metrics (requires RTK_HOOK_AUDIT=1)
rtk rewrite <cmd>       # Rewrite a raw command to its RTK equivalent (hook source of truth)
rtk hook                # Hook processors for LLM CLI tools
```

### Global Options

```bash
rtk -v|-vv|-vvv <cmd>   # Verbosity (only BEFORE the subcommand)
rtk --ultra-compact <cmd>  # Ultra-compact mode: ASCII icons, inline format (Level 2)
rtk --skip-env <cmd>    # SKIP_ENV_VALIDATION=1 for child processes (Next.js, tsc, lint, prisma)
```

## 4. Precedence Contract (HARD)

[ref: #rtk-precedence]

1. **mandatory-tools owns tool selection.** `fd`, `rg`, `lsd`, `ruplacer`, `uv`, `ruff` stay canonical for their domains; RTK's own `rtk ls` / `rtk read` / `rtk grep` / `rtk find` / `rtk tree` do NOT replace them. RTK MAY prefix any of them (passthrough is safe), but the modern-tool mandate of `mandatory-tools` is never weakened by this skill. Note: `rtk rg` runs ripgrep NATIVELY with a compact output filter — it is the preferred form of `rg` when large output is expected.
2. **The MCP tool layer is untouched.** Web search goes through `kagimcp`; memory and symbolic operations through `serena` MCP tools (bootstrap §8). RTK never substitutes for an MCP tool.
3. **Dedicated filters SHOULD be used.** For every command in the §3 inventory, run the `rtk`-prefixed form to harvest the token savings — this is the point of the skill.
4. **Passthrough guarantee:** `rtk git` passthrough works for ALL git subcommands, even unlisted ones.
5. **`rtk init` is FORBIDDEN for the agent** (it writes instructions into CLAUDE.md-style files; the instructions already live HERE). `rtk trust`/`untrust`/`hook`/`telemetry` change machine or project state — use only with the user's explicit request.

## 5. Token Savings Overview

[ref: #rtk-savings-overview]

| Category | Commands | Typical Savings |
|----------|----------|-----------------|
| Tests | vitest, playwright, cargo test, jest | 90–99% |
| Build | next, tsc, lint, prettier | 70–87% |
| Git | status, log, diff, add, commit | 59–80% |
| Forges | gh pr, gh run, glab | 26–87% |
| Package managers | pnpm, npm, npx, uv | 70–90% |
| Files | ls, read, grep, find | 60–75% |
| Infrastructure | docker, kubectl, oc | 85% |
| Network | curl, wget | 65–70% |

Overall average: **60–90% token reduction** on common development operations.

## 6. Violation Protocol

[ref: #rtk-violation-protocol]

If you run a §3-inventoried command WITHOUT the `rtk` prefix while this skill is active, disclose the miss in one line and prefix the next invocation. Never weaken §4: an `rtk`-prefixed call that replaces an MCP tool or a `mandatory-tools` tool choice is a violation — halt, discard, rerun through the correct layer. If the installed rtk is NEWER than the §2 pin and §3 was not refreshed, say so and propose the refresh.

# graphify-protocol

Agent skill that turns folders of code, documentation, images, video, and papers into a persistent, queryable knowledge graph.

## What this skill does

`graphify-protocol` defines a slash-command interface and a multi-stage pipeline for building knowledge graphs from arbitrary inputs. The skill itself is a documentation-only protocol; the actual work is performed by the `graphify` Python package (`graphifyy` on PyPI). The pipeline covers:

- File detection.
- AST and LLM-based semantic extraction.
- Graph construction.
- Community detection and labeling.
- Export and serving.

The skill exposes commands such as `/graphify`, `/graphify query`, `/graphify path`, and `/graphify explain`.

## When to use it

Use this skill when the request involves:

- Understanding a codebase, its architecture, or file relationships.
- Querying a project as a knowledge graph.
- Explaining connections between symbols, files, or concepts.
- Ingesting documentation, papers, images, or video into a graph.

The skill is especially relevant when a `graphify-out/` directory already exists in the workspace.

## Repository layout

```text
graphify-protocol/
├── references/           # Sub-command and pipeline reference docs
│   ├── add-watch.md
│   ├── exports.md
│   ├── extraction-spec.md
│   ├── github-and-merge.md
│   ├── hooks.md
│   ├── query.md
│   ├── transcribe.md
│   └── update.md
├── .graphify_version     # Declares the recommended graphify package version (0.8.39)
└ SKILL.md                # Skill entry point and /graphify command reference
```

## How to use this skill

1. Install the `graphify` package from PyPI:
   - `uv tool install graphifyy` or `pip install graphifyy`.
   - Optional extras: `graphifyy[gemini]` for Gemini backend, `graphifyy[video]` for video/audio transcription.
2. Open `SKILL.md` for the command reference and lazy-load routing index.
3. Build the graph with `/graphify` and the appropriate source path or URL.
4. Query the graph with `/graphify query`, `/graphify path`, or `/graphify explain`.
5. Export or serve the graph using the options documented in `references/exports.md`.

## Reference index

| File | Purpose |
|------|---------|
| `references/add-watch.md` | Ingestion and watch mode (`add`, `--watch`, URLs) |
| `references/exports.md` | Export formats: HTML, SVG, GraphML, Obsidian, wiki, Neo4j, FalkorDB, MCP stdio |
| `references/extraction-spec.md` | Semantic extraction JSON schema, node/edge/hyperedge rules |
| `references/github-and-merge.md` | GitHub clone and graph merge workflows |
| `references/hooks.md` | Git hooks and Claude Code integration |
| `references/query.md` | Query commands: `query`, `path`, `explain`, `--dfs`, `--budget` |
| `references/transcribe.md` | Video/audio transcription with `yt-dlp` and Whisper |
| `references/update.md` | Incremental update pipeline |

## Important environment variables

- `GEMINI_API_KEY` / `GOOGLE_API_KEY` — enables the Gemini semantic extraction backend.
- `GRAPHIFY_GEMINI_MODEL` — overrides the default Gemini model (`gemini-3-flash-preview`).
- `GRAPHIFY_WHISPER_MODEL` — selects the Whisper model for transcription (default `base`).
- `GRAPHIFY_WHISPER_PROMPT` — domain hint passed to Whisper.

## Conventions

- Slash commands (`/graphify ...`) are the primary user interface.
- Output artifacts are written to `graphify-out/`.
- Semantic extraction requires general-purpose subagents; read-only Explore subagents will silently drop chunks.
- Token spend is tracked in `graphify-out/cost.json` but is not hard-capped.
- The recommended package version is stored in `.graphify_version`.

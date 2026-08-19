# graphify-protocol
[ref: #gp-intro]

Turns code, docs, images, video, and papers into a queryable knowledge graph.

**DRAFT:** this skill is currently marked `draft: true` in `SKILL.md`, so it is invisible to automatic skill discovery. Use it only when explicitly loaded or referenced.

## What it does
[ref: #gp-what]

This skill defines the `/graphify` command interface for building knowledge graphs from arbitrary inputs. It runs a multi-stage pipeline that detects files, extracts structure from code ASTs, extracts semantics from documents and images, builds a graph, detects communities, labels them, and produces interactive HTML, a plain-language report, and raw graph data. You can then query the graph, trace paths between concepts, and export to formats such as Obsidian, Neo4j, FalkorDB, SVG, GraphML, or MCP.

## When it activates
[ref: #gp-when]

When explicitly loaded, activates when a `graphify-out/` directory exists in the workspace and you ask a question about the codebase, its architecture, or file relationships. Also activates when you use the `/graphify` slash command.

Examples:

- "How does authentication work in this project?"
- "What calls the payment service?"
- "/graphify ."
- "/graphify query trace data flow from API to database"

## How to run / use it
[ref: #gp-how]

Install the `graphify` package from PyPI, for example with `uv tool install graphifyy` or `pip install graphifyy`.
Run `/graphify <path>` to build a graph from a directory, or `/graphify https://github.com/<owner>/<repo>` to clone and graph a repository.
Once `graphify-out/graph.json` exists, ask natural-language questions and the agent will query the graph directly.
Set `GEMINI_API_KEY` or `GOOGLE_API_KEY` to enable the Gemini semantic extraction backend; otherwise the agent dispatches general-purpose subagents.
Use flags such as `--update`, `--directed`, `--no-viz`, `--svg`, `--graphml`, `--neo4j`, `--wiki`, or `--obsidian` to customize the pipeline.

## What it produces
[ref: #gp-produces]

- `graphify-out/graph.html` — interactive graph.
- `graphify-out/GRAPH_REPORT.md` — plain-language audit report.
- `graphify-out/graph.json` — raw graph data.
- Optional exports: Obsidian vault, Neo4j/FalkorDB cypher, SVG, GraphML, MCP server, or wiki.
- `graphify-out/cost.json` with cumulative token spend.

## Dependencies and why they matter
[ref: #gp-deps]

- `graphifyy` (PyPI package) — performs the actual extraction, graph building, clustering, and export. This skill only defines the command interface and workflow; the package does the heavy lifting.

## Strengths and trade-offs
[ref: #gp-tradeoffs]

### Strong sides
[ref: #gp-strong]

- Works on heterogeneous corpora: code, documentation, papers, images, and video.
- Persistent graph lets you ask follow-up questions without rebuilding.
- Community detection surfaces cross-document connections you would not think to ask about.
- Multiple export formats integrate with common tools.

### Weak sides / limits
[ref: #gp-weak]

- Semantic extraction costs tokens; large corpora can become expensive.
- The agent relies on the external `graphifyy` package, so behavior depends on the installed version.
- Large corpora trigger a warning and may require narrowing to a subfolder.
- Video and audio transcription adds dependencies and time.
- The skill is in draft; discovery and activation depend on explicit loading.

### Common pitfalls / gotchas
[ref: #gp-pitfalls]

- Semantic extraction must use writable agents (`coder` in this runtime; the upstream docs refer to them as "general-purpose"); read-only agents will drop chunks silently.
- If `graphify-out/graph.json` already exists, natural-language questions are answered by querying the graph, not by rebuilding.
- Set `GEMINI_API_KEY` or `GOOGLE_API_KEY` for Gemini backend; `GRAPHIFY_GEMINI_MODEL` overrides the default model.
- Token spend is tracked but not hard-capped.

## Repository layout
[ref: #gp-layout]

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
├── .graphify_version     # Recommended graphify package version
├── SKILL.md              # Agent entry point and `/graphify` command reference
└── README.md
```

## Reference overview
[ref: #gp-refs]

| File | What it covers |
|------|----------------|
| `references/add-watch.md` | Ingestion and watch mode (`add`, `--watch`, URLs) |
| `references/exports.md` | Export formats: HTML, SVG, GraphML, Obsidian, wiki, Neo4j, FalkorDB, MCP stdio |
| `references/extraction-spec.md` | Semantic extraction JSON schema, node/edge/hyperedge rules |
| `references/github-and-merge.md` | GitHub clone and cross-repo graph merge workflows |
| `references/hooks.md` | Git commit hook and Claude Code integration |
| `references/query.md` | Query commands: `query`, `path`, `explain`, `--dfs`, `--budget` |
| `references/transcribe.md` | Video and audio transcription with `yt-dlp` and Whisper |
| `references/update.md` | Incremental update and cluster-only pipelines |

## Important conventions / gotchas
[ref: #gp-conventions]

- The actual work is performed by the PyPI package `graphifyy`, not by this skill directly.
- Semantic extraction requires writable agents (`coder` in this runtime; upstream docs call them "general-purpose"); read-only subagents will drop chunks silently.
- Large corpora trigger a warning and may ask you to narrow to a subfolder.
- Token spend is tracked but not hard-capped.
- `GEMINI_API_KEY` or `GOOGLE_API_KEY` enables Gemini backend; `GRAPHIFY_GEMINI_MODEL` overrides the default model.
- `GRAPHIFY_WHISPER_MODEL` and `GRAPHIFY_WHISPER_PROMPT` configure video/audio transcription.

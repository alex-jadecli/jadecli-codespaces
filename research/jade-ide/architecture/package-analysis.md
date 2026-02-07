# ---
# entity_id: document-package-analysis
# entity_name: Jade IDE Package Fork vs Build Analysis
# entity_type_id: document
# entity_path: research/jade-ide/architecture/package-analysis.md
# entity_language: markdown
# entity_state: active
# entity_created: 2026-01-23T00:00:00Z
# entity_actors: [dev, claude]
# ---

# Package Analysis: Fork vs Build Decisions

## Executive Summary

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    JADE IDE PACKAGE STRATEGY                                 │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│   FORK (1)        PRIVATE FORK (1)      BUILD (7)         USE AS DEP (5)   │
│   ┌────────┐      ┌────────────────┐    ┌──────────────┐  ┌────────────┐   │
│   │ VS Code│      │ Claude Code    │    │ jade-core    │  │ Claude SDK │   │
│   │        │      │ (reference)    │    │ jade-cli     │  │ MCP SDK    │   │
│   └────────┘      └────────────────┘    │ jade-ai      │  │ ACP SDK    │   │
│                                         │ jade-proto   │  │ Tree-sitter│   │
│                                         │ jade-server  │  │ Electron   │   │
│                                         │ dotfiles-    │  └────────────┘   │
│                                         │   claude     │                   │
│                                         │ .github      │                   │
│                                         └──────────────┘                   │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Detailed Package Breakdown

### CATEGORY 1: MUST FORK

#### 1.1 VS Code (microsoft/vscode)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         VS CODE FORK ANALYSIS                                │
├──────────────────┬──────────────────────────────────────────────────────────┤
│ Repository       │ microsoft/vscode                                         │
│ License          │ MIT                                                       │
│ Stars            │ 165k+                                                     │
│ Size             │ ~15M LOC                                                  │
│ Languages        │ TypeScript (95%), JavaScript, CSS                        │
├──────────────────┼──────────────────────────────────────────────────────────┤
│ WHY FORK?        │                                                          │
│                  │ • Cannot build equivalent from scratch                   │
│                  │ • 10+ years of development                               │
│                  │ • Cursor, Kiro, Windsurf all fork this                   │
│                  │ • MIT license allows commercial use                       │
├──────────────────┼──────────────────────────────────────────────────────────┤
│ FORK STRATEGY    │                                                          │
│                  │ ┌────────────────────────────────────────────────┐       │
│                  │ │ 1. Initial Fork                                │       │
│                  │ │    git clone --depth 1 microsoft/vscode        │       │
│                  │ │    git remote add upstream microsoft/vscode    │       │
│                  │ ├────────────────────────────────────────────────┤       │
│                  │ │ 2. Rebrand (product.json, assets/)             │       │
│                  │ │    - applicationName: "jade-ide"               │       │
│                  │ │    - nameLong: "Jade IDE"                      │       │
│                  │ │    - icons, splash, about dialog               │       │
│                  │ ├────────────────────────────────────────────────┤       │
│                  │ │ 3. Modify Extension Host                       │       │
│                  │ │    - Inject jade-ai as bundled extension       │       │
│                  │ │    - Custom completion provider                │       │
│                  │ │    - AI context sidebar                        │       │
│                  │ ├────────────────────────────────────────────────┤       │
│                  │ │ 4. Build Infrastructure                        │       │
│                  │ │    - GitHub Actions for CI/CD                  │       │
│                  │ │    - Code signing (Apple, Microsoft, Linux)    │       │
│                  │ │    - Auto-update server                        │       │
│                  │ ├────────────────────────────────────────────────┤       │
│                  │ │ 5. Sync Schedule                               │       │
│                  │ │    - Monthly: git fetch upstream               │       │
│                  │ │    - git merge upstream/main (resolve conflicts)│      │
│                  │ │    - Tag: jade-v{VS_CODE_VERSION}-{JADE_BUILD}  │       │
│                  │ └────────────────────────────────────────────────┘       │
├──────────────────┼──────────────────────────────────────────────────────────┤
│ ESTIMATED EFFORT │ 2-3 months for initial fork + branding                   │
│                  │ Ongoing: 1-2 weeks/month for upstream sync               │
├──────────────────┼──────────────────────────────────────────────────────────┤
│ RISKS            │ • Merge conflicts with upstream changes                  │
│                  │ • Breaking changes in VS Code API                        │
│                  │ • Build system complexity                                │
└──────────────────┴──────────────────────────────────────────────────────────┘
```

---

### CATEGORY 2: PRIVATE FORK (Reference Only)

#### 2.1 Claude Code (@anthropic-ai/claude-code)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                      CLAUDE CODE REFERENCE ANALYSIS                          │
├──────────────────┬──────────────────────────────────────────────────────────┤
│ Package          │ @anthropic-ai/claude-code                                │
│ License          │ Check Anthropic TOS (not open source)                    │
│ Type             │ npm CLI package                                          │
├──────────────────┼──────────────────────────────────────────────────────────┤
│ WHY STUDY?       │                                                          │
│                  │ • Best-in-class agentic CLI                              │
│                  │ • MCP integration patterns                               │
│                  │ • Tool use architecture                                  │
│                  │ • Permission system design                               │
├──────────────────┼──────────────────────────────────────────────────────────┤
│ APPROACH         │                                                          │
│                  │ ┌────────────────────────────────────────────────┐       │
│                  │ │ DO:                                            │       │
│                  │ │ • Study public documentation                   │       │
│                  │ │ • Learn from usage patterns                    │       │
│                  │ │ • Reference MCP integration approach           │       │
│                  │ │ • Analyze CLAUDE.md conventions                │       │
│                  │ ├────────────────────────────────────────────────┤       │
│                  │ │ DON'T:                                         │       │
│                  │ │ • Copy source code directly                    │       │
│                  │ │ • Reverse engineer proprietary features        │       │
│                  │ │ • Violate Anthropic TOS                        │       │
│                  │ └────────────────────────────────────────────────┘       │
├──────────────────┼──────────────────────────────────────────────────────────┤
│ LEGAL NOTE       │ Consult IP lawyer before any code reference             │
└──────────────────┴──────────────────────────────────────────────────────────┘
```

---

### CATEGORY 3: BUILD FROM SCRATCH

#### 3.1 jade-core

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           jade-core                                          │
│                     Shared Library Specification                             │
├──────────────────┬──────────────────────────────────────────────────────────┤
│ Language         │ TypeScript + Rust (WASM)                                 │
│ Package Manager  │ pnpm (monorepo)                                          │
│ Distribution     │ npm: @jade-ide/core                                      │
├──────────────────┼──────────────────────────────────────────────────────────┤
│ MODULES          │                                                          │
│                  │ @jade-ide/core                                           │
│                  │ ├── /config          4-tier config resolution            │
│                  │ ├── /entity          Frontmatter + AST indexing          │
│                  │ ├── /team            File locking, presence              │
│                  │ ├── /telemetry       Privacy-first analytics             │
│                  │ └── /utils           Shared utilities                    │
├──────────────────┼──────────────────────────────────────────────────────────┤
│ DEPENDENCIES     │                                                          │
│                  │ ┌────────────────────────────────────────────────┐       │
│                  │ │ Production:                                    │       │
│                  │ │ • yaml (frontmatter parsing)                   │       │
│                  │ │ • zod (schema validation)                      │       │
│                  │ │ • tree-sitter (AST parsing)                    │       │
│                  │ │ • pino (logging)                               │       │
│                  │ │ • opentelemetry (observability)                │       │
│                  │ ├────────────────────────────────────────────────┤       │
│                  │ │ Development:                                   │       │
│                  │ │ • vitest (testing)                             │       │
│                  │ │ • tsup (bundling)                              │       │
│                  │ │ • typescript                                   │       │
│                  │ └────────────────────────────────────────────────┘       │
├──────────────────┼──────────────────────────────────────────────────────────┤
│ ESTIMATED EFFORT │ 3-4 weeks for initial implementation                     │
└──────────────────┴──────────────────────────────────────────────────────────┘
```

#### 3.2 jade-ai

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           jade-ai                                            │
│                    Multi-Model AI Orchestration                              │
├──────────────────┬──────────────────────────────────────────────────────────┤
│ Language         │ TypeScript                                               │
│ Distribution     │ npm: @jade-ide/ai                                        │
├──────────────────┼──────────────────────────────────────────────────────────┤
│ ADAPTERS         │                                                          │
│                  │ ┌────────────────────────────────────────────────┐       │
│                  │ │                                                │       │
│                  │ │   ┌─────────┐   ┌─────────┐   ┌─────────┐     │       │
│                  │ │   │ Claude  │   │ Ollama  │   │ OpenAI  │     │       │
│                  │ │   │ Adapter │   │ Adapter │   │ Adapter │     │       │
│                  │ │   └────┬────┘   └────┬────┘   └────┬────┘     │       │
│                  │ │        │             │             │          │       │
│                  │ │        └─────────────┼─────────────┘          │       │
│                  │ │                      │                        │       │
│                  │ │                      ▼                        │       │
│                  │ │              ┌─────────────┐                  │       │
│                  │ │              │   Model     │                  │       │
│                  │ │              │   Router    │                  │       │
│                  │ │              └─────────────┘                  │       │
│                  │ │                                                │       │
│                  │ └────────────────────────────────────────────────┘       │
├──────────────────┼──────────────────────────────────────────────────────────┤
│ FEATURES         │ • Model routing (cost, speed, capability)                │
│                  │ • Fallback chains                                        │
│                  │ • Context window management                              │
│                  │ • Streaming support                                      │
│                  │ • Token counting                                         │
├──────────────────┼──────────────────────────────────────────────────────────┤
│ DEPENDENCIES     │ • @anthropic-ai/sdk                                      │
│                  │ • ollama-js                                              │
│                  │ • openai                                                 │
│                  │ • @google/generative-ai                                  │
├──────────────────┼──────────────────────────────────────────────────────────┤
│ ESTIMATED EFFORT │ 2-3 weeks                                                │
└──────────────────┴──────────────────────────────────────────────────────────┘
```

#### 3.3 jade-proto

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                          jade-proto                                          │
│                    Protocol Implementation Layer                             │
├──────────────────┬──────────────────────────────────────────────────────────┤
│ Language         │ TypeScript                                               │
│ Distribution     │ npm: @jade-ide/proto                                     │
├──────────────────┼──────────────────────────────────────────────────────────┤
│ PROTOCOLS        │                                                          │
│                  │ ┌────────────────────────────────────────────────┐       │
│                  │ │                                                │       │
│                  │ │  ┌─────────────────────────────────────────┐   │       │
│                  │ │  │            PROTOCOL BRIDGE               │   │       │
│                  │ │  └─────────────────────────────────────────┘   │       │
│                  │ │         │            │            │           │       │
│                  │ │         ▼            ▼            ▼           │       │
│                  │ │  ┌──────────┐ ┌──────────┐ ┌──────────┐       │       │
│                  │ │  │   MCP    │ │   ACP    │ │   A2A    │       │       │
│                  │ │  │  Client  │ │  Client  │ │  Client  │       │       │
│                  │ │  │  Server  │ │          │ │          │       │       │
│                  │ │  └──────────┘ └──────────┘ └──────────┘       │       │
│                  │ │                                                │       │
│                  │ └────────────────────────────────────────────────┘       │
├──────────────────┼──────────────────────────────────────────────────────────┤
│ MCP FEATURES     │ • Tool registration and discovery                        │
│                  │ • Resource providers                                     │
│                  │ • Prompt templates                                       │
│                  │ • stdio and HTTP transports                              │
├──────────────────┼──────────────────────────────────────────────────────────┤
│ ACP FEATURES     │ • IDE-agent communication                                │
│                  │ • Context sharing                                        │
│                  │ • Action execution                                       │
├──────────────────┼──────────────────────────────────────────────────────────┤
│ DEPENDENCIES     │ • @anthropic-ai/mcp-sdk                                  │
│                  │ • @zed-industries/acp-sdk (when available)               │
│                  │ • ws (WebSocket)                                         │
├──────────────────┼──────────────────────────────────────────────────────────┤
│ ESTIMATED EFFORT │ 4-5 weeks                                                │
└──────────────────┴──────────────────────────────────────────────────────────┘
```

#### 3.4 jade-cli

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           jade-cli                                           │
│                    Standalone Terminal Agent                                 │
├──────────────────┬──────────────────────────────────────────────────────────┤
│ Language         │ TypeScript (with Ink for TUI)                            │
│ Distribution     │ npm: jade-cli (global install)                           │
├──────────────────┼──────────────────────────────────────────────────────────┤
│ COMMANDS         │                                                          │
│                  │ jade                                                     │
│                  │ ├── chat [--model <m>]    Interactive chat              │
│                  │ ├── agent <task>          Agentic task execution        │
│                  │ ├── edit <file>           AI-assisted editing           │
│                  │ ├── commit                Smart commit messages         │
│                  │ ├── review [pr]           PR review assistance          │
│                  │ ├── config                                              │
│                  │ │   ├── show              Show resolved config          │
│                  │ │   ├── set <k> <v>       Set config value              │
│                  │ │   └── tier              Show config tiers             │
│                  │ ├── mcp                                                 │
│                  │ │   ├── list              List MCP servers              │
│                  │ │   ├── add <name>        Add MCP server                │
│                  │ │   └── remove <name>     Remove MCP server             │
│                  │ ├── auth                                                │
│                  │ │   ├── login             Authenticate                  │
│                  │ │   ├── logout            Sign out                      │
│                  │ │   └── status            Show auth status              │
│                  │ └── version               Show version                  │
├──────────────────┼──────────────────────────────────────────────────────────┤
│ DEPENDENCIES     │ • @jade-ide/core                                        │
│                  │ • @jade-ide/ai                                          │
│                  │ • @jade-ide/proto                                       │
│                  │ • ink (React TUI)                                       │
│                  │ • yargs or commander                                    │
├──────────────────┼──────────────────────────────────────────────────────────┤
│ ESTIMATED EFFORT │ 4-6 weeks                                                │
└──────────────────┴──────────────────────────────────────────────────────────┘
```

#### 3.5 jade-server

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                          jade-server                                         │
│                      Backend Platform Services                               │
├──────────────────┬──────────────────────────────────────────────────────────┤
│ Language         │ Python (FastAPI) + TypeScript (tRPC)                     │
│ Distribution     │ Docker container / Cloudflare Workers                    │
├──────────────────┼──────────────────────────────────────────────────────────┤
│ SERVICES         │                                                          │
│                  │ ┌────────────────────────────────────────────────┐       │
│                  │ │                                                │       │
│                  │ │  ┌──────────┐  ┌──────────┐  ┌──────────┐     │       │
│                  │ │  │   Auth   │  │ Billing  │  │   Sync   │     │       │
│                  │ │  │ Service  │  │ Service  │  │ Service  │     │       │
│                  │ │  └──────────┘  └──────────┘  └──────────┘     │       │
│                  │ │                                                │       │
│                  │ │  ┌──────────┐  ┌──────────┐  ┌──────────┐     │       │
│                  │ │  │   MCP    │  │ Telemetry│  │  Teams   │     │       │
│                  │ │  │  Server  │  │ Ingester │  │ Service  │     │       │
│                  │ │  └──────────┘  └──────────┘  └──────────┘     │       │
│                  │ │                                                │       │
│                  │ └────────────────────────────────────────────────┘       │
├──────────────────┼──────────────────────────────────────────────────────────┤
│ INFRASTRUCTURE   │ • PostgreSQL (Neon)                                      │
│                  │ • Redis (Upstash)                                        │
│                  │ • R2/S3 (Cloudflare)                                     │
│                  │ • Stripe (billing)                                       │
├──────────────────┼──────────────────────────────────────────────────────────┤
│ ESTIMATED EFFORT │ 6-8 weeks                                                │
└──────────────────┴──────────────────────────────────────────────────────────┘
```

---

### CATEGORY 4: USE AS DEPENDENCY

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    THIRD-PARTY DEPENDENCIES                                  │
├──────────────────┬──────────────────────────────────────────────────────────┤
│ Package          │ Usage                                    │ License      │
├──────────────────┼──────────────────────────────────────────┼──────────────┤
│ @anthropic-ai/   │ Claude API client                        │ Apache 2.0   │
│   sdk            │                                          │              │
├──────────────────┼──────────────────────────────────────────┼──────────────┤
│ @anthropic-ai/   │ Model Context Protocol                   │ Apache 2.0   │
│   mcp-sdk        │                                          │              │
├──────────────────┼──────────────────────────────────────────┼──────────────┤
│ tree-sitter      │ AST parsing for entity extraction        │ MIT          │
├──────────────────┼──────────────────────────────────────────┼──────────────┤
│ ollama-js        │ Local LLM integration                    │ MIT          │
├──────────────────┼──────────────────────────────────────────┼──────────────┤
│ electron         │ Desktop app framework (via VS Code)      │ MIT          │
├──────────────────┼──────────────────────────────────────────┼──────────────┤
│ ink              │ React-based TUI for CLI                  │ MIT          │
├──────────────────┼──────────────────────────────────────────┼──────────────┤
│ fastapi          │ Python API framework                     │ MIT          │
├──────────────────┼──────────────────────────────────────────┼──────────────┤
│ trpc             │ TypeScript RPC framework                 │ MIT          │
├──────────────────┼──────────────────────────────────────────┼──────────────┤
│ zod              │ Schema validation                        │ MIT          │
└──────────────────┴──────────────────────────────────────────┴──────────────┘
```

---

## Total Effort Estimate

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         DEVELOPMENT TIMELINE                                 │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  Month 1    Month 2    Month 3    Month 4    Month 5    Month 6    Month 7 │
│    │          │          │          │          │          │          │      │
│    ▼          ▼          ▼          ▼          ▼          ▼          ▼      │
│    ┌──────────────────┐                                                      │
│    │   jade-core      │ (3-4 weeks)                                         │
│    └──────────────────┘                                                      │
│         ┌────────────────┐                                                   │
│         │   jade-ai      │ (2-3 weeks)                                      │
│         └────────────────┘                                                   │
│              ┌──────────────────────┐                                        │
│              │   jade-proto         │ (4-5 weeks)                           │
│              └──────────────────────┘                                        │
│                   ┌────────────────────────┐                                 │
│                   │   jade-cli             │ (4-6 weeks)                    │
│                   └────────────────────────┘                                 │
│                             ┌──────────────────────────────────┐             │
│                             │   jade-ide (VS Code fork)        │ (8-12 wks) │
│                             └──────────────────────────────────┘             │
│                                                  ┌────────────────────────┐  │
│                                                  │   jade-server         │  │
│                                                  │   (6-8 weeks)         │  │
│                                                  └────────────────────────┘  │
│                                                                              │
│  ════════════════════════════════════════════════════════════════════════   │
│  MVP Timeline: ~4-5 months (with focused team)                              │
│  Full Product: ~7-9 months                                                   │
│  ════════════════════════════════════════════════════════════════════════   │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

*Generated: 2026-01-23 | Entity: document-package-analysis*

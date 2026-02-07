# ---
# entity_id: document-jade-architecture
# entity_name: Jade IDE GitHub Organization Architecture
# entity_type_id: document
# entity_path: research/jade-ide/architecture/github-org-structure.md
# entity_language: markdown
# entity_state: active
# entity_created: 2026-01-23T00:00:00Z
# entity_actors: [dev, claude]
# entity_dependencies: [vscode, electron, claude-code]
# ---

# Jade IDE - GitHub Organization Architecture

## Organization Overview

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                          github.com/jade-ide                                 │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │                        CORE PRODUCTS                                 │    │
│  ├─────────────────────────────────────────────────────────────────────┤    │
│  │                                                                      │    │
│  │   ┌──────────────┐    ┌──────────────┐    ┌──────────────┐          │    │
│  │   │   jade-ide   │    │   jade-cli   │    │  jade-server │          │    │
│  │   │   (FORK)     │    │   (BUILD)    │    │   (BUILD)    │          │    │
│  │   │             │    │              │    │              │          │    │
│  │   │  VS Code    │◄───│  Standalone  │    │  MCP/ACP     │          │    │
│  │   │  Fork       │    │  CLI Agent   │    │  Backend     │          │    │
│  │   └──────────────┘    └──────────────┘    └──────────────┘          │    │
│  │          │                   │                   │                  │    │
│  └──────────┼───────────────────┼───────────────────┼──────────────────┘    │
│             │                   │                   │                       │
│  ┌──────────┼───────────────────┼───────────────────┼──────────────────┐    │
│  │          ▼                   ▼                   ▼                  │    │
│  │                     SHARED LIBRARIES                                │    │
│  ├─────────────────────────────────────────────────────────────────────┤    │
│  │                                                                      │    │
│  │   ┌──────────────┐    ┌──────────────┐    ┌──────────────┐          │    │
│  │   │ jade-core    │    │ jade-ai      │    │ jade-proto   │          │    │
│  │   │   (BUILD)    │    │   (BUILD)    │    │   (BUILD)    │          │    │
│  │   │             │    │              │    │              │          │    │
│  │   │  Shared     │    │  AI/LLM      │    │  MCP/ACP     │          │    │
│  │   │  Utilities  │    │  Adapters    │    │  Protocol    │          │    │
│  │   └──────────────┘    └──────────────┘    └──────────────┘          │    │
│  │                                                                      │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
│                                                                              │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │                      INFRASTRUCTURE                                  │    │
│  ├─────────────────────────────────────────────────────────────────────┤    │
│  │                                                                      │    │
│  │   ┌──────────────┐    ┌──────────────┐    ┌──────────────┐          │    │
│  │   │  .github     │    │ dotfiles-    │    │  terraform-  │          │    │
│  │   │   (BUILD)    │    │   claude     │    │    infra     │          │    │
│  │   │             │    │   (BUILD)    │    │   (BUILD)    │          │    │
│  │   │  Org-wide   │    │              │    │              │          │    │
│  │   │  Workflows  │    │  Shared      │    │  Cloud IaC   │          │    │
│  │   └──────────────┘    │  Configs    │    └──────────────┘          │    │
│  │                       └──────────────┘                              │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
│                                                                              │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │                      DOCUMENTATION                                   │    │
│  ├─────────────────────────────────────────────────────────────────────┤    │
│  │   ┌──────────────┐    ┌──────────────┐    ┌──────────────┐          │    │
│  │   │    docs      │    │  examples    │    │  tutorials   │          │    │
│  │   │   (BUILD)    │    │   (BUILD)    │    │   (BUILD)    │          │    │
│  │   └──────────────┘    └──────────────┘    └──────────────┘          │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘

Legend: (FORK) = Fork from upstream  |  (BUILD) = Build from scratch
```

---

## Repository Dependency Graph

```
                              ┌─────────────────┐
                              │   UPSTREAM      │
                              │   DEPENDENCIES  │
                              └────────┬────────┘
                                       │
        ┌──────────────────────────────┼──────────────────────────────┐
        │                              │                              │
        ▼                              ▼                              ▼
┌───────────────┐            ┌───────────────┐            ┌───────────────┐
│   vscode      │            │  @anthropic/  │            │    zed/       │
│  (microsoft)  │            │    sdk        │            │   acp-sdk     │
│               │            │               │            │               │
│  MIT License  │            │  Apache 2.0   │            │  Apache 2.0   │
└───────┬───────┘            └───────┬───────┘            └───────┬───────┘
        │                            │                            │
        │ FORK                       │ DEPEND                     │ DEPEND
        │                            │                            │
        ▼                            ▼                            ▼
┌───────────────┐            ┌───────────────┐            ┌───────────────┐
│               │            │               │            │               │
│   jade-ide    │◄───────────│   jade-ai     │◄───────────│  jade-proto   │
│               │            │               │            │               │
│  Private Fork │            │  AI Adapters  │            │  Protocol     │
│  + Extensions │            │  Claude/Ollama│            │  Impl (MCP/   │
│               │            │               │            │   ACP/A2A)    │
└───────┬───────┘            └───────┬───────┘            └───────┬───────┘
        │                            │                            │
        │                            │                            │
        └────────────────────────────┼────────────────────────────┘
                                     │
                                     ▼
                            ┌───────────────┐
                            │               │
                            │   jade-core   │
                            │               │
                            │  Shared Utils │
                            │  Config Mgmt  │
                            │  Telemetry    │
                            └───────┬───────┘
                                    │
                    ┌───────────────┴───────────────┐
                    │                               │
                    ▼                               ▼
           ┌───────────────┐               ┌───────────────┐
           │               │               │               │
           │   jade-cli    │               │  jade-server  │
           │               │               │               │
           │  Standalone   │               │  Backend API  │
           │  Terminal     │               │  MCP Server   │
           │  Agent        │               │  Auth/Billing │
           └───────────────┘               └───────────────┘
```

---

## Fork vs Build Decision Matrix

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    FORK vs BUILD DECISION MATRIX                            │
├──────────────────┬──────────┬───────────────────────────────────────────────┤
│     Package      │ Decision │                  Rationale                    │
├──────────────────┼──────────┼───────────────────────────────────────────────┤
│                  │          │                                               │
│  VS Code         │  FORK    │  Core IDE, 15M+ LOC, impossible to rebuild   │
│  (microsoft/     │  ██████  │  Cursor, Kiro, Windsurf all fork this        │
│   vscode)        │          │  License: MIT (commercial OK)                 │
│                  │          │                                               │
├──────────────────┼──────────┼───────────────────────────────────────────────┤
│                  │          │                                               │
│  Electron        │  USE AS  │  No need to fork, use as dependency          │
│  (electron/      │   DEP    │  VS Code fork includes Electron               │
│   electron)      │  ░░░░░░  │  License: MIT                                 │
│                  │          │                                               │
├──────────────────┼──────────┼───────────────────────────────────────────────┤
│                  │          │                                               │
│  Claude Code     │  PRIVATE │  Reference impl, learn patterns              │
│  (@anthropic/    │   FORK   │  Modify for Jade integration                  │
│   claude-code)   │  ▓▓▓▓▓▓  │  License: Check terms                         │
│                  │          │                                               │
├──────────────────┼──────────┼───────────────────────────────────────────────┤
│                  │          │                                               │
│  MCP SDK         │  USE AS  │  Standard protocol implementation             │
│  (@anthropic/    │   DEP    │  Build adapters on top                        │
│   mcp-sdk)       │  ░░░░░░  │  License: Apache 2.0                          │
│                  │          │                                               │
├──────────────────┼──────────┼───────────────────────────────────────────────┤
│                  │          │                                               │
│  ACP SDK         │  USE AS  │  Emerging standard, contribute upstream       │
│  (zed-         │   DEP    │  Build protocol bridge                         │
│   industries)    │  ░░░░░░  │  License: Apache 2.0                          │
│                  │          │                                               │
├──────────────────┼──────────┼───────────────────────────────────────────────┤
│                  │          │                                               │
│  Tree-sitter     │  USE AS  │  AST parsing, no modifications needed         │
│  (tree-sitter/   │   DEP    │  Build grammars as needed                     │
│   tree-sitter)   │  ░░░░░░  │  License: MIT                                 │
│                  │          │                                               │
├──────────────────┼──────────┼───────────────────────────────────────────────┤
│                  │          │                                               │
│  jade-core       │  BUILD   │  Your unique value proposition                │
│                  │  ██████  │  Config management, multi-tier .claude        │
│                  │          │  Team collaboration features                  │
│                  │          │                                               │
├──────────────────┼──────────┼───────────────────────────────────────────────┤
│                  │          │                                               │
│  jade-ai         │  BUILD   │  AI orchestration layer                       │
│                  │  ██████  │  Multi-model support (Claude, Ollama, etc)    │
│                  │          │  Context management, RAG                      │
│                  │          │                                               │
├──────────────────┼──────────┼───────────────────────────────────────────────┤
│                  │          │                                               │
│  jade-cli        │  BUILD   │  Standalone CLI product                       │
│                  │  ██████  │  Works with/without jade-ide                  │
│                  │          │  Claude Code alternative/complement           │
│                  │          │                                               │
├──────────────────┼──────────┼───────────────────────────────────────────────┤
│                  │          │                                               │
│  jade-proto      │  BUILD   │  Protocol bridge layer                        │
│                  │  ██████  │  MCP + ACP + A2A unified interface            │
│                  │          │  Enables multi-agent orchestration            │
│                  │          │                                               │
├──────────────────┼──────────┼───────────────────────────────────────────────┤
│                  │          │                                               │
│  jade-server     │  BUILD   │  Backend services                             │
│                  │  ██████  │  Auth, billing, telemetry, sync               │
│                  │          │  MCP server for tools                         │
│                  │          │                                               │
└──────────────────┴──────────┴───────────────────────────────────────────────┘

Legend:  ██████ = Build from scratch    ▓▓▓▓▓▓ = Private fork    ░░░░░░ = Use as dep
```

---

## Technology Stack

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           JADE IDE TECH STACK                               │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  LAYER 4: PRODUCTS                                                          │
│  ┌──────────────────────────────────────────────────────────────────────┐   │
│  │  jade-ide (Desktop)  │  jade-cli (Terminal)  │  jade-web (Browser)   │   │
│  └──────────────────────────────────────────────────────────────────────┘   │
│                                     │                                        │
│  ─────────────────────────────────────────────────────────────────────────  │
│                                                                              │
│  LAYER 3: APPLICATION                                                        │
│  ┌────────────────┐  ┌────────────────┐  ┌────────────────┐                 │
│  │ Extension Host │  │ AI Context     │  │ Team Features  │                 │
│  │ (TypeScript)   │  │ (TypeScript)   │  │ (TypeScript)   │                 │
│  ├────────────────┤  ├────────────────┤  ├────────────────┤                 │
│  │ • Custom LSP   │  │ • RAG Pipeline │  │ • File Locking │                 │
│  │ • Completion   │  │ • Embeddings   │  │ • Presence     │                 │
│  │ • Diagnostics  │  │ • Context Mgmt │  │ • Sync         │                 │
│  └────────────────┘  └────────────────┘  └────────────────┘                 │
│                                                                              │
│  ─────────────────────────────────────────────────────────────────────────  │
│                                                                              │
│  LAYER 2: CORE LIBRARIES                                                     │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │                          jade-core                                   │    │
│  │  TypeScript + Rust (via wasm-bindgen for performance-critical)       │    │
│  ├─────────────────────────────────────────────────────────────────────┤    │
│  │  • Config resolution (4-tier .claude)                                │    │
│  │  • Frontmatter parsing                                               │    │
│  │  • Entity indexing (AST via tree-sitter)                             │    │
│  │  • Telemetry & logging                                               │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
│                                                                              │
│  ┌────────────────────────────┐  ┌────────────────────────────────────┐     │
│  │        jade-ai             │  │          jade-proto                │     │
│  │  TypeScript + Python       │  │  TypeScript                        │     │
│  ├────────────────────────────┤  ├────────────────────────────────────┤     │
│  │  • Claude SDK adapter      │  │  • MCP client/server               │     │
│  │  • Ollama adapter          │  │  • ACP client                      │     │
│  │  • OpenAI adapter          │  │  • A2A orchestration               │     │
│  │  • Gemini adapter          │  │  • Protocol bridge                 │     │
│  │  • Model router            │  │  • Tool registry                   │     │
│  └────────────────────────────┘  └────────────────────────────────────┘     │
│                                                                              │
│  ─────────────────────────────────────────────────────────────────────────  │
│                                                                              │
│  LAYER 1: PLATFORM                                                           │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │                          jade-server                                 │    │
│  │  Python (FastAPI) + TypeScript (tRPC)                                │    │
│  ├─────────────────────────────────────────────────────────────────────┤    │
│  │  • Authentication (OAuth, API keys)                                  │    │
│  │  • Billing (Stripe integration)                                      │    │
│  │  • Usage metering                                                    │    │
│  │  • Settings sync                                                     │    │
│  │  • MCP tool server                                                   │    │
│  │  • WebSocket for real-time                                           │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
│                                                                              │
│  ─────────────────────────────────────────────────────────────────────────  │
│                                                                              │
│  LAYER 0: INFRASTRUCTURE                                                     │
│  ┌────────────────┐  ┌────────────────┐  ┌────────────────┐                 │
│  │ PostgreSQL     │  │ Redis          │  │ S3/R2          │                 │
│  │ (Neon)         │  │ (Upstash)      │  │ (Cloudflare)   │                 │
│  ├────────────────┤  ├────────────────┤  ├────────────────┤                 │
│  │ • User data    │  │ • Sessions     │  │ • Artifacts    │                 │
│  │ • Entities     │  │ • Rate limits  │  │ • Backups      │                 │
│  │ • Audit logs   │  │ • Pub/sub      │  │ • Assets       │                 │
│  └────────────────┘  └────────────────┘  └────────────────┘                 │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Package Details: What to Build

### 1. jade-ide (FORK from VS Code)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              jade-ide                                        │
│                    Private Fork of microsoft/vscode                          │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  MODIFICATIONS REQUIRED:                                                     │
│                                                                              │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │ 1. BRANDING                                                          │    │
│  │    ├── Replace VS Code → Jade IDE                                   │    │
│  │    ├── Update icons, splash screens, about dialogs                  │    │
│  │    ├── Custom themes (jade-dark, jade-light)                        │    │
│  │    └── Update package.json, product.json                            │    │
│  ├─────────────────────────────────────────────────────────────────────┤    │
│  │ 2. EXTENSION HOST                                                    │    │
│  │    ├── Add jade-ai extension (bundled, not marketplace)             │    │
│  │    ├── Modify completion provider for AI suggestions                │    │
│  │    ├── Add context window management                                │    │
│  │    └── Inject jade-core services                                    │    │
│  ├─────────────────────────────────────────────────────────────────────┤    │
│  │ 3. SETTINGS                                                          │    │
│  │    ├── Add jade.* namespace settings                                │    │
│  │    ├── 4-tier config resolution                                     │    │
│  │    ├── Team settings sync                                           │    │
│  │    └── Enterprise policy support                                    │    │
│  ├─────────────────────────────────────────────────────────────────────┤    │
│  │ 4. TELEMETRY                                                         │    │
│  │    ├── Replace MS telemetry with jade-server                        │    │
│  │    ├── Privacy-first (opt-in, anonymized)                           │    │
│  │    └── Usage analytics for billing                                  │    │
│  ├─────────────────────────────────────────────────────────────────────┤    │
│  │ 5. BUILD SYSTEM                                                      │    │
│  │    ├── Modify gulp/webpack for jade builds                          │    │
│  │    ├── Cross-platform: Windows, macOS, Linux                        │    │
│  │    ├── Auto-update infrastructure                                   │    │
│  │    └── Code signing setup                                           │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
│                                                                              │
│  FILES TO MODIFY:                                                            │
│  ├── product.json              (branding, update URL)                       │
│  ├── src/vs/workbench/         (workbench customizations)                   │
│  ├── src/vs/editor/            (AI completion integration)                  │
│  ├── extensions/               (bundled jade extensions)                    │
│  └── build/                    (build scripts)                              │
│                                                                              │
│  FORK MAINTENANCE:                                                           │
│  ├── Track upstream: git remote add upstream microsoft/vscode               │
│  ├── Monthly sync: git fetch upstream && git merge upstream/main            │
│  ├── Resolve conflicts in: product.json, custom extensions                  │
│  └── Test matrix: Windows/macOS/Linux × Arm64/x64                           │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 2. jade-cli (BUILD from scratch)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              jade-cli                                        │
│                     Standalone Terminal AI Agent                             │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ARCHITECTURE:                                                               │
│                                                                              │
│       ┌─────────────────────────────────────────────────────────────┐       │
│       │                      USER INPUT                              │       │
│       │                   (Terminal / stdin)                         │       │
│       └────────────────────────┬────────────────────────────────────┘       │
│                                │                                             │
│                                ▼                                             │
│       ┌─────────────────────────────────────────────────────────────┐       │
│       │                     COMMAND PARSER                           │       │
│       │              (yargs / commander / oclif)                     │       │
│       └────────────────────────┬────────────────────────────────────┘       │
│                                │                                             │
│                ┌───────────────┼───────────────┐                            │
│                │               │               │                            │
│                ▼               ▼               ▼                            │
│       ┌─────────────┐ ┌─────────────┐ ┌─────────────┐                       │
│       │    Chat     │ │   Agent     │ │   Config    │                       │
│       │   Mode      │ │   Mode      │ │   Mode      │                       │
│       │             │ │             │ │             │                       │
│       │  Direct     │ │  Agentic    │ │  Settings   │                       │
│       │  Q&A        │ │  Tasks      │ │  Management │                       │
│       └──────┬──────┘ └──────┬──────┘ └──────┬──────┘                       │
│              │               │               │                              │
│              └───────────────┼───────────────┘                              │
│                              │                                               │
│                              ▼                                               │
│       ┌─────────────────────────────────────────────────────────────┐       │
│       │                     jade-ai                                  │       │
│       │           (Multi-model AI orchestration)                     │       │
│       └────────────────────────┬────────────────────────────────────┘       │
│                                │                                             │
│                                ▼                                             │
│       ┌─────────────────────────────────────────────────────────────┐       │
│       │                    jade-proto                                │       │
│       │             (MCP tools, ACP agents)                          │       │
│       └─────────────────────────────────────────────────────────────┘       │
│                                                                              │
│  LANGUAGE: TypeScript (with Ink for TUI) or Rust (for speed)                │
│                                                                              │
│  FEATURES:                                                                   │
│  ├── jade chat              Interactive chat mode                           │
│  ├── jade agent "task"      Agentic task execution                          │
│  ├── jade edit file.ts      AI-assisted file editing                        │
│  ├── jade commit            Smart commit message generation                 │
│  ├── jade review            PR review assistance                            │
│  ├── jade config            Configuration management                        │
│  ├── jade mcp               MCP server management                           │
│  └── jade auth              Authentication management                       │
│                                                                              │
│  DIFFERENTIATORS FROM CLAUDE CODE:                                           │
│  ├── Multi-model support (Claude, Ollama, Gemini, GPT)                      │
│  ├── Team features (shared context, file locking)                           │
│  ├── 4-tier config resolution                                               │
│  ├── Entity-aware (uses frontmatter for context)                            │
│  └── Jade IDE integration (shared state)                                    │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 3. jade-core (BUILD from scratch)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              jade-core                                       │
│                      Shared Library for All Products                         │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  MODULES:                                                                    │
│                                                                              │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │                        config/                                       │    │
│  │  4-tier configuration resolution                                     │    │
│  ├─────────────────────────────────────────────────────────────────────┤    │
│  │                                                                      │    │
│  │   Tier 4: Organization   ─► ~/.config/jade/org/<org>/               │    │
│  │            │                                                         │    │
│  │            ▼                                                         │    │
│  │   Tier 3: Enterprise     ─► /etc/jade/ (IT-managed)                 │    │
│  │            │                                                         │    │
│  │            ▼                                                         │    │
│  │   Tier 2: Project        ─► ./<project>/.jade/                      │    │
│  │            │                                                         │    │
│  │            ▼                                                         │    │
│  │   Tier 1: Personal       ─► ~/.jade/ (chezmoi managed)              │    │
│  │                                                                      │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
│                                                                              │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │                        entity/                                       │    │
│  │  AST-based entity indexing                                           │    │
│  ├─────────────────────────────────────────────────────────────────────┤    │
│  │  • Frontmatter parser (YAML in comments)                            │    │
│  │  • Tree-sitter integration                                          │    │
│  │  • Dependency graph construction                                    │    │
│  │  • Breaking change detection                                        │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
│                                                                              │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │                        team/                                         │    │
│  │  Collaboration features                                              │    │
│  ├─────────────────────────────────────────────────────────────────────┤    │
│  │  • File locking (frontmatter-based)                                 │    │
│  │  • Presence awareness                                               │    │
│  │  • Conflict detection                                               │    │
│  │  • Session tracking                                                 │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
│                                                                              │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │                        telemetry/                                    │    │
│  │  Privacy-first analytics                                             │    │
│  ├─────────────────────────────────────────────────────────────────────┤    │
│  │  • Opt-in collection                                                │    │
│  │  • Anonymization                                                    │    │
│  │  • Usage metering for billing                                       │    │
│  │  • Audit logging                                                    │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
│                                                                              │
│  LANGUAGE: TypeScript (primary) + Rust (wasm for perf-critical)             │
│                                                                              │
│  DISTRIBUTION:                                                               │
│  ├── npm: @jade-ide/core                                                    │
│  ├── crates.io: jade-core (Rust)                                            │
│  └── wasm: @jade-ide/core-wasm                                              │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Development Priority Order

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        DEVELOPMENT ROADMAP                                   │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  PHASE 1: FOUNDATION (Months 1-2)                                           │
│  ═══════════════════════════════                                            │
│                                                                              │
│     ┌──────────┐     ┌──────────┐     ┌──────────┐                         │
│     │ jade-core│────►│ jade-ai  │────►│jade-proto│                         │
│     │          │     │          │     │          │                         │
│     │ Config   │     │ Claude   │     │ MCP impl │                         │
│     │ Entity   │     │ Ollama   │     │          │                         │
│     └──────────┘     └──────────┘     └──────────┘                         │
│         1.1              1.2              1.3                               │
│                                                                              │
│  PHASE 2: CLI PRODUCT (Months 2-3)                                          │
│  ═══════════════════════════════                                            │
│                                                                              │
│     ┌──────────────────────────────────────────┐                            │
│     │                jade-cli                   │                            │
│     │                                          │                            │
│     │  Chat ──► Agent ──► Tools ──► Config     │                            │
│     │  2.1      2.2       2.3       2.4        │                            │
│     └──────────────────────────────────────────┘                            │
│                                                                              │
│  PHASE 3: IDE FORK (Months 3-5)                                             │
│  ══════════════════════════════                                             │
│                                                                              │
│     ┌──────────────────────────────────────────┐                            │
│     │                jade-ide                   │                            │
│     │                                          │                            │
│     │  Fork ──► Brand ──► Integrate ──► Ship   │                            │
│     │  3.1      3.2       3.3          3.4     │                            │
│     └──────────────────────────────────────────┘                            │
│                                                                              │
│  PHASE 4: PLATFORM (Months 5-7)                                             │
│  ══════════════════════════════                                             │
│                                                                              │
│     ┌──────────────────────────────────────────┐                            │
│     │              jade-server                  │                            │
│     │                                          │                            │
│     │  Auth ──► Billing ──► Sync ──► Teams     │                            │
│     │  4.1      4.2        4.3      4.4        │                            │
│     └──────────────────────────────────────────┘                            │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Upstream Dependencies Summary

| Package | Source | License | Action | Risk |
|---------|--------|---------|--------|------|
| VS Code | microsoft/vscode | MIT | FORK | Low - MIT allows commercial |
| Electron | electron/electron | MIT | DEP | Low |
| Claude SDK | @anthropic-ai/sdk | Apache 2.0 | DEP | Low |
| MCP SDK | @anthropic-ai/mcp | Apache 2.0 | DEP | Low |
| ACP SDK | zed-industries/acp | Apache 2.0 | DEP | Low |
| Tree-sitter | tree-sitter/tree-sitter | MIT | DEP | Low |
| Ink (TUI) | vadimdemedes/ink | MIT | DEP | Low |
| FastAPI | tiangolo/fastapi | MIT | DEP | Low |
| Ollama | ollama/ollama | MIT | DEP | Low |

---

*Generated: 2026-01-23 | Entity: document-jade-architecture*

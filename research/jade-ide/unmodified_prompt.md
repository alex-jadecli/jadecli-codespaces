# ---
# entity_id: document-unmodified-prompt
# entity_name: Jade IDE Research Prompt (Unmodified)
# entity_type_id: document
# entity_path: research/jade-ide/unmodified_prompt.md
# entity_language: markdown
# entity_state: active
# entity_created: 2026-01-23T00:00:00Z
# entity_actors: [dev, claude]
# locked_by: null
# locked_at: null
# status: available
# ---

# Original Research Prompt - Jade IDE

> Captured verbatim from initial session request.

---

Create a structured research used Claude code optimized front matter and modern research techniques to organize knowledge as new insights are gained.

Focus on researching, if i am staring a business to fork vscode (like what cursor, Gemini and kiro did) that will be called jade-ide and a CLI extension that works with Claude code that could be used standalone or in jade-ide , set up the research context to describe my Linux os 26.04 , vram 11gb , ram 128 gb, and 24 thread cpu running windows 10 with wsl for Ubuntu 26.04. research and provide guidance for how to properly set up a 26.04 Linux environment that is tuned for Claude code and local ollama assisted development  on that local machine. All installations , package managers , configurations , and dotfiles need to use modern GitHub organizational techniques for launching commercial grade consumer technology that an engineer can maintain by learning from others mistakes and anti patterns.  One of the core benefits jade will offer is improving the team oriented culture of managing git projects and that starts by implementing it for ourselves. On this new 26.04 environment, consider the complexity of 4 scenarios)
1. An engineer will have their own local dotfiles e.g. "~/.claude",
2. A project may or may not have "~/<organization>/<project-repo>/.claude",
3. IT will need to set up enterprise / organizational configs for Claude for the repo
4. There may be usefulness in having shared .claude files as parts of a dotfiles utility at a GitHub organization level and per project.

The above scenario is only the dotfiles for .claude for an engineer can easily have 20+ on their machine at an organization over time. Think about we can use chezmoi and other relevant modern packages / techniques / processes / automation used by modern ai companies like anthropic , Google Gemini , OpenAI , cursor and GitHub with copilot. And think about how the agentclientprotcol can help us (process Llms.txt https://agentclientprotocol.com/llms.txt)

Save this prompt into "unmodified_prompt.md", then cp and optimize the formatting as "init.sh" to start a multi agent research process where they all contribute researching using parallel.ai api's for better web search and extract type abilities. They should append write structured output to <2604-research>-append-progress.txt without opening the file as they progress.

---

## System Context

| Component | Specification |
|-----------|---------------|
| Host OS | Windows 10 |
| WSL Distro | Ubuntu 26.04 |
| RAM | 128 GB |
| VRAM | 11 GB (GPU) |
| CPU | 24 threads |
| Primary Use | Claude Code + Ollama local dev |

## Research Domains

1. **VS Code Fork Architecture** - Cursor, Gemini, Kiro patterns
2. **Ubuntu 26.04 Optimization** - Claude Code + Ollama tuning
3. **Dotfiles Management** - chezmoi, multi-tier .claude configs
4. **Enterprise Git Culture** - Team-oriented project management
5. **Agent Client Protocol** - LLM integration standards

---

*Prompt captured: 2026-01-23*

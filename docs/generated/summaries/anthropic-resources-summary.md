# Anthropic Resources Summary

Optimized for LLM consumption. Overview of Anthropic company resources and research.

## Company Overview

**Anthropic:** AI safety company (founded 2021)

**Focus:** Building safe, beneficial, interpretable AI systems

**Key Products:**
- Claude AI models (text, vision, tool use, extended thinking)
- Anthropic API (for developers)
- Claude on web (claude.ai)
- Platform Claude (integrated tools)

---

## Constitutional AI (CAI)

**Core Innovation:** Train AI to be helpful, harmless, honest without large-scale human feedback.

**How It Works:**
1. AI generates responses to prompts
2. AI critiques own response against constitution
3. AI revises based on self-critique
4. Iterate to improve

**Advantages:**
- Scalable (less human annotation)
- Transparent (clear principles)
- Interpretable (can explain reasoning)

**Principles:**
- Helpful: Assist users effectively
- Harmless: Avoid enabling harm
- Honest: Provide accurate information
- Thoughtful: Consider complexity

---

## Claude Models

### Capability Levels

**Claude Opus 4.5** (~200K context)
- Most capable overall
- Complex reasoning, coding, analysis
- Higher cost and latency

**Claude Sonnet 4.5** (~200K context)
- Balanced speed/quality
- Best for production
- Most commonly used

**Claude Haiku 4.5** (~200K context)
- Fast, cost-effective
- Simple tasks
- Quick responses

### Capabilities by Model

| Capability | Haiku | Sonnet | Opus |
|-----------|-------|--------|------|
| Text | Yes | Yes | Yes |
| Vision | Yes | Yes | Yes |
| Tools | Yes | Yes | Yes |
| Reasoning | Basic | Advanced | Expert |
| Context | 200K | 200K | 200K |
| Speed | Fast | Balanced | Slow |
| Cost | $ | $$ | $$$ |

---

## Research Areas

### Interpretability

Understanding how AI models work internally.

**Goals:**
- Explain model decisions
- Find and fix failures
- Build more trustworthy systems

### AI Alignment

Ensuring AI systems pursue intended goals safely.

**Topics:**
- Constitutional AI principles
- Scaling oversight (supervise increasingly capable AI)
- Mechanistic interpretability

### Capability Research

Advancing AI to solve harder problems.

**Areas:**
- Extended thinking (long reasoning chains)
- Tool use (function calling)
- Multimodal (vision + text)

---

## Career Opportunities

### Research Positions

**Fields:**
- AI safety and alignment
- Interpretability and mechanistic understanding
- Capability scaling and training
- Language model evaluation

**Expectations:**
- PhD or equivalent experience
- Published research
- Systems thinking
- Hands-on implementation

### Engineering Positions

**Areas:**
- Infrastructure and ML systems
- API and platform development
- Deployment and scaling
- Developer tools

**Skills Needed:**
- Distributed systems
- ML infrastructure
- Performance optimization
- System design

### Product & Operations

**Teams:**
- Product management
- Operations
- Sales and customer success
- Strategic partnerships

---

## Resources Available (docs/anthropic/)

### By Category

**Careers:**
- Job postings
- Internship opportunities
- University recruitment
- Contractor/consultant roles

**Engineering:**
- Architecture guides
- Best practices
- Design patterns
- Performance guidelines

**Research & Learn:**
- Published papers
- Research directions
- Technical documentation
- Learning materials

**News & Events:**
- Company announcements
- Conference talks
- Event information
- Community updates

**Legal & Compliance:**
- Privacy policy
- Terms of service
- Compliance documents
- Data handling

**AI for Science:**
- Special program details
- Application process
- Research areas
- Partner institutions

---

## Products & Services

### Claude API

**Access:** https://docs.anthropic.com

**Features:**
- Text generation
- Vision analysis
- Tool use
- Batch processing
- Vision fine-tuning (selected partners)

**Pricing:** Per-token, varies by model and capability

### Claude on Web

**Access:** https://claude.ai

**Features:**
- Free tier (limited)
- Pro subscription (unlimited)
- Project organization
- File upload and analysis
- Integration with Google services

### Platform Claude

**Features:**
- Unified interface
- Chat search and memory
- Style personalization
- Project management
- Tool integrations (Google Drive, Gmail, etc.)
- iOS shortcuts

---

## Key Concepts

**Extended Thinking:** Claude's ability to reason through complex problems with long "thinking" chains before responding.

**Tool Use:** Claude can call external functions/APIs based on task requirements.

**Vision:** Image understanding - describe, OCR, analyze, identify.

**Streaming:** Real-time token output for faster perceived response.

**Batch Processing:** Asynchronous API for cost-effective bulk processing.

---

## Getting Started

### If You're a Developer

1. Read: [Claude API Primer](../platform-claude/claude-api-primer.md)
2. Explore: [Claude Cookbooks](../platform-claude/cookbooks.md)
3. Browse: [Prompt Library](../platform-claude/prompt-library.md)
4. Reference: [Glossary](../platform-claude/glossary.md)

### If You're Interested in Safety/Research

1. Read papers from docs/anthropic/learn/
2. Explore Constitutional AI principles
3. Check research directions
4. Apply to research internships

### If You're Considering Working Here

1. Check [careers](../anthropic/careers/) for positions
2. Understand company values and mission
3. Review technical interview guidance
4. Look at engineering best practices

---

## Company Values

**Safety First:** Responsible AI development, not just capability

**Transparency:** Open about capabilities and limitations

**Thoughtfulness:** Consider long-term impacts

**Collaboration:** Work with academic institutions and safety researchers

**Diversity:** Build inclusive teams and technology

---

## Resources Not Included Here

**Note:** Some company materials are internal or confidential:
- Detailed financial information
- Internal tools and infrastructure
- Unreleased models
- Beta features under development

For latest info, visit: https://www.anthropic.com

---

## Token Count: ~800 tokens

Used for: Hiring context, research area selection, capability evaluation.

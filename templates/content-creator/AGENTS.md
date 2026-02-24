# Content Creator Workspace - Agent Orchestration

Welcome to the **Content Creator OpenCode Workspace**. This repository is configured to natively leverage OpenCode's `Task(Category + Skills)` architecture for high-efficiency, multi-platform, bilingual content creation. 

We do not rely on clunky, monolithic prompts or custom manual agents. Instead, we use native OpenCode categories combined with highly focused skills.

## Core Architecture

This workspace uses the following native OpenCode categories:

1. **`writing`**: For generating primary drafts, outlines, and literary prose.
2. **`deep`**: For researching technical topics or analyzing complex literary/artistic themes.
3. **`quick`**: For fast repurposing of content into social media posts.
4. **`unspecified-high` / `unspecified-low`**: For running local python scripts (e.g., Audits).

### The Skill Routing System (`.opencode/skills/`)

Skills are injected into the agent's context only when needed. They define the specific "Voice" or "Format" for the task at hand. 

- **Content Forms**: `voice-blog`, `voice-weekly`, `voice-social`
- **Domain Contexts**: `domain-tech`, `domain-artistic`, `domain-literary`, `domain-design`, `domain-personal`
- **Platform Formats**: `platform-social`, `platform-video`, `platform-audio-podcast`, etc.

*Example Delegation:*
```typescript
task(
  category="writing",
  load_skills=["voice-blog", "domain-artistic"], 
  prompt="Draft a blog post about the intersection of photography and AI. Focus on emotion over technical facts."
)
```

## Standard Operating Procedures (Commands)

The orchestrator (Sisyphus) should execute these via OpenCode commands (located in `.opencode/commands/`):

1. **`/brainstorm`**:
   - **Trigger**: User asks to brainstorm or plan a topic.
   - **Action**: Spin up a `deep` task loading `content-research-writer` (and potentially `librarian` in parallel) to generate hooks and a core outline.

2. **`/draft`**: 
   - **Trigger**: User asks to write a new blog post.
   - **Action**: Identify the domain (tech/art/personal). Spin up a `writing` task loading `voice-blog` and `domain-[type]`.

3. **`/enrich`**:
   - **Trigger**: User wants to add images, placeholders, or Mermaid charts to a draft.
   - **Action**: Spin up a `writing` task loading `skill-image-enrichment` to insert visual elements before the audit phase.
3. **`/repurpose`**: 
   - **Trigger**: User asks to turn a blog post into social media content or a video script.
   - **Action**: Spin up parallel `quick` tasks loading the consolidated `platform-social` or `platform-video` skills. For LinkedIn/WeChat, directly reuse the blog content if applicable.
4. **`/audit`**: 
   - **Trigger**: User asks to check SEO or Brand Voice.
   - **Action**: Run `python scripts/seo_optimizer.py <file>` or `python scripts/brand_voice_analyzer.py <file>`. Parse the JSON/CLI output and provide a summary.

## Core Rules for Sisyphus

1. **Never use marketing speak.** If the user asks for a blog on photography, load `domain-artistic`, and ensure the output is emotional, reflective, and factually sparse. 
2. **Parallelize Distribution.** If asked to repurpose for Twitter and Xiaohongshu, run two parallel tasks. Do not wait for one to finish before starting the other.
3. **Always check Language.** This workspace supports English and Chinese. Pass the explicit language requirement to the subagents if specified.
4. **File Output Location.** All outputs (drafts, enriched content, scripts, social posts) MUST be saved directly to the workspace output directory (or relevant markdown files) `contents/*/` for the user to review.
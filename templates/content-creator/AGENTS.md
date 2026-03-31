# Content Creator Workspace - Agent Orchestration

Welcome to the **Content Creator OpenCode Workspace**. This repository is configured to natively leverage OpenCode's `Task(Category + Skills)` architecture for high-efficiency, multi-platform, bilingual content creation.

We do not rely on clunky, monolithic prompts or custom manual agents. Instead, we use native OpenCode categories combined with highly focused skills.

## Core Architecture

This workspace uses the following native OpenCode categories:

1. **`writing`**: For generating primary drafts, outlines, and literary prose.
2. **`deep`**: For researching technical topics or analyzing complex literary/artistic themes.
3. **`quick`**: For fast repurposing of content into social media posts.
4. **`unspecified-high` / `unspecified-low`**: For running local Python scripts (e.g., Audits, Video Pipeline).

### The Skill Routing System (`.opencode/skills/`)

Skills are injected into the agent's context only when needed. They define the specific "Voice" or "Format" for the task at hand.

**Root Router**: `voice-optimization/SKILL.md` — all content creation starts here.

- **Content Types**: `type-blog`, `type-weekly`, `type-social`
- **Domain Contexts**: `domain-tech`, `domain-artistic`, `domain-literary`, `domain-design`, `domain-personal`
- **Platform Formats**: `platform-social`, `platform-video`, `platform-text`
- **Specialized Skills**: `frontmatter-notion-property`, `image-enrichment`, `seo-optimization`, `video-pipeline`

*Example Delegation:*
```typescript
task(
  category="writing",
  load_skills=["type-blog", "domain-artistic", "voice-optimization"],
  prompt="Draft a blog post about the intersection of photography and AI. Focus on emotion over technical facts."
)
```

## Standard Operating Procedures (Commands)

The orchestrator (Sisyphus) should execute these via OpenCode commands (located in `.opencode/commands/`):

### Content Writing Commands

1. **`/blog-writing <题材> [资料]`**:
   - **Trigger**: User wants to write a blog post.
   - **Action**: Full pipeline — brainstorm → draft → enrich → audit → finalize.
   - **Skills**: `type-blog` + domain + `voice-optimization` + `seo-optimization`

2. **`/weekly-writing <题材> [资料]`**:
   - **Trigger**: User wants to create a newsletter/weekly digest.
   - **Action**: Topic curation → item writing → review → finalize.
   - **Skills**: `type-weekly` + domain + `voice-optimization`

3. **`/mlog-writing <题材> [资料]`**:
   - **Trigger**: User wants to log music-related content (composition, covers, production).
   - **Action**: Understand context → write with musical voice → enrich with audio references → finalize.
   - **Skills**: `type-blog` + `domain-artistic` + `voice-optimization`

4. **`/plog-writing <题材> [资料]`**:
   - **Trigger**: User wants to log photography content (works, experiences, gear).
   - **Action**: Understand context → write with visual voice → enrich with photo placeholders → finalize.
   - **Skills**: `type-blog` + `domain-artistic` + `voice-optimization`

### Distribution Commands

5. **`/social-repurposing <源文档> [平台]`**:
   - **Trigger**: User wants to distribute content to social platforms.
   - **Action**: Spin up parallel `quick` tasks for each platform (Twitter, WeChat, Zhihu, CSDN, Xiaohongshu).
   - **Skills**: `platform-social` + `platform-text` + `voice-optimization`

6. **`/video-repurposing <源文档> [语言]`**:
   - **Trigger**: User wants to create a video from content.
   - **Action**: Generate recipe.json → HTML PPT → TTS → render frames → compile video.
   - **Skills**: `platform-video` + `video-pipeline` + `voice-optimization`
   - **Python Scripts**: `scripts/video_pipeline/`

## Core Rules for Sisyphus

1. **Never use marketing speak.** If the user asks for a blog on photography, load `domain-artistic`, and ensure the output is emotional, reflective, and factually sparse.
2. **Parallelize Distribution.** If asked to repurpose for Twitter and Xiaohongshu, run two parallel tasks. Do not wait for one to finish before starting the other.
3. **Always check Language.** This workspace supports English and Chinese. Pass the explicit language requirement to the subagents if specified.
4. **File Output Location.** All content MUST be saved within the `Assets` directory mimicking the Notion database structure.
   - **Blog**: `Assets/Blog/[name]/[name].md`
   - **Weekly**: `Assets/Weekly/[name]/[name].md`
   - **Mlog (Music)**: `Assets/Mlog/[name]/[name].md`
   - **Plog (Photography)**: `Assets/Plog/[name]/[name].md`
   - **Video**: `Assets/Video/[name]/recipe.json` + `slides/` + `audio/` + `frames/` + `[name].mp4`
   - **Distributions**: `Assets/[Category]/[name]/distributions/[platform]/`
5. **Video Pipeline**: LLM only generates `recipe.json`. Python scripts handle all TTS/rendering/compositing. Never run FFmpeg commands directly.
6. **Audit Before Finalize.** Always run SEO and brand voice checks before marking content as done.

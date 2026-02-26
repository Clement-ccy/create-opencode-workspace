# Draft Command (`/draft`)

**Description**: Initiates a new writing session for long-form content (blogs, newsletters, essays).

## Orchestration Flow

1. **Understand Request**: Determine the `topic`, `language` (English/Chinese), the `domain` (technical, artistic, design, literary, personal), and a unique routing name `[name]` for the article.
2. **Select Skills**:
   - Always load: `voice-blog` (or `voice-weekly` if it's a newsletter), `skill-frontmatter-notion` (for Notion-compatible YAML), and `skill-seo`.
   - Load Domain Skill: e.g., `domain-artistic` (for photography/music), `domain-tech` (for programming).
3. **Execute Task**:
   - Spin up a `writing` category task.
   - Inject the selected skills.
   - Provide the specific topic, an explicit instruction on the target language, and the unique routing name.
   - Example Prompt to Agent: "Draft a blog post about {topic} in {language}. Adhere strictly to the loaded voice and domain guidelines. The output MUST be saved to `Assets/[Category]/[name]/[name].md` and include the standard Notion frontmatter."
4. **Finalize**: 
   - Present the draft to the user.
   - Ask if they want to run an `/audit` on the draft or `/repurpose` it for social media.
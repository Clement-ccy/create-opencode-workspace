# Draft Command (`/draft`)

**Description**: Initiates a new writing session for long-form content (blogs, newsletters, essays).

## Orchestration Flow

1. **Understand Request**: Determine the `topic`, `language` (English/Chinese), and the `domain` (technical, artistic, design, literary, personal).
2. **Select Skills**:
   - Always load: `voice-blog` (or `voice-weekly` if it's a newsletter).
   - Load Domain Skill: e.g., `domain-artistic` (for photography/music), `domain-tech` (for programming).
3. **Execute Task**:
   - Spin up a `writing` category task.
   - Inject the selected skills.
   - Provide the specific topic and an explicit instruction on the target language.
   - Example Prompt to Agent: "Draft a blog post about {topic} in {language}. Adhere strictly to the loaded voice and domain guidelines."
4. **Finalize**: 
   - Present the draft to the user.
   - Ask if they want to run an `/audit` on the draft or `/repurpose` it for social media.
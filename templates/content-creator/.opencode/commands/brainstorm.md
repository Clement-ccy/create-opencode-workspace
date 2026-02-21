# Brainstorm Command (`/brainstorm`)

**Description**: Initiates a deep research session to generate a multi-platform content outline.

## Orchestration Flow

1. **Understand Request**: Determine the `topic` and specific angles or target audience provided by the user.
2. **Execute Research**:
   - Spin up a `deep` category task to conduct thorough research.
   - Inject the built-in `content-research-writer` skill.
   - Concurrently, if it's a technical or external-heavy topic, spin up a `librarian` task to gather the latest docs/news.
   - Prompt the `deep` agent to: "Analyze audience pain points, provide 5 viral title hooks, and output a comprehensive outline suitable for a core blog post on the topic: {topic}."
3. **Finalize**: 
   - Synthesize the collected outlines and title suggestions.
   - Present the finalized plan to the user and ask if they are ready to proceed with `/draft`.

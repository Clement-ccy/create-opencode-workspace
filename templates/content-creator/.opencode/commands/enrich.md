# Enrich Command (`/enrich`)

**Description**: Supplements and optimizes the draft with image placeholders, descriptions, and Mermaid charts. This command sits between `/draft` and `/audit`.

## Orchestration Flow

1. **Understand Request**: Identify the source draft that needs visual enrichment.
2. **Select Skills**:
   - Always load: `skill-image-enrichment`.
3. **Execute Task**:
   - Spin up a `writing` category task.
   - Inject the `skill-image-enrichment` skill.
   - Provide the draft text and ask the agent to insert image placeholders (`<!-- IMAGE: ... -->`), add Mermaid diagrams where processes or architectures are explained, and ensure standard alt text and naming conventions.
   - Example Prompt: "Review this draft and insert appropriate visual elements using the guidelines in skill-image-enrichment. Add Mermaid charts for logic flow, and detailed image placeholders for photos/screenshots."
4. **Finalize**: 
   - Present the visually enriched draft to the user.
   - Ask if they are ready to run an `/audit` on the draft.
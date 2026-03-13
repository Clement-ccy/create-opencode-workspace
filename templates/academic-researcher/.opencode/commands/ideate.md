# Ideate Command (`/ideate`)

**Description**: Initiates a deep research session to collect literature, analyze the research landscape, and generate novel research ideas based on a user-provided topic or content.

## Orchestration Flow

1. **Understand Request**: Determine the research `topic`, target `domain` (CS-AI, CS-NLP, CS-Systems, or generic), and any specific papers or content the user has provided as input.
2. **Execute Research**:
   - Spin up a `deep` category task with skills: `voice-proposal`, `skill-literature`, and the appropriate `domain-*` skill.
   - Concurrently, spin up a `librarian` task to search for recent papers, surveys, and state-of-the-art results on the topic.
   - The `deep` agent should: analyze the research landscape, identify gaps, collect key references, and propose 2-3 novel research ideas with potential contributions.
3. **Structure Output**:
   - Save the research proposal to `idea/proposal.md`.
   - For each core reference paper found, create a directory under `idea/references/<paper-key>/` with `meta/bibtex.txt`, `meta/meta_info.txt`, and `meta/toc.txt`.
   - Update `idea/metadata.json` with the research domain and keywords.
4. **Finalize**:
   - Present the generated ideas and collected references to the user.
   - Remind the user that they MUST run `/review` before proceeding to `/plan`. The automated review will check novelty and citation validity.

## Important Notes
- This command is for idea generation ONLY. It does NOT create experiment plans.
- All references must be real papers. The `/review` command will validate them.
- Output goes to `idea/` directory exclusively.

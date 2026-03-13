# Write Command (`/write`)

**Description**: Writes or revises paper sections in `writing/paper/sections/`. Supports both Markdown and LaTeX output formats.

## Orchestration Flow

1. **Understand Request**:
   - Determine which section(s) to write: abstract, introduction, related_work, method, experiments, results, discussion, conclusion.
   - Determine the output format: Markdown (default) or LaTeX.
   - Determine the language: English (default for papers) or Chinese.
2. **Gather Context**:
   - Read `idea/proposal.md` for the research narrative.
   - Read relevant experiment reports from `exp/EXPERIMENT_RESULTS/`.
   - Read existing paper sections from `writing/paper/sections/` for consistency.
   - Read core references from `idea/references/` for related work.
3. **Execute Writing**:
   - Spin up a `writing` category task with skills: `voice-academic`, `skill-citation`, and the appropriate `domain-*` skill.
   - For each requested section, provide specific guidance:
     - **Abstract**: Concise summary (150-300 words) covering problem, method, results, impact.
     - **Introduction**: Problem statement, motivation, contributions list, paper organization.
     - **Related Work**: Organized by theme/approach, clearly differentiating this work.
     - **Method**: Formal description with notation, algorithms, architecture details.
     - **Experiments**: Setup, datasets, baselines, metrics, implementation details.
     - **Results**: Tables, figures references, statistical analysis.
     - **Discussion**: Limitations, broader impact, comparison analysis.
     - **Conclusion**: Summary of contributions, future work.
4. **Format Output**:
   - Markdown: Save to `writing/paper/sections/<section>.md`
   - LaTeX: Save to `writing/paper/sections/<section>.tex`
   - Ensure all citations use standard format: `[Author et al., Year]` for Markdown, `\cite{key}` for LaTeX.
5. **Finalize**:
   - Present the written section for review.
   - Suggest running `/cite` to verify all references are properly managed.

## Important Notes
- Write one section at a time for quality. Do not attempt to write the entire paper in one pass.
- Always cross-reference with experiment results for accuracy.
- Maintain consistent notation across sections.

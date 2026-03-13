# Cite Command (`/cite`)

**Description**: Manages references and citations. Add new references, update BibTeX entries, check citation integrity, and synchronize between idea/references/ and writing/references/.

## Orchestration Flow

1. **Understand Request**:
   - Determine the action: `add` (new reference), `check` (validate existing), `sync` (synchronize references), or `format` (generate BibTeX file).
2. **Execute Action**:
   - **Add**: 
     - Spin up a `quick` category task with skill: `skill-citation`.
     - Search for the paper via Semantic Scholar/arXiv.
     - Create entry in `writing/references/` with BibTeX and brief notes.
     - If it's a core reference, also create detailed entry in `idea/references/<paper-key>/`.
   - **Check**:
     - Run: `python .opencode/skills/skill-citation/scripts/citation_validator.py writing/references/`
     - Report any invalid or missing citations.
   - **Sync**:
     - Compare references in `idea/references/` and `writing/references/`.
     - Ensure all cited papers in paper sections have corresponding BibTeX entries.
   - **Format**:
     - Generate a consolidated `references.bib` file in `writing/references/`.
3. **Finalize**:
   - Report the action taken and any issues found.
   - If citations were added, show the BibTeX entries for confirmation.

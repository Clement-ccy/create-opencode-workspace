# Review Command (`/review`)

**Description**: Runs automated review scripts to validate the research idea's novelty and citation integrity. This is a mandatory gate before proceeding to `/plan`.

## Orchestration Flow

1. **Pre-check**: Verify that `idea/proposal.md` exists and has content. If not, instruct the user to run `/ideate` first.
2. **Execute Novelty Check**:
   - Run: `python .opencode/skills/skill-novelty-check/scripts/novelty_checker.py idea/proposal.md`
   - This script queries the Semantic Scholar API to find similar existing papers and provides a novelty assessment.
3. **Execute Citation Validation**:
   - Run: `python .opencode/skills/skill-citation/scripts/citation_validator.py idea/references/`
   - This script validates that all cited papers are real (not hallucinated) by checking against Semantic Scholar, CrossRef, and arXiv APIs.
4. **Analyze Results**:
   - Parse the output from both scripts.
   - Summarize: novelty score, similar papers found, citation validity rate, any flagged issues.
5. **Gate Decision**:
   - If both checks pass: Inform the user they can proceed to `/plan`.
   - If novelty check fails: Suggest the user refine their idea via `/ideate` with more specific differentiation.
   - If citation validation fails: List the problematic citations and ask the user to correct them.

## Important Notes
- These scripts should be executed directly via the `bash` tool by the Orchestrator, NOT delegated to a subagent.
- This is a MANDATORY gate. The orchestrator must enforce this before allowing `/plan`.
- If scripts are not available or fail to run, warn the user and suggest manual review.

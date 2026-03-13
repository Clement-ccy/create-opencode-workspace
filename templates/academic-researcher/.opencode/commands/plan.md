# Plan Command (`/plan`)

**Description**: Creates a detailed experiment plan including model selection, dataset choice, evaluation metrics, baselines, and step-by-step execution plan. Saved as `idea/plan.json`.

## Orchestration Flow

1. **Pre-check**: 
   - Verify `idea/proposal.md` exists.
   - Check if `/review` has been run (look for review results or ask user to confirm). Warn if review hasn't been completed.
2. **Gather Context**:
   - Read `idea/proposal.md` for the research idea.
   - Read `idea/references/` for collected literature context.
   - Read `idea/metadata.json` for domain information.
3. **Execute Planning**:
   - Spin up an `ultrabrain` category task with skills: `skill-experiment-design` and the appropriate `domain-*` skill.
   - The agent should produce a comprehensive plan covering:
     - Models/architectures to use or build
     - Datasets (with sources and preprocessing steps)
     - Baselines for comparison
     - Evaluation metrics (with justification)
     - Ablation studies
     - Computational requirements estimate
     - Step-by-step execution plan
4. **Structure Output**:
   - Save the plan to `idea/plan.json` following the structured format:
     ```json
     [
       {
         "category": "Category Name",
         "title": "Task Title",
         "description": "What this task accomplishes",
         "steps": {
           "step1": "**Step Name**: Detailed description...",
           "step2": "**Step Name**: Detailed description..."
         }
       }
     ]
     ```
5. **Finalize**:
   - Present the plan summary to the user.
   - Ask for confirmation or modifications before proceeding to `/experiment`.

# Experiment Command (`/experiment`)

**Description**: Generates experiment scripts based on the plan and optionally executes them. Produces code in `exp/scripts/` with results tracked in `exp/runs/` and `exp/results/`.

## Orchestration Flow

1. **Pre-check**:
   - Verify `idea/plan.json` exists and is populated (not just the template). If missing, instruct user to run `/plan` first.
   - Read the plan to understand what experiments need to be implemented.
2. **Execute Script Generation**:
   - Spin up a `deep` category task with skills: `skill-experiment-design` and the appropriate `domain-*` skill.
   - For each experiment category in `plan.json`, generate the corresponding Python scripts in `exp/scripts/`.
   - Scripts should include: data loading, model setup, training loop, evaluation, and result saving.
   - Each script should save results to `exp/results/` in a structured format.
3. **Track Experiments**:
   - Run `python .opencode/skills/skill-experiment-design/scripts/experiment_tracker.py init <experiment-name>` to initialize tracking.
   - Log configuration and parameters.
4. **Execute (if requested)**:
   - If the user asks to run experiments, execute the generated scripts via `bash`.
   - Monitor output and save logs to `exp/runs/<experiment-name>/`.
5. **Finalize**:
   - Present generated scripts for review.
   - Ask if user wants to execute immediately or review first.
   - Remind user to run `/analyze` after experiments complete.

## Important Notes
- Script generation and execution are separate steps. Always generate first, then optionally execute.
- Use experiment_tracker.py to maintain version history of experiment configs.

# Analyze Command (`/analyze`)

**Description**: Analyzes experiment results and generates structured reports (REPORT.md + RESULTS.json) in `exp/EXPERIMENT_RESULTS/`.

## Orchestration Flow

1. **Pre-check**:
   - Verify experiment results exist in `exp/runs/` or `exp/results/`.
   - If no results found, instruct user to run `/experiment` first.
2. **Gather Data**:
   - Read all result files from `exp/results/` and any logs from `exp/runs/`.
   - Read `idea/plan.json` to understand the expected metrics and baselines.
3. **Execute Analysis**:
   - Spin up a `deep` category task with skills: `skill-data-analysis` and `voice-report`.
   - The agent should:
     - Compute summary statistics across all experiment runs.
     - Compare against baselines listed in the plan.
     - Generate comparison tables, charts descriptions, and statistical significance tests where applicable.
     - Identify trends, anomalies, and key findings.
4. **Structure Output**:
   - Create `exp/EXPERIMENT_RESULTS/<experiment-name>/REPORT.md` with the full analysis narrative.
   - Create `exp/EXPERIMENT_RESULTS/<experiment-name>/RESULTS.json` with structured numerical results.
   - Generate analysis plot descriptions in `writing/analytical_plots/`.
5. **Finalize**:
   - Present the analysis summary to the user.
   - Suggest which findings are most suitable for the paper.
   - Ask if the user wants to proceed to `/write`.

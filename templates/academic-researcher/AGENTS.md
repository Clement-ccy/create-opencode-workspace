# Academic Researcher Workspace - Agent Orchestration

Welcome to the **Academic Researcher OpenCode Workspace**. This repository is configured to natively leverage OpenCode's `Task(Category + Skills)` architecture for end-to-end academic research, experimentation, and paper writing.

We do not rely on monolithic prompts or ad-hoc workflows. Instead, we use native OpenCode categories combined with focused research skills and strict workflow gates.

## Core Architecture

Categories used:

1. **`deep`**: Literature research, idea generation (`/ideate`), experiment execution (`/experiment`), data analysis (`/analyze`).
2. **`ultrabrain`**: Experiment planning (`/plan`) — model selection, dataset choice, evaluation metrics.
3. **`writing`**: Paper writing (`/write`), citation management (`/cite`).
4. **`unspecified-high`**: Automated review (`/review`) — running Python validation scripts.

### The Skill Routing System

- **Voices**: `voice-academic`, `voice-proposal`, `voice-report`
- **Domains**: `domain-cs-ai`, `domain-cs-nlp`, `domain-cs-systems`, `domain-generic`
- **Research Skills**: `skill-literature`, `skill-experiment-design`, `skill-data-analysis`, `skill-citation`, `skill-novelty-check`

### Workflow Gates (CRITICAL)

This workspace enforces a sequential workflow with automated gates:

```
/ideate → /review (automated gate) → /plan → /experiment → /analyze → /write
```

- **Gate 1**: After `/ideate`, user MUST run `/review` which executes `novelty_checker.py` and `citation_validator.py`. If review fails, go back to `/ideate`.
- **Gate 2**: `/experiment` REQUIRES `idea/plan.json` to exist and be populated. User MUST run `/plan` first.
- `/analyze` can only run after experiment results exist in `exp/runs/` or `exp/results/`.
- `/write` can run at any stage but will warn if no experiment results exist.
- `/cite` can run at any time to manage references.

## Standard Operating Procedures (Commands)

The orchestrator (Sisyphus) should execute these via OpenCode commands (located in `.opencode/commands/`):

1. **`/ideate`**:
   - **Trigger**: User asks to explore a research topic or generate ideas.
   - **Action**: Spin up a `deep` task loading `voice-proposal`, `skill-literature`, and `domain-*` to propose a research direction and draft a proposal outline.

2. **`/review`**:
   - **Trigger**: User requests validation of novelty or references after ideation.
   - **Action**: Run `python .opencode/skills/skill-novelty-check/scripts/novelty_checker.py <proposal>` and `python .opencode/skills/skill-citation/scripts/citation_validator.py <references>`; summarize pass/fail and issues.

3. **`/plan`**:
   - **Trigger**: User wants a concrete experiment plan.
   - **Action**: Spin up an `ultrabrain` task loading `skill-experiment-design` and `domain-*` to populate `idea/plan.json` with models, datasets, baselines, and metrics.

4. **`/experiment`**:
   - **Trigger**: User requests experiment execution or script generation.
   - **Action**: Spin up a `deep` task loading `skill-experiment-design` and `domain-*` to implement scripts in `exp/scripts/` and run experiments.

5. **`/analyze`**:
   - **Trigger**: User wants analysis of experiment outputs.
   - **Action**: Spin up a `deep` task loading `skill-data-analysis` and `voice-report` to produce `REPORT.md` and `RESULTS.json` per experiment.

6. **`/write`**:
   - **Trigger**: User wants to draft or refine paper sections.
   - **Action**: Spin up a `writing` task loading `voice-academic`, `domain-*`, and `skill-citation` to write sections in `writing/paper/sections/`.

7. **`/cite`**:
   - **Trigger**: User asks to add or validate citations.
   - **Action**: Spin up a `quick` task loading `skill-citation` to manage BibTeX in `writing/references/`.

## Core Rules for Sisyphus

1. **Enforce workflow gates.** Never skip `/review` before `/plan`. Never skip `/plan` before `/experiment`. Check for required files before proceeding.
2. **All references must be real.** Never fabricate citations. Always use `citation_validator.py` before finalizing any reference list.
3. **Dual reference system.** Core references (detailed, with extracted sections) go in `idea/references/`. Writing references (BibTeX + brief notes) go in `writing/references/`.
4. **Experiment tracking.** Every experiment run must produce a `REPORT.md` + `RESULTS.json` in `exp/EXPERIMENT_RESULTS/<experiment-name>/`.
5. **Output formats.** Writing output supports both Markdown and LaTeX. Default is Markdown in `writing/paper/sections/`. LaTeX can be generated on request.
6. **Language support.** This workspace supports English and Chinese. Pass explicit language to subagents.
7. **File output locations.**
   - Ideas and proposals → `idea/`
   - Experiment plans → `idea/plan.json`
   - Experiment code → `exp/scripts/`
   - Experiment results → `exp/runs/`, `exp/results/`, `exp/EXPERIMENT_RESULTS/`
   - Paper sections → `writing/paper/sections/`
   - Figures and plots → `writing/paper/figures/`, `writing/analytical_plots/`
   - References → `idea/references/` (core) and `writing/references/` (citations)

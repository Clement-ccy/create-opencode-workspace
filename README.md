# create-opencode-workspace

A CLI tool to quickly scaffold pre-configured [OhMyOpenCode](https://github.com/ohmyopencode/opencode) workspaces.

It provides pre-configured workspace templates including a **Content Creator** for multi-platform bilingual content and an **Academic Researcher** for end-to-end research lifecycle management, all natively leveraging OpenCode's `Task(Category + Skills)` architecture.

## Usage

You can scaffold a new OpenCode workspace interactively using `npx`:

```bash
npx create-opencode-workspace
```

Follow the prompts:
1. Select the workspace template (e.g., `content-creator`, `academic-researcher`).
2. Enter your project name.

Once completed, navigate into your new project and start OpenCode!

```bash
cd my-opencode-workspace
opencode
```

## Available Templates

### 1. Content Creator
A content generation matrix built entirely on OpenCode's native skills architecture. It supports generating core blog drafts, parallel repurposing to social media (Xiaohongshu, Twitter, WeChat, etc.), and running local SEO & Brand Voice audits via Python.

- **/draft**: Starts a long-form draft with proper domain voice routing.
- **/repurpose**: Concurrently converts the core blog into multiple social media formats.
- **/audit**: Runs local Python scripts for semantic SEO and tone checks.

### 2. Academic Researcher
A full-lifecycle academic research workspace built on OpenCode's native skills architecture. It covers idea generation, literature review, experiment planning, experiment execution, data analysis, and paper writing (Markdown + LaTeX). Includes automated novelty checking and citation validation via Python scripts.

- **/ideate**: Explores a research topic, collects literature, and generates research ideas.
- **/review**: Runs automated novelty and citation validation scripts (mandatory gate).
- **/plan**: Creates a structured experiment plan (models, datasets, metrics).
- **/experiment**: Generates and executes experiment scripts.
- **/analyze**: Analyzes results, producing REPORT.md + RESULTS.json per experiment.
- **/write**: Drafts paper sections with academic voice routing.
- **/cite**: Manages references and BibTeX entries.

## Development

To test this CLI locally:
```bash
git clone https://github.com/yourusername/create-opencode-workspace.git
cd create-opencode-workspace
npm install
npm start
```

## License
MIT

# create-opencode-workspace

A CLI tool to quickly scaffold pre-configured [OhMyOpenCode](https://github.com/ohmyopencode/opencode) workspaces.

Currently, it provides a highly optimized **Content Creator Workspace** which natively leverages OpenCode's `Task(Category + Skills)` architecture for high-efficiency, multi-platform, bilingual content creation.

## Usage

You can scaffold a new OpenCode workspace interactively using `npx`:

```bash
npx create-opencode-workspace
```

Follow the prompts:
1. Select the workspace template (e.g., `content-creator`).
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

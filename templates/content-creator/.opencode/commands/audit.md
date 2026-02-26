# Audit Command (`/audit`)

**Description**: Runs an automated audit on a piece of content (local file) using python scripts to check Brand Voice and SEO optimization.

## Orchestration Flow

1. **Understand Request**: 
   - Identify the file path to audit (e.g., `drafts/post.md`).
   - Identify the audit type (`seo` or `brand`).
   - Identify the language (the scripts now auto-detect Chinese or English).
2. **Execute Task**:
   - `audit-seo`: Run `python .opencode/skills/skill-seo/scripts/seo_optimizer.py <file-path>`
   - `audit-brand`: Run `python .opencode/skills/voice-blog/scripts/brand_voice_analyzer.py <file-path>`
   - **Important**: These commands should be executed directly via the `bash` tool by the Orchestrator, not delegated to a subagent unless complex reasoning is required on the output.
3. **Analyze Output**: 
   - Parse the JSON/CLI output returned by the python script.
   - Summarize the readability score, keyword density (Baidu/Google), tone dimension scores, and explicit recommendations.
   - Ask the user if they want the Orchestrator to automatically implement the recommended fixes.

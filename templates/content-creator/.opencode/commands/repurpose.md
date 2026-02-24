# Repurpose Command (`/repurpose`)

**Description**: Converts a piece of long-form content (like a blog or essay) into social media posts, video scripts, or podcast scripts.

## Orchestration Flow

1. **Understand Request**: 
   - Identify the source content (the long-form draft).
   - Identify target platforms (e.g., social, video, audio). If the target is WeChat/LinkedIn, consider using the direct blog text.
   - Identify the language (English/Chinese).
2. **Select Skills**:
   - Always load: `voice-social` (for social platforms).
   - Load Consolidated Platform Skills: e.g., `platform-social` (for Xiaohongshu/Twitter/Weibo/WeChat), `platform-video` (for Bilibili/YouTube/TikTok), or `platform-audio-podcast`.
3. **Execute Task (Parallelized)**:
   - For each target platform requested, spin up an independent `quick` category task **in parallel**.
   - Example Prompt to Agent A: "Convert this text into a {Platform A} post in {Language}. Follow the `{platform-X}` skill guidelines."
   - Example Prompt to Agent B: "Convert this text into a {Platform B} post in {Language}. Follow the `{platform-Y}` skill guidelines."
4. **Finalize**: 
   - Wait for all parallel tasks to finish.
   - Output the formatted posts/scripts sequentially for the user to review.

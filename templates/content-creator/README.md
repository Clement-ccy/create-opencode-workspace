---
name: content-creator
description: 内容创作系统，以博客为核心，支持技术、艺术、设计、文学、个人随笔等多种类型。使用深度路由系统自动匹配写作规范，支持跨平台分发。Use when creating blog posts, personal essays, technical articles, artistic content, or when user mentions writing, content creation, 博客, 写作.
license: MIT
metadata:
  version: 5.1.0
  author: Clement Chen
  category: writing
  updated: 2026-02-27
  python-tools: brand_voice_analyzer.py, seo_optimizer.py
  languages: English, 中文
  framework: OpenCode Native Task Architecture
---

# Content Creator (OpenCode Native Workspace)

以博客为核心的内容创作系统，支持技术、艺术、设计、文学、个人随笔等多种类型。通过 OpenCode 原生的 `Task(Category + Skills)` 架构，实现高度模块化、高效并行、支持双语（中英）的内容创作、多平台分发以及本地内容审查。

## 🎯 核心工作流 (SOP)

本工作空间由一组内置命令驱动（定义在 `.opencode/commands/` 中），请直接使用以下指令来启动特定工作流：

1. **策划：** 使用 `/brainstorm <主题>` 调研主题。
2. **起草：** 使用 `/draft` 基于大纲撰写核心博客 (Core Blog)。
3. **补图：** 使用 `/enrich` 丰富博客的插图与可视化图表（可选）。
4. **校验：** **强制**使用 `/audit <文件>` 调用本地技能目录下的脚本 进行语调与 SEO 校验。
5. **分发：** 使用 `/repurpose <文件>` 将核心博客裂变为多平台文案。

## 代理调度规则

- 凡是涉及资料搜集与大纲生成的任务，必须挂载内置技能 `content-research-writer`。
- 凡是涉及 SEO 优化的任务，必须挂载内置技能 `SEO Optimizer`。
- 凡是涉及平台分发的改写，必须使用 `task(category="writing", load_skills=["platform-social-<platform>"], run_in_background=true)` 进行**并发处理**。

---

## 🧩 技能路由系统 (Skill Routing System)

所有特定格式、语调和要求都已模块化并存放在 `.opencode/skills/` 目录中。系统会根据指令动态注入以下技能：

### 1. 核心内容语调 (Core Voices)
- `voice-blog`: 标准长文博客
- `voice-social`: 社交媒体短图文
- `voice-weekly`: 新闻信与周刊

### 2. 领域上下文 (Domain Contexts)
*用于决定文章的深度、专业性或感性维度*
- `domain-technical`: 技术（事实驱动、代码、架构）
- `domain-artistic`: 艺术（摄影、音乐等，偏向感性、非 marketing）
- `domain-design`: 设计（UI/UX、美学讨论）
- `domain-literary`: 文学（散文、评论）
- `domain-personal`: 个人（生活观察、吐槽、随想）**最不需要遵循「去 AI 味」规则的类型，主打真实情绪。**

### 3. 分发平台格式 (Platform Formats)
*用于决定最终输出的排版和特征*
- 社交媒体：`platform-social` (统一处理小红书、推特、微博等), `platform-social-wechat` / `platform-social-linkedin` (可直接复用原文或微调)
- 音视频：`platform-video` (统一处理 B站、YouTube、TikTok 等), `platform-audio-podcast`
- 图片技能：`skill-image-enrichment` (博客插图与 Mermaid 占位符)
- 辅助技能：`skill-seo` (中文/英文双语 SEO 优化指南)

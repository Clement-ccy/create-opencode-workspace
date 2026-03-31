---
name: platform-video
description: 视频内容生产管线规范——从文档到视频的完整流程
metadata:
  version: 3.0.0
  updated: 2026-03-30
---

# 视频内容生产管线规范

本技能定义从源文档到最终视频的完整自动化管线，包括脚本撰写、HTML 动态 PPT 生成、TTS 音频合成、帧渲染和视频编译。

---

## 适用平台

- 长视频：Bilibili (B站)、YouTube
- 短视频：TikTok、抖音、视频号

---

## 管线流程总览

```
源文档 → JSON 脚本 → HTML PPT → TTS 音频 → Playwright 渲染 → FFmpeg 合成
```

### 阶段 1: 文档理解与脚本生成

从源文档提取核心信息，生成结构化的 JSON 脚本（recipe.json）。

### 阶段 2: HTML 动态 PPT 制作

将 JSON 脚本转化为带 CSS 动画的 HTML 幻灯片。

### 阶段 3: TTS 语音合成

为每页幻灯片生成对应音频（使用 edge-tts）。

### 阶段 4: 渲染与合成

用 Playwright 截取每页帧画面，用 FFmpeg 将帧+音频合成最终视频。

---

## JSON 脚本格式 (recipe.json)

LLM 必须输出符合以下 schema 的 JSON 文件，Python 脚本会消费此 JSON：

```json
{
  "title": "视频标题",
  "description": "视频简介，用于平台发布",
  "tags": ["标签1", "标签2"],
  "language": "zh-CN",
  "total_duration_estimate": 180,
  "slides": [
    {
      "id": 1,
      "type": "title",
      "text": "开场标题文字",
      "narration": "开场旁白文本",
      "visual_note": "画面描述，用于生成 PPT 时参考",
      "animation": "fadeIn",
      "duration_hint": 5
    },
    {
      "id": 2,
      "type": "content",
      "title": "本页标题",
      "bullets": ["要点 1", "要点 2", "要点 3"],
      "narration": "旁白文本，逐条讲解要点",
      "visual_note": "图表/示意图描述",
      "animation": "slideLeft",
      "duration_hint": 15
    },
    {
      "id": 3,
      "type": "quote",
      "text": "引用的文字内容",
      "attribution": "出处",
      "narration": "旁白文本",
      "animation": "fadeIn",
      "duration_hint": 8
    },
    {
      "id": 4,
      "type": "code",
      "language": "python",
      "code": "print('Hello World')",
      "explanation": "代码解释旁白",
      "animation": "typewriter",
      "duration_hint": 12
    },
    {
      "id": 5,
      "type": "closing",
      "text": "结束语/CTA",
      "narration": "结尾旁白",
      "animation": "fadeIn",
      "duration_hint": 5
    }
  ]
}
```

### Slide 类型定义

| type | 用途 | 必填字段 |
|------|------|---------|
| `title` | 视频开场标题 | text, narration |
| `content` | 内容页（要点列表） | title, bullets, narration |
| `quote` | 引用/金句页 | text, narration |
| `code` | 代码展示页 | code, language, narration |
| `image` | 图片展示页 | image_url, caption, narration |
| `closing` | 结束页 | text, narration |

### Animation 支持

| animation | 效果 |
|-----------|------|
| `fadeIn` | 淡入 |
| `slideLeft` | 从左滑入 |
| `slideRight` | 从右滑入 |
| `slideUp` | 从下滑入 |
| `typewriter` | 逐字打出 |
| `zoomIn` | 缩放进入 |
| `none` | 无动画 |

---

## HTML PPT 规范

HTML 幻灯片必须满足以下要求：

### 基本结构

```html
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <style>
    /* 全局样式 */
    .slide {
      width: 1920px;
      height: 1080px;
      position: absolute;
      top: 0;
      left: 0;
      display: flex;
      align-items: center;
      justify-content: center;
      opacity: 0;
    }
    .slide.active { opacity: 1; }
    
    /* 动画定义 */
    @keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }
    @keyframes slideLeft { from { transform: translateX(100px); opacity: 0; } }
    @keyframes typewriter { from { width: 0; } }
  </style>
</head>
<body>
  <div class="slide" id="slide-1">...</div>
  <div class="slide" id="slide-2">...</div>
</body>
</html>
```

### 设计要求

| 规则 | 说明 |
|------|------|
| 分辨率 | 1920×1080 (16:9) |
| 字体 | 中文：思源黑体/Noto Sans CJK；英文：Inter/Roboto |
| 配色 | 遵循文章主题或使用默认深色主题 |
| 动画 | 使用 CSS `@keyframes`，每页独立触发动画 |
| 编码 | UTF-8 |
| 中文 | 必须设置 `lang="zh-CN"` 和合适的字体 fallback |

---

## Python 脚本调用规范

在执行视频管线时，按以下顺序调用 Python 脚本：

```bash
# 1. 校验 recipe.json
python scripts/video_pipeline/validate_recipe.py Assets/Video/[name]/recipe.json

# 2. 生成 HTML PPT
python scripts/video_pipeline/generate_ppt.py Assets/Video/[name]/recipe.json Assets/Video/[name]/slides/

# 3. 生成 TTS 音频
python scripts/video_pipeline/generate_tts.py Assets/Video/[name]/recipe.json Assets/Video/[name]/audio/

# 4. 渲染帧
python scripts/video_pipeline/render_slides.py Assets/Video/[name]/slides/ Assets/Video/[name]/frames/

# 5. 合成视频
python scripts/video_pipeline/compile_video.py Assets/Video/[name]/recipe.json Assets/Video/[name]/ [name].mp4
```

---

## 转化原则

1. **听觉友好**：视频是听的，把书面语改为口语化表达
2. **结构重组**：黄金 3 秒原则，最吸引人的内容放在最前面
3. **视觉提示**：每页幻灯片必须有清晰的视觉焦点
4. **节奏控制**：每页幻灯片根据内容复杂度设定 duration_hint

---

## 输出文件结构

```
Assets/Video/[name]/
├── recipe.json              # 结构化脚本
├── slides/                  # HTML 幻灯片文件
│   ├── slide-01.html
│   ├── slide-02.html
│   └── ...
├── audio/                   # TTS 音频文件
│   ├── slide-01.mp3
│   ├── slide-02.mp3
│   └── ...
├── frames/                  # 渲染的帧画面
│   ├── frame-01.png
│   ├── frame-02.png
│   └── ...
└── [name].mp4               # 最终视频
```

---

## 注意事项

- **时长控制**：
  - 短视频（TikTok/抖音/视频号）：30-60 秒（3-5 页幻灯片）
  - 长视频（B站/YouTube）：3-10 分钟（8-20 页幻灯片）
- LLM 不直接运行 FFmpeg 命令，只生成 `recipe.json`
- Python 脚本需要安装依赖：`edge-tts`、`playwright`、`ffmpeg-python`
- Playwright 需要预装 Chromium：`playwright install chromium`

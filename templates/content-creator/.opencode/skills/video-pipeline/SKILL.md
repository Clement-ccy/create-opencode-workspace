---
name: video-pipeline
description: 视频内容生产管线——从 JSON 脚本到 HTML PPT 渲染的完整 Python 自动化流程
metadata:
  version: 1.0.0
  updated: 2026-03-30
---

# Video Pipeline — 视频生产自动化管线

本 skill 定义视频生产的完整 Python 自动化管线，将 `platform-video` 生成的 JSON 脚本转化为最终视频。

---

## 管线架构

```
recipe.json → validate → generate_ppt → render_slides → generate_tts → compile_video → .mp4
```

### 各阶段说明

| 阶段 | 脚本 | 输入 | 输出 |
|------|------|------|------|
| 校验 | `validate_recipe.py` | recipe.json | 校验结果 (JSON) |
| PPT 生成 | `generate_ppt.py` | recipe.json | slides/*.html |
| 帧渲染 | `render_slides.py` | slides/*.html | frames/*.png |
| TTS 合成 | `generate_tts.py` | recipe.json | audio/*.mp3 |
| 视频合成 | `compile_video.py` | recipe.json + frames + audio | [name].mp4 |

---

## 调用方式

### 完整管线

```bash
cd scripts/video_pipeline

# 1. 校验脚本
python validate_recipe.py ../../Assets/Video/[name]/recipe.json

# 2. 生成 HTML PPT
python generate_ppt.py ../../Assets/Video/[name]/recipe.json ../../Assets/Video/[name]/slides/

# 3. 生成 TTS 音频
python generate_tts.py ../../Assets/Video/[name]/recipe.json ../../Assets/Video/[name]/audio/

# 4. 渲染帧
python render_slides.py ../../Assets/Video/[name]/slides/ ../../Assets/Video/[name]/frames/

# 5. 合成视频
python compile_video.py ../../Assets/Video/[name]/recipe.json ../../Assets/Video/[name]/ [name].mp4
```

### 单步执行

```bash
# 仅生成 PPT
python generate_ppt.py [recipe.json] [output_dir]

# 仅生成 TTS
python generate_tts.py [recipe.json] [output_dir]

# 仅渲染帧
python render_slides.py [slides_dir] [frames_dir]

# 仅合成视频
python compile_video.py [recipe.json] [assets_dir] [output.mp4]
```

---

## 依赖

```bash
pip install -r scripts/video_pipeline/requirements.txt
playwright install chromium
```

### 依赖清单

| 包 | 用途 |
|----|------|
| `edge-tts` | TTS 语音合成（免费、Neural 音质、中文支持） |
| `playwright` | 无头浏览器，渲染 HTML 幻灯片为帧画面 |
| `ffmpeg-python` | 视频合成（音频+帧拼接） |
| `Pillow` | 图像处理 |

---

## HTML PPT 生成规范

`generate_ppt.py` 根据 `recipe.json` 的 `slides` 数组为每页生成一个 HTML 文件。

### 每页 HTML 结构

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body {
      width: 1920px;
      height: 1080px;
      display: flex;
      align-items: center;
      justify-content: center;
      font-family: 'Noto Sans SC', 'Inter', sans-serif;
      background: #1a1a2e;
      color: #eee;
    }
    .content { max-width: 1400px; text-align: center; }
    .title { font-size: 72px; font-weight: 700; margin-bottom: 40px; }
    .subtitle { font-size: 36px; opacity: 0.8; }
    .bullet { font-size: 32px; margin: 20px 0; text-align: left; }
    .quote { font-size: 42px; font-style: italic; }
    .code {
      background: #16213e;
      padding: 30px;
      border-radius: 12px;
      font-family: 'Fira Code', monospace;
      font-size: 28px;
      text-align: left;
    }
    /* 动画 */
    @keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }
    @keyframes slideLeft {
      from { transform: translateX(100px); opacity: 0; }
      to { transform: translateX(0); opacity: 1; }
    }
    @keyframes typewriter { from { width: 0; } to { width: 100%; } }
    .animate { animation: fadeIn 0.8s ease-in-out forwards; }
  </style>
</head>
<body>
  <div class="content animate">
    <!-- 根据 slide type 插入不同内容 -->
  </div>
</body>
</html>
```

### Slide 类型 → HTML 模板

| type | 模板 |
|------|------|
| `title` | `<h1 class="title">{text}</h1><p class="subtitle">{visual_note}</p>` |
| `content` | `<h2>{title}</h2>` + `{bullets}` 每个 `<div class="bullet">• {bullet}</div>` |
| `quote` | `<blockquote class="quote">"{text}"</blockquote><cite>— {attribution}</cite>` |
| `code` | `<pre class="code"><code>{code}</code></pre>` |
| `closing` | `<h1 class="title">{text}</h1>` |

---

## TTS 合成规范

`generate_tts.py` 为每页 slide 生成一个 `.mp3` 文件。

### 规则

- 使用 `edge-tts` 的 Neural 语音
- 中文：`zh-CN-XiaoxiaoNeural`（女声）或 `zh-CN-YunxiNeural`（男声）
- 英文：`en-US-JennyNeural`（女声）或 `en-US-GuyNeural`（男声）
- 语速：`+0%`（默认）
- 输出：`slide-{id}.mp3`

---

## 帧渲染规范

`render_slides.py` 使用 Playwright 无头 Chromium 渲染 HTML 幻灯片为 PNG 帧。

### 规则

- 分辨率：1920×1080
- 截图时机：等待 CSS 动画播放完毕（1 秒等待）
- 输出：`frame-{id}.png`

---

## 视频合成规范

`compile_video.py` 使用 FFmpeg 将帧画面和音频合成为最终视频。

### 合成逻辑

1. 读取 `recipe.json` 中每个 slide 的 `duration_hint`
2. 将对应的帧画面显示时长设为对应音频的时长（或 duration_hint）
3. 使用 `concat` filter 将所有帧+音频拼接
4. 输出 H.264 编码的 MP4，分辨率 1920×1080，帧率 30fps

### FFmpeg 命令参考

```bash
ffmpeg -framerate 30 -i frames/frame-%02d.png -i audio/slide-%02d.mp3 \
       -c:v libx264 -pix_fmt yuv420p -c:a aac \
       output.mp4
```

---

## Dry Run 模式

所有脚本支持 `--dry-run` 参数，只输出将执行的操作而不实际执行：

```bash
python generate_ppt.py recipe.json slides/ --dry-run
python generate_tts.py recipe.json audio/ --dry-run
python render_slides.py slides/ frames/ --dry-run
python compile_video.py recipe.json assets/ output.mp4 --dry-run
```

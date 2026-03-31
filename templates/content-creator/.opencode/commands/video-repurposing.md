# Video Repurposing Command (`/video-repurposing`)

**Description**: 视频制作管线——从源文档到最终视频的完整自动化流程。

## 使用方式

```
/video-repurposing <源文档路径> [语言]
```

- `<源文档路径>`：必填，源内容文件路径（博客文章、周间、笔记等）
- `[语言]`：可选，指定视频语言（zh-CN / en），默认中文

## Orchestration Flow

### Phase 1: 文档理解与脚本生成

1. **读取源文档**：加载用户指定的源内容文件
2. **加载 Skills**：`platform-video` + `voice-optimization`
3. **生成 JSON 脚本**：
   - 启动 `writing` 类别任务
   - 根据 `platform-video` skill 的 JSON schema 生成 `recipe.json`
   - 确定视频长度（短视频 3-5 页 / 长视频 8-20 页）
   - 输出文件到 `Assets/[category]/[name]/video/recipe.json`

### Phase 2: HTML PPT 生成

1. **加载 Skills**：`platform-video`
2. **生成幻灯片**：
   - 启动 `writing` 类别任务
   - 根据 `recipe.json` 的每页内容生成 HTML 幻灯片
   - 每页一个独立 HTML 文件，包含 CSS 动画
   - 分辨率 1920×1080，支持中文渲染
   - 输出到 `Assets/[category]/[name]/video/slides/`

### Phase 3: TTS 音频合成

1. **执行脚本**：
   ```bash
   python scripts/video_pipeline/generate_tts.py Assets/[category]/[name]/video/recipe.json Assets/[category]/[name]/audio/
   ```
2. **验证输出**：确保每页幻灯片都有对应的音频文件

### Phase 4: 帧渲染

1. **执行脚本**：
   ```bash
   python scripts/video_pipeline/render_slides.py Assets/[category]/[name]/video/slides/ Assets/[category]/[name]/video/frames/
   ```
2. **验证输出**：确保帧画面数量与幻灯片数量匹配

### Phase 5: 视频合成

1. **执行脚本**：
   ```bash
   python scripts/video_pipeline/compile_video.py Assets/[category]/[name]/video/recipe.json Assets/[category]/[name]/video/ [name].mp4
   ```
2. **验证输出**：生成的 MP4 文件大小和时长是否合理

### Phase 6: Finalize

1. 确认最终视频文件在 `Assets/[category]/[name]/video/[name].mp4`
2. 生成平台发布文案（标题 + 简介 + 标签）
3. 向用户展示成品

## 输出结构

```
Assets/[category]/[name]/video/
├── recipe.json              # 结构化脚本
├── slides/                  # HTML 幻灯片
│   ├── slide-01.html
│   ├── slide-02.html
│   └── ...
├── audio/                   # TTS 音频
│   ├── slide-01.mp3
│   ├── slide-02.mp3
│   └── ...
├── frames/                  # 渲染的帧画面
│   ├── frame-01.png
│   ├── frame-02.png
│   └── ...
├── [name].mp4               # 最终视频
└── release_note.md          # 平台发布文案
```

## 前置依赖

执行前请确保已安装 Python 依赖：

```bash
pip install -r scripts/video_pipeline/requirements.txt
playwright install chromium
```

## 时长控制

| 视频类型 | 幻灯片数量 | 时长 |
|---------|-----------|------|
| 短视频 | 3-5 页 | 30-60 秒 |
| 中等 | 6-10 页 | 1-3 分钟 |
| 长视频 | 8-20 页 | 3-10 分钟 |

## Skills 路由

| 阶段 | Skills 组合 |
|------|-----------|
| 脚本生成 | `platform-video` + `voice-optimization` + `type-social` |
| PPT 生成 | `platform-video` |
| 最终审查 | `platform-video` |

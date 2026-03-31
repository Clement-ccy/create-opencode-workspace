# Mlog Writing Command (`/mlog-writing`)

**Description**: 音乐日志（Music Log）写作流程——记录编曲过程、翻唱录制、音乐制作、专辑感受等音乐相关内容。

## 使用方式

```
/mlog-writing <题材> [资料路径]
```

- `<题材>`：必填，音乐主题（如 "《XXX》翻唱记录"、"新编曲实验：Lo-Fi Beat 制作"、"最近在听的 Jazz Fusion"）
- `[资料路径]`：可选，用户的制作笔记/DAW 项目截图/音频片段描述

## Orchestration Flow

### Phase 1: 理解与调研

1. **理解请求**：
   - 确定类型：编曲记录 / 翻唱记录 / 制作笔记 / 专辑/歌曲感受 / 音乐探索
   - 确定音乐风格：电子/摇滚/爵士/古典/民谣/嘻哈/实验...
2. **补充背景**：
   - 如果是编曲/制作类：了解用户的 DAW 工具、音色风格、技术细节
   - 如果是翻唱类：了解原曲背景、改编方向
   - 如果是感受类：启动 `librarian` agent 搜集作品/艺人信息

### Phase 2: 撰写

1. **加载 Skills**：`type-blog` + `domain-artistic` + `voice-optimization` + `frontmatter-notion-property`
2. **执行写作**：
   - 启动 `writing` 类别任务
   - 输出风格：
     - 编曲/制作类 → 技术感受混合，记录创作思路和遇到的问题
     - 翻唱类 → 个人化叙述，为什么选这首歌，改编的心路历程
     - 感受类 → 感性表达，允许主观和碎片化
   - 允许使用音乐术语，但要解释给非专业读者

### Phase 3: 补充与审查

1. **视觉补充**：
   - 插入 DAW 界面截图/波形图的 `<!-- IMAGE: -->` 占位符
   - 如果有音频片段，标注播放链接
2. **语调审查**：
   ```bash
   python .opencode/skills/voice-optimization/scripts/brand_voice_analyzer.py <file-path> artistic
   ```

### Phase 4: Finalize

1. 保存到 `Assets/Mlogs/[name]/[name].md`
2. 向用户展示成品

## 输出结构

```
Assets/Mlogs/[name]/
├── [name].md              # 最终音乐日志
├── media/                 # DAW 截图/封面/音频文件/歌词文件
└── distributions/         # 分发版本（如果后续执行）
```

## Mlog 写作风格

| 原则 | 说明 |
|------|------|
| 过程导向 | 记录「怎么做的」和「为什么这么做」，不只是结果 |
| 技术感受混合 | 可以聊压缩比、EQ 设置，但也要写感受 |
| 允许不完美 | 编曲失败、翻唱翻车都是好素材 |
| 音乐链接 | 尽量附上相关歌曲的播放链接 |
| 声音画面 | 用文字描述声音的质感（"薄如蝉翼的 pad"、"厚实的 808"） |

## 内容结构参考

### 编曲/制作记录
```markdown
# [项目名称] — [一句话概括]

## 起因
[为什么开始做这个]

## 制作过程
[DAW 工具、音色选择、遇到的问题、解决方案]

## 成果/未完成
[最终效果描述，或「还没做完但想先记下来」]

## 下一步
[接下来想改进的地方]
```

### 翻唱记录
```markdown
# [歌曲名] 翻唱 — [改编方向]

## 为什么选这首歌
[个人关联/被什么打动]

## 改编思路
[和原版的区别、保留什么、改变什么]

## 录制过程
[录音设备/环境、录了几次、哪里卡住了]

[成品链接/试听]
```

## Skills 路由

| 类型 | Skills 组合 |
|------|-----------|
| 编曲/制作记录 | `type-blog` + `domain-artistic` + `voice-optimization` |
| 翻唱记录 | `type-blog` + `domain-artistic` + `voice-optimization` |
| 专辑/歌曲感受 | `type-blog` + `domain-artistic` + `voice-optimization` |
| 音乐探索/推荐 | `type-blog` + `domain-artistic` + `voice-optimization` |

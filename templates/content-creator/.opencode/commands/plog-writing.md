# Plog Writing Command (`/plog-writing`)

**Description**: 摄影日志（Photography Log）写作流程——记录摄影作品的拍摄过程、后期思路、摄影经历和器材体验。

## 使用方式

```
/plog-writing <题材> [资料路径]
```

- `<题材>`：必填，摄影主题（如 "周末城市街拍"、"富士 XT-5 使用一个月感受"、"海边日落拍摄笔记"）
- `[资料路径]`：可选，用户的拍摄笔记/EXIF 信息/照片描述

## Orchestration Flow

### Phase 1: 理解

1. **理解请求**：
   - 确定类型：作品集记录 / 拍摄过程 / 后期思路 / 器材体验 / 摄影感悟
   - 确定拍摄题材：风光/人文/人像/街拍/微距/黑白/胶片...
2. **补充背景**：
   - 如果用户提供了照片描述/EXIF：作为核心素材
   - 如果是器材类：启动 `librarian` agent 搜集器材参数和竞品信息

### Phase 2: 撰写

1. **加载 Skills**：`type-blog` + `domain-artistic` + `voice-optimization` + `frontmatter-notion-property`
2. **执行写作**：
   - 启动 `writing` 类别任务
   - 输出风格：
     - 作品记录 → 以图为中心，文字辅助说明拍摄思路
     - 拍摄过程 → 叙事性，记录等待光线/寻找机位的过程
     - 后期思路 → 技术分享，但要讲清楚「为什么这样调」
     - 器材体验 → 真实使用感受，不要写成评测
   - 注重「视觉感受的文字化」

### Phase 3: 补充与审查

1. **视觉补充**：
   - 插入照片的 `<!-- IMAGE: -->` 占位符（这是摄影日志的核心）
   - 每张照片附：标题、拍摄参数（可选）、拍摄故事
2. **语调审查**：
   ```bash
   python .opencode/skills/voice-optimization/scripts/brand_voice_analyzer.py <file-path> artistic
   ```

### Phase 4: Finalize

1. 保存到 `Assets/Plogs/[name]/[name].md`
2. 向用户展示成品

## 输出结构

```
Assets/Plogs/[name]/
├── [name].md              # 最终摄影日志
├── media/                 # 照片文件
└── distributions/         # 分发版本（如果后续执行）
```

## Plog 写作风格

| 原则 | 说明 |
|------|------|
| 以图为主 | 文字是照片的延伸，不是主角 |
| 场景感 | 描述拍摄时的环境、光线、天气、心情 |
| 参数可选 | 不必每张都写 EXIF，重要照片才标注 |
| 后期坦诚 | 如实说明后期调整，不要假装直出 |
| 允许感性 | 摄影是视觉艺术，允许诗意和留白 |
| 器材聊使用 | 器材体验聊「用起来怎么样」，不聊参数表 |

## 内容结构参考

### 作品集记录
```markdown
# [系列名称/拍摄主题]

## 背景
[什么时候拍的、在哪里、为什么拍]

## 作品

<!-- IMAGE: 标题: XXX / 类型: 风光照片 / 内容: 描述 -->
[拍摄故事或思路]

<!-- IMAGE: 标题: XXX / 类型: 人像照片 / 内容: 描述 -->
[拍摄故事或思路]

## 后记
[拍完之后的感受，不需要总结]
```

### 拍摄过程
```markdown
# [拍摄主题] — [一句话]

## 出发
[为什么想去拍、做了什么准备]

## 等待与捕捉
[到了现场、光线变化、等待的过程、按下快门的瞬间]

## 后期
[调色思路、为什么这样处理]

[成品照片]
```

### 器材体验
```markdown
# [器材名称] 使用 [时间] 的感受

## 入手原因
[为什么买它]

## 日常使用
[带出去拍了什么、手感如何]

## 优点/槽点
[真实的使用感受]

## 样张
<!-- IMAGE: ... -->
```

## Skills 路由

| 类型 | Skills 组合 |
|------|-----------|
| 作品集/拍摄记录 | `type-blog` + `domain-artistic` + `voice-optimization` |
| 拍摄过程 | `type-blog` + `domain-artistic` + `voice-optimization` |
| 后期思路 | `type-blog` + `domain-artistic` + `voice-optimization` |
| 器材体验 | `type-blog` + `domain-artistic` + `voice-optimization` |

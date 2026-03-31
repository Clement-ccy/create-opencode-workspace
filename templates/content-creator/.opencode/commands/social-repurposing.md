# Social Repurposing Command (`/social-repurposing`)

**Description**: 多平台社交分发——将长文内容并行转化为 Twitter/X、微信公众号、知乎、CSDN、小红书 的最佳发布格式。

## 使用方式

```
/social-repurposing <源文档路径> [平台列表]
```

- `<源文档路径>`：必填，源内容文件路径
- `[平台列表]`：可选，逗号分隔的目标平台（twitter,wechat,zhihu,csdn,xiaohongshu），默认全部

## Orchestration Flow

### Phase 1: 理解请求

1. **读取源文档**：加载用户指定的源内容文件
2. **确定目标平台**：
   - 如果用户指定了平台列表，仅生成对应平台
   - 如果未指定，默认生成全部 5 个平台
3. **确定语言**：根据源文档语言自动判断，或用户指定

### Phase 2: 并行分发（核心）

为每个目标平台启动一个独立的 `quick` 类别任务，**全部并行执行**：

**Twitter/X**:
```typescript
task(
  category="quick",
  load_skills=["platform-social", "voice-optimization", "frontmatter-notion-property"],
  prompt="将以下内容转化为 Twitter Thread 格式，每条推文不超过 280 字符，控制在 5-12 条。输出保存到 Assets/[Category]/[name]/distributions/twitter/[name]_twitter.md"
)
```

**微信公众号**:
```typescript
task(
  category="quick",
  load_skills=["platform-text", "voice-optimization", "frontmatter-notion-property"],
  prompt="将以下内容适配到微信公众号格式，段落不超过 3 行（移动端），使用引用块突出关键信息。输出保存到 Assets/[Category]/[name]/distributions/wechat/[name]_wechat.md"
)
```

**知乎**:
```typescript
task(
  category="quick",
  load_skills=["platform-text", "voice-optimization", "frontmatter-notion-property"],
  prompt="将以下内容适配到知乎格式，使用编号小标题便于跳读，保持深度分析风格。输出保存到 Assets/[Category]/[name]/distributions/zhihu/[name]_zhihu.md"
)
```

**CSDN**:
```typescript
task(
  category="quick",
  load_skills=["platform-text", "voice-optimization", "frontmatter-notion-property"],
  prompt="将以下内容适配到 CSDN 技术博客格式，保持完整代码块，添加技术标签。输出保存到 Assets/[Category]/[name]/distributions/csdn/[name]_csdn.md"
)
```

**小红书**:
```typescript
task(
  category="quick",
  load_skills=["platform-social", "voice-optimization", "frontmatter-notion-property"],
  prompt="将以下内容适配到小红书格式，使用 Emoji 做视觉引导，每个要点一行，300-800 字。输出保存到 Assets/[Category]/[name]/distributions/xiaohongshu/[name]_xiaohongshu.md"
)
```

### Phase 3: 等待并汇总

1. 等待所有并行任务完成
2. 检查每个平台的输出质量
3. 如果某个平台的输出有问题，单独重试

### Phase 4: Finalize

1. 向用户展示所有平台的分发版本
2. 提供每个版本的文件路径

## 输出结构

```
Assets/[Category]/[name]/distributions/
├── twitter/[name]_twitter.md
├── wechat/[name]_wechat.md
├── zhihu/[name]_zhihu.md
├── csdn/[name]_csdn.md
└── xiaohongshu/[name]_xiaohongshu.md
```

## 平台特性速查

| 平台 | 字数 | 配图 | 语调 | 标签 |
|------|------|------|------|------|
| Twitter/X | 280字/条 | 可选 | 轻快/锐利 | 1-3个 # |
| 微信公众号 | 1500-3000字 | 3-6张 | 深度/个人化 | 无 |
| 知乎 | 2000-5000字 | 可选截图 | 专业/逻辑 | 3-5个话题 |
| CSDN | 1000-4000字 | 代码截图 | 专业/教程 | 3-5个技术标签 |
| 小红书 | 300-800字 | 封面+内页图 (3:4) | 感性/亲切 | 5-10个 # |

## Skills 路由

| 平台 | Skills 组合 |
|------|-----------|
| Twitter/X | `platform-social` + `voice-optimization` |
| 微信公众号 | `platform-text` + `voice-optimization` |
| 知乎 | `platform-text` + `voice-optimization` |
| CSDN | `platform-text` + `voice-optimization` |
| 小红书 | `platform-social` + `voice-optimization` |

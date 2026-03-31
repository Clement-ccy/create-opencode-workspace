# Blog Writing Command (`/blog-writing`)

**Description**: 完整的博客写作流程——从主题调研到最终发布，包含 brainstorm → draft → enrich → audit 全部步骤。

## 使用方式

```
/blog-writing <题材> [资料路径]
```

- `<题材>`：必填，写作的主题或关键词
- `[资料路径]`：可选，用户提供的参考资料/源文档路径

## Orchestration Flow

### Phase 1: Brainstorm（调研与提纲）

1. **理解请求**：解析用户输入的题材和参考资料。
2. **确定路由**：
   - 领域 (Domain)：根据题材判断 → `domain-tech` / `domain-artistic` / `domain-design` / `domain-literary` / `domain-personal`
   - 语言：用户指定或默认中文
3. **执行调研**：
   - 启动 `deep` 类别任务，加载 `content-research-writer` skill
   - 并行启动 `librarian` agent 搜集外部资料（如果涉及技术/外部资源密集型主题）
   - 生成 5 个标题 Hook + 完整提纲

### Phase 2: Draft（撰写正文）

1. **加载 Skills**：`type-blog` + `voice-optimization` + 对应领域 skill + `frontmatter-notion-property` + `seo-optimization`
2. **执行写作**：
   - 启动 `writing` 类别任务
   - 明确指定：主题、语言、领域、输出路径
   - 确保包含 Notion frontmatter

### Phase 3: Enrich（视觉补充）

1. **加载 Skills**：`image-enrichment`
2. **执行补充**：
   - 启动 `writing` 类别任务
   - 在适当位置插入 `<!-- IMAGE: ... -->` 占位符
   - 添加 Mermaid 图表（如果适用）

### Phase 4: Audit（SEO/语调审查）

1. **SEO 审查**：
   ```bash
   python .opencode/skills/seo-optimization/scripts/seo_optimizer.py <file-path> "核心关键词" "长尾词1,长尾词2"
   ```
2. **品牌语调审查**：
   ```bash
   python .opencode/skills/voice-optimization/scripts/brand_voice_analyzer.py <file-path> <domain>
   ```
3. **处理结果**：
   - 如果分数 ≥ 85：直接通过
   - 如果分数 70-84：根据建议做微调
   - 如果分数 < 70：根据建议进行修改后重新审计

### Phase 5: Finalize（完成输出）

1. 将最终版本保存到 `Assets/Blogs/[name]/[name].md`
2. 向用户展示成品
3. 询问是否需要：
   - `/social-repurposing`：多平台分发
   - `/video-repurposing`：制作视频版本

## 输出结构

```
Assets/Blogs/[name]/
├── [name].md              # 最终博客文章（含 Notion frontmatter）
├── media/                 # 图片/媒体资源
└── distributions/         # 社交/视频分发（如果后续执行）
```

## Skills 路由参考

| 输入 | Skills 组合 |
|------|-----------|
| 技术主题 | `type-blog` + `domain-tech` + `voice-optimization` + `seo-optimization` |
| 艺术/摄影 | `type-blog` + `domain-artistic` + `voice-optimization` |
| 设计类 | `type-blog` + `domain-design` + `voice-optimization` + `seo-optimization` |
| 个人随笔 | `type-blog` + `domain-personal` + `voice-optimization` |

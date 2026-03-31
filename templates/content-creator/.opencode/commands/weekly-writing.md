# Weekly Writing Command (`/weekly-writing`)

**Description**: 周刊写作完整流程——从选题搜集到条目撰写，生成符合模板结构的周刊文章。

## 使用方式

```
/weekly-writing <题材> [资料路径]
```

- `<题材>`：必填，周刊主题（如 "AI 周刊"、"科技资讯"）
- `[资料路径]`：可选，用户提供的资讯/链接集合

## Orchestration Flow

### Phase 1: 选题筛选

1. **理解请求**：解析周刊主题、条目数量目标（8-12 条为宜）。
2. **搜集资料**：
   - 启动 `librarian` agent 搜集本周热点，并抓取热点内图片，如果没有进行截图，如果有视频可以截出一定帧数作为 .gif 动图
   - 如果用户提供了资料路径，直接读取并分析
3. **筛选排序**：
   - 按重要性排序，选择 8-12 条条目
   - 为每条条目确定栏目归属（要闻/开发生态/行业动态 等）
   - 确定每条的 `#N` 编号

### Phase 2: 撰写周刊

1. **加载 Skills**：`type-weekly` + `voice-optimization` + `frontmatter-notion-property`
2. **执行写作**：
   - 启动 `writing` 类别任务
   - 严格遵循 `type-weekly` 的模板结构：

### Phase 3: 审查

1. **品牌语调审查**：
   ```bash
   python .opencode/skills/voice-optimization/scripts/brand_voice_analyzer.py <file-path> weekly
   ```
2. **去 AI 味检查**：
   - 检查是否有「值得注意的是」「此外」等填充词
   - 确保长短句混合、节奏变化
3. **结构检查**：
   - Frontmatter 字段是否完整
   - 本期要点编号与正文 `#N` 是否对应
   - 每个条目是否有 blockquote 摘要

### Phase 4: Finalize

1. 保存到 `Assets/Weeklys/[name]/[name].md`
2. 将搜集到的图片保存到 `Assets/Weeklys/[name]/` 目录
3. 向用户展示成品
4. 询问是否需要分发到其他平台

## 输出结构

```
Assets/Weeklys/[name]/
├── [name].md              # 最终周刊文章
├── image.png              # 搜集到的图片
├── image-1.png
└── distributions/         # 分发版本（如果后续执行）
```

## Skills 路由

| 输入 | Skills 组合 |
|------|-----------|
| 科技/AI 周刊 | `type-weekly` + `domain-tech` + `voice-optimization` |
| 艺术/文化资讯 | `type-weekly` + `domain-artistic` + `voice-optimization` |
| 通用资讯 | `type-weekly` + `voice-optimization` |

---
name: skill-seo
description: 博客/文章的 SEO 优化指南与流程，包含关键词策略、排版结构和技术要求。中英通用。
metadata:
  version: 2.0.0
  updated: 2026-02-26
---

# SEO Optimization Guide (SEO 优化指南)

## Overview (概述)

本指南提供全面的内容创作 SEO 优化策略，中英文通用。无论语言是什么，SEO 的核心逻辑（搜索意图、结构化、关键词自然融入）是一致的。
This guide provides comprehensive SEO optimization strategies for content creation, applicable to both Chinese and English content.

## Quick Reference (快速参考)

| Metric (指标) | Target Range (英文/English) | Target Range (中文/Chinese) |
|--------|-------------|-------------|
| Title Length (标题) | 50-60 chars | ≤ 30 汉字 |
| Meta Description (描述) | 150-160 chars | 80-120 汉字 |
| URL Slug (链接路径) | 50-60 chars (lowercase, hyphens) | 尽量使用英文翻译或拼音拼写，使用短横线 |
| Keyword Density (关键词密度)| 1-3% | 2-8% |
| Content Length (正文长度) | 1,500-1,000,000 words | 800-1,000,000 字 |

---

## 1. 写作实操流程与关键词策略 (SEO Workflow & Strategy)

在动笔之前，必须明确「为谁写」以及「由于什么词被找到」。

### 关键词研究核心逻辑 (Keyword Strategy)
- **核心词 (Focus Keyword)**：文章的主题词，全篇只专注 1 个核心词，必须放在标题开头。
- **长尾词 (Long-tail Keywords)**：竞争度低但意图明确的词组，挖掘 3-5 个自然分布在正文中。
- **LSI 关键词 / 相关词**：与主题语义相关的词汇/同义词，用于丰富上下文。
- **搜索意图分析 (Search Intent)**：分析用户搜索该词是为了**学习知识**（Info）、**寻找产品**（Commercial）还是**直接购买**（Transactional）。

### TDK 优化 (Title, Description, Keywords)

TDK 是爬虫抓取的第一印象，决定了点击率 (CTR)。
- **标题 (Title/H1)**：必须包含**核心关键词**，且尽量**靠左**。需要包含独特的视角或利益点。
- **描述 (Description)**：包含动作动词 + 核心关键词 + 具体利益点 + CTA（行动呼吁）。

**示例 (Examples):**
- ❌ Bad Title: 关于手冲咖啡的介绍 / Introduction to Hand Drip Coffee
- ✅ Good Title: **手冲咖啡入门**教程：新手必看的 5 个步骤与避坑指南 / **Hand Drip Coffee Guide**: 5 Essential Steps for Beginners

---

## 2. 结构化与排版 (Structure & Formatting)

### 标签层级 (H-Tags Hierarchy)

- **H1**: 全页唯一，即文章主标题
- **H2**: 主要章节标题，**至少包含一次**核心关键词或长尾词
- **H3**: H2 下的细分步骤，用于切分长段落
- **禁止**全文只有一大段文本。

### 倒金字塔结构与首段优化

- **首段 (First 100 Words/前100字)**：**必须出现**核心关键词。
- **中间**: 结论先行，先说结果，再详述论据。段落要短（英文每段不超过3-4句，中文不超过3-4行）。
- **结尾**: 总结并提供行动呼吁 (CTA)。核心关键词需在结尾再次出现。

### 关键词密度与自然植入

遵循「F型」布局，重点在标题、首段、小标题、结尾出现。避免堆砌（Keyword Stuffing），使用同义词。

---

## 3. 技术性优化 (Technical SEO)

### URL 与内外链策略 (URLs & Links)

- **URL Slug**: 使用英文短横线连接（不要用下划线），包含关键词，避免停用词 (a, an, the)。
  - ❌ `domain.com/?p=123` 或 `domain.com/shouchong_kafei`
  - ✅ `domain.com/hand-drip-coffee-guide`
- **Internal Links (内链)**: 链接到 2-5 个站内相关文章（不存在的不强求），使用描述性锚文本。
- **External Links (外链)**: 链接到 1-3 个权威来源，并设置新标签页打开。

### 图片 SEO (Image SEO)

搜索引擎看不懂图片，只能看代码。
- **文件名 (File Name)**: 上传前重命名为包含关键词的描述性英文。例如 `hand-drip-coffee-pouring.jpg`（不要用 `IMG_001.jpg`）。
- **Alt 文本 (Alt Text)**: 必须填写，描述图片内容并自然包含关键词。
  - ✅ `alt="手冲咖啡注水手法演示：中心注水法"`

---

## 4. 自动化审查与评估 (Automated SEO Audit)

在完成博客撰写后，Orchestrator 必须调用本地脚本评估文章的 SEO 质量。

**执行命令**:
```bash
python .opencode/skills/skill-seo/scripts/seo_optimizer.py <file-path> "核心关键词" "长尾词1,长尾词2"
```

**打分标准与建议**:
- **85-100**: 优秀 (Excellent) - 可以直接发布
- **70-84**: 良好 (Good) - 建议进行小幅优化
- **50-69**: 需改进 (Needs Work) - 请审查并应用脚本输出的优化建议
- **< 50**: 差 (Poor) - 需要大量重写

---

## 5. 发布前自查清单 (Pre-Publish Checklist)

- [ ] **标题 (Title)** 是否包含了核心关键词，且足够吸引人？
- [ ] **描述 (Meta Description)** 是否包含核心词并促使用户点击？
- [ ] **URL** 是否为简短的英文关键词路径？
- [ ] **首段 (First 100 words)** 是否出现了核心关键词？
- [ ] 是否使用了 H2、H3 **标签**构建清晰的层级，并在 H2 中包含了关键词？
- [ ] 关键词**密度**是否自然（无堆砌感）？
- [ ] 是否添加了指向站内其他文章的**内链**？
- [ ] 所有图片是否都添加了描述性的文件名和 **Alt 属性**？

# SEO Optimization Guide

## Overview

This guide provides comprehensive SEO optimization strategies for content creation. Use this as a reference when optimizing blog posts, articles, and web content.

## Quick Reference

| Metric | Target Range |
|--------|-------------|
| Title Length | 50-60 characters |
| Meta Description | 150-160 characters |
| URL Slug | 50-60 characters |
| Paragraph Length | 40-150 words |
| Keyword Density | 1-3% |
| Content Length | 1,500-2,500 words (comprehensive) |

---

## 1. Keyword Research

### Primary Keyword Selection

- **Search Volume**: 500-5,000 monthly searches (sweet spot)
- **Competition**: Low to medium
- **Relevance**: Direct match to content topic
- **Intent**: Matches user search intent

### Keyword Types

| Type | Purpose | Example |
|------|---------|---------|
| Primary | Main focus of content | "content marketing strategy" |
| Secondary | Support primary keyword | "content marketing tips", "marketing strategy guide" |
| LSI (Latent Semantic Indexing) | Contextually related terms | "blog posts", "social media", "engagement", "audience" |
| Long-tail | Specific phrases | "how to create a content marketing strategy for small business" |

### Keyword Research Tools

- **Free**: Google Keyword Planner, Ubersuggest, AnswerThePublic
- **Paid**: Ahrefs, SEMrush, Moz Pro
- **Competitor Analysis**: Check what keywords competitors rank for

---

## 2. On-Page SEO Elements

### Title Tag Optimization

```
Best Practice: Primary Keyword - Compelling Benefit | Brand Name
Example: Content Marketing Strategy - Drive 3x More Traffic | YourBrand
```

**Rules:**
- Include primary keyword near the beginning
- Keep under 60 characters
- Make it compelling for clicks
- Avoid keyword stuffing

### Meta Description

```
Template: [Action verb] + [primary keyword] + [specific benefit] + [CTA]
Example: Learn how to create a content marketing strategy that drives 3x more traffic. Get your free template now.
```

**Rules:**
- 150-160 characters
- Include primary keyword naturally
- Include a call-to-action
- Match the page content

### URL Structure

```
Good: /blog/content-marketing-strategy-guide
Bad: /blog/p=123 or /blog/10-29-2023-post
```

**Rules:**
- Short and descriptive
- Include primary keyword
- Use hyphens (not underscores)
- Lowercase only
- Avoid stop words (a, an, the, and)

### Header Structure

```
H1: Primary Keyword + Unique Angle (Only one per page)
  H2: Secondary Keyword Variation 1
    H3: Supporting point
    H3: Supporting point
  H2: Secondary Keyword Variation 2
    H3: Supporting point
    H4: Detailed sub-point
```

---

## 3. Content Optimization

### Keyword Placement

| Location | Requirement |
|----------|-------------|
| Title | Primary keyword (within first 60 chars) |
| First paragraph | Primary keyword (within first 100 words) |
| H1 | Primary keyword |
| 2-3 H2s | Primary or secondary keywords |
| Body | Natural distribution (1-3% density) |
| Conclusion | Primary keyword |
| Image alt text | Keywords where relevant |

### Content Length Guidelines

| Content Type | Recommended Length |
|--------------|-------------------|
| Blog Post | 1,500-2,500 words |
| Pillar Content | 3,000-5,000 words |
| Landing Page | 500-1,000 words |
| Product Page | 300-500 words + specs |

### Internal Linking

- Link to 2-5 relevant internal pages
- Use descriptive anchor text
- Prioritize important pages
- Create topic clusters

### External Linking

- Link to 1-3 authoritative sources
- Open in new tab for external links
- Cite sources properly
- Link to high-domain-authority sites

---

## 4. Technical SEO

### Page Speed

- Optimize images (WebP format, compression)
- Minimize CSS and JavaScript
- Use browser caching
- Implement lazy loading
- Target: Under 3 seconds load time

### Mobile Optimization

- Responsive design
- Touch-friendly elements
- Readable font sizes (16px minimum)
- Proper viewport meta tag
- Avoid interstitials

### Structured Data (Schema Markup)

```json
{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "Article Title",
  "author": {
    "@type": "Person",
    "name": "Author Name"
  },
  "datePublished": "2024-01-15",
  "dateModified": "2024-01-20"
}
```

### Core Web Vitals

| Metric | Target |
|--------|--------|
| LCP (Largest Contentful Paint) | < 2.5 seconds |
| FID (First Input Delay) | < 100ms |
| CLS (Cumulative Layout Shift) | < 0.1 |

---

## 5. Image SEO

### Optimization Checklist

- [ ] Descriptive file name (content-marketing-strategy.jpg)
- [ ] Alt text with keyword (when relevant)
- [ ] Compressed file size (< 100KB)
- [ ] Appropriate dimensions
- [ ] Responsive images (srcset)
- [ ] Lazy loading implemented

### Alt Text Guidelines

```
Good: "Content marketing strategy framework diagram showing planning stages"
Bad: "image1.jpg" or "marketing" or keyword stuffing
```

---

## 6. SEO Scoring System

Using `scripts/seo_optimizer.py`:

### Score Calculation

| Factor | Max Points |
|--------|-----------|
| Content Length | 20 |
| Keyword Optimization | 30 |
| Structure | 25 |
| Readability | 25 |
| **Total** | **100** |

### Score Interpretation

| Score | Status | Action |
|-------|--------|--------|
| 85-100 | Excellent | Publish with confidence |
| 70-84 | Good | Minor improvements recommended |
| 50-69 | Needs Work | Review recommendations |
| Below 50 | Poor | Major revision required |

### Common Recommendations

1. **Increase content length** - Target 300+ words minimum
2. **Add keywords naturally** - Aim for 1-3% density
3. **Improve structure** - Add H2/H3 headings
4. **Add internal links** - Connect related content
5. **Simplify sentences** - Improve readability

---

## 7. Chinese SEO

### SEO 特点

| 因素 | 要求 |
|------|------|
| 标题长度 | 30个汉字以内 |
| 描述长度 | 80-120个汉字 |
| 关键词密度 | 2-8% |
| 内容长度 | 800-2000字 |

### 中文关键词策略

1. **核心关键词**: 放在标题开头
2. **长尾关键词**: 自然分布在正文中
3. **相关词**: 使用同义词和相关术语
4. **地域词**: 结合目标城市/地区

### 收录优化

- 提交站点地图到站长平台
- 确保网站ICP备案
- 使用统计
- 优化移动端体验
- 定期更新内容

---

## 8. SEO Workflow

### Before Writing

1. Research primary keyword
2. Identify 3-5 secondary keywords
3. List 10-15 LSI keywords
4. Analyze competitor content
5. Create content outline

### During Writing

1. Include primary keyword in title
2. Use keyword in first 100 words
3. Structure with proper headings
4. Write for humans first, SEO second
5. Include internal links naturally

### After Writing

```bash
# Run SEO analysis
python scripts/seo_optimizer.py article.md "primary keyword" "secondary,keywords"

# Check recommendations and apply fixes
```

### Before Publishing

- [ ] Title optimized (50-60 chars)
- [ ] Meta description written (150-160 chars)
- [ ] URL slug clean and descriptive
- [ ] Images have alt text
- [ ] Internal links added
- [ ] External links to authoritative sources
- [ ] Mobile-friendly formatting
- [ ] Page speed optimized

---

## 9. Common SEO Mistakes

### Avoid These Pitfalls

| Mistake | Consequence | Fix |
|---------|-------------|-----|
| Keyword stuffing | Penalty, poor UX | Use natural language, 1-3% density |
| Duplicate content | Indexing issues | Create original content |
| Thin content | Low rankings | Aim for comprehensive coverage |
| Broken links | Poor UX, crawl errors | Regular link audits |
| Missing meta descriptions | Lower CTR | Write compelling descriptions |
| Slow page speed | Higher bounce rate | Optimize images, code |
| No internal links | Poor crawlability | Link to related content |

---

## 10. SEO Tools Reference

### Analysis Tools

| Tool | Purpose | Type |
|------|---------|------|
| Google Search Console | Performance monitoring | Free |
| Google Analytics | Traffic analysis | Free |
| scripts/seo_optimizer.py | Content optimization | Free |
| Ahrefs | Comprehensive SEO | Paid |
| SEMrush | Competitive analysis | Paid |

### Browser Extensions

- MozBar (Domain authority)
- SEO Minion (On-page analysis)
- Keywords Everywhere (Search volume)
- Check My Links (Broken link checker)

---

## Quick Commands

```bash
# Analyze content SEO
python scripts/seo_optimizer.py article.md "primary keyword"

# Analyze with secondary keywords
python scripts/seo_optimizer.py article.md "main keyword" "secondary,keywords,list"

# Check keyword density only
grep -io "keyword" article.md | wc -l
```

---

## 11. SEO 写作实操流程

### 第一阶段：选题与关键词策略 (Preparation)

在动笔之前，必须明确「为谁写」以及「由于什么词被找到」。

#### 关键词研究核心逻辑

不仅仅是找词，而是找「有流量且竞争适度」的词，并确定用户搜这个词是想干什么。

**操作规范：**

- **核心词 (Focus Keyword)**：文章的主题词（如「SEO 写作」），只专注 1 个核心词
- **长尾词 (Long-tail Keywords)**：竞争度低但意图明确的词组，挖掘 3-5 个用来构建文章
- **LSI 关键词**：与主题语义相关的词汇，用于丰富上下文
- **搜索意图分析**：分析用户搜索该词是为了**学习知识**（Info）、**寻找产品**（Commercial）还是**直接购买**（Transactional）

**实操示例：**

| | 错误做法 | 正确做法 |
|---|---------|---------|
| 核心词 | 「咖啡」（词太宽泛） | 「手冲咖啡入门」 |
| 长尾词 | - | 「手冲咖啡粉推荐」「手冲咖啡水温多少合适」 |
| 意图判断 | - | 用户想学习教程，文章以「教程+避坑指南」为主 |

### 第二阶段：结构化大纲 (Structure & TDK)

#### TDK 优化 (Title, Description, Keywords)

搜索引擎偏好结构清晰、逻辑严密的内容，TDK 是爬虫抓取的第一印象，决定了点击率 (CTR)。

**操作规范：**

- **标题 (Title/H1)**：必须包含**核心关键词**，且尽量**靠左**。长度控制在 30 字以内。
- **描述 (Description)**：对标题的补充，包含关键词及其变体，激发好奇心。

**实操示例：**

| | 示例 |
|---|------|
| ❌ Bad Title | 关于手冲咖啡的介绍 |
| ✅ Good Title | **手冲咖啡入门**教程：新手必看的 5 个步骤与避坑指南 (2024版) |
| ✅ Description | 想在家做手冲咖啡但不知道从何下手？本文详细解析**手冲咖啡**的水温、粉水比及器具选择，教你 3 分钟冲出一杯好咖啡。 |

#### 标签层级 (H-Tags Hierarchy)

告诉爬虫文章的骨架。H1 是大标题，H2 是章节，H3 是小点。

**操作规范：**

- **H1**：全页唯一，即文章主标题
- **H2**：主要章节标题，**至少包含一次**核心关键词或长尾词
- **H3**：H2 下的细分步骤，用于切分长段落
- **禁止**全文只有一大段文本

**实操示例：**

```
H1: 手冲咖啡入门全指南
├── H2: 准备工作：你需要哪些器具？ (包含相关词「器具」)
│   ├── H3: 手冲壶的选择
│   └── H3: 滤杯与滤纸
├── H2: 核心步骤：**手冲咖啡**的具体流程 (包含核心词)
│   ├── H3: 闷蒸
│   └── H3: 注水
```

### 第三阶段：正文写作与布局 (Content Writing)

#### 倒金字塔结构与首段优化

现代用户没有耐心，必须在第一屏就抓住眼球，降低**跳出率**。

**操作规范：**

- **首段 (First 100 Words)**：前 100 字内**必须出现**核心关键词
- **中间**：结论先行，先说结果，再详述论据
- **结尾**：总结并提供行动呼吁 (CTA)

**实操示例：**

| | 示例 |
|---|------|
| ❌ 错误开头 | 大家好，今天天气不错，我们来聊聊咖啡。咖啡有很多种……（废话多，无关键词） |
| ✅ 正确开头 | 很多新手在学习**手冲咖啡入门**时，往往卡在水温和研磨度上。本文将为你揭秘黄金粉水比（1:15），助你轻松入门。 |

#### 关键词密度与自然植入

密度控制在 **1%-2%**，避免堆砌（Keyword Stuffing）导致被算法惩罚。

**操作规范：**

- **分布**：遵循「F型」布局，重点在标题、首段、小标题、结尾出现
- **变体使用**：不要死磕一个词，使用同义词

**实操示例：**

| | 示例 |
|---|------|
| ❌ 堆砌 | 我们提供最好的**SEO服务**。我们的**SEO服务**很便宜。如果你需要**SEO服务**，请联系我们购买**SEO服务**。 |
| ✅ 自然 | 如果你正在寻找专业的**SEO服务**，我们可以提供帮助。通过系统的**网站排名优化**，你的流量将获得显著增长。 |

#### 内容的可读性与排版

提升用户停留时长 (Dwell Time)，这是排名上升的重要信号。

**操作规范：**

- **段落**：每段不超过 3-4 行
- **视觉锚点**：使用**加粗**标记重点句子
- **列表**：凡是并列内容，必须使用列表
- **原创性与价值**：内容必须具备增量价值，严格避免抄袭

### 第四阶段：技术性优化 (Technical Optimization)

#### URL 与内外链策略

构建网站的网状结构，传递权重 (Link Juice)。

**操作规范：**

- **URL**：使用英文短横线连接，包含关键词
- **内链**：文中提到某个概念时，链接到站内相关文章
- **外链**：引用权威数据并适当添加

**实操示例：**

| | 示例 |
|---|------|
| ❌ Bad URL | domain.com/?p=12345 或 domain.com/shouchong-kafei-zenme-zuo |
| ✅ Good URL | domain.com/hand-drip-coffee-guide |

#### 图片 SEO (Alt Text)

搜索引擎看不懂图片，只能看代码。

**操作规范：**

- **Alt 文本**：必须填写，描述图片内容并包含关键词
- **文件名**：上传前重命名图片，不要用 IMG_001.jpg

**实操示例：**

```
图片内容：一张正在注水的咖啡照片
文件名：hand-drip-coffee-pouring.jpg
Alt 属性：<img src="..." alt="手冲咖啡注水手法演示：中心注水法" />
```

---

## 12. 效果自查清单

发布文章前，请回答以下问题：

- [ ] **标题**是否包含了核心关键词，且足够吸引人？
- [ ] **URL** 是否为简短的英文关键词路径？
- [ ] **首段**前 100 字是否出现了关键词？
- [ ] 是否使用了 H2、H3 **标签**构建清晰的层级？
- [ ] 关键词**密度**是否自然（没有强行插入的感觉）？
- [ ] 是否添加了指向站内其他文章的**内链**？
- [ ] 所有图片是否都添加了 **Alt 属性**？
- [ ] 文章是否解决了用户的**搜索意图**（真的有干货吗）？

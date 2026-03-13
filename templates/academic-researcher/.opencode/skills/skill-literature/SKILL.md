---
name: skill-literature
description: 文献搜索与综述工作流与规范
metadata:
  version: 1.0.0
  updated: 2026-03-05
---

# 文献搜索与综述

## 概述
本技能用于文献调研、筛选、整理与综述写作。适配 `/ideate` 和 `/write` 任务。

## 检索策略
1. **关键词组合**：任务名 + 方法名 + 指标 + 领域。
2. **同义词扩展**：如“retrieval-augmented”≈“RAG”。
3. **限定条件**：年份、会议、期刊、数据集。

## 数据库与渠道
- Semantic Scholar
- Google Scholar
- arXiv
- ACM DL
- IEEE Xplore

## 相关性评估
| 维度 | 判断标准 | 操作 |
|---|---|---|
| 主题匹配 | 任务/方法相同 | 阅读摘要 |
| 影响力 | 会议/期刊权威 | 记录 venue |
| 证据质量 | 实验充分 | 查看实验部分 |

## 引用管理结构
### 核心参考 (idea/references/<key>/)
- `meta/bibtex.txt`：完整 BibTeX
- `meta/meta_info.txt`：标题、作者、年份、venue、相关性、关键结论
- `meta/toc.txt`：目录或章节
- `sections/`：关键段落摘录

### 写作参考 (writing/references/)
- `.bib`：汇总 BibTeX
- 简短注释：每篇 2-3 行

## 文献综述写作模式
- **按主题/方法分组**，避免流水账。
- **指出研究空白**，引出本文贡献。
- **公平评价**，不歪曲对手方法。

## 参考文献规模建议
| 论文类型 | 参考数 | 说明 |
|---|---|---|
| 短文/Workshop | 15-30 | 足够覆盖核心工作 |
| 会议长文 | 30-60 | 领域内关键工作 |
| 期刊 | 60+ | 覆盖完整谱系 |

## 检索记录模板
```text
查询词: <keyword>
数据库: <source>
筛选条件: <year/venue>
命中数: <n>
保留论文: <list>
```

## 检查清单
- [ ] 关键词覆盖多种表述
- [ ] 核心论文已建立参考目录
- [ ] 综述按主题组织
- [ ] 研究空白明确
- [ ] 引用信息可验证

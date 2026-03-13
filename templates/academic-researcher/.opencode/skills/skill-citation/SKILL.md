---
name: skill-citation
description: 引用管理与 BibTeX 规范
metadata:
  version: 1.0.0
  updated: 2026-03-05
---

# 引用管理与 BibTeX

## 概述
本技能用于文献引用的格式规范、双参考系统与验证流程。适用于 `/cite` 和 `/write`。

## BibTeX 格式规范
### 常见条目必填字段
| 类型 | 必填字段 | 说明 |
|---|---|---|
| @article | author, title, journal, year | 期刊论文 |
| @inproceedings | author, title, booktitle, year | 会议论文 |
| @book | author, title, publisher, year | 书籍 |

### Key 命名规范
`author_year_keyword`（如 `smith_2023_diffusion`）。

## 文中引用方式
- **Markdown**：`[Author et al., Year]`、`[1]`、`[Author, Year]`
- **LaTeX**：`\cite{key}` / `\citep{key}` / `\citet{key}`

## 双参考系统
| 目录 | 作用 | 内容 |
|---|---|---|
| idea/references/ | 研究核心文献 | 详细元数据与摘录 |
| writing/references/ | 论文引用 | 汇总 BibTeX |

### 同步规则
- idea/references/ 先建立完整条目。
- writing/references/ 只收录最终引用。
- 更新 BibTeX 时同步两个目录。

## 引用验证 (citation_validator.py)
```bash
python .opencode/skills/skill-citation/scripts/citation_validator.py <references-path>
```
验证来源：Semantic Scholar / CrossRef / arXiv。

## 常见错误
- 伪造文献（禁止）。
- 年份或会议错误。
- 自引比例过高。
- 遗漏关键相关工作。

## 检查清单
- [ ] BibTeX 字段完整
- [ ] Key 命名一致
- [ ] 引用格式正确
- [ ] 通过 citation_validator.py
- [ ] 未遗漏关键相关工作

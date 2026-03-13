---
name: academic-researcher
description: 学术研究全生命周期工作空间，支持从想法生成、文献研究、实验规划、实验执行、数据分析到论文写作的完整流程。Generic academic template with domain skills for specialization. Use when conducting research, writing papers, running experiments, or when user mentions 研究, 论文, 实验, paper, research.
license: MIT
metadata:
  version: 1.0.0
  author: Clement Chen
  category: research
  updated: 2026-03-05
  python-tools: novelty_checker.py, citation_validator.py, experiment_tracker.py
  languages: English, 中文
  framework: OpenCode Native Task Architecture
---

# Academic Researcher (OpenCode Native Workspace)

学术研究全生命周期工作空间。通过 OpenCode 原生的 `Task(Category + Skills)` 架构，覆盖从想法生成到论文发表的完整研究流程。

## 核心工作流 (SOP)

本工作空间由一组内置命令驱动（定义在 `.opencode/commands/` 中），遵循严格的研究流程：

1. **构思：** 使用 `/ideate <主题>` 进行文献搜集与想法生成。
2. **审查：** **强制** 使用 `/review` 运行自动化新颖性和引用验证脚本。
3. **规划：** 使用 `/plan` 确定实验方案（模型、数据集、评估指标等）。
4. **实验：** 使用 `/experiment` 生成实验脚本并执行。
5. **分析：** 使用 `/analyze` 分析实验结果，生成 REPORT.md + RESULTS.json。
6. **写作：** 使用 `/write` 按章节撰写论文（Markdown + LaTeX）。
7. **引用：** 随时使用 `/cite` 管理参考文献。

## 代理调度规则

- 凡是涉及文献搜集与想法生成的任务，使用 `deep` 类别并挂载 `voice-proposal` + `skill-literature`。
- 凡是涉及实验规划的任务，使用 `ultrabrain` 类别并挂载 `skill-experiment-design`。
- 凡是涉及自动化审查的任务，使用 `unspecified-high` 类别直接运行 Python 脚本。
- 凡是涉及论文写作的任务，使用 `writing` 类别并挂载 `voice-academic` + `skill-citation`。

---

## 技能路由系统 (Skill Routing System)

### 1. 学术写作语调 (Academic Voices)
- `voice-academic`: 论文写作规范（正式、精确、学术）
- `voice-proposal`: 研究提案/想法阐述
- `voice-report`: 实验报告撰写

### 2. 领域上下文 (Domain Contexts)
- `domain-cs-ai`: AI/ML 领域（深度学习、强化学习等）
- `domain-cs-nlp`: 自然语言处理领域
- `domain-cs-systems`: 系统领域（分布式、OS、网络等）
- `domain-generic`: 通用学术（跨领域适用）

### 3. 研究技能 (Research Skills)
- `skill-literature`: 文献搜索与综述
- `skill-experiment-design`: 实验设计与版本跟踪
- `skill-data-analysis`: 数据分析与可视化
- `skill-citation`: 引用管理（BibTeX）
- `skill-novelty-check`: 新颖性验证

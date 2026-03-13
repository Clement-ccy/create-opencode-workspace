---
name: skill-novelty-check
description: 新颖性验证流程与评估标准
metadata:
  version: 1.0.0
  updated: 2026-03-05
---

# 新颖性验证

## 概述
本技能用于研究提案的新颖性评估，帮助定位与已有工作差异。

## 新颖性的类型
- **问题新颖**：提出新问题或新场景。
- **方法新颖**：已有问题的新方法。
- **数据新颖**：新数据集或评测设定。
- **发现新颖**：对已知方法的新发现。

## novelty_checker.py 使用
```bash
python .opencode/skills/skill-novelty-check/scripts/novelty_checker.py <proposal-file>
```
工具会检索 Semantic Scholar，输出相似度与最相近工作。

## 应对新颖性不足
- 明确区分与现有方法的差异点。
- 承认相关工作并准确定位贡献。
- 调整研究问题或方法范围。

## 评估标准
| 维度 | 判定问题 | 证据 |
|---|---|---|
| 问题 | 是否被广泛研究 | 相关文献数量 |
| 方法 | 是否已有相同方法 | 相似算法 |
| 数据 | 是否已有同数据 | 数据集对比 |
| 发现 | 是否已有相同结论 | 综述与分析 |

## 检查清单
- [ ] novelty_checker.py 已运行
- [ ] 相似工作已分析
- [ ] 差异点写清楚
- [ ] 提案范围可辩护

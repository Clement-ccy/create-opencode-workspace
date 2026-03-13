---
name: voice-report
description: 实验报告撰写语调与结构规范
metadata:
  version: 1.0.0
  updated: 2026-03-05
---

# 实验报告写作语调

## 概述
本技能用于撰写实验报告（REPORT.md）。强调客观、可复现、细节完整。

## 报告风格
- **事实驱动**：只陈述观察结果。
- **细节完整**：可复现为第一目标。
- **结构清晰**：与实验流程对应。

## REPORT.md 结构指南
1. **Objective**：实验目标与假设。
2. **Setup**：硬件/软件环境、数据版本。
3. **Methodology**：实验流程与配置。
4. **Results**：结果表格/图。
5. **Analysis**：解释结果与异常。
6. **Conclusions**：结论与限制。
7. **Next Steps**：后续实验计划。

## Setup 描述规范
- 硬件：CPU/GPU/内存/存储。
- 软件：OS、驱动、库版本。
- 配置：batch size、lr、seed。

## 结果陈述规范
- 只陈述结果，不下结论。
- 结果要包含方差或置信区间。
- 明确说明统计显著性。

## RESULTS.json 结构约定
```json
{
  "experiment": "name",
  "metrics": {
    "accuracy": {"mean": 0.912, "std": 0.006},
    "f1": {"mean": 0.897, "std": 0.008}
  },
  "configs": {
    "seed": [1, 2, 3],
    "batch_size": 64
  }
}
```

## 报告与研究叙事连接
- 把实验结果映射到研究问题。
- 说明与先前实验的差异。

## 检查清单
- [ ] Objective 与假设明确
- [ ] Setup 信息完整
- [ ] Results 含误差与显著性
- [ ] Analysis 解释异常
- [ ] Next Steps 给出可操作计划

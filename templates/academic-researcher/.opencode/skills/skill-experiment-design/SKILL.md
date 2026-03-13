---
name: skill-experiment-design
description: 实验设计与版本跟踪规范
metadata:
  version: 1.0.0
  updated: 2026-03-05
---

# 实验设计与版本跟踪

## 概述
本技能用于实验规划、对照设计、版本跟踪与复现要求。适用于 `/plan` 与 `/experiment`。

## 实验设计原则
- **控制变量**：一次只改变一个变量。
- **消融设计**：移除核心组件观察影响。
- **基线选择**：选择公认强基线 + 自身简化版本。
- **统计显著性**：至少 3-5 次重复实验。

## plan.json 结构规范
```json
[
  {
    "category": "Category Name",
    "title": "Task Title",
    "description": "Description",
    "steps": {
      "step1": "**Step**: Details...",
      "step2": "**Step**: Details..."
    }
  }
]
```

## 版本跟踪 (experiment_tracker.py)
```bash
python .opencode/skills/skill-experiment-design/scripts/experiment_tracker.py init <name>
python .opencode/skills/skill-experiment-design/scripts/experiment_tracker.py log <name> --config <json>
python .opencode/skills/skill-experiment-design/scripts/experiment_tracker.py status
```

## 复现性清单
- Random seeds
- 硬件规格
- 软件版本
- 数据预处理
- 训练细节（epoch/batch/lr/schedule）

## 基线选择标准
| 标准 | 说明 |
|---|---|
| 公认基线 | 社区常用模型 |
| 可复现 | 公开代码/可重现 |
| 相同设置 | 同数据、同评测 |

## 消融实验示例
```text
完整模型 → 去掉组件 A → 去掉组件 B → 替换损失函数
```

## 检查清单
- [ ] 控制变量清晰
- [ ] 消融设计完整
- [ ] 基线选择合理
- [ ] 计划已写入 plan.json
- [ ] 复现信息完整

---
name: domain-cs-nlp
description: 自然语言处理研究领域指南与评估规范
metadata:
  version: 1.0.0
  updated: 2026-03-05
---

# 自然语言处理研究领域

## 概述
本技能用于 NLP 研究的任务定义、实验流程与评估标准。适用于语言模型、机器翻译、问答、信息抽取、对话系统等方向。

## 研究方向
- **语言模型 (LM)**：预训练、对齐、效率与推理能力。
- **机器翻译 (MT)**：对齐、低资源、鲁棒性。
- **问答 (QA)**：可解释性、长文档推理。
- **信息抽取 (IE)**：实体、关系、事件抽取。
- **对话系统**：多轮一致性、礼貌性与安全性。

## 常见实验模式
1. **微调 (Fine-tuning)**：说明预训练模型版本与微调策略。
2. **提示学习 (Prompting)**：模板与示例选择策略。
3. **上下文学习 (ICL)**：k-shot 设置，示例顺序与采样。
4. **评估流水线**：自动评测 + 人工评测结合。

## 标准指标（按任务）
| 任务 | 指标 | 说明 |
|---|---|---|
| 翻译 | BLEU / COMET | 需要固定评测脚本 |
| 摘要 | ROUGE / BERTScore | 长度控制说明 |
| 问答 | Exact Match / F1 | 需说明评测版本 |
| 信息抽取 | Precision/Recall/F1 | 需报告 micro/macro |
| 语言模型 | Perplexity | 需说明 tokenizer |

## 标准数据集（按任务）
| 任务 | 数据集 | 备注 |
|---|---|---|
| 综合评测 | GLUE, SuperGLUE | 通用基准 |
| 问答 | SQuAD, Natural Questions | 需说明版本 |
| 翻译 | WMT | 指定语言对 |
| 摘要 | CNN/DailyMail, XSum | 需说明抽取/生成设定 |
| 对话 | MultiWOZ, DailyDialog | 需说明对话轮数 |

## NLP 论文结构约定 (ACL/EMNLP/NAACL)
1. **Introduction**：问题、挑战与贡献。
2. **Method**：任务定义 + 模型架构 + 训练策略。
3. **Experiments**：数据、指标、实现细节。
4. **Analysis**：误差分析、人类评价、案例。

## 人工评估协议
- 说明评审人数、评分维度（流畅性/一致性/事实性）。
- 提供评测指南与一致性（Cohen's kappa）。
- 混入对照样本防止偏差。

## 任务 → 指标 → 数据集 → 基线速查表
| 任务 | 指标 | 数据集 | 常见基线 |
|---|---|---|---|
| 翻译 | BLEU/COMET | WMT | Transformer | 
| 摘要 | ROUGE | CNN/DM | BART, PEGASUS |
| 问答 | EM/F1 | SQuAD | BERT, RoBERTa |
| IE | F1 | ACE | BiLSTM-CRF |
| LM | Perplexity | WikiText-103 | GPT 系列 |

## 报告规范
- 明确 tokenization、最大长度与解码策略。
- 对生成结果提供案例并说明失败类型。
- 多模型对比需保持相同训练数据。

## 检查清单
- [ ] 任务定义与指标匹配
- [ ] 评测脚本版本说明清楚
- [ ] 人工评估协议完整
- [ ] 结果包含误差分析
- [ ] 基线选择合理且可复现

# Cognitive Gate —— 大模型前的编译层 / 后的审计层（最小可运行参考实现）

> 这不是一个产品 demo，而是一个**控制层优先**的架构证明：模型是引擎，本仓库提供方向盘和刹车。

## 它解决什么

对齐马斯克 2026 年真实项目与言论的五个痛点：

| 马斯克的体系 | Cognitive Gate 提供的层 |
|---|---|
| **Grok**（输出不可控、不可审计） | 输出前**意图编译** + 输出后**约束审计** |
| **Optimus / Macrohard**（需要确定性任务而非概率文本） | 从"模糊指令"到结构化 `CognitiveRequest` 的**翻译层** |
| **Macrohard**（跨任务规则一致性） | **跨任务约束继承**：说三次"不对"→ 永久锁定 |
| **太空算力**（轨道数据中心极贵） | **P1 分型器**：判断任务值不值得、用哪类算力 |
| **跨公司 AI 治理** | 统一的 **AI 决策审计协议**（协议，不是集成） |

## 安装

需要 Python 3.9 或更高版本。运行时只依赖 Python 标准库：

```bash
git clone https://github.com/somo-ui/cognitive-gate.git
cd cognitive-gate
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install .
```

安装后可直接使用 `cognitive-gate --demo`。开发测试不需要额外依赖：

```bash
python -m unittest discover -s tests -v
```

## 3 分钟验证（无需 API key，纯标准库）

```bash
cd cognitive-gate
python -m unittest tests.test_gate -v     # 跑测试
cognitive-gate --demo                     # 看端到端演示（含"说三次不对永久锁定"）
cognitive-gate --input "帮我整理房间，但别用红色方案"   # 单条请求
```

默认使用 `MockGrok`，因此零配置即可端到端跑通。所有个人数据仅落在本地
`constraints.json` / `decision_history.jsonl`，可物理删除。

## 架构

```
用户指令
   │
   ▼
[编译层]  CompileLayer  →  CognitiveRequest(goal/mode/constraints/risk/reconstructed_text)
   │
   ▼
[P1分型]  P1Classifier  →  任务分型 + 算力路由（地面 / 太空 / 本地）
   │
   ▼
[模型]    MockGrok / GrokAdapter（可插拔；默认 mock，可换真 xAI Grok）
   │
   ▼
[审计层]  AuditLayer    →  输出 vs 生效/锁定约束 → 通过 或 拦截(blocked_reason)
   │
   ▼
[留痕]    决策档案(decision_record.json) + 决策病历(decision_history.jsonl)
```

约束库 `ConstraintStore` 持久化到 JSON，因此**跨任务、跨会话**继承规则——
这正是"模拟整个公司运作"需要的规则一致性。

## 接入真实 Grok

```python
import os
os.environ["XAI_API_KEY"] = "你的key"
from cognitive_gate import CognitiveGateProtocol
gate = CognitiveGateProtocol()   # 自动选用 GrokAdapter
```
`GrokAdapter` 的网络调用骨架已预留（见 `cognitive_gate/model_adapter.py`）。

## 诚实的范围声明（重要）

本仓库解决的是 **可控性 / 可审计性 / 一致性**（工程与 UX 层面的问题），
**不解决**马斯克担心的"AI 接管人类"那种**生存性安全**问题。

对 LLM 输出的语义合规审计目前是 **best-effort 护栏**，不是数学保证——
这是开放研究问题。本层用可解释规则 + 可插拔模型自检做"最大努力拦截"，
并明确标注 `confidence` 的不确定性。请勿将其宣传为对灭绝风险的保险。

## 文件

```
cognitive_gate/
  compile_layer.py     编译层（CognitiveRequest）
  p1_classifier.py     P1 任务分型器
  constraint_store.py  跨任务约束继承（说三次不对永久锁定）
  audit_layer.py       输出后审计层
  model_adapter.py     可插拔模型（MockGrok 默认 / GrokAdapter 预留）
  protocol.py          统一审计协议（编排以上全部）
demo.py                CLI 演示
tests/test_gate.py     单元测试
```

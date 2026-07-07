# Prompt 工程代码实践

> Prompt 工程的目标不是把提示词写长，而是让输入、约束、输出和回归测试都可控。

## 最小结构化 Prompt

```python
import json
from dataclasses import dataclass


@dataclass
class PromptCase:
    question: str
    expected_intent: str


SYSTEM_PROMPT = """
你是一个意图分类器，只输出 JSON。

可选 intent：
- data_query：用户要查询或分析业务数据
- chitchat：闲聊、天气、问候

输出格式：
{"intent": "...", "reason": "..."}
"""


def build_messages(question: str) -> list[dict]:
    return [
        {"role": "system", "content": SYSTEM_PROMPT.strip()},
        {"role": "user", "content": question},
    ]


def parse_json_response(text: str) -> dict:
    data = json.loads(text)
    if data.get("intent") not in {"data_query", "chitchat"}:
        raise ValueError("invalid intent")
    return data
```

## 面试讲法

我会把 Prompt 当成一个小型接口来设计：

1. 输入：用户问题、历史、检索上下文、工具 schema。
2. 约束：角色、禁止事项、输出格式、边界条件。
3. 输出：JSON schema 或固定字段。
4. 测试：固定 case 做回归，避免改 prompt 后引入退化。

## 常见失败点

| 失败 | 原因 | 修复 |
| :--- | :--- | :--- |
| 输出不是 JSON | 只在自然语言里要求，缺少 parser 和重试 | 使用 JSON mode / schema parser |
| 幻觉字段 | Schema 太长或上下文不准 | RAG 召回 + 字段白名单 |
| prompt 越写越长 | 没有拆任务 | Router、Planner、Tool executor 分层 |
| 改 prompt 后效果退化 | 没有回归集 | 建 prompt eval cases |

## 练习

1. 写 5 个 intent 分类 case。
2. 模拟一次模型输出非法 JSON，补 parser 错误处理。
3. 把 prompt 分成 router、planner、executor 三段，说明各自职责。

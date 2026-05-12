# 02_ReAct_Agent_代码实践

> 来源: AI Agent面试实践/01_Agent基础架构/02_ReAct_Agent_代码实践.py

`python
"""
【面试必会】手写 ReAct Agent 框架 —— 从零实现一个极简 Agent

学习目标：
1. 理解 Agentic Loop 的代码实现
2. 掌握 Function Call / Tool Use 的底层逻辑
3. 能手撕一个最小可用 Agent（面试加分项）

运行前准备：
- 确保已安装 openai: pip install openai
- 配置 API_KEY（支持阿里云 DashScope、DeepSeek、OpenAI 等）

【重要安全提示】
不要在代码中硬编码 API Key！应该通过环境变量传入：
  Windows PowerShell: $env:DEEPSEEK_API_KEY = "sk-..."
  Windows CMD:        set DEEPSEEK_API_KEY=sk-...
  Linux/Mac:          export DEEPSEEK_API_KEY=sk-...
"""

import json
import os
from openai import OpenAI

# ========================
# 第一步：定义工具（Tools）
# ========================
# 工具是 Agent 的"手脚"——让 LLM 能获取外部信息或执行操作

def get_weather(city: str) -> str:
    """查询指定城市的天气"""
    # 模拟 API 调用（实际项目中接真实天气 API）
    weather_db = {
        "深圳": "晴天，28°C",
        "北京": "多云，22°C",
        "上海": "小雨，20°C",
    }
    return weather_db.get(city, "未知城市，无法查询天气")


def calculate_bmi(weight_kg: float, height_cm: float) -> str:
    """计算 BMI 指数"""
    height_m = height_cm / 100
    bmi = weight_kg / (height_m ** 2)
    if bmi < 18.5:
        level = "偏瘦"
    elif bmi < 24:
        level = "正常"
    elif bmi < 28:
        level = "偏胖"
    else:
        level = "肥胖"
    return f"BMI = {bmi:.2f}，属于{level}范围"


# ========================
# 第二步：工具注册表
# ========================
# 面试要点：为什么用注册表？——解耦工具定义与 Agent 逻辑，支持动态加载

TOOL_REGISTRY = {
    "get_weather": get_weather,
    "calculate_bmi": calculate_bmi,
}

# 工具的 JSON Schema 描述（供 LLM 理解工具用途和参数）
TOOLS_SCHEMA = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "查询指定城市的当前天气情况",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "城市名称，如'深圳'、'北京'"
                    }
                },
                "required": ["city"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "calculate_bmi",
            "description": "根据体重和身高计算 BMI 健康指数",
            "parameters": {
                "type": "object",
                "properties": {
                    "weight_kg": {
                        "type": "number",
                        "description": "体重，单位千克"
                    },
                    "height_cm": {
                        "type": "number",
                        "description": "身高，单位厘米"
                    }
                },
                "required": ["weight_kg", "height_cm"]
            }
        }
    }
]


# ========================
# 第三步：Agent 核心类（面试重点！）
# ========================

class ReActAgent:
    """
    极简 ReAct Agent 实现

    面试时如果被问"怎么实现一个 Agent"，可以按这个结构回答：
    1. 初始化：LLM 客户端 + 工具注册表
    2. 主循环（Agentic Loop）：
       - 把用户消息 + 历史记录传给 LLM
       - LLM 决定是「直接回答」还是「调用工具」
       - 如果调用工具：执行工具 → 将结果加入历史 → 再次调用 LLM
       - 循环直到产生最终答案或达到最大迭代次数
    3. 输出：返回最终答案
    """

    def __init__(self, model: str = None, max_iterations: int = 5):
        """
        初始化 Agent

        支持多 LLM 提供商（通过环境变量自动识别）：
        - DeepSeek: 设置 DEEPSEEK_API_KEY，自动使用 https://api.deepseek.com/v1
        - 阿里云: 设置 DASHSCOPE_API_KEY，自动使用阿里兼容接口
        - OpenAI: 设置 OPENAI_API_KEY，自动使用官方接口

        参数:
            model: 模型名称，None 时自动根据提供商选择默认模型
            max_iterations: 最大迭代次数，防止死循环
        """
        # ===== 自动识别 LLM 提供商 =====
        # 优先级：DeepSeek > 阿里云 > OpenAI
        if os.getenv("DEEPSEEK_API_KEY"):
            api_key = os.getenv("DEEPSEEK_API_KEY")
            base_url = "https://api.deepseek.com/v1"
            default_model = "deepseek-chat"
            print("[配置] 检测到 DeepSeek API Key，使用 DeepSeek 接口")
        elif os.getenv("DASHSCOPE_API_KEY"):
            api_key = os.getenv("DASHSCOPE_API_KEY")
            base_url = "https://dashscope.aliyuncs.com/compatible-mode/v1"
            default_model = "qwen3-max"
            print("[配置] 检测到阿里云 DashScope API Key，使用阿里接口")
        elif os.getenv("OPENAI_API_KEY"):
            api_key = os.getenv("OPENAI_API_KEY")
            base_url = "https://api.openai.com/v1"
            default_model = "gpt-4o"
            print("[配置] 检测到 OpenAI API Key，使用官方接口")
        else:
            raise ValueError(
                "未找到任何 API Key！\n"
                "请先设置环境变量之一：\n"
                "  DEEPSEEK_API_KEY（推荐）\n"
                "  DASHSCOPE_API_KEY\n"
                "  OPENAI_API_KEY"
            )

        # 创建 OpenAI 兼容客户端（DeepSeek/阿里都兼容 OpenAI SDK）
        self.client = OpenAI(api_key=api_key, base_url=base_url)

        # 如果没有指定模型，使用默认模型
        self.model = model or default_model
        self.max_iterations = max_iterations
        self.messages = []

    def run(self, user_input: str) -> str:
        """执行 Agent 主循环"""
        # 系统提示词：明确告诉 LLM 它的角色和行为规范
        system_prompt = """你是一个智能助手，可以帮助用户查询天气、计算 BMI 等。
当需要外部信息时，请调用工具。请用中文回答。"""

        self.messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_input}
        ]

        for i in range(self.max_iterations):
            print(f"\n--- 第 {i + 1} 轮迭代 ---")

            # 调用 LLM
            response = self.client.chat.completions.create(
                model=self.model,
                messages=self.messages,
                tools=TOOLS_SCHEMA,
                tool_choice="auto"  # 让模型自己决定是否调用工具
            )

            message = response.choices[0].message

            # 把助手的回复加入历史
            self.messages.append({
                "role": "assistant",
                "content": message.content or "",
                "tool_calls": [tc.model_dump() for tc in message.tool_calls] if message.tool_calls else []
            })

            # 情况 1：LLM 直接回答了（没有 tool_calls）
            if not message.tool_calls:
                print(f"[最终回答] {message.content}")
                return message.content

            # 情况 2：LLM 要求调用工具
            print(f"[思考] LLM 决定调用工具...")
            for tool_call in message.tool_calls:
                func_name = tool_call.function.name
                func_args = json.loads(tool_call.function.arguments)

                print(f"[行动] 调用工具: {func_name}({func_args})")

                # 执行工具
                if func_name in TOOL_REGISTRY:
                    result = TOOL_REGISTRY[func_name](**func_args)
                else:
                    result = f"错误：未知工具 '{func_name}'"

                print(f"[观察] 工具返回: {result}")

                # 将工具结果加入历史（role=tool）
                self.messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": str(result)
                })

        return "达到最大迭代次数，未能完成回答。"


# ========================
# 第四步：运行测试
# ========================

if __name__ == "__main__":
    print("=" * 50)
    print("【测试 1】查询天气 —— 单工具调用")
    print("=" * 50)
    agent = ReActAgent()
    result = agent.run("深圳今天天气怎么样？")

    print("\n" + "=" * 50)
    print("【测试 2】BMI 计算 —— 需要提取参数并调用工具")
    print("=" * 50)
    agent2 = ReActAgent()
    result2 = agent2.run("我体重 70kg，身高 175cm，帮我算一下 BMI")

    print("\n" + "=" * 50)
    print("【测试 3】无需工具 —— 直接回答")
    print("=" * 50)
    agent3 = ReActAgent()
    result3 = agent3.run("什么是人工智能？")

"""
【面试追问准备】

Q: 为什么要限制 max_iterations？
A: 防止 Agent 陷入死循环（比如工具一直返回错误，LLM 一直重试）。

Q: tool_choice="auto" 是什么意思？
A: 让 LLM 自己决定是生成文本回答还是输出工具调用。也可以设为 "none"（禁止调用）或指定具体工具。

Q: 为什么工具返回要加 role="tool"？
A: 这是 OpenAI 规范要求的，让 LLM 知道"这是工具执行的结果"，便于下一轮推理。

Q: 怎么支持一次调用多个工具？
A: 遍历 message.tool_calls 列表，并行执行多个工具，然后把每个结果都加入历史。
"""

`

# 02_Harness代码实践_Subagent与DispatchMap

> 来源: AI Agent面试实践/07_Harness工程深入/02_Harness代码实践_Subagent与DispatchMap.py

`python
"""
【面试加分项】Harness 工程核心模式 —— Subagent 隔离 + Dispatch Map

来源：从 learn-claude-code (s02 + s04) 提炼

学习目标：
1. 掌握 Dispatch Map 模式（解耦工具注册与循环逻辑）
2. 掌握 Subagent 上下文隔离设计
3. 理解"模型做决策，代码只执行"的 Harness 哲学

运行前准备：
- pip install openai
- 设置环境变量：DEEPSEEK_API_KEY 或 DASHSCOPE_API_KEY
"""

import json
import os
from openai import OpenAI


# ============================================================================
# 第一步：Dispatch Map 模式 —— 工具注册表
# ============================================================================
# 核心思想：用一个字典把工具名映射到处理函数
# 好处：新增工具只需加一行，循环代码完全不用改
#
# 类比：餐厅的点餐系统
#   - 顾客（模型）说"我要宫保鸡丁"（工具名 + 参数）
#   - 系统查菜单（Dispatch Map），找到负责做这道菜的厨师（handler）
#   - 厨师做菜，把成品送回顾客
#   - 新增菜品？只要在菜单上加一行，厨房不用重新装修

# ===== 工具实现 =====
# 每个工具都是"原子操作"：做一件事，做好一件事

def run_bash(command: str) -> str:
    """执行 Shell 命令"""
    import subprocess
    # 安全拦截：防止危险命令
    dangerous = ["rm -rf /", "sudo", "shutdown", "> /dev/"]
    if any(d in command for d in dangerous):
        return "Error: Dangerous command blocked by harness"
    try:
        r = subprocess.run(command, shell=True, capture_output=True,
                          text=True, timeout=30, cwd=os.getcwd())
        out = (r.stdout + r.stderr).strip()
        return out[:5000] if out else "(no output)"
    except subprocess.TimeoutExpired:
        return "Error: Timeout (30s)"
    except Exception as e:
        return f"Error: {e}"


def read_file(path: str, limit: int = None) -> str:
    """读取文件内容"""
    try:
        with open(path, "r", encoding="utf-8") as f:
            lines = f.readlines()
        if limit and limit < len(lines):
            lines = lines[:limit] + [f"... ({len(lines) - limit)} more lines)\n"]
        return "".join(lines)[:5000]
    except Exception as e:
        return f"Error: {e}"


def write_file(path: str, content: str) -> str:
    """写入文件"""
    try:
        os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        return f"Wrote {len(content)} bytes to {path}"
    except Exception as e:
        return f"Error: {e}"


def edit_file(path: str, old_text: str, new_text: str) -> str:
    """替换文件中的指定文本"""
    try:
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
        if old_text not in content:
            return f"Error: Text not found in {path}"
        content = content.replace(old_text, new_text, 1)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        return f"Edited {path}"
    except Exception as e:
        return f"Error: {e}"


# ===== Dispatch Map —— 核心设计 =====
# 面试要点：这就是"注册表模式"，解耦工具定义和循环逻辑

TOOL_HANDLERS = {
    "bash":       lambda **kw: run_bash(kw["command"]),
    "read_file":  lambda **kw: read_file(kw["path"], kw.get("limit")),
    "write_file": lambda **kw: write_file(kw["path"], kw["content"]),
    "edit_file":  lambda **kw: edit_file(kw["path"], kw["old_text"], kw["new_text"]),
}

# 如果想新增一个工具，比如 "grep_search"：
# 1. 写个 run_grep 函数
# 2. 在 TOOL_HANDLERS 中加一行："grep_search": lambda **kw: run_grep(kw["pattern"])
# 3. 在 TOOLS_SCHEMA 中加对应的 JSON Schema
# 4. 循环代码完全不用改！这就是 Dispatch Map 的威力


# ============================================================================
# 第二步：Subagent —— 上下文隔离
# ============================================================================
# 核心思想：派一个"实习生"去完成子任务，只拿结果报告，不看过程草稿
#
# 类比：项目经理（主 Agent）派实习生（Subagent）去调研竞品
#   - 实习生有自己的笔记本（独立的 messages[]），记录调研过程
#   - 调研完了，实习生销毁自己的笔记本（子 Agent 上下文丢弃）
#   - 只交给经理一份 2 页的报告（summary）
#   - 经理的笔记本（主 Agent 上下文）永远干净

# Subagent 的系统提示词（更专注，不需要知道主任务的全貌）
SUBAGENT_SYSTEM = """你是一个专注的助手。请完成给定的任务，
然后提供一个简洁的总结（不超过200字），说明你做了什么和结果是什么。
不要解释过程，只给出最终答案和关键发现。"""


def create_client():
    """创建 LLM 客户端（支持多提供商）"""
    if os.getenv("DEEPSEEK_API_KEY"):
        return OpenAI(
            api_key=os.getenv("DEEPSEEK_API_KEY"),
            base_url="https://api.deepseek.com/v1"
        ), "deepseek-chat"
    elif os.getenv("DASHSCOPE_API_KEY"):
        return OpenAI(
            api_key=os.getenv("DASHSCOPE_API_KEY"),
            base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
        ), "qwen3-max"
    else:
        raise ValueError("请设置 DEEPSEEK_API_KEY 或 DASHSCOPE_API_KEY")


client, MODEL = create_client()


# Subagent 可用的工具（不能递归派生子 Agent，防止无限嵌套）
CHILD_TOOLS = [
    {"type": "function", "function": {
        "name": "bash", "description": "运行 shell 命令",
        "parameters": {"type": "object", "properties": {"command": {"type": "string"}}, "required": ["command"]}
    }},
    {"type": "function", "function": {
        "name": "read_file", "description": "读取文件",
        "parameters": {"type": "object", "properties": {"path": {"type": "string"}, "limit": {"type": "integer"}}, "required": ["path"]}
    }},
    {"type": "function", "function": {
        "name": "write_file", "description": "写入文件",
        "parameters": {"type": "object", "properties": {"path": {"type": "string"}, "content": {"type": "string"}}, "required": ["path", "content"]}
    }},
]


def run_subagent(prompt: str) -> str:
    """
    运行一个 Subagent，返回 summary

    面试要点：
    1. sub_messages 是全新的列表，不继承父 Agent 的任何上下文
    2. 子 Agent 只共享文件系统（通过磁盘协作），不共享对话历史
    3. 安全限制：最多循环 20 次，防止无限循环
    4. 只返回最终文本，中间的工具调用结果全部丢弃
    """
    sub_messages = [{"role": "user", "content": prompt}]

    # 安全限制：最多 20 轮迭代
    for i in range(20):
        response = client.chat.completions.create(
            model=MODEL,
            messages=[{"role": "system", "content": SUBAGENT_SYSTEM}] + sub_messages,
            tools=CHILD_TOOLS,
            max_tokens=4000,
        )

        msg = response.choices[0].message
        sub_messages.append({"role": "assistant", "content": msg.content or "",
                              "tool_calls": [tc.model_dump() for tc in msg.tool_calls] if msg.tool_calls else []})

        # 如果没有工具调用，子 Agent 完成任务，返回总结
        if not msg.tool_calls:
            return msg.content or "(no summary)"

        # 执行工具调用
        results = []
        for tc in msg.tool_calls:
            handler = TOOL_HANDLERS.get(tc.function.name)
            if handler:
                try:
                    args = json.loads(tc.function.arguments)
                    output = handler(**args)
                except Exception as e:
                    output = f"Error: {e}"
            else:
                output = f"Unknown tool: {tc.function.name}"
            results.append({"role": "tool", "tool_call_id": tc.id, "content": str(output)})

        sub_messages.extend(results)

    return "(Subagent reached max iterations)"


# ============================================================================
# 第三步：主 Agent（带 Subagent 调度）
# ============================================================================

# 主 Agent 的系统提示词（更宏观，负责任务规划和子 Agent 调度）
MAIN_SYSTEM = """你是一个智能项目管理助手。你可以：
1. 直接调用工具完成任务
2. 当任务较复杂时，使用 task 工具委派给子 Agent
3. 子 Agent 完成后，根据结果继续推进主任务

使用 task 工具的场景：
- 需要探索未知代码库
- 需要完成独立的子任务（如生成测试用例、写文档）
- 当前上下文已经很长，想保持干净
"""

# 主 Agent 的工具 = 所有基础工具 + task（委派子 Agent）
PARENT_TOOLS = CHILD_TOOLS + [
    {"type": "function", "function": {
        "name": "task",
        "description": "委派子 Agent 完成独立任务。子 Agent 有独立的上下文，只返回总结。",
        "parameters": {"type": "object", "properties": {
            "prompt": {"type": "string", "description": "给子 Agent 的详细任务描述"},
            "description": {"type": "string", "description": "任务的简短描述（用于日志）"}
        }, "required": ["prompt"]}
    }},
]


def agent_loop(user_input: str):
    """
    主 Agent 循环

    面试要点：
    1. 这是 s01 + s02 + s04 的组合实现
    2. 循环结构永远不变：LLM → check tool_calls → execute → loop
    3. 新增工具或能力只需要：加 handler + 加 schema，循环不动
    """
    messages = [
        {"role": "system", "content": MAIN_SYSTEM},
        {"role": "user", "content": user_input}
    ]

    for i in range(10):  # 安全上限
        print(f"\n--- 主 Agent 第 {i+1} 轮 ---")

        response = client.chat.completions.create(
            model=MODEL, messages=messages,
            tools=PARENT_TOOLS, max_tokens=4000,
        )

        msg = response.choices[0].message
        messages.append({"role": "assistant", "content": msg.content or "",
                          "tool_calls": [tc.model_dump() for tc in msg.tool_calls] if msg.tool_calls else []})

        # 如果没有工具调用，直接返回答案
        if not msg.tool_calls:
            print(f"[最终回答] {msg.content}")
            return msg.content

        # 执行工具调用
        results = []
        for tc in msg.tool_calls:
            if tc.function.name == "task":
                # ===== 关键：Subagent 调度 =====
                args = json.loads(tc.function.arguments)
                desc = args.get("description", "subtask")
                prompt = args["prompt"]
                print(f"\n[Subagent 调度] {desc}")
                print(f"  任务: {prompt[:100]}...")
                # 派生子 Agent，只拿 summary
                output = run_subagent(prompt)
                print(f"  结果: {output[:200]}...")
            else:
                # 普通工具，直接执行
                handler = TOOL_HANDLERS.get(tc.function.name)
                if handler:
                    try:
                        args = json.loads(tc.function.arguments)
                        output = handler(**args)
                    except Exception as e:
                        output = f"Error: {e}"
                else:
                    output = f"Unknown tool: {tc.function.name}"
                print(f"[{tc.function.name}] {str(output)[:200]}")

            results.append({"role": "tool", "tool_call_id": tc.id, "content": str(output)})

        messages.extend(results)

    return "达到最大迭代次数"


# ============================================================================
# 测试
# ============================================================================

if __name__ == "__main__":
    print("=" * 50)
    print("Harness 工程实践：Dispatch Map + Subagent 隔离")
    print("=" * 50)

    # 测试 1：简单任务（直接工具调用）
    print("\n【测试 1】直接调用工具：查看当前目录")
    result = agent_loop("请用 bash 命令列出当前目录下的所有文件和文件夹")

    # 测试 2：复杂任务（Subagent 调度）
    print("\n" + "=" * 50)
    print("【测试 2】委派子 Agent：分析项目结构")
    print("=" * 50)
    result2 = agent_loop(
        "请分析当前项目的代码结构。\n"
        "先用 task 工具让一个子 Agent 去查看所有 Python 文件的名字和大致内容，\n"
        "然后你根据子 Agent 的报告，总结这个项目是做什么的。"
    )

    print("\n" + "=" * 50)
    print("测试完成")
    print("=" * 50)

"""
【面试追问准备】

Q: 为什么要用 Dispatch Map 而不是 if-else 链？
A: Dispatch Map 解耦了工具定义和循环逻辑。新增工具只需在 Map 中加一行，
   循环代码完全不用改，符合开闭原则。if-else 链每加一个工具就要改循环。

Q: Subagent 和主 Agent 共享什么？隔离什么？
A: 共享文件系统（通过磁盘协作），隔离对话历史（独立的 messages[]）。
   子 Agent 的中间过程和工具调用结果不传给父 Agent，只返回 summary。

Q: 子 Agent 为什么不能递归派生子 Agent？
A: CHILD_TOOLS 中没有 task 工具，防止无限嵌套。生产环境中可以设置嵌套深度限制。

Q: 这个模式和 LangGraph 的 Subgraph 有什么区别？
A: 这是简化版的手动实现。LangGraph 的 Subgraph 是声明式的，自动管理状态传递。
   这个实现更底层，展示了"隔离"的核心原理。

Q: Harness 工程师和提示词工程师的区别？
A: 提示词工程师优化输入文本让模型输出更好；Harness 工程师构建环境让模型能自主行动。
   前者是"教模型说话"，后者是"给模型手脚和眼睛"。
"""

`
`

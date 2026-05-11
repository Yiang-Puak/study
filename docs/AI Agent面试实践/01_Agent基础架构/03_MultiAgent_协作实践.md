# 03_MultiAgent_协作实践

> 来源: AI Agent面试实践/01_Agent基础架构/03_MultiAgent_协作实践.py

`python
"""
【面试加分项】Multi-Agent 多智能体协作 —— 代码实践

学习目标：
1. 理解 Multi-Agent 的角色分工与通信机制
2. 掌握"主从协调"模式的设计思路
3. 能手撕一个多 Agent 协作示例

场景设计：
- 研究员 Agent：负责信息检索和分析
- 写手 Agent：负责撰写最终报告
- 审核员 Agent：负责检查报告质量

运行前准备：pip install openai
"""

import json
import os
from openai import OpenAI


# ========================
# 第一步：定义不同角色的 Agent
# ========================

class BaseAgent:
    """Agent 基类 —— 面试要点：封装共性，解耦差异"""

    def __init__(self, name: str, role: str, model: str = "qwen3-max"):
        self.name = name
        self.role = role
        self.client = OpenAI(
            api_key=os.getenv("DASHSCOPE_API_KEY"),
            base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
        )
        self.model = model
        self.memory = []  # 短期记忆：对话历史

    def think(self, task: str, context: str = "") -> str:
        """接收任务 + 上下文，返回思考结果"""
        messages = [
            {"role": "system", "content": self.role},
            {"role": "user", "content": f"任务：{task}\n上下文：{context}\n请完成你的职责。"}
        ]

        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages
        )
        result = response.choices[0].message.content

        # 记录到记忆
        self.memory.append({"task": task, "result": result})
        return result


class ResearchAgent(BaseAgent):
    """研究员 Agent：擅长搜索和分析信息"""

    def __init__(self):
        super().__init__(
            name="研究员",
            role="""你是一位专业研究员，擅长从杂乱信息中提取关键点。
你的输出格式必须是 JSON：
{
  "key_points": ["要点1", "要点2", ...],
  "analysis": "简要分析",
  "sources": ["信息来源或依据"]
}
只输出 JSON，不要额外解释。"""
        )

    def research(self, topic: str) -> dict:
        """模拟研究过程 —— 实际项目中这里会调用搜索引擎/数据库"""
        # 模拟知识库
        knowledge = {
            "AI Agent": {
                "key_points": [
                    "Agent = LLM + 记忆 + 工具 + 规划",
                    "ReAct 是 thought-action-observation 循环",
                    "Multi-Agent 通过消息传递协作"
                ],
                "analysis": "AI Agent 是 2024-2026 年大模型落地的核心方向",
                "sources": ["LangChain 官方文档", "ReAct 论文"]
            },
            "RAG": {
                "key_points": [
                    "RAG = 检索 + 增强 + 生成",
                    "Embedding 质量决定检索效果",
                    "混合检索（语义+关键词）效果更好"
                ],
                "analysis": "RAG 解决了 LLM 知识时效性和幻觉问题",
                "sources": ["RAG Survey 2024", "LlamaIndex 文档"]
            }
        }

        # 先用 LLM 分析，再结合模拟数据
        raw = self.think(f"请研究主题：{topic}", "请提取关键要点")

        # 如果 LLM 返回了有效 JSON，解析它；否则用模拟数据兜底
        try:
            result = json.loads(raw)
        except json.JSONDecodeError:
            result = knowledge.get(topic, {
                "key_points": ["暂无详细数据"],
                "analysis": "需要更多研究",
                "sources": []
            })

        return result


class WriterAgent(BaseAgent):
    """写手 Agent：擅长将研究内容整理成报告"""

    def __init__(self):
        super().__init__(
            name="写手",
            role="""你是一位技术文档写手，擅长将研究要点整理成结构化的中文报告。
报告格式：
## 标题
### 核心要点
- 要点...
### 分析
...
### 参考资料
...
请确保内容专业、简洁、有条理。"""
        )

    def write(self, research_result: dict) -> str:
        """根据研究结果撰写报告"""
        context = json.dumps(research_result, ensure_ascii=False, indent=2)
        return self.think("将以下研究内容整理成报告", context)


class ReviewerAgent(BaseAgent):
    """审核员 Agent：检查报告质量并提出修改建议"""

    def __init__(self):
        super().__init__(
            name="审核员",
            role="""你是一位技术文档审核员，负责检查报告质量。
你需要评估：
1. 内容准确性（要点是否正确）
2. 结构完整性（是否有标题、要点、分析、参考资料）
3. 语言流畅度

输出格式必须是 JSON：
{
  "score": 85,
  "issues": ["问题1", "问题2"],
  "suggestions": ["建议1", "建议2"],
  "passed": true/false
}
只输出 JSON。"""
        )

    def review(self, report: str) -> dict:
        """审核报告并返回评分和建议"""
        raw = self.think("请审核以下报告", report)
        try:
            return json.loads(raw)
        except json.JSONDecodeError:
            return {
                "score": 80,
                "issues": ["JSON 解析失败，假设通过"],
                "suggestions": [],
                "passed": True
            }


# ========================
# 第二步：主协调器（Orchestrator）
# ========================
# 面试要点：为什么需要 Orchestrator？
# —— 解耦 Agent 之间的直接依赖，由中央协调器分配任务、传递消息

class MultiAgentOrchestrator:
    """多 Agent 协调器 —— 实现"任务分发 → 执行 → 审核 → 输出"的流水线"""

    def __init__(self):
        self.researcher = ResearchAgent()
        self.writer = WriterAgent()
        self.reviewer = ReviewerAgent()

    def run(self, topic: str) -> dict:
        """执行完整的多 Agent 协作流程"""
        print(f"\n{'=' * 50}")
        print(f"🎯 任务启动：撰写《{topic}》技术报告")
        print(f"{'=' * 50}")

        # Stage 1: 研究
        print(f"\n📚 [研究员] 正在研究主题...")
        research = self.researcher.research(topic)
        print(f"✅ 研究完成：{json.dumps(research, ensure_ascii=False, indent=2)}")

        # Stage 2: 撰写
        print(f"\n✍️ [写手] 正在撰写报告...")
        report = self.writer.write(research)
        print(f"✅ 报告完成：\n{report}")

        # Stage 3: 审核
        print(f"\n🔍 [审核员] 正在审核报告...")
        review = self.reviewer.review(report)
        print(f"✅ 审核完成：{json.dumps(review, ensure_ascii=False, indent=2)}")

        # Stage 4: 如果审核不通过，反馈给写手修改（一轮迭代）
        if not review.get("passed", True):
            print(f"\n🔄 [写手] 根据审核意见修改报告...")
            feedback = json.dumps(review, ensure_ascii=False)
            report = self.writer.write({
                "original": research,
                "feedback": feedback
            })
            print(f"✅ 修改完成：\n{report}")

        return {
            "topic": topic,
            "research": research,
            "report": report,
            "review": review
        }


# ========================
# 第三步：运行测试
# ========================

if __name__ == "__main__":
    orchestrator = MultiAgentOrchestrator()

    # 测试：让三个 Agent 协作完成一份报告
    result = orchestrator.run("AI Agent")

    print(f"\n{'=' * 50}")
    print("📋 最终输出")
    print(f"{'=' * 50}")
    print(result["report"])

"""
【面试追问准备】

Q: Multi-Agent 怎么避免循环依赖？
A: 通过中央协调器（Orchestrator）模式，Agent 之间不直接通信，
   所有消息都经过协调器转发，由协调器控制流程。

Q: Agent 之间怎么共享状态？
A: 常见方案：1）共享状态池（Shared State）；2）消息队列；
   3）LangGraph 的 StateGraph 机制。

Q: 和 LangGraph 的多 Agent 有什么区别？
A: LangGraph 用图结构（节点=Agent，边=流转条件）定义协作流程，
   支持条件分支和循环，适合复杂工作流。
   上面的示例是简化版 Pipeline 模式，适合线性任务链。

Q: 实际生产中 Multi-Agent 的难点？
A: 1）状态一致性问题；2）循环调用控制；3）错误传播隔离；
   4）Token 成本爆炸（多 Agent × 多轮对话）。
"""

`

# 02 | Agent Skill 定制行为指南

## 一句话定义

Agent Skill 是一组可复用的行为指南，通常包含 Prompt、工具集合、工作流、约束条件和输出规范。Tool 解决“能做什么”，Skill 解决“怎么把一组能力按正确流程做好”。

---

## Skill 和 Tool 的区别

| 对比项 | Tool | Agent Skill |
|--------|------|-------------|
| 本质 | 单个外部能力接口 | 可复用行为流程 |
| 粒度 | 较小 | 较大 |
| 组成 | 函数名、描述、参数、执行逻辑 | Prompt、Workflow、Tools、Rules、Examples |
| 例子 | `search_web(query)` | “写技术调研报告”Skill |
| 解决问题 | 让模型能执行动作 | 让模型稳定完成一类任务 |

---

## Skill 的组成

| 组成 | 说明 |
|------|------|
| Name | Skill 名称，如 `code_review` |
| Description | Skill 适用场景 |
| Trigger | 什么时候应该启用该 Skill |
| Workflow | 执行步骤 |
| Tool Set | 可使用的工具集合 |
| Constraints | 不能做什么、安全边界 |
| Output Format | 输出格式要求 |
| Examples | 少量高质量示例 |
| Evaluation | 如何判断 Skill 执行成功 |

---

## 示例：代码审查 Skill

```text
Name: code_review
Description: 当用户要求审查代码质量、安全性或性能问题时启用。
Workflow:
  1. 读取相关文件和调用链
  2. 理解业务目标
  3. 检查正确性、边界条件、安全、性能
  4. 给出按严重程度排序的问题
  5. 提供最小修改建议
Tools:
  - read_file
  - grep_search
  - run_tests
Constraints:
  - 不直接大规模重写代码
  - 不暴露密钥
  - 不删除用户代码
Output:
  - 问题列表
  - 风险等级
  - 建议修复方案
```

---

## Skill 路由

Agent 可以根据用户意图选择不同 Skill：

| 用户请求 | 应选择 Skill |
|----------|--------------|
| “帮我看这段代码有没有问题” | code_review |
| “帮我写部署文档” | deployment_doc |
| “帮我重构这个模块” | refactor_planning |
| “帮我学习 RAG” | study_tutor |

路由策略可以是：

- 规则匹配
- Embedding 相似度
- LLM 分类
- 多策略融合

---

## Skill 工程化管理

| 主题 | 做法 |
|------|------|
| 注册中心 | 统一存储 Skill 名称、描述和版本 |
| 版本管理 | Skill 更新后保留旧版本，防止行为漂移 |
| 评估集 | 为每个 Skill 准备典型任务和评分标准 |
| 日志追踪 | 记录 Skill 触发、工具调用、结果质量 |
| 权限控制 | 不同 Skill 允许的工具集合不同 |

---

## 面试答题模板

**问题：Agent Skill 和 Tool 有什么区别？如何设计 Skill？**

1. **核心定义**：Tool 是单个外部能力，Skill 是完成一类任务的可复用行为流程。
2. **边界区别**：Tool 解决“能不能做”，Skill 解决“怎么稳定做好”。
3. **组成部分**：Skill 通常包含触发条件、Prompt、Workflow、可用工具、约束、输出格式和示例。
4. **工程实现**：用 Skill Registry 统一管理，通过规则、Embedding 或 LLM 分类进行路由。
5. **生产优化**：对 Skill 做版本管理、日志追踪和评估集测试，避免更新后行为漂移。

---

## 自检清单

- [ ] 能解释 Tool 与 Skill 的区别
- [ ] 能设计一个 Skill 的组成结构
- [ ] 能说明 Skill 如何路由和版本管理
- [ ] 能说出 Skill 评估指标

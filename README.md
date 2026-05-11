# AI 面试冲刺手册

> Python、AI Agent、Git 面试学习材料 —— 基于 MkDocs Material 构建的静态站点

## 在线访问

**https://Yiang-Puak.github.io/study/**

支持手机、iPad、电脑自适应浏览，支持深色/浅色模式切换和全文搜索。

## 内容结构

- **AI Agent 面试实践**
  - Agent 基础架构（ReAct、MultiAgent）
  - 记忆系统
  - RAG 检索增强
  - LangChain / LangGraph
  - 模型微调与性能优化
  - Prompt 工程与 AI 编程工具
  - Harness 工程深入
  - 综合模拟面试题库

- **Python 面试实践**
  - 零基础入门（变量、循环、函数等）
  - Python 语言特性
  - 数据结构与常用库
  - 面试高频手撕题（滑动窗口、快排、LRU、TopK、DP 等）
  - Python 进阶面试题

- **Git 面试实践**
  - 核心概念与面试答题模板
  - Git 进阶与实战

## 本地预览

```bash
pip install mkdocs-material mkdocs-minify-plugin
cd "面试学习文件夹"
mkdocs serve
```

浏览器打开 `http://127.0.0.1:8000/`。

## 自动部署

本仓库配置了 GitHub Actions，每次 `git push` 到 `main` 分支后自动构建并部署到 GitHub Pages，无需手动操作。

## 技术栈

- [MkDocs](https://www.mkdocs.org/)
- [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/)
- GitHub Actions + GitHub Pages

## 更新记录

- 2026-05-11: 初始化站点，整合 AI Agent、Python、Git 面试学习材料

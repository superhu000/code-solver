---
name: code-solver
description: 算法解题与代码审查。支持 solve（fast/detail 两种模式）和 review 两个子命令，生成可直接运行的代码并归档。
---

# Solving Algorithms

两个子命令：`solve` 解题、`review` 审查代码。

## 命令格式

```bash
/solving-algorithms solve [fast|detail] <题目输入> [语言]
/solving-algorithms review <代码或报错>
```

### solve — 解题

```bash
/solving-algorithms solve leetcode 206 java              # fast 模式（默认），最佳解法
/solving-algorithms solve detail leetcode 1 java         # detail 模式，暴力+最优多方案对比
/solving-algorithms solve [粘贴原题文本]                   # 默认 fast + java
/solving-algorithms solve detail [粘贴原题文本] python     # detail 模式 + python
```

| 模式 | 说明 |
|------|------|
| fast | 快速生成简洁题解，再生产可执行代码 |
| detail |生成结构化详细题解， 暴力+最优多方案对比，再生成代码，含测试代码文件，用例优先使用官方样例 |

### review — 代码审查

```bash
/code-solver review [粘贴代码]
/code-solver review 这段代码报了空指针错误 [粘贴代码]
```

分析代码问题，发现知识盲点，推荐学习资料和巩固题型。

## 工作流程

```
① resolve 获取归档路径 → 第一轮：生成题解（含核心逻辑代码）→ Write 题解到 archiveDir（用户可读）
② 第二轮：生成完整代码 → Write 代码（+测试）到 archiveDir/src/
```

模型先调用 resolve 获取归档路径（脚本自动创建目录），然后生成完整题解 Markdown（含核心逻辑代码）直接 Write 到归档目录（用户立刻可读）。第二轮直接将完整代码 Write 到 archiveDir/src/。不暂存不移动，题解和代码分两轮生成，不编译、不执行、不读模板。

---
以下为输入命令：
```bash
/code-solver $ARGUMENTS
```

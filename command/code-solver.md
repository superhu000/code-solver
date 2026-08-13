---
name: code-solver
description: 快速生成算法题解与代码、审查用户代码，或创建每日一题和专项训练计划。
---

# Code Solver

当前版本由仓库根目录 VERSION 定义；运行行为以 skill/code-solver/SKILL.md 为准。

将 $ARGUMENTS 交给 skill/code-solver/SKILL.md 执行。

## 命令

```text
/code-solver solve [fast|detail] <题目或链接> [语言]
/code-solver review [--rules <规范路径>] <代码或报错>
/code-solver train daily [天数] [目标或要求]
/code-solver train drill <专题> [题数] [目标或要求]
/code-solver train submit <代码或做题描述>
/code-solver train summary
```

省略模式时使用 fast，省略语言时使用 java。

## 执行约束

- fast：先生成并归档简洁题解，再生成可运行代码。
- detail：先生成并归档详细题解，再生成代码与测试代码。
- review：只读取一个最高优先级规范源；用户上传或指定的规范优先。
- train：仅训练路径读取训练规则；计划优先复用已有题解和公开教学链接。
- 当前题已有题解和代码直接引用；缺少归档时在同一次任务内复用 solve。
- 不创建临时文件，不回读刚写入的题解或代码。
- 不编译、不运行、不在终端验证生成代码；由用户自行测试。

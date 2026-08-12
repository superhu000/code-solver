# code-solver

> 轻量算法解题、代码审查与训练 Skill：先交付题解，再生成用户可运行的代码；不编译、不执行。

## 模式

| 模式 | 第一产物 | 第二产物 | 额外产物 |
|---|---|---|---|
| `solve fast` | 简洁题解 | 可运行解题代码 | 无 |
| `solve detail` | 详细题解 | 可运行解题代码 | 可运行测试代码 |
| `review` | 按规范生成审查结果 | 按需给出修改建议 | 无 |
| `train daily` | 个性化每日一题计划 | 今日题目与资料 | 计划总结 |
| `train drill` | 单一专题递进计划 | 专题题目与资料 | 专题总结 |

默认使用 `fast + Java 17 + 中文`。

## 核心原则

1. **题解优先**：模型按内置模板一次生成完整题解，立即写入最终归档目录。
2. **两轮生成**：fast 为“题解 → 代码”；detail 为“题解 → 代码与测试代码”。
3. **最少读写**：不生成临时文件，不回读已写产物，不在 solve 流程加载 Review 规范或 Spec。
4. **不编译不执行**：Skill 不在终端编译、运行或修复生成代码，由用户自行验证。
5. **官方样例优先**：detail 测试代码优先使用题面中的官方样例，再补必要边界用例。
6. **规范可覆盖**：review 支持本次上传、指定路径、项目级和内置四级代码规范。
7. **训练复用**：计划优先引用已有题解；领取题目时缺少归档才复用 solve 生成题解与代码。

## 使用

```text
/code-solver solve leetcode 206 java
/code-solver solve detail leetcode 1 java
/code-solver solve <粘贴题面> python
/code-solver review <粘贴代码或报错>
/code-solver review --rules <规范文件路径> <代码>
/code-solver train daily 30 <目标或要求>
/code-solver train drill sliding-window 10
/code-solver train submit <代码或做题描述>
/code-solver train summary
```

## 归档

新归档采用扁平目录，减少建目录和查找开销：

```text
code-solver-workspace/
└── <平台>/<中文题型>/<题号>-<题名>-<语言>/
    ├── 题解.md              # solve
    ├── Main.java            # 或 solution.py/.c/.cpp/.ts
    └── Test.java            # 仅 detail；其他语言使用对应测试文件名
```

review 写入 `审查.md`。旧归档不迁移、不扫描，新结果直接使用新结构。

训练计划保存到 `code-solver-workspace/training/`。计划大纲、进度和总结只引用原题解，用户代码单独保存在计划目录的 `submissions/`。

## 项目结构

```text
code-solver/
├── command/code-solver.md
├── skill/code-solver/
│   ├── SKILL.md
│   ├── references/
│   │   ├── training.md
│   │   └── review-rules.md
│   └── scripts/
│       ├── archive.py
│       ├── training.py
│       └── training_store.py
└── spec/versions/
    ├── 0.13.0-lightweight-pipeline.md
    └── 0.14.0-training-plans.md
```

## 版本

当前版本：**0.14.0**。训练计划增量见
[`spec/versions/0.14.0-training-plans.md`](spec/versions/0.14.0-training-plans.md)。

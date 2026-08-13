# Code Solver

> 面向算法学习的轻量 Skill：题解、可运行代码、代码审查与训练计划闭环。

当前正式版本：**1.0.0**（唯一版本号见 [VERSION](VERSION)）。当前行为以 [spec/CURRENT.md](spec/CURRENT.md) 为准；历史变更保存在 [spec/releases/](spec/releases/)。

## 能力

| 能力 | 命令 | 交付 |
|---|---|---|
| 快速解题 | solve fast | 简洁题解 + 可运行单文件代码 |
| 深度解题 | solve detail | 详细题解 + 代码 + 独立测试代码 |
| 代码审查 | review | 按最高优先级规则给出证据化问题与最小修改 |
| 每日一题 | train daily | 个性化计划、当日题目、进度与总结 |
| 专项训练 | train drill | 由易到难的专题计划、进度与专题总结 |

默认使用 fast + Java 17 + 中文。

## 使用

```text
/code-solver solve leetcode 206 java
/code-solver solve detail leetcode 1 java
/code-solver review <代码或报错>
/code-solver train daily 30 <目标>
/code-solver train drill sliding-window 7
/code-solver train submit <代码或做题描述>
/code-solver train summary
```

## 关键边界

- 先归档题解，再生成代码；不创建临时产物，也不回读刚写入的产物。
- 生成代码为标准库、单文件且带运行入口；Skill 不编译、不运行、不自动修复。
- review 只采用一个最高优先级规范源。
- 训练优先引用已有题解；仅当当前题缺少归档时，复用内部 solve 流程补齐。
- 不在计划中复制题面、官方题解或付费教学内容。

## 仓库结构

```text
code-solver/
├── VERSION
├── README.md
├── command/code-solver.md
├── skill/code-solver/
│   ├── SKILL.md
│   ├── references/
│   └── scripts/
└── spec/
    ├── CURRENT.md
    ├── CHANGELOG.md
    ├── README.md
    ├── releases/
    └── templates/
```

## Spec 与发布

新增或修改功能时，先更新 spec/CURRENT.md，再同步 README、命令入口与运行时 Skill，并执行：

```bash
python skill/code-solver/scripts/check_docs.py
```

该检查只验证文档约定、版本号与路径引用，不运行算法代码或训练脚本。详细流程见 [spec/README.md](spec/README.md)。

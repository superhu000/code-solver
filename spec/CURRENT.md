# Code Solver 1.0.0 当前 Spec

- 状态：当前生效
- 发布日期：2026-08-13
- 版本来源：仓库根目录 VERSION
- 运行时入口：command/code-solver.md → skill/code-solver/SKILL.md
- 历史基线：0.13.0 解题/审查流水线、0.14.0 训练计划

## 目标与范围

Code Solver 提供 solve、review、每日一题与专项训练，帮助用户形成“识别题型 → 选择方法 → 写出代码 → 记录复盘”的闭环。本文件是当前行为的唯一功能契约；README、命令入口和运行时 Skill 必须与之同步。

## 命令契约

| 命令 | 默认值 | 必须交付 |
|---|---|---|
| solve fast <题目> [语言] | Java 17、中文 | 题解.md → 可运行代码 |
| solve detail <题目> [语言] | Java 17、中文 | 详细题解 → 代码 + 独立测试代码 |
| review [--rules 路径] <代码或报错> | 内置规则 | 审查.md，按需修订代码 |
| train daily [days] [goal] | 30 天、每天一题 | 计划、今日题、进度、总结 |
| train drill <topic> [count] [goal] | 7 题 | 专项计划、当前题、进度、专题总结 |
| train submit <代码或描述> | 最近激活计划 | 静态评估与进度记录 |
| train summary | 最近激活计划 | 当前计划总结 |

## 核心行为

### Solve

1. 仅一次解析题目与归档路径。
2. 第一轮生成完整题解并直接写入最终目录。
3. 第二轮生成最终代码；detail 同一轮生成解题代码与测试代码。
4. 不创建临时文件、不回读产物、不读取 Spec、不编译或运行代码。
5. 代码使用标准库、单文件、可运行入口；detail 测试优先题面官方样例，只补必要边界。

### Review

规则只采用最高优先级的一份：本次上传/粘贴 → --rules → <project>/.code-solver/review-rules.md → 内置规则。输出包含位置、证据、影响、最小修改与优先级；无证据不报问题。

### Training

- 创建计划时只扫描一次既有题解；精确题号存在题解与代码时直接关联，绝不复制。
- 当前题缺少任一归档时，在同一次任务内复用 solve 补齐；不递归调用命令或 Skill。
- 用户代码只做一次静态评估，最多两个关键问题；文字描述必须标为用户自述。
- 状态仅为 completed、partial、blocked、skipped。daily 当天完成后不提前发下一题；drill 可继续。
- 总结只读取本计划的进度和已关联笔记；专项总结额外含识别信号、通用步骤、边界清单和代表题阶梯。

## 数据与归档

code-solver-workspace/
- <平台>/<中文题型>/<题号>-<题名>-<语言>/：题解.md（review 为 审查.md）、代码、detail 测试。
- training/daily|drill/<plan>/：计划.md、state.json、进度.md、history.jsonl、总结.md、submissions/。

旧归档不迁移、不扫描。计划不复制题面、算法笔记、官方题解或付费内容。

## 性能与验收

| 模式 | 模型生成轮次 | 路径解析 | 产物回读 | 运行验证 |
|---|---:|---:|---:|---:|
| fast | 2 | 1 | 0 | 0 |
| detail | 2 | 1 | 0 | 0 |
| review | 1 | 1 | 0 | 0 |
| train | 当前题最少化 | 创建计划时一次索引 | 仅当前计划 | 0 |

- [ ] README、命令入口、SKILL 与本文件的命令、目录和版本一致。
- [ ] solve/review 不读取训练规则或 Spec。
- [ ] 完整归档存在时训练不重复生成。
- [ ] detail 不生成测试报告 Markdown。
- [ ] 新功能先更新本文件，再更新 CHANGELOG。

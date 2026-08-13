# code-solver

> 刷题秒出题解与可运行代码，自动归档，开箱即用。

code-solver 是一个 OpenCode Skill，专为算法刷题者设计。根据平台、题号或题名，自动识别题目类型、匹配算法模式，生成符合规范的多语言解题代码和 Markdown 题解，并自动分类归档，摆脱枯燥整理过程，便于后续复习与整理。

## 快速开始

**1. 安装**

将 `command/` 和 `skills/` 复制到项目根目录下的 `.opencode/`：

```bash
cp -r command  <项目根目录>/.opencode/
cp -r skills   <项目根目录>/.opencode/
```

**2. 一条命令解题**

```text
/code-solver leetcode 42 java
```

**3. 查看归档产物**

```text
code-solver-workspace/
└── leetcode/链表/206-反转链表-java/
    ├── 题解.md
    └── Main.java
```

## 特性

- **效率优先**：输入平台、题号及语言，一行指令三个参数自动帮你生成题解与代码，快速学习算法思路
- **多语言支持**：Java / Python 3 / C / C++ / TypeScript
- **三种模式**：fast 快速解题 · detail 详细题解+测试代码 · review 代码审查
- **自动归档**：按平台/题型/题号扁平目录，中文题名保留，无需手动创建与整理，摆脱痛苦的笔记过程
- **多解法对比**：detail 模式提供方案对比表，辅助理解算法取舍
- **不编译不执行**：生成即交付，由用户自行验证

## 使用指南

### 解题模式

| 模式 | 生成文件 | 适用场景 | Few-Shot |
|---|---|---|---|
| `solve fast` | 简洁题解、可运行解题代码 | 日常刷题，快速出解 | 求职者速通力扣hot100 |
| `solve detail` | 详细题解、可运行解题代码、测试代码 | 复杂难题，需要测试覆盖与方案对比 | 各大厂复杂机试题 | 
| `review` | 按规范生成审查结果、按需给出修改建议 | 代码审查与改进 | 刷题提交时不知哪里WA |

省略参数时默认使用 `solve` + `fast` + `java`。

### 命令参考

```text
/code-solver solve [fast|detail] <题源> <题号或题名> [语言]
/code-solver solve <粘贴题面> [语言]
/code-solver review [--rules <规范文件路径>] <代码或报错>
```

```
fast 模式（默认）（-f/fast 从detail回到fast，缓存模式，使用一次即可）
/code-solver solve <题源> <题号|题名|原题信息> [语言]
/code-solver solve leetcode 206 java
/code-solver solve nowcoder NC1 cpp
/code-solver solve <原题信息> java
```

```
detail 模式（-d 或 detail） 
/code-solver solve -d <题源> <题号|题名|原题信息> [语言]
/code-solver solve -d leetcode 1 python
/code-solver solve detail acwing 100 typescript
/code-solver solve -d huawei <原题信息> java
```



```
代码审查
/code-solver review <题源> <题号/题名> <粘贴代码>
/code-solver review leetcode 接雨水 <粘贴代码> cpp
/code-solver review leetcode 200 <粘贴代码> java
```

### 归档目录结构

```text
code-solver-workspace/
└── <平台>/<中文题型>/<题号>-<题名>-<语言>/
    ├── 题解.md              # solve 产物
    ├── Main.java            # 或 solution.py / solution.c / solution.cpp / solution.ts
    └── Test.java            # 仅 detail；其他语言使用对应测试文件名
```

review 模式写入 `代码审查.md`。

### 题解内容（solve）

| 段落 | fast | detail |
|---|---|---|
| 题目描述 | 1-2 句，含输入输出约定和数据范围 | 问题拆解：目标/输入输出/数据范围/复杂度上限 |
| 思路推导 | 3-5 句，覆盖题目本质、算法选择和关键状态 | 方案对比表（2-4 种，含时限可行性）+ 推荐方案充分展开（状态定义/转移方程/正确性论证，不限句数） |
| 核心代码 | 关键行附中文注释，不超过 3 处 | 推荐方案核心实现，附函数签名和弹性步骤 |
| 复杂度分析 | 时间 + 空间 | 时间 + 空间，独立成段 |
| 边界与易错点 | — | 2-4 个边界用例 + 2-5 条易错点（含溢出分析） |
| 关键点 | 1-3 条，记录关键识别信号和易错点 | 2-4 条知识沉淀（可复用模式、可迁移结论） |



### 代码审查（review）
review 模式不只是"找 bug"，而是一套从**思路到语法到成长**的完整审查闭环。

- **思路先行**：先分析算法方向是否正确、是否忽略边界，再看语法——思路对了代码才有意义
- **diff 带注释**：修改建议以 unified diff 输出，`+` 行附带注释说明改动意图，不只告诉你"改什么"还告诉你"为什么改"
- **问题逐条拆解**：每个错误点独立分析优先级、位置、证据和影响，不遗漏也不凑数
- **盲点补全**：指出语法和算法的知识缺口，推荐 2-3 道针对性练习题，并附开源项目（如 hello-algo、代码随想录）、书籍和文档等学习资源


### 代码约束

- 单文件、仅标准库、英文标识符、关键逻辑中文注释
- LeetCode 函数题也补充明确的输入约定和可运行入口
- detail 测试代码优先使用题面官方样例，再补 1~3 个必要边界
- 测试代码独立入口，不依赖 JUnit、pytest 等第三方框架
- 测试代码调用解题代码公开接口，不复制另一份算法实现


## 安装

### OpenCode（.opencode）

```bash
cp -r command  <项目根目录>/.opencode/
cp -r skills   <项目根目录>/.opencode/
```

放入后结构：

```text
<项目根目录>/.opencode/
├── command/code-solver.md
└── skills/code-solver/
    ├── SKILL.md
    ├── references/
    │   ├── fast-template.md
    │   ├── detail-template.md
    │   └── review-rules.md
    └── scripts/archive.py
```

### 环境要求

- OpenCode（用于识别 Skill 并触发 `/code-solver`）
- Python 3（archive.py 仅依赖标准库，无需 pip install）

## 项目结构

```text
code-solver/
├── command/code-solver.md              # 命令入口，转发给 SKILL.md
├── skills/code-solver/
│   ├── SKILL.md                        # 主逻辑：路由、流程、模板引用、性能预算
│   ├── references/
│   │   ├── fast-template.md            # fast 题解模板（可自定义）
│   │   ├── detail-template.md          # detail 题解模板（可自定义）
│   │   └── review-rules.md             # 默认审查规范
│   └── scripts/archive.py              # 归档脚本（resolve / list）
└── spec/versions/                      # 版本决策记录（运行时不读取）
```

## 版本

当前版本：**0.13.0**。版本决策与验收标准见
[`spec/versions/0.13.0-lightweight-pipeline.md`](spec/versions/0.13.0-lightweight-pipeline.md)。

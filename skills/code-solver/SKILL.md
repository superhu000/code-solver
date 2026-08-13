---
name: code-solver
description: 快速解答算法题并审查代码，先归档中文题解，再生成 Java、Python、C、C++ 或 TypeScript 可运行单文件；detail 额外生成可运行测试代码，review 支持用户上传或指定代码规范,生成代码审查报告。用于力扣/LeetCode平台刷题、公司题库、刷题复盘。
---

# Code Solver

## 核心契约

- 默认使用 `fast + Java 17 + 中文`。
- 始终先生成完整题解并写入最终归档，再生成代码。
- 不创建临时文件，不移动产物，不回读刚写入的文件。
- 不编译、不运行、不在终端验证或自动修复生成代码；由用户测试。
- 不读取 Spec。solve 模式不读取任何 reference 文件。
- 只在 review 模式按“Review 规范”读取一个规范源。

## 路由

| 条件 | 模式 |
|---|---|
| 包含代码、报错或明确要求检查 | `review` |
| 指定 `detail`/`-d`/详细题解/测试代码 | `detail` |
| 其他算法题 | `fast` |

仅当题面缺少决定算法或输入输出的关键信息时，一次性询问；其余信息在内存中归一化，不调用解析脚本。

## Solve 流程

### 1. 只解析一次并创建归档

从当前输入直接确定平台、题号、题名、语言和笼统题型。调用一次：

```text
python <skill_dir>/scripts/archive.py resolve \
  --project-root <project> --platform <platform> --category <category> \
  --language <language> --problem-id <id> --title <title> --mode <fast|detail>
```

只使用返回的 `note`、`code`、`test` 路径。不要再次 resolve、list 或扫描归档。

### 2. 第一轮：一次生成题解并立即写入

根据当前模式模板一次生成完整 Markdown，直接写入 `note`。不要先生成 JSON、草稿或分章节补写。

若宿主支持进度消息，写入后立即向用户显示核心思路和题解路径，再继续生成代码。

### 3. 第二轮：直接生成最终代码

复用当前上下文中的算法和核心代码，不读取 `note`：

- fast：一次生成并写入 `code`。
- detail：同一轮生成 `code` 和 `test`，分别写入两个最终路径；不要为测试再发起一轮算法推理。

完成后立即停止，不执行编译、运行、测试、诊断或修复循环。

## Fast 题解模板

```markdown
# {题名} 题解
> 平台：{platform}｜题号：{id}｜语言：{language}｜链接：{url}

## 核心思路
{题目本质、约束、选择的算法、关键状态或不变量；保持简洁}

## 算法步骤
1. {step}
2. {step}
3. {step}

## 核心代码
{仅 solve 方法/函数，不含 I/O 外壳}

## 复杂度
- 时间：{time}
- 空间：{space}

## 记忆点
- {识别信号 → 算法模式}

> 完整可运行代码：{code_file}
```

## Detail 题解模板

```markdown
# {题名} 详细题解
> 平台：{platform}｜题号：{id}｜语言：{language}｜链接：{url}

## 问题拆解
- 目标：{goal}
- 输入输出：{io}
- 约束与边界：{constraints}

## 方案对比
| 方案 | 核心思路 | 时间 | 空间 | 取舍 |
|---|---|---|---|---|
| 直接/暴力 | ... | ... | ... | ... |
| 推荐方案 | ... | ... | ... | ... |

推荐方案
{关键推导、状态定义或不变量}

## 核心代码
{推荐方案的 solve 方法/函数，不含 I/O 外壳}

**算法步骤**
1. {step}
2. {step}
3. {step}

**官方样例与边界**
- 官方样例：{题面已有样例；不得把自造用例标为官方}
- 必要边界：{仅补充能暴露错误的边界}

## 复杂度与易错点
- 时间：{time}；空间：{space}
- 易错点：{mistakes}

## 知识沉淀
- {识别信号、算法思维模式、可复用代码模板、可迁移结论}

> 解题代码：{code_file}｜测试代码：{test_file}
```

不得创建“测试说明.md”“测试报告.md”等额外文档。

## 代码契约

| 语言 | 解题文件 | detail 测试文件 | 用户运行入口 |
|---|---|---|---|
| Java 17 | `Main.java` | `Test.java` | `public static void main` |
| Python 3 | `solution.py` | `test_solution.py` | `if __name__ == "__main__"` |
| C17 | `solution.c` | `test.c` | `main` |
| C++17 | `solution.cpp` | `test.cpp` | `main` |
| TypeScript | `solution.ts` | `test.ts` | 顶层入口 |

- 解题代码必须是单文件、标准库、英文标识符、关键逻辑中文注释。
- LeetCode 函数题也要补充明确的输入约定和可运行入口。
- 测试代码必须有独立入口，不依赖 JUnit、pytest 等第三方框架。
- 测试代码优先使用题面官方样例，再补 1～3 个必要边界；输出清晰的通过/失败信息。
- 测试代码调用解题代码公开接口，不复制另一份算法实现。
- 保持文件紧凑；不要加入教程式长注释、重复实现或无关工具类。

## Review 规范

review 只读取以下最高优先级的一个规范源，找到后停止：

1. 用户本次上传或粘贴的规范。
2. `--rules` 明确指定的文件。
3. `<project>/.code-solver/review-rules.md`。
4. `<skill_dir>/references/review-rules.md`。

不要合并多个规范，也不要修改用户规范。按选中规范一次完成审查；无证据的问题不输出。仅当用户明确要求时生成修订代码。

Review 输出结构：结论、问题（位置/证据/影响/最小修改）、优先级、知识盲点。调用一次 `archive.py resolve --mode review`，将结果直接写入 `代码审查.md`；不运行被审代码。


## 归档约定

新产物使用扁平结构：

```text
code-solver-workspace/<平台>/<中文题型>/<题号>-<题名>-<语言>/
├── 题解.md（或 代码审查.md）
├── Main.java（或 solution.*）
└── Test.java（或 test.*，仅 detail）
```

旧归档保持原样，不迁移、不扫描。题型从下表选最接近的一个英文 key 传给 archive.py，不分级、不组合；无法判断时用 other：

| key | 题型 | key | 题型 | key | 题型 |
|---|---|---|---|---|---|
| array | 数组 | two-pointers | 双指针 | monotonic-stack | 单调栈 |
| string | 字符串 | sliding-window | 滑动窗口 | monotonic-queue | 单调队列 |
| linked-list | 链表 | binary-search | 二分查找 | union-find | 并查集 |
| stack | 栈 | dfs | 深度优先搜索 | trie | 字典树 |
| queue | 队列 | bfs | 广度优先搜索 | segment-tree | 线段树 |
| hash | 哈希表 | backtracking | 回溯 | topological-sort | 拓扑排序 |
| heap | 堆 | sorting | 排序 | shortest-path | 最短路径 |
| tree | 树 | greedy | 贪心 | minimum-spanning-tree | 最小生成树 |
| graph | 图 | dynamic-programming | 动态规划 | bit-manipulation | 位运算 |
| matrix | 矩阵 | divide-and-conquer | 分治 | math | 数学 |
| prefix-sum | 前缀和 | difference-array | 差分 | state-compression | 状态压缩 |
| simulation | 模拟 | design | 设计 | string-matching | 字符串匹配 |
| geometry | 几何 | other | 其他 | | |

## 性能预算

| 模式 | 模型生成轮次 | 目录调用 | 文件写入 | 产物回读 | 运行验证 |
|---|---:|---:|---:|---:|---:|
| fast | 2 | 1 | 2 | 0 | 0 |
| detail | 2 | 1 | 3 | 0 | 0 |
| review | 1 | 1 | 1 | 0 | 0 |

完成后输出一行：
- fast：完成（fast模式，请用户自行验证），题解归档到{note路径}，可运行代码归档到{code路径}
- detail：完成（detail模式，请用户自行验证），题解归档到{note路径}，可运行代码归档到{code路径}，测试代码归档到{test路径}
- review：完成（review模式），代码审查归档到{note路径}



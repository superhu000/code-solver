---
name: code-solver
description: 解答算法题并审查代码，生成可直接运行的单文件程序并归档结构化中文题解。支持 Java、Python、C++、TypeScript。在处理 LeetCode/力扣题目、算法解题、刷题、代码审查、报错定位或算法复盘时使用。
---

# Solving Algorithms

## 目标

帮助用户快速刷题，做到**想得出、写得出、记得住**。

## 注意

不编译、不执行、不读模板。
题解由模型直接生成，脚本只管目录。
默认 `fast + Java 17 + 中文`。
`<skill_dir>` 为本目录，`<project>` 为项目根。
不要读取 `references/SPEC.md`。

**最高优先级：先生成题解，立刻归档，再生成可执行文件**

## 架构原则

1. **题解优先** — 题解是最高优先级产物，含核心逻辑代码。模型先生成完整题解 Markdown 并直接写入归档目录，用户立刻可读。完整代码可以慢一步。
2. **不编译不执行** — 代码由用户自行运行，消除环境差异和耗时
3. **不读模板** — 模型凭自身知识生成，不读取算法或语言模板
4. **模型直接写文件** — 模型用 Write 工具直接生成题解和源码到归档目录，轻量高效
5. **直接生成** — 脚本只负责解析路径和创建目录，模型直接写入最终位置，不暂存不移动

## 路由

- `detail`/`-d`/要求测试用例 → detail；否则 → fast
- 给出代码/报错/要求检查 → `kind=review`；否则 → `kind=solve`
- 题面缺少关键输入输出定义时一次性询问

## 代码契约

| 语言 | 文件 | 入口 |
|------|------|------|
| Java 17 | `Main.java` | `public class Main` + `main` |
| Python | `solution.py` | `if __name__ == "__main__":` |
| C/C++ | `solution.c`/`.cpp` | `main` |
| TypeScript | `solution.ts` | 顶层入口 |

英文标识符，**关键逻辑加中文注释**，禁止第三方依赖。LeetCode 题目也要写成可运行程序。

### 统一代码风格

所有语言遵循统一结构：**核心算法方法 + main 入口**。模型每次按此结构生成，保持风格一致。

**Java**：
```java
import java.util.*;

public class Main {
    // 核心算法方法（题解中展示此部分）
    static int solve(int[] nums) {
        // 算法逻辑
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        // 读取输入
        // int result = solve(...);
        // System.out.println(result);
    }
}
```

**Python**：
```python
def solve(...):
    # 算法逻辑（题解中展示此部分）

if __name__ == "__main__":
    # 读取输入
    # result = solve(...)
    # print(result)
```

**C/C++**：
```c
#include <stdio.h>
// 核心算法函数（题解中展示此部分）
int solve(int* nums, int n) {
    // 算法逻辑
}

int main() {
    // 读取输入
    // int result = solve(...);
    // printf("%d\n", result);
    return 0;
}
```

**TypeScript**：
```typescript
// 核心算法函数（题解中展示此部分）
function solve(...): number {
    // 算法逻辑
}

// 入口
const input = ''; // 从 stdin 读取
// console.log(solve(...));
```

题解中的"核心代码"部分展示 `solve` 方法/函数，不含 main 入口和 I/O 代码。

| 语言 | 测试文件（detail） |
|------|-------------------|
| Java | `Test.java` |
| Python | `test_solution.py` |
| C | `test.c` |
| C++ | `test.cpp` |
| TypeScript | `test.ts` |

## 题型分类

`category` 使用英文标识符，由脚本映射为中文归档目录名。分类保持笼统：

1. **先按数据结构**：`graph`/`tree`/`linked-list`/`array`/`string`/`hash`/`stack`/`heap`
2. **再按算法场景**：`sorting`/`simulation`/`dynamic-programming`/`greedy`/`backtracking`/`search`/`binary-search`/`two-pointers`/`sliding-window`/`prefix-sum`

合并规则：BFS/DFS 统一用 `search`；单调栈用 `stack`。

## 效率要求（关键）

- **题解第一优先**。模型先调用 resolve 获取归档路径，然后生成完整题解 Markdown（含核心逻辑代码）并直接 Write 到归档目录（用户立刻可读），再生成完整代码。题解和代码分两轮生成，不是一次性同时生成。
- **禁止在 `<think>` 中写完整代码**。思考只写思路要点和关键变量，代码直接通过 Write 工具输出。
- **题解包含核心逻辑代码**。题解中嵌入算法关键部分代码块（不含 I/O 模板），完整可运行代码见 `src/` 目录。
- **思考要简短**。确定题目本质、算法选择、复杂度即可，不要逐行推演代码。
- **生成顺序**：① resolve 获取路径 → 第一轮生成题解（含核心代码）→ Write 题解到 archiveDir → ② 第二轮生成完整代码 → Write 代码到 archiveDir/src/ → Write 测试（detail）。
- **第二轮复用题解代码**。第二轮生成完整代码时，题解中的核心代码（solve 方法）作为上下文，直接扩展为完整程序（加 main 入口和 I/O），不重新思考算法。
- detail 模式的测试代码写入 `src/Test.java`（或对应语言的测试文件），不放在题解中。

## 流程（2 步）

### 步骤 1：resolve 路径 → 生成题解，直接写入归档目录

模型调用 resolve 获取归档路径 → 生成完整题解 Markdown → 直接 Write 到归档目录

```bash
# 1. resolve 获取归档路径（自动创建目录）
python <skill_dir>/scripts/pipeline.py resolve --project-root <project> --category <category> --kind <solve|review> "leetcode 206 java"
# 返回 {"archiveDir": "...", "note": ".../题解.md", "code": ".../src/Main.java", ...}

# 2. Write 题解直接到 archiveDir/题解.md（resolve 返回的 note 路径）
```

题解直接在归档目录，用户立刻可读。

### 步骤 2：第二轮 — 生成代码，直接写入归档目录

模型基于题解中的核心代码（solve 方法），扩展为完整可运行程序 → Write 到 `archiveDir/src/`（resolve 返回的路径，已存在）

- 代码 → `<archiveDir>/src/Main.java`（fast 和 detail）
- 测试 → `<archiveDir>/src/Test.java`（仅 detail）

> 第二轮复用题解中的核心代码，不重新思考算法。只需加 main 入口和 I/O 代码，扩展为完整程序。
> 代码直接写入归档目录。用户在阅读题解的同时代码已开始生成。

## 题解模板

所有模式题解均包含核心逻辑代码块（算法关键部分，不含 I/O 模板）。完整可运行代码见 `src/` 目录。题解顶部包含题目基本信息（题名、平台、题号、链接）。

### Fast

```
# {题名} 题解

> 平台：{platform} | 题号：{id} | 链接：{url}

## 思路
{essence：题目本质、算法选择、关键思路}

## 核心代码
```{language}
{算法关键部分代码，不含 I/O 模板}
```

## 步骤
1. {step}
2. {step}
3. {step}

## 复杂度
- 时间：{time}
- 空间：{space}

## 记忆点
- {signal/pattern}
- {signal/pattern}

> 完整代码见 src/，运行：`{运行命令}`
```

### Detail

```
# {题名} 题解

> 平台：{platform} | 题号：{id} | 链接：{url}

## 问题分析
**题目简化**：{problem_simplification}
**输入输出**：{input_output}
**约束与边界**：{constraints_analysis}
** 启发思考**

## 算法方案
**方案 1：{暴力解名称}**
- 思路：{approach}
- 时间：{time}，空间：{space}
- 优点：{pros}，缺点：{cons}

**方案 2：{最优解名称}**
- 思路：{approach}
- 时间：{time}，空间：{space}
- 优点：{pros}，缺点：{cons}

**方案对比**：{comparison}

## 核心代码（最优解）
```{language}
{最优解算法关键部分代码，不含 I/O 模板}
```

## 算法步骤（最优解）
1. {step}
2. {step}
3. {step}

## 复杂度
- 时间：{time}
- 空间：{space}

## 测试用例
1. 输入：{stdin} → 期望输出：{expected}
> 完整代码见 src/，测试见 src/Test.java，运行：`{运行命令}`
> 测试用例优先使用官方样例

## 知识沉淀
- **核心知识点**：{knowledge_points}
- **算法模式**：{algorithm_pattern}
- **易错点**：{common_mistakes}
```

### Review

```
# {题名} 代码审查

> 平台：{platform} | 题号：{id} | 链接：{url}

## 审查结论
{essence}

## 问题列表
**问题 1：{problem}**
- 证据：{evidence}
- 原因：{cause}
- 最小修改：{fix}

## 修改策略
1. {step}
2. {step}

## 知识盲点
- {blind_spot}
- {blind_spot}

## 学习资料
- {topic}：{description}（{type}）

## 推荐巩固题型
- {title}（{difficulty}）：{reason}
```

## 运行命令

| 语言 | 命令 |
|------|------|
| Java | `cd src && java Main.java` |
| Python | `cd src && python solution.py` |
| C | `cd src && gcc -std=c17 -O2 solution.c -o app && ./app` |
| C++ | `cd src && g++ -std=c++17 -O2 solution.cpp -o app && ./app` |
| TypeScript | `cd src && tsc solution.ts --target ES2020 && node solution.js` |

## 归档查询

```bash
python <skill_dir>/scripts/pipeline.py list --project-root <project> --keyword 反转
```

## 停止预算

| 模式 | 推理 | resolve | Write | 修复 |
|------|------|---------|-------|------|
| fast | 2（题解+代码） | 1 | 2（题解+代码） | 0 |
| detail | 2（题解+代码） | 1 | 3（题解+代码+测试） | 0 |

成功后回复不超过 6 行。

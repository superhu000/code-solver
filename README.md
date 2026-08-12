# code-solver


> AI 驱动的算法解题助手 —— 解题、审查与归档，不编译不执行，模型直接写文件。

code-solver 是一个 Skill，帮助学习者快速刷题，支持生成清晰的题解、可直接运行的代码，并进行归档。核心设计原则：**模型直接写文件，脚本只管目录** —— 模型负责算法判断、结构化解释和代码，脚本只负责创建归档目录和查询。

## 功能特性

### 两个子命令

| 子命令 | 模式 | 做什么 |
|--------|------|--------|
| **solve** | fast（默认） | 给出最佳解法，含核心逻辑代码的精简题解 |
| **solve** | detail | 暴力 + 最优多方案对比，含测试代码和测试用例，用例优先使用官方样例 |
| **review** | — | 分析代码问题，发现知识盲点，推荐学习资料和巩固题型 |

### 支持语言

| 语言 | 文件名 | 入口要求 |
|------|--------|---------|
| Java 17 | `Main.java` | `public class Main` + `public static void main` |
| Python 3 | `solution.py` | `if __name__ == "__main__":` |
| C17 | `solution.c` | `main` |
| C++17 | `solution.cpp` | `main` |
| TypeScript | `solution.ts` | 顶层可执行入口 |

### 输入解析

支持三种输入方式，由 `parse.py` 脚本统一解析为 ProblemSpec JSON：

1. **平台简写**：`leetcode 206 java`
2. **URL**：`https://leetcode.cn/problems/reverse-linked-list/`
3. **原题文本**：多行文本，支持 `题目:`/`输入:`/`输出:`/`样例:`/`约束:` 等标记分段

### 文档归档

题解由模型直接生成 Markdown（含核心逻辑代码），归档结构为：

```
code-solver-workspace/
└── <平台>/<题型>/<语言>/<题号>-<题名>/
    ├── 题解.md（或 审查.md）
    └── src/
        └── Main.java（等完整可运行源码）
    —— test
        |__ test.java(单元测试)
```

题型保持笼统分类，先按数据结构（图/树/链表/数组/字符串/哈希表/栈/堆），不好分时按算法场景（排序/模拟/动态规划/贪心/回溯/搜索/二分查找/双指针/滑动窗口/前缀和）。

## 安装

### 前置要求

- Python 3.10+
- JDK 17+（Java 题目运行用，非编译用）
- gcc / g++（C/C++ 题目运行用）
- Node.js + TypeScript（TypeScript 题目运行用）

### 一键安装（Windows）

1. **下载并解压**：将下载的压缩包解压到项目根目录（或任意位置）
2. **运行安装**：进入解压目录，双击 `install.cmd`
3. **完成确认**：按提示按任意键结束
4. **移动到项目根目录**（如解压位置不在项目根目录）

安装完成后项目结构：
```
项目根目录/
└── .opencode/（或 .cac/）
    ├── README.md
    ├── commands/
    │   └── coder-solver.md
    └── skills/
        └── coder-solver/
            ├── SKILL.md
            ├── references/
            └── scripts/
```

### 一键安装（Linux / macOS）

```bash
unzip code-solver-1.0.zip
cd code-solver-1.0
chmod +x install.sh
./install.sh
mv .opencode /path/to/your/project/
```

### 验证安装

```bash
python .opencode/skills/code-solver/scripts/pipeline.py doctor
```

## 使用方式

两个子命令：`solve` 解题、`review` 审查代码。

```bash
# solve — 解题
/code-solver solve leetcode 206 java              # fast 模式（默认），最佳解法
/code-solver solve detail leetcode 1 java         # detail 模式，暴力+最优多方案对比
/code-solver solve [粘贴原题文本]                   # 默认 fast + java
/code-solver solve detail [粘贴原题文本] python     # detail 模式 + python

# review — 代码审查
/code-solver review [粘贴代码]
/code-solver review 这段代码报了空指针错误 [粘贴代码]
```

### 配置

`<project>/.solving-algorithms/config.json` 中放置项目级覆盖配置。
```json
{
  "storage": { "root": "" },
  "defaults": { "language": "java", "mode": "fast" }
}
```


### 归档管理

```bash
# 列出所有归档
python skills/code-solver/scripts/pipeline.py list --project-root .

# 按平台和语言过滤
python skills/code-solver/scripts/pipeline.py list --platform leetcode --language java

# 按关键词搜索
python skills/code-solver/scripts/pipeline.py list --keyword 反转
```

## 项目结构

```
code-solver/
├── commands/
│   └── code-solver.md      # 命令入口
├── skills/code-solver/
│   ├── SKILL.md                   # Skill 定义（模型行为契约）
│   ├── references/
│   │   ├── SPEC.md                # 产品规格与版本记录
│   │   ├── algorithm-templates/   # 算法模板（保留，模型不再读取）
│   │   └── language-templates/    # 语言模板（保留，模型不再读取）
│   └── scripts/
│       ├── pipeline.py            # archive + list + doctor
│       ├── parse.py               # 输入解析器
│       ├── config.py              # 配置和路径
│       ├── contract.py            # 命名和路径工具
│       ├── archive.py             # 归档目录创建和查询
│       └── render.py              # 运行命令工具
├── install.sh / install.ps1 / install.cmd  # 安装脚本
└── LICENSE
```

## 设计原则

1. **模型直接写文件** — 模型直接生成 Markdown 题解（含核心逻辑代码）和源码文件，不经过脚本渲染
2. **不编译不执行** — 代码由用户自行运行验证，消除环境差异
3. **不读模板** — 模型凭自身知识生成，不读取算法或语言模板
4. **题解优先** — 题解含核心逻辑代码，写完立即归档，用户立刻可读；完整代码可以慢一步
5. **单一 Spec** — 所有产品决策、契约和验收标准只在 `references/SPEC.md` 中维护

## 版本

当前版本：**0.12.0**，详见 [SPEC.md](skills/code-solver/references/SPEC.md) 第 12 节版本历史。

## License

MIT

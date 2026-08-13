# code-solver

> 轻量算法解题与代码审查 Skill：先交付题解，再生成用户可运行的代码。

## 模式

| 模式 | 第一产物 | 第二产物 | 额外产物 |
|---|---|---|---|
| `solve fast` | 简洁题解 | 可运行解题代码 | 无 |
| `solve detail` | 详细题解 | 可运行解题代码 | 可运行测试代码 |
| `review` | 按规范生成审查结果 | 按需给出修改建议 | 无 |

默认使用 `fast + Java 17 + 中文`。

## 核心原则

1. **题解优先**：模型按内置模板一次生成完整题解，立即写入最终归档目录。
2. **两轮生成**：fast 为“题解 → 代码”；detail 为“题解 → 代码与测试代码”。
3. **最少读写**：不生成临时文件，不回读已写产物，不在 solve 流程加载 Review 规范或 Spec。
4. **不编译不执行**：Skill 不在终端编译、运行或修复生成代码，由用户自行验证。
5. **官方样例优先**：detail 测试代码优先使用题面中的官方样例，再补必要边界用例。
6. **规范可覆盖**：review 支持本次上传、指定路径、项目级和内置四级代码规范。

## 使用

```text
/code-solver solve leetcode 206 java
/code-solver solve detail leetcode 1 java
/code-solver solve <粘贴题面> python
/code-solver review <粘贴代码或报错>
/code-solver review --rules <规范文件路径> <代码>
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

## 项目结构

```text
code-solver/
├── command/code-solver.md
├── skill/code-solver/
│   ├── SKILL.md
│   ├── references/review-rules.md
│   └── scripts/archive.py
└── spec/versions/0.13.0-lightweight-pipeline.md
```

## 安装

本包是 CodeAgent Skill 项目压缩包，解压后放入对应目录即可被识别，无需额外安装依赖。

### 1. 解压

```text
tar -xzf code-solver-v0.13.0.tar.gz
# 或
unzip code-solver-v0.13.0.zip
```

解压后得到 `code-solver-v0.13.0/` 目录，包含以下内容：

```text
code-solver-v0.13.0/
├── README.md
├── command/
│   └── code-solver.md              # 命令入口
├── skills/
│   └── code-solver/
│       ├── SKILL.md                # Skill 主逻辑
│       ├── references/
│       │   └── review-rules.md     # 默认审查规范
│       └── scripts/
│           └── archive.py          # 归档脚本
└── spec/versions/                  # 版本决策记录（运行时不读取）
```

### 2. 放入对应目录

根据你使用的客户端选择目录：

**OpenCode（.opencode）：**

```text
cp -r code-solver-v0.13.0/command  <项目根目录>/.opencode/
cp -r code-solver-v0.13.0/skills   <项目根目录>/.opencode/
```

放入后结构：

```text
<项目根目录>/.opencode/
├── command/code-solver.md
└── skills/code-solver/
    ├── SKILL.md
    ├── references/review-rules.md
    └── scripts/archive.py
```

**CodeAgentCLI 3.0（.cac）：**

```text
cp -r code-solver-v0.13.0/command  <项目根目录>/.cac/
cp -r code-solver-v0.13.0/skills   <项目根目录>/.cac/
```

放入后结构：

```text
<项目根目录>/.cac/
├── command/code-solver.md
└── skills/code-solver/
    ├── SKILL.md
    ├── references/review-rules.md
    └── scripts/archive.py
```

### 3. 环境要求

- OpenCode 或 CodeAgentCLI 3.0（用于识别 Skill 并触发 `/code-solver`）
- Python 3（archive.py 仅依赖标准库，无需 pip install）

### 4. 开始使用

在项目根目录下启动客户端，输入命令即可：

```text
/code-solver solve leetcode 206 java
```

题解和代码自动归档到项目根目录下的 `code-solver-workspace/`，无需手动创建。

## 版本

当前版本：**0.13.0**。本次决策与验收标准见
[`spec/versions/0.13.0-lightweight-pipeline.md`](spec/versions/0.13.0-lightweight-pipeline.md)。


# Spec 管理规则

## 职责

- CURRENT.md：当前版本的唯一功能契约，可修改。
- CHANGELOG.md：面向用户的版本记录。
- releases/：已发布版本的冻结快照，只读。
- templates/：后续增量 Spec 的统一模板。

## 修改流程

1. 基于 CURRENT.md 在分支上设计改动，先处理不兼容行为与迁移。
2. 同步更新 CURRENT.md、README.md、command/code-solver.md、运行时 SKILL 与受影响脚本。
3. 更新根目录 VERSION 和 CHANGELOG.md。
4. 运行 python skill/code-solver/scripts/check_docs.py。
5. 发布时把当前契约冻结到 releases/<version>.md；历史 release 不再改写。

## 版本规则

MAJOR 表示不兼容变更；MINOR 表示兼容的新能力；PATCH 表示不改变契约的修复。禁止只改运行时文档而不改 CURRENT。

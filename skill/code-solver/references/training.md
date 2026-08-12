# Training workflow

仅在 `train` 模式读取本文件一次。

## 命令

```text
train daily [days=30] [goal]
train drill <topic> [count=7] [goal]
train submit <code-or-description>
train summary
```

省略参数时使用当前激活计划。用户说“开始今天刷题”视为 `train daily`；说“继续专项”视为当前 `train drill`。
`submit` 和 `summary` 默认作用于最近激活的 daily 或 drill 计划，无需重复指定。

## 创建计划

1. 调用一次 `training.py notes` 获取已有题解索引。
2. 根据用户目标、水平、时间和语言生成大纲。信息不足时采用 `Java 17、每天一题、30 分钟、面试算法`，不要追问。
3. daily 默认 30 天，按基础数据结构 → 高频模式 → 搜索/树 → 动态规划/贪心 → 综合复盘组织。
4. drill 默认 7 题，按前置知识 → 入门 → 基础 → 变式 → 综合递进。难度以简单、中等为主，只有用户要求时安排困难题。
5. 精确题目已归档时，把原题解作为 `note`、源码作为 `code`；同题型旧笔记作为 `resources`。不要复制题解。
6. 未归档题目只保存平台、题号、标题、难度、专题和公开链接，不预先生成全部题解。
7. 优先引用 LeetCode 官方题目/Study Plan、用户笔记；知识补充可引用 OI Wiki、CP-Algorithms、USACO Guide、dev.java。只保存标题和链接，不复制正文或付费内容。
8. 有网络检索能力时，在创建计划阶段批量验证公开题目链接；每日领取时不联网。无法确认的链接不得编造，应改用对应官方 Study Plan 或专题页。
9. 调用 `training.py resolve` 创建计划目录，直接写入 `计划.md` 和 `state.json`，不使用临时文件；写入后立即进入“领取题目”，开始第一题。

`state.json` 最小结构：

```json
{
  "version": 1,
  "kind": "daily",
  "title": "30天每日一题",
  "goal": "补齐高频算法模式",
  "current": 0,
  "status": "active",
  "items": [{
    "seq": 1, "topic": "哈希表", "platform": "leetcode",
    "problemId": "1", "title": "两数之和", "difficulty": "简单",
    "language": "java", "url": "https://leetcode.cn/problems/two-sum/",
    "resources": [], "note": null, "code": null, "status": "pending"
  }]
}
```

`计划.md` 包含目标、阶段大纲和逐题表格。每题必须显示题目链接、难度、学习目标、已有笔记或教学资源。

## 领取题目

1. 调用 `training.py current --kind <daily|drill>`。
2. daily 当天已完成时只返回进度，不提前发下一题；drill 可继续下一题。
3. 返回 `reuse=true` 时直接展示已有题解和代码链接。
4. 返回 `reuse=false` 时，在当前任务内执行 fast Solve 流程生成题解与代码；若只缺一个文件，仅补缺失文件，不覆盖已有内容。
5. 调用 `training.py link` 记录题解和代码路径，再向用户展示题目、目标、资源、题解和代码。

这里的 solve 是内部流程复用，不是再次触发命令。不得递归调用 Skill。

## 提交与进度

- 代码提交：保存到计划的 `submissions/`，模型一次静态评估，最多输出两个关键问题；不运行、不重写完整代码。
- 文字提交：按用户自述记录状态、用时、方法、困难和参考资料，不声称代码通过。
- 状态只使用 `completed`、`partial`、`blocked`、`skipped`。
- 调用一次 `training.py record`，更新 `state.json`、追加 `history.jsonl` 并刷新 `进度.md`。
- `partial` 后安排同类型同难度变式；`blocked` 后引用基础笔记并降低下一题难度。只调整未开始项目，不重建整个计划。
- `record` 返回 `finished=true` 时立即生成总结。

## 总结

计划结束或用户要求总结时，读取当前 `state.json`、`进度.md` 和其中已关联的题解，写入 `总结.md`：完成率、用时、已掌握内容、高频问题、代表题目、笔记链接和下一步建议。

drill 总结额外包含：专题识别信号、通用解题步骤、边界清单、代表题目阶梯。不要扫描计划外笔记。

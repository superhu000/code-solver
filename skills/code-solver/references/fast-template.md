# Fast 题解模板

> solve fast 模式第一轮读取本文件，按占位符填充后生成完整题解写入 `题解.md`。
> 用户可按需修改本模板风格，不影响 Skill 流程，修改后删去或同步修改示例即可。
> 占位符统一使用 `{名称}` 格式，如 `{题名}`、`{platform}`。

---

# {题名} 题解
> 平台：{platform}｜题号：{id}｜难度：{difficulty}｜题型：{category}｜语言：{language}｜链接：{url}

## 题目描述
{1-2 句概括题意；须包含输入输出约定和数据范围，不复制完整题面}

## 核心思路
{3-5 句；覆盖题目本质、算法选择和关键状态或不变量；步骤融入行文，不单独列表}

## 核心代码
{函数签名}
{仅 solve 方法/函数，不含 I/O 外壳；关键行附中文行内注释，不超过 3 处}

## 复杂度
- 时间：{time}
- 空间：{space}

## 记忆点
{1-3 条，每条一行，记录关键识别信号和易错点}

> 完整可运行代码：{code_file}

---

## 示例（LeetCode 206 反转链表）

以下为一次完整填充的示例，仅供风格参考，不得复制到实际题解。

# 反转链表 题解
> 平台：leetcode｜题号：206｜难度：简单｜题型：linked-list｜语言：java｜链接：https://leetcode.cn/problems/reverse-linked-list/

## 题目描述
给定单链表头节点 `head`，反转链表并返回新头节点。节点数 0-5000，节点值任意整数。

## 核心思路
本质是逐个改变节点的 `next` 指针方向。用迭代法维护 `prev` 和 `curr` 两个指针，每轮将 `curr.next` 指向 `prev` 后同步右移，直到 `curr` 为空时 `prev` 即为新头节点。

## 核心代码
```java
ListNode reverseList(ListNode head)
ListNode prev = null, curr = head;
while (curr != null) {
    ListNode next = curr.next;  // 暂存后继，防止断链
    curr.next = prev;           // 反转指针方向
    prev = curr;
    curr = next;
}
return prev;
```

## 复杂度
- 时间：O(n)
- 空间：O(1)

## 记忆点
- 链表反转用迭代双指针 prev/curr，必须暂存 next 再改指针，否则断链

> 完整可运行代码：leetcode/链表/206-反转链表-java/Main.java

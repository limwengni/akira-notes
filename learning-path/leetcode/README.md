# LeetCode Learning Path - Beginner

> 1-2 hours/day - Focus on understanding patterns, not grinding problems.

---

## Day 1 - Arrays
**Goal:** get comfortable reading and traversing arrays.

| Problem | Difficulty | Link |
|---|---|---|
| Two Sum | Easy | [leetcode.com/problems/two-sum](https://leetcode.com/problems/two-sum) |
| Contains Duplicate | Easy | [leetcode.com/problems/contains-duplicate](https://leetcode.com/problems/contains-duplicate) |
| Maximum Subarray | Easy, but tricky | [leetcode.com/problems/maximum-subarray](https://leetcode.com/problems/maximum-subarray) |

**Focus:** understand index access, loops, and when to use a second variable to track a running value.

**Keep it light:** if `Maximum Subarray` feels hard, read the solution idea and come back on Day 5.

---

## Day 2 - Strings
**Goal:** get comfortable with string manipulation.

| Problem | Difficulty | Link |
|---|---|---|
| Reverse String | Easy | [leetcode.com/problems/reverse-string](https://leetcode.com/problems/reverse-string) |
| Valid Palindrome | Easy | [leetcode.com/problems/valid-palindrome](https://leetcode.com/problems/valid-palindrome) |
| Valid Anagram | Easy | [leetcode.com/problems/valid-anagram](https://leetcode.com/problems/valid-anagram) |

**Focus:** strings are close to character arrays. Most beginner problems are about comparing, counting, or cleaning characters.

---

## Day 3 - Hash Maps
**Goal:** understand when O(1) lookup changes everything.

| Problem | Difficulty | Link |
|---|---|---|
| Two Sum (redo with hash map) | Easy | [leetcode.com/problems/two-sum](https://leetcode.com/problems/two-sum) |
| Valid Anagram (redo with hash map) | Easy | [leetcode.com/problems/valid-anagram](https://leetcode.com/problems/valid-anagram) |
| First Unique Character | Easy | [leetcode.com/problems/first-unique-character-in-a-string](https://leetcode.com/problems/first-unique-character-in-a-string) |

**Focus:** when you find yourself doing nested loops, ask "can a hash map remove one of these loops?"

---

## Day 4 - Two Pointers
**Goal:** learn to use two pointers to avoid O(n^2) solutions.

| Problem | Difficulty | Link |
|---|---|---|
| Valid Palindrome (two pointer) | Easy | [leetcode.com/problems/valid-palindrome](https://leetcode.com/problems/valid-palindrome) |
| Merge Sorted Array | Easy | [leetcode.com/problems/merge-sorted-array](https://leetcode.com/problems/merge-sorted-array) |
| Move Zeroes | Easy | [leetcode.com/problems/move-zeroes](https://leetcode.com/problems/move-zeroes) |

**Focus:** two pointers usually means one at the start and one at the end, or both moving forward. It works especially well on sorted arrays and palindrome-type problems.

---

## Day 5 - Review + Mixed
**Goal:** revisit anything you struggled with, then try something new.

| Problem | Difficulty | Link |
|---|---|---|
| Best Time to Buy and Sell Stock | Easy | [leetcode.com/problems/best-time-to-buy-and-sell-stock](https://leetcode.com/problems/best-time-to-buy-and-sell-stock) |
| Climbing Stairs | Easy, but new idea | [leetcode.com/problems/climbing-stairs](https://leetcode.com/problems/climbing-stairs) |
| Re-attempt 1-2 problems you could not solve earlier | Review | - |

**Focus:** `Climbing Stairs` is your first taste of dynamic programming. Just notice the pattern; do not stress it yet.

---

---

## Day 6 - Sliding Window
**Goal:** learn to avoid nested loops when working with subarrays or substrings.

| Problem | Difficulty | Link |
|---|---|---|
| Maximum Average Subarray I | Easy | [leetcode.com/problems/maximum-average-subarray-i](https://leetcode.com/problems/maximum-average-subarray-i) |
| Longest Substring Without Repeating Characters | Medium | [leetcode.com/problems/longest-substring-without-repeating-characters](https://leetcode.com/problems/longest-substring-without-repeating-characters) |
| Minimum Size Subarray Sum | Medium | [leetcode.com/problems/minimum-size-subarray-sum](https://leetcode.com/problems/minimum-size-subarray-sum) |

**Focus:** a window slides across the array — expand the right side, shrink the left when a condition breaks. One loop, no nesting.

---

## Day 7 - Binary Search
**Goal:** understand how to search in O(log n) instead of O(n).

| Problem | Difficulty | Link |
|---|---|---|
| Binary Search | Easy | [leetcode.com/problems/binary-search](https://leetcode.com/problems/binary-search) |
| Search Insert Position | Easy | [leetcode.com/problems/search-insert-position](https://leetcode.com/problems/search-insert-position) |
| First Bad Version | Easy | [leetcode.com/problems/first-bad-version](https://leetcode.com/problems/first-bad-version) |

**Focus:** always ask — can I cut the search space in half? Binary search only works on sorted data. The key is getting `left`, `right`, and `mid` right without off-by-one errors.

---

## Day 8 - Linked Lists
**Goal:** get comfortable with pointer manipulation.

| Problem | Difficulty | Link |
|---|---|---|
| Reverse Linked List | Easy | [leetcode.com/problems/reverse-linked-list](https://leetcode.com/problems/reverse-linked-list) |
| Merge Two Sorted Lists | Easy | [leetcode.com/problems/merge-two-sorted-lists](https://leetcode.com/problems/merge-two-sorted-lists) |
| Linked List Cycle | Easy | [leetcode.com/problems/linked-list-cycle](https://leetcode.com/problems/linked-list-cycle) |

**Focus:** linked lists have no index access — you move by following `.next`. Draw it out on paper first. Linked List Cycle introduces the fast/slow pointer trick.

---

## Day 9 - Stacks and Queues
**Goal:** learn when order of processing matters.

| Problem | Difficulty | Link |
|---|---|---|
| Valid Parentheses | Easy | [leetcode.com/problems/valid-parentheses](https://leetcode.com/problems/valid-parentheses) |
| Implement Queue using Stacks | Easy | [leetcode.com/problems/implement-queue-using-stacks](https://leetcode.com/problems/implement-queue-using-stacks) |
| Min Stack | Medium | [leetcode.com/problems/min-stack](https://leetcode.com/problems/min-stack) |

**Focus:** stack = last in first out. Queue = first in first out. Valid Parentheses is the classic stack problem — if you get that one, you understand stacks.

---

## Day 10 - Review + Mixed
**Goal:** consolidate everything from Day 6-9, then try a step up.

| Problem | Difficulty | Link |
|---|---|---|
| Product of Array Except Self | Medium | [leetcode.com/problems/product-of-array-except-self](https://leetcode.com/problems/product-of-array-except-self) |
| 3Sum | Medium | [leetcode.com/problems/3sum](https://leetcode.com/problems/3sum) |
| Re-attempt 1-2 problems you could not solve earlier | Review | - |

**Focus:** Product of Array Except Self is a classic that combines prefix and suffix arrays. 3Sum extends Two Sum with sorting and two pointers — do not brute force it.

---

## After Day 10
You are no longer a beginner. Move on to:
- Trees and BFS/DFS
- Dynamic Programming (proper)
- Graphs

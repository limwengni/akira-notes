# Day 12 Notes - Trees and Recursion

**Goal:** Get comfortable traversing binary trees with recursion.

**Focus:** A tree node has `val`, `left`, and `right` (either can be null). Recursion handles the travelling — you just write what one node should do, and the function visits every node automatically.

| Problem | Difficulty | Link |
|---|---|---|
| Maximum Depth of Binary Tree | Easy | [leetcode.com/problems/maximum-depth-of-binary-tree](https://leetcode.com/problems/maximum-depth-of-binary-tree) |
| Invert Binary Tree | Easy | [leetcode.com/problems/invert-binary-tree](https://leetcode.com/problems/invert-binary-tree) |
| Diameter of Binary Tree | Easy | [leetcode.com/problems/diameter-of-binary-tree](https://leetcode.com/problems/diameter-of-binary-tree) |

---

## The Core Recursion Pattern

Every tree problem starts from this skeleton:

```csharp
ReturnType Solve(TreeNode node) {
    if (node == null) return baseCase;   // 1. stop condition
    // 2. recurse on children
    var left  = Solve(node.left);
    var right = Solve(node.right);
    // 3. combine and return
    return combine(left, right);
}
```

Two orderings you'll see:
- **Post-order** (recurse first, act after): used when you need child results to compute the current answer. e.g. MaxDepth
- **Pre-order** (act first, recurse after): used when you need to do something to the current node before touching children. e.g. Invert

---

## Maximum Depth of Binary Tree

**Problem:** Return the number of levels in the tree. A single node has depth 1.

**My understanding:** If I know the depth of my left subtree and right subtree, my depth = `Math.Max(left, right) + 1`. The `+1` counts the current node itself. `null` = depth 0 (nothing there).

**Pattern:** post-order — recurse first, combine after.

**Final answer (C#):**
```csharp
public int MaxDepth(TreeNode root) {
    if (root == null) return 0;
    int left  = MaxDepth(root.left);
    int right = MaxDepth(root.right);
    return Math.Max(left, right) + 1;
}
```

**Complexity:** O(n) — visits every node once.

---

## Invert Binary Tree

**Problem:** Mirror the tree — swap left and right children at every node.

**My understanding:** For every node, swap its left and right children, then do the same recursively for both sides. Classic three-step swap: save → overwrite → restore from temp. Without saving temp first, `root.left = root.right` destroys the original left forever.

**Pattern:** pre-order — swap current node first, then recurse into the (now swapped) children.

**What tripped me up:**
- First instinct was `while` loop — recursion IS the loop, don't mix them
- `root.left = root.right` alone isn't a swap — need temp just like linked list reverse

**Final answer (C#):**
```csharp
public TreeNode InvertTree(TreeNode root) {
    if (root == null) return null;

    TreeNode temp = root.left;
    root.left  = root.right;
    root.right = temp;

    InvertTree(root.left);
    InvertTree(root.right);

    return root;
}
```

**Complexity:** O(n) — visits every node once.

---

## Same Tree

**Problem:** Given two binary trees, return true if they are identical — same structure and same values at every node.

**My understanding:** At each pair of nodes: both null = same, one null = different, values differ = different, else recurse on both sides.

**What tripped me up:**
- Forgot the both-null base case first — without it, hitting two nulls would fall through and crash on `.left` of a null node
- Forgot to compare `p.val != q.val` — same structure but different numbers would wrongly return true
- Added redundant `if (p != null && q != null)` at the end — unnecessary because all null cases already returned above; by that point both are guaranteed non-null

**Final answer (C#):**
```csharp
public bool IsSameTree(TreeNode p, TreeNode q) {
    if (p == null && q == null) return true;   // both ended → same
    if (p != null && q == null) return false;  // structure mismatch
    if (p == null && q != null) return false;  // structure mismatch
    if (p.val != q.val) return false;          // value mismatch

    return IsSameTree(p.left, q.left) &&
           IsSameTree(p.right, q.right);
}
```

**Complexity:** O(n) — visits every pair of nodes once.

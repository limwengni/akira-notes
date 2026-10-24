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

---

## Diameter of Binary Tree

**Problem:** Return the length of the longest path between any two nodes (measured in edges). The path does not have to pass through the root.

**My understanding:** At any node, the longest path passing through it = left depth + right depth. Track the maximum of this across all nodes. The recursive function returns depth (like MaxDepth) and updates the diameter as a side effect along the way.

**Key insight:** Two separate jobs — the recursive function returns depth; the class-level variable tracks the best diameter seen so far. Almost identical to MaxDepth with one extra line.

**Final answer (C#):**
```csharp
public class Solution {
    int maxDiameter = 0;

    public int Depth(TreeNode root) {
        if (root == null) return 0;

        int left  = Depth(root.left);
        int right = Depth(root.right);

        maxDiameter = Math.Max(maxDiameter, left + right);  // update diameter at this node

        return Math.Max(left, right) + 1;                   // return depth as usual
    }

    public int DiameterOfBinaryTree(TreeNode root) {
        Depth(root);
        return maxDiameter;
    }
}
```

**Pattern:** helper function + class-level variable. The helper does the recursion and updates as a side effect; the main method kicks it off and returns the stored result. Reusable pattern for many tree problems.

**Complexity:** O(n) — visits every node once.

---

## Balanced Binary Tree

**Problem:** Return true if the tree is height-balanced — for every node, the height difference between left and right subtrees is at most 1, and both subtrees are also balanced.

**My understanding:** Need heights to check balance, so use a depth helper. Trick: return `-1` as a poison value meaning "unbalanced" instead of a separate flag. If anything below is unbalanced, propagate `-1` up immediately — no point checking further.

**The -1 poison pattern:**
- Balanced subtree → return its height (normal number)
- Unbalanced subtree → return -1 (bubbles up through all callers)
- Main function just checks `helper(root) != -1`

**What tripped me up:**
- First instinct was `return false` for null — wrong, empty tree is balanced → `return true`. In the helper, null = height 0
- Needed the depth helper pattern from Diameter, but here `-1` replaces the class-level variable

**Final answer (C#):**
```csharp
public int Depth(TreeNode root) {
    if (root == null) return 0;

    int left  = Depth(root.left);
    int right = Depth(root.right);

    if (left == -1 || right == -1) return -1;       // already unbalanced below
    if (Math.Abs(left - right) > 1) return -1;      // unbalanced at this node

    return Math.Max(left, right) + 1;               // balanced, return height
}

public bool IsBalanced(TreeNode root) {
    return Depth(root) != -1;
}
```

**Complexity:** O(n) — visits every node once, short-circuits as soon as imbalance is found.

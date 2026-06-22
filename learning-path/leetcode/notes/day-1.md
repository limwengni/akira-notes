# Day 1 Notes - Arrays

**Goal:** Get comfortable reading and traversing arrays.

**Focus:** Understand index access, loops, and when to use a second variable to track a running value.

| Problem | Difficulty | Link |
|---|---|---|
| Two Sum | Easy | [leetcode.com/problems/two-sum](https://leetcode.com/problems/two-sum) |
| Contains Duplicate | Easy | [leetcode.com/problems/contains-duplicate](https://leetcode.com/problems/contains-duplicate) |
| Maximum Subarray | Easy, but tricky | [leetcode.com/problems/maximum-subarray](https://leetcode.com/problems/maximum-subarray) |

---

## Two Sum

**Problem:** Given an array of integers and a target, return the indices of the two numbers that add up to the target. Each element can only be used once.

**My understanding:** Find which element combination sums to the target, but return their positions (indices), not the actual numbers.

**My first attempt:**
```csharp
int a = 0, b = 0;

for (int i = 0; i < nums.Length; i++)
{
    for (int j = i + 1; j < nums.Length; j++)
    {
        if (nums[i] + nums[j] != target)
        {
            continue;
        }
        else
        {
            a = i;
            b = j;
        }
    }
}

return [a, b];
```

**What I learned:**
- `j = i + 1` is the key — stops you from reusing the same element and avoids checking duplicates
- No need to store `a` and `b` — just `return` immediately when found, which also stops the loops early
- C# needs a fallback `return` at the end even if it'll never be hit, because the compiler doesn't know the problem guarantees a solution
- Flipping the condition (`==` instead of `!=`) removes the need for `continue/else`

**Final answer (C#):**
```csharp
for (int i = 0; i < nums.Length; i++)
{
    for (int j = i + 1; j < nums.Length; j++)
    {
        if (nums[i] + nums[j] == target)
        {
            return new int[] { i, j };
        }
    }
}

return new int[] { };
```

**Complexity:** O(n²) — nested loop, checks every pair. Fine for now.

---

## Contains Duplicate

**Problem:** Given an array of integers, return `true` if any value appears at least twice, `false` if all elements are distinct.

**My understanding:** Check if the array has any repeated value.

**My approach:** Keep a "seen" list — before inserting each element, check if it's already there. If yes, return true immediately.

**My first attempt:**
```csharp
int[] nums = [1, 2, 3, 4];
HashSet<int> seen = new HashSet<int>();

foreach (var i in nums)
{
    if (seen.Contains(i)) return true;
    seen.Add(i);
}

return false;
```

**What I learned:**
- HashSet can't hold duplicates by nature — useful for "have I seen this before" problems
- Single loop is enough, no need to compare every pair like Two Sum
- One-liner shortcut: dump everything into a HashSet then compare Count vs Length — if they differ, duplicates existed

**Final answer (C#):**
```csharp
int[] nums = [1, 2, 3, 4];
HashSet<int> seen = new HashSet<int>();

foreach (var i in nums)
{
    if (seen.Contains(i)) return true;
    seen.Add(i);
}

return false;
```

**Bonus one-liner:**
```csharp
return nums.Length != new HashSet<int>(nums).Count;
```
HashSet can't hold duplicates — if the count after inserting everything is less than the original length, duplicates existed.

**Complexity:** O(n) — single loop, HashSet lookup is instant. Better than Two Sum's O(n²).

---

## Maximum Subarray

**Problem:** Given an array of integers, find the contiguous subarray with the largest sum and return that sum.

**My understanding:** Find which continuous chunk of the array gives the biggest sum. Subarray means no skipping — elements must be next to each other.

**My first attempt (pseudocode):**
```
max = first element
sum = 0

for each element:
    sum += element
    if sum > max → max = sum
    if sum < 0 → reset sum to 0

return max
```

**What I learned:**
- This is Kadane's Algorithm — if the running sum goes negative, it's dragging you down so discard it and start fresh
- Update `max` before resetting `sum` — otherwise you lose the value
- Return `max` not `sum` — sum gets reset to 0, max holds the real answer
- Not like Two Sum — they want the sum itself, not indices

**Final answer (C#):**
```csharp
int max = nums[0];
int sum = 0;

foreach (var num in nums)
{
    sum += num;
    if (sum > max) max = sum;
    if (sum < 0) sum = 0;
}

return max;
```

**Complexity:** O(n) — single loop, one pass through the array.

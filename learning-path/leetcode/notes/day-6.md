# Day 6 Notes - Sliding Window

**Goal:** Learn to avoid nested loops when working with subarrays or substrings.

**Focus:** A window slides across the array — expand the right side, shrink the left when a condition breaks. One loop, no nesting.

| Problem | Difficulty | Link |
|---|---|---|
| Maximum Average Subarray I | Easy | [leetcode.com/problems/maximum-average-subarray-i](https://leetcode.com/problems/maximum-average-subarray-i) |
| Longest Substring Without Repeating Characters | Medium | [leetcode.com/problems/longest-substring-without-repeating-characters](https://leetcode.com/problems/longest-substring-without-repeating-characters) |
| Minimum Size Subarray Sum | Medium | [leetcode.com/problems/minimum-size-subarray-sum](https://leetcode.com/problems/minimum-size-subarray-sum) |

---

## Maximum Average Subarray I

**Problem:** Given an integer array `nums` and integer `k`, find the contiguous subarray of length `k` with the maximum average and return that average.

**My understanding:** Fixed window of size `k` — find which window has the biggest sum, divide by `k` at the end.

**Key insight:** Instead of summing k elements every step, just add the incoming element and remove the outgoing one. One pass, no nesting.

**What I learned:**
- Initialize the first window with a separate loop, then slide from `i = k`
- `max / k` does integer division — cast to `(double)max / k`
- Same pattern as Max Subarray but fixed window size

**Final answer (C#):**
```csharp
int sum = 0;
for (int i = 0; i < k; i++)
    sum += nums[i];

int max = sum;

for (int i = k; i < nums.Length; i++)
{
    sum += nums[i];
    sum -= nums[i - k];
    max = Math.Max(max, sum);
}

return (double)max / k;
```

**Complexity:** O(n) — single pass after initial window.

---

## Longest Substring Without Repeating Characters

**Problem:** Given a string `s`, find the length of the longest substring without repeating characters.

**My understanding:** Find the longest stretch of characters where none repeat.

**Key insight:** Variable window — expand right, shrink left when a duplicate enters. Use HashSet to track what's in the current window.

**What I learned:**
- Use `while` not `if` when shrinking — need to keep removing from left until duplicate is fully gone
- `if` only removes one character then moves on — window can still have duplicates
- This cost me an interview at Ant Group 😅

**Final answer (C#):**
```csharp
HashSet<char> seen = new();
int left = 0;
int right = 0;
int max = 0;

while (right < s.Length)
{
    while (seen.Contains(s[right]))
    {
        seen.Remove(s[left]);
        left++;
    }
    seen.Add(s[right]);
    max = Math.Max(max, right - left + 1);
    right++;
}

return max;
```

**Complexity:** O(n) — each character is added and removed at most once.

---

## Minimum Size Subarray Sum

**Problem:** Given an array of positive integers and a target, return the minimum length of a subarray whose sum is >= target. Return 0 if none exists.

**My understanding:** Find the shortest continuous chunk that sums to at least target.

**Key insight:** Variable window — expand right to grow the sum, shrink left when sum >= target to find the smallest valid window.

**What I learned:**
- Initialize `min = int.MaxValue` not 0 — `Math.Min(0, anything)` always returns 0
- Use `while` not `if` when shrinking — keep shrinking as long as sum >= target
- Return `min == int.MaxValue ? 0 : min` to handle the no-solution case

**Final answer (C#):**
```csharp
int sum = 0;
int left = 0;
int min = int.MaxValue;

for (int right = 0; right < nums.Length; right++)
{
    sum += nums[right];

    while (sum >= target)
    {
        min = Math.Min(min, right - left + 1);
        sum -= nums[left];
        left++;
    }
}

return min == int.MaxValue ? 0 : min;
```

**Complexity:** O(n) — each element is added and removed at most once.

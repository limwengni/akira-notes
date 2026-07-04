# Day 5 Notes - Review + Mixed

**Goal:** Revisit anything struggled with, then try something new.

**Focus:** Best Time to Buy and Sell Stock introduces greedy tracking. Climbing Stairs is the first taste of dynamic programming — notice the pattern, don't stress it yet.

| Problem | Difficulty | Link |
|---|---|---|
| Best Time to Buy and Sell Stock | Easy | [leetcode.com/problems/best-time-to-buy-and-sell-stock](https://leetcode.com/problems/best-time-to-buy-and-sell-stock) |
| Climbing Stairs | Easy, but new idea | [leetcode.com/problems/climbing-stairs](https://leetcode.com/problems/climbing-stairs) |

---

## Best Time to Buy and Sell Stock

**Problem:** Given an array of prices where `prices[i]` is the stock price on day `i`, return the maximum profit you can achieve by buying on one day and selling on a later day. Return `0` if no profit is possible.

**My understanding:** Find the max profit — buy low, sell high, but you must buy before you sell.

**My first attempt (pseudocode):**
```
max = first element
profit = 0

for each element:
    profit -= element        // wrong — was trying to apply Kadane's but incorrect here
    max = Math.Max(max, profit)
    if profit < 0 → reset
```

**What I learned:**
- Kadane's pattern doesn't directly apply here — profit is `sell - buy`, not a running sum
- Track `minPrice` (cheapest buy seen so far) instead of resetting to 0
- For each price, best profit today = `currentPrice - minPrice`
- If prices only go down, `currentPrice - minPrice` is always ≤ 0, so `maxProfit` stays 0 naturally

**Final answer (C#):**
```csharp
int minPrice = prices[0];
int maxProfit = 0;

for (int i = 0; i < prices.Length; i++)
{
    minPrice = Math.Min(minPrice, prices[i]);
    maxProfit = Math.Max(maxProfit, prices[i] - minPrice);
}

return maxProfit;
```

**Complexity:** O(n) — single pass, two variables.

---

## Climbing Stairs

**Problem:** You are climbing a staircase with `n` steps. Each time you can climb 1 or 2 steps. Return the number of distinct ways to reach the top.

**My understanding:** Count all possible combinations of 1-step and 2-step moves that add up to `n`.

**Key insight:** To reach step `n`, you either came from step `n-1` (took 1 step) or step `n-2` (took 2 steps). So:

```
ways(n) = ways(n-1) + ways(n-2)
```

This is Fibonacci. Base cases: `n=1` → 1 way, `n=2` → 2 ways.

**What I learned:**
- This is dynamic programming — reuse previous results instead of recalculating
- Recursion would work but is slow (recalculates same values repeatedly)
- DP version only needs two variables (`prev` and `curr`), not an array
- Loop starts at 3 because base cases cover 1 and 2, and condition is `i <= n` not `i < n`

**Final answer (C#):**
```csharp
int prev = 1;
int curr = 2;
int next;

if (n <= 2) return n; // base cases: n=1 → 1 way, n=2 → 2 ways, both equal n

for (int i = 3; i <= n; i++)
{
    next = prev + curr;
    prev = curr;
    curr = next;
}

return curr;
```

**Complexity:** O(n) — single loop, constant space.

---

## What Tripped Me Up

**Best Time to Buy and Sell Stock:**
- First instinct was to apply Kadane's Algorithm but the mechanics are different — profit is `sell - buy`, not a running sum
- Tracking `minPrice` is the key insight, not resetting to 0

**Climbing Stairs:**
- Looks like recursion but DP is better — recursion recalculates the same values repeatedly
- Loop condition must be `i <= n` not `i < n`, otherwise you stop one step short
- Just two variables needed (`prev` and `curr`), no array required
- Edge case: without the `n <= 2` guard, `n = 1` skips the loop and wrongly returns `curr = 2`

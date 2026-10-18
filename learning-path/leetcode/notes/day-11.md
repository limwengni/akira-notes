# Day 11 Notes - Needs Revisit

## Minimum Swaps to Sort by Digit Sum

**Problem:** [LeetCode 3551 - Minimum Swaps to Sort by Digit Sum](https://leetcode.com/problems/minimum-swaps-to-sort-by-digit-sum/)

**Difficulty:** Medium

**Status:** Needs revisit

This problem combines several ideas and felt difficult. The digit-sum part is understood; the harder part is building the target order and counting the minimum swaps.

### Main pipeline

```text
1. Calculate the digit sum for every number.
2. Build the final target order by sorting numbers by:
   - smaller digit sum first
   - smaller number first when digit sums are equal
3. Compare the current nums array with the target array.
4. Use indexMap[number] to find where the desired number currently is.
5. Swap it into the correct position.
6. Update indexMap after every swap.
```

### Important meanings

```text
sums[number]    = digit sum of that number
target[i]       = number that should finally be at index i
indexMap[number] = number's current index in nums
```

`indexMap` starts with the original indices, but after swaps it must be updated to store the numbers' current indices.

For example:

```text
nums   = [37, 100]
sums   = { 37: 10, 100: 1 }
target = [100, 37]
```

At index `0`, the target says `100` belongs there. `indexMap[100]` tells us that `100` is currently at index `1`, so we swap indices `0` and `1`. The answer is one swap.

### Why it is difficult

The problem is not just digit sums. It combines digit extraction, custom sorting, dictionaries, array mutation, and minimum-swap reasoning. Revisit this after practising easier sorting and dictionary problems.

**Complexity:** O(n log n) time because of sorting; O(n) extra space for the digit-sum dictionary, target list, and index dictionary.

---

## Find the N-th Value After K Seconds

**Problem:** [LeetCode 3179 - Find the N-th Value After K Seconds](https://leetcode.com/problems/find-the-n-th-value-after-k-seconds/)

Start with an array of `n` ones. Each second, every position becomes the sum of itself and all values before it. Return the final value at the last index after `k` seconds.

### Example

```text
Start: [1, 1, 1, 1]
After 1 second: [1, 2, 3, 4]
After 2 seconds: [1, 3, 6, 10]
```

The update is done from left to right in place:

```csharp
nums[i] = nums[i] + nums[i - 1];
```

The old `nums[i]` is the current value from the previous second. The `nums[i - 1]` value is already the newest prefix sum from the current second, so it acts as the running left sum. No separate `leftSum` variable is needed.

```csharp
public class Solution
{
    public int ValueAfterKSeconds(int n, int k)
    {
        const int mod = 1_000_000_007;
        int[] nums = new int[n];
        Array.Fill(nums, 1);

        for (int second = 1; second <= k; second++)
        {
            for (int i = 1; i < n; i++)
            {
                nums[i] = (nums[i] + nums[i - 1]) % mod;
            }
        }

        return nums[n - 1];
    }
}
```

For `n = 4, k = 1`, the full state becomes `[1, 2, 3, 4]`, but the method returns only the last value: `4`.

**Complexity:** O(n × k) time because the array is updated once for every position during every second; O(n) space for the array.

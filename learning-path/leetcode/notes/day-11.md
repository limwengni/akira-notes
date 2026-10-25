# Day 11 Notes

| Problem | Difficulty | Link |
|---|---|---|
| Minimum Swaps to Sort by Digit Sum | Medium | [leetcode.com/problems/minimum-swaps-to-sort-by-digit-sum](https://leetcode.com/problems/minimum-swaps-to-sort-by-digit-sum) |
| Find the N-th Value After K Seconds | Easy | [leetcode.com/problems/find-the-n-th-value-after-k-seconds](https://leetcode.com/problems/find-the-n-th-value-after-k-seconds) |

---

## Minimum Swaps to Sort by Digit Sum

**Problem:** [LeetCode 3551 - Minimum Swaps to Sort by Digit Sum](https://leetcode.com/problems/minimum-swaps-to-sort-by-digit-sum/)

**Difficulty:** Medium

**Status:** ✅ Solved

### Main pipeline

```text
1. Calculate the digit sum for every number → sumMap
2. Record each number's original index → indexMap (same loop)
3. Build target = sorted copy of nums by: smaller digit sum first, tie → smaller number
4. Swap loop: for each i, if nums[i] != target[i]:
   - find target[i]'s current position via indexMap
   - swap nums[i] with nums[oldIndex]
   - update indexMap for BOTH swapped numbers
   - swaps++
```

### Important meanings

```text
sumMap[number]   = digit sum of that number
target[i]        = number that should finally be at index i
indexMap[number] = number's CURRENT index in nums (updates after every swap)
```

### What tripped me up

- Modified `nums[i]` directly in the digit sum loop → by the time `sumMap[nums[i]] = sum` ran, `nums[i]` was already 0. Fix: use a temp variable `n = nums[i]` and divide `n`, never `nums[i]`
- `sum` must be declared INSIDE the loop — declared outside means it accumulates across all numbers instead of resetting per number
- Classic swap bug: wrote `nums[oldIndex] = nums[i]` after already overwriting `nums[i]` → used `temp` but forgot to place it. Always: save → overwrite → restore from temp
- indexMap update: use `temp` (the displaced number's value) as the key for `oldIndex`, not `nums[oldIndex]` — clearer and avoids reading a value that just changed

### Trace example

```text
nums   = [37, 100, 50]
target = [100, 50, 37]
indexMap = {37:0, 100:1, 50:2}

i=0: target[0]=100, indexMap[100]=1 → swap indices 0,1
     nums=[100,37,50], indexMap={100:0, 37:1, 50:2}, swaps=1

i=1: target[1]=50, indexMap[50]=2 → swap indices 1,2
     nums=[100,50,37], indexMap={100:0, 50:1, 37:2}, swaps=2

i=2: nums[2]==target[2]==37 → skip
Result: 2 swaps
```

### Final answer (C#)

```csharp
public class Solution {
    public int MinSwaps(int[] nums) {
        Dictionary<int, int> sumMap = new();
        Dictionary<int, int> indexMap = new();

        for (int i = 0; i < nums.Length; i++) {
            int sum = 0;        // reset for each number
            int n = nums[i];    // don't touch nums[i]

            while (n > 0) {
                sum += n % 10;
                n /= 10;
            }

            sumMap[nums[i]] = sum;
            indexMap[nums[i]] = i;  // original position
        }

        int[] target = [.. nums];
        Array.Sort(target, (a, b) => sumMap[a] != sumMap[b]
            ? sumMap[a].CompareTo(sumMap[b])
            : a.CompareTo(b));

        int swaps = 0;
        for (int i = 0; i < nums.Length; i++) {
            if (nums[i] == target[i]) continue;

            int oldIndex = indexMap[target[i]];   // where target[i] currently lives
            int temp = nums[i];
            nums[i] = nums[oldIndex];             // bring target[i] here
            nums[oldIndex] = temp;                // displace current number

            indexMap[nums[i]] = i;                // target[i] now at i
            indexMap[temp] = oldIndex;            // displaced number now at oldIndex

            swaps++;
        }

        return swaps;
    }
}
```

**Complexity:** O(n log n) — sort dominates. O(n) extra space for the two dictionaries and target array.

**Note:** requires distinct numbers — duplicate keys would break both dictionaries. Constraints guarantee `nums` consists of distinct positive integers.

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

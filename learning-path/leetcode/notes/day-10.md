# Day 10 Notes - Review and Mixed Patterns

**Goal:** Combine earlier array techniques and learn how to reuse work instead of repeatedly scanning the same values.

| Problem | Difficulty | Link |
|---|---|---|
| Left and Right Sum Differences | Easy warm-up | [leetcode.com/problems/left-and-right-sum-differences](https://leetcode.com/problems/left-and-right-sum-differences) |
| Product of Array Except Self | Medium | [leetcode.com/problems/product-of-array-except-self](https://leetcode.com/problems/product-of-array-except-self) |
| Find Pivot Index | Easy | [leetcode.com/problems/find-pivot-index](https://leetcode.com/problems/find-pivot-index) |
| Find the Highest Altitude | Easy | [leetcode.com/problems/find-the-highest-altitude](https://leetcode.com/problems/find-the-highest-altitude) |
| Maximum Subarray | Medium | [leetcode.com/problems/maximum-subarray](https://leetcode.com/problems/maximum-subarray) |
| Best Time to Buy and Sell Stock | Easy | [leetcode.com/problems/best-time-to-buy-and-sell-stock](https://leetcode.com/problems/best-time-to-buy-and-sell-stock) |
| Maximum Value of a String in an Array | Easy | [leetcode.com/problems/maximum-value-of-a-string-in-an-array](https://leetcode.com/problems/maximum-value-of-a-string-in-an-array) |
| 3Sum | Medium | [leetcode.com/problems/3sum](https://leetcode.com/problems/3sum) |

---

## Left and Right Sum Differences

**Problem:** For every index, calculate the absolute difference between the sum of all numbers to its left and the sum of all numbers to its right. The current number belongs to neither side.

**Example:**
```text
nums = [10, 4, 8, 3]

left sums  = [0, 10, 14, 22]
right sums = [15, 11, 3, 0]
answer     = [15, 1, 11, 22]
```

At index `1`, the current number is `4`:
```text
left sum  = 10
right sum = 8 + 3 = 11
answer    = |10 - 11| = 1
```

**Key rule:** save the running sum first to exclude the current number, then update the sum so the current number is available to the next position.

```csharp
leftAnswer[i] = leftSum;
leftSum += nums[i];
```

The right pass follows the same order while moving backward:

```csharp
rightAnswer[i] = rightSum;
rightSum += nums[i];
```

At index `0`, nothing is on the left, so its left sum is `0`. At the final index, nothing is on the right, so its right sum is `0`.

### Final answer (C#)

```csharp
public class Solution
{
    public int[] LeftRightDifference(int[] nums)
    {
        int[] leftAnswer = new int[nums.Length];
        int leftSum = 0;

        for (int i = 0; i < nums.Length; i++)
        {
            leftAnswer[i] = leftSum;
            leftSum += nums[i];
        }

        int[] rightAnswer = new int[nums.Length];
        int rightSum = 0;

        for (int i = nums.Length - 1; i >= 0; i--)
        {
            rightAnswer[i] = rightSum;
            rightSum += nums[i];
        }

        int[] answer = new int[nums.Length];

        for (int i = 0; i < nums.Length; i++)
            answer[i] = Math.Abs(leftAnswer[i] - rightAnswer[i]);

        return answer;
    }
}
```

**Complexity:** O(n) time; O(n) extra space.

### Connection to Product of Array Except Self

```text
Sum version:
store left and right separately
then combine with subtraction

Product version:
store left directly in answer
then combine with right using multiplication
```

In the sum solution, `rightAnswer` is an empty separate array, so the right pass assigns the running value directly:

```csharp
rightAnswer[i] = rightSum;
```

In the product solution, `answer[i]` already contains the left product. The right pass must combine that stored value with the running right product:

```csharp
answer[i] *= rightProduct;
```

The exclusion does **not** come from choosing `=` or `*=`. In both problems, the current number is excluded because the running sum or product is used **before** it is updated with `nums[i]`.

---

## Product of Array Except Self

**Problem:** For every index, return the product of every number except the number at that index. The solution must run in O(n) time without division.

**Example:**
```text
nums   = [1,  2, 3, 4]
answer = [24, 12, 8, 6]

index 0: 2 × 3 × 4 = 24
index 1: 1 × 3 × 4 = 12
index 2: 1 × 2 × 4 = 8
index 3: 1 × 2 × 3 = 6
```

**Initial confusion:** This needs multiplication (a product), not addition (a sum). Starting another full scan for every index would work but take O(n²). Calculating one total product and dividing by the current number is forbidden and also causes problems when zeros appear.

### Prefix and suffix pattern

```text
answer[i] = product of everything left of i
          × product of everything right of i
```

| Index | Current | Left product | Right product | Answer |
|---:|---:|---:|---:|---:|
| 0 | 1 | 1 | 24 | 24 |
| 1 | 2 | 1 | 12 | 12 |
| 2 | 3 | 2 | 4 | 8 |
| 3 | 4 | 6 | 1 | 6 |

When one side is empty, its product is `1` because multiplying by `1` changes nothing.

### First pass - left to right

Store the product of everything before the current index. Use the running product first so the current number is excluded, then include the current number for the next index.

```csharp
int leftProduct = 1;

for (int i = 0; i < nums.Length; i++)
{
    answer[i] = leftProduct;
    leftProduct *= nums[i];
}
```

```text
i = 0: answer[0] = 1; leftProduct becomes 1
i = 1: answer[1] = 1; leftProduct becomes 2
i = 2: answer[2] = 2; leftProduct becomes 6
i = 3: answer[3] = 6; leftProduct becomes 24

answer after first pass = [1, 1, 2, 6]
```

### Second pass - right to left

Multiply each stored left product by the product of everything to its right. Again, use the running product first, then include the current number for the next index to the left.

```csharp
int rightProduct = 1;

for (int i = nums.Length - 1; i >= 0; i--)
{
    answer[i] *= rightProduct;
    rightProduct *= nums[i];
}
```

```text
i = 3: answer[3] = 6 × 1  = 6;  rightProduct becomes 4
i = 2: answer[2] = 2 × 4  = 8;  rightProduct becomes 12
i = 1: answer[1] = 1 × 12 = 12; rightProduct becomes 24
i = 0: answer[0] = 1 × 24 = 24

final answer = [24, 12, 8, 6]
```

### Final answer (C#)

```csharp
public class Solution
{
    public int[] ProductExceptSelf(int[] nums)
    {
        int[] answer = new int[nums.Length];
        int leftProduct = 1;

        for (int i = 0; i < nums.Length; i++)
        {
            answer[i] = leftProduct;
            leftProduct *= nums[i];
        }

        int rightProduct = 1;

        for (int i = nums.Length - 1; i >= 0; i--)
        {
            answer[i] *= rightProduct;
            rightProduct *= nums[i];
        }

        return answer;
    }
}
```

**Memory shortcut:**
```text
Left  → save, then multiply
Right → apply, then multiply
```

**Transferable rule:** use the running value first to exclude the current element, then update it so the current element is available to the next position.

**Complexity:** O(n) time. The returned answer array does not count as extra space under the problem's rules, so auxiliary space is O(1).

---

## Find Pivot Index

**Problem:** Return the first index where the sum of all numbers on the left equals the sum of all numbers on the right. The current number belongs to neither side.

Calculate the total first. During the second pass, remove the current number and the left sum from the total; whatever remains is the right sum.

```csharp
public class Solution
{
    public int PivotIndex(int[] nums)
    {
        int totalSum = 0;
        foreach (int num in nums)
            totalSum += num;

        int leftSum = 0;

        for (int i = 0; i < nums.Length; i++)
        {
            int rightSum = totalSum - leftSum - nums[i];

            if (leftSum == rightSum)
                return i;

            leftSum += nums[i];
        }

        return -1;
    }
}
```

**Important order:** calculate the right sum and compare first; only then add `nums[i]` to `leftSum` for the next index.

**Complexity:** O(n) time because there are two sequential passes; O(1) extra space because only fixed variables are used.

---

## Find the Highest Altitude

Keep the current altitude and the highest altitude seen so far. There is no need to store every altitude in an array.

```csharp
int altitude = 0;
int highest = 0;

foreach (int change in gain)
{
    altitude += change;
    highest = Math.Max(highest, altitude);
}
```

**Complexity:** O(n) time; O(1) extra space.

---

## Maximum Subarray

Kadane's algorithm tracks two values:

```text
current = best subarray sum ending at this index
largest = best sum found anywhere so far
```

At every number, choose whether to start a new subarray or continue the previous one:

```csharp
public int MaxSubArray(int[] nums)
{
    int current = nums[0];
    int largest = nums[0];

    for (int i = 1; i < nums.Length; i++)
    {
        current = Math.Max(nums[i], current + nums[i]);
        largest = Math.Max(largest, current);
    }

    return largest;
}
```

**Complexity:** O(n) time; O(1) extra space. Initializing from `nums[0]` correctly handles arrays containing only negative numbers.

---

## Best Time to Buy and Sell Stock

Track the cheapest buying price seen so far and the best profit seen so far. For each later price, calculate the profit from selling today before updating the cheapest price.

```csharp
int minPrice = prices[0];
int maxProfit = 0;

for (int i = 1; i < prices.Length; i++)
{
    maxProfit = Math.Max(maxProfit, prices[i] - minPrice);
    minPrice = Math.Min(minPrice, prices[i]);
}
```

The order ensures the buying day always comes before the selling day.

**Complexity:** O(n) time; O(1) extra space.

---

## Maximum Value of a String in an Array

For each string:

```text
numeric string → use its real integer value
non-numeric string → use its character length
```

Track only the current value and maximum value; no result array is needed.

```csharp
int maxValue = 0;

foreach (string str in strs)
{
    int currentValue = int.TryParse(str, out int number)
        ? number
        : str.Length;

    maxValue = Math.Max(maxValue, currentValue);
}
```

**Complexity:** O(total character count) time, or O(n × k) when there are `n` strings of maximum length `k`; O(1) extra space.

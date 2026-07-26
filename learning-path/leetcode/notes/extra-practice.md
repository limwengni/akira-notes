# Extra Practice Notes

Problems beyond the Day 1-5 plan. Focus: `Dictionary<TKey, List<TValue>>` pattern.

---

## Pairs That Sum to Zero

**Problem:** Given an array of integers, return the indices of all pairs that sum to zero.

**Example:**
```
Input:  nums = [-3, 0, 1, 3, -1, 2]
Output: [[0,3], [2,4]]  // -3+3=0, 1+(-1)=0
```

**My understanding:** Find all index pairs where the two values add up to zero. Multiple pairs possible, so collect all of them.

**What tripped me up:**
- Used `else` when adding to dict — only added when no complement found. Bug: future numbers couldn't pair with already-seen numbers
- Used `dict[nums[i]] = new List<int> { i }` which overwrites the list on duplicates — use `Add` instead
- Dict value needs to be `List<int>` not `int` because same number can appear at multiple indices

**Key insight:** Check complement → collect pairs → always update dict. In that order, every iteration. Finding pairs and updating dict are independent — never put one inside the other's if/else.

**Final answer (C#):**
```csharp
List<int[]> result = new();
Dictionary<int, List<int>> dict = new();
int target = 0;

for (int i = 0; i < nums.Length; i++)
{
    int partner = target - nums[i];

    if (dict.ContainsKey(partner))
    {
        foreach (var j in dict[partner])
            result.Add(new int[] { j, i });
    }

    if (!dict.ContainsKey(nums[i]))
        dict[nums[i]] = new List<int>();
    dict[nums[i]].Add(i);
}

return result;
```

**Complexity:** O(n) — single pass, dict lookup is instant.

---

## Group Anagrams

**Problem:** Given an array of strings, group the anagrams together.

**Example:**
```
Input:  ["eat", "tea", "tan", "ate", "nat", "bat"]
Output: [["eat","tea","ate"], ["tan","nat"], ["bat"]]
```

**My understanding:** Anagrams share the same characters same count. Group all strings that are anagrams of each other.

**Key insight:** Sort the characters of each word — anagrams all sort to the same string. Use that sorted string as the dict key.

```
"eat" → sort → "aet"
"tea" → sort → "aet"   // same key, same group
"ate" → sort → "aet"   // same key, same group
"tan" → sort → "ant"   // different key, different group
```

**What tripped me up:**
- `c.ToString()` gives `"System.Char[]"` not the actual string — use `new string(c)` instead
- `string[]` is fixed size, can't `.Add()` to it — use `List<string>`
- Used original word as dict key instead of sorted word

**Final answer (C#):**
```csharp
Dictionary<string, List<string>> dict = new();

for (int i = 0; i < strings.Length; i++)
{
    char[] c = strings[i].ToCharArray();
    Array.Sort(c);
    string sorted = new string(c);

    if (!dict.ContainsKey(sorted))
        dict[sorted] = new List<string>();
    dict[sorted].Add(strings[i]);
}

return dict.Values.ToList();
```

**Complexity:** O(n * k log k) — n strings, each sorted in k log k where k is string length.

---

## Top K Frequent Elements

**Problem:** Given an array of integers and a number `k`, return the `k` most frequent elements.

**Example:**
```
Input:  nums = [1,1,1,2,2,3], k = 2
Output: [1, 2]
```

**My understanding:** Count how many times each number appears, then return the top k numbers by frequency.

**What tripped me up:**
- `OrderByDescending` returns `KeyValuePair<int,int>` — need `.Select(x => x.Key)` to extract just the numbers
- `.ToList()` returns `List<int>`, `.ToArray()` returns `int[]` — match whatever the method signature expects

**Final answer (C#):**
```csharp
Dictionary<int, int> dict = new();

for (int i = 0; i < nums.Length; i++)
{
    if (dict.ContainsKey(nums[i]))
        dict[nums[i]]++;
    else
        dict[nums[i]] = 1;
}

return dict.OrderByDescending(x => x.Value)
           .Take(k)
           .Select(x => x.Key)
           .ToArray();
```

**Complexity:** O(n log n) — sorting the dict dominates.

---

## Permutation in String

**Problem:** Given two strings `s1` and `s2`, return `true` if `s2` contains a permutation of `s1`.

**Example:**
```
Input:  s1 = "ab", s2 = "eidbaooo"
Output: true  // "ba" is a permutation of "ab"
```

**My understanding:** Check if any substring of `s2` with length `s1.Length` has the same character frequencies as `s1`.

**Key insight:** Fixed window of size `s1.Length` slides across `s2`. Instead of sorting (slow), compare character frequency dicts. Add incoming char, remove outgoing char, compare after each slide.

**What tripped me up:**
- `dictS2[s2[right]]++` crashes if key doesn't exist — initialize to 0 first
- `dictS2.Remove(s2[left])` removes the whole key — decrement first, only remove if count hits 0
- Need to check first window match before the while loop — if `s1 == s2`, loop never runs
- `left = right - s1.Length` must be calculated before using `left`

**Final answer (C#):**
```csharp
Dictionary<char, int> dictS1 = new();
Dictionary<char, int> dictS2 = new();
int left = 0;
int right = s1.Length;

for (int i = 0; i < s1.Length; i++)
{
    if (dictS1.ContainsKey(s1[i])) dictS1[s1[i]]++;
    else dictS1[s1[i]] = 1;
}

for (int i = 0; i < s1.Length; i++)
{
    if (dictS2.ContainsKey(s2[i])) dictS2[s2[i]]++;
    else dictS2[s2[i]] = 1;
}

// check first window
bool isMatch = dictS1.All(x => dictS2.GetValueOrDefault(x.Key, 0) == x.Value);
if (isMatch) return true;

while (right < s2.Length)
{
    if (!dictS2.ContainsKey(s2[right])) dictS2[s2[right]] = 0;
    dictS2[s2[right]]++;
    left = right - s1.Length;
    dictS2[s2[left]]--;
    if (dictS2[s2[left]] == 0) dictS2.Remove(s2[left]);

    isMatch = dictS1.All(x => dictS2.GetValueOrDefault(x.Key, 0) == x.Value);
    if (isMatch) return true;

    right++;
}

return false;
```

**Complexity:** O(n) — single pass, dict comparison is O(26) = constant for lowercase letters.

---

## Fruit Into Baskets

**Problem:** Given an array of fruit types, return the maximum number of fruits you can pick from a contiguous subarray with at most 2 distinct fruit types.

**Example:**
```
Input:  fruits = [1, 2, 1, 2, 3]
Output: 4  // [1, 2, 1, 2] has 2 types
```

**My understanding:** Longest subarray with at most 2 distinct values. Variable window — expand right, shrink left when more than 2 types in window.

**What tripped me up:**
- Dict tracks **counts** not just presence — need count to know when a type is fully gone from window
- Shrink condition is `dict.Count > 2` not `dict[x] > 2` — count of distinct types, not count of one fruit
- When shrinking, decrement `fruits[left]` not `fruits[right]`
- `right` starts at 0, not `fruits.Length - 1`

**Final answer (C#):**
```csharp
Dictionary<int, int> dict = new();
int left = 0, right = 0, max = 0;

while (right < fruits.Length)
{
    if (!dict.ContainsKey(fruits[right])) dict[fruits[right]] = 0;
    dict[fruits[right]]++;

    while (dict.Count > 2)
    {
        dict[fruits[left]]--;
        if (dict[fruits[left]] == 0)
            dict.Remove(fruits[left]);
        left++;
    }

    max = Math.Max(max, right - left + 1);
    right++;
}

return max;
```

**Complexity:** O(n) — each element added and removed at most once.

---

## Rank Transform of an Array

**Problem:** Replace each element with its rank — smallest distinct value is rank 1, next distinct value rank 2, etc. Equal values share the same rank.

**Example:**
```
Input:  arr = [40, 10, 20, 30]
Output: [4, 1, 2, 3]

Input:  arr = [100, 100, 100]
Output: [1, 1, 1]
```

**My understanding:** Rank = position in sorted order with duplicates collapsed. Two phases: sort a copy to learn the ranks (dict of value → rank), then walk the original order and look each one up.

**What tripped me up:**
- First idea was assigning ranks while scanning the original order and reshuffling when new numbers squeeze in — messy and O(n²). Sorting first makes ranks come for free
- Must sort a **copy** (`arr.Clone()`) — phase 2 needs the original order, and `Array.Sort(arr)` has no undo
- Duplicate rule: duplicates must not touch the rank counter — `rank++` goes **inside** the "not in dict yet" check, otherwise `[10,10,20]` ranks to `[1,1,3]` instead of `[1,1,2]`
- `int[]` has no `.Add` — fixed size, assign by index. Size known upfront → array; unknown → `List<int>`

**Final answer (C#):**
```csharp
public int[] ArrayRankTransform(int[] arr)
{
    int[] sorted = (int[])arr.Clone();
    Array.Sort(sorted);

    Dictionary<int, int> dict = new();
    int rank = 1;

    foreach (var sort in sorted)
    {
        if (!dict.ContainsKey(sort))
        {
            dict[sort] = rank;
            rank++;
        }
    }

    int[] res = new int[arr.Length];

    for (int i = 0; i < arr.Length; i++)
        res[i] = dict[arr[i]];

    return res;
}
```

**Complexity:** O(n log n) — the sort dominates; both loops are O(n). Empty array works for free: both loops run zero times, returns empty array.

First problem combining three days' tools at once: arrays (Day 1) + sorting + hash map (Day 3).

---

## Sequential Digits

**Problem:** Return all numbers in range `[low, high]` whose digits are sequential (each digit is one more than the previous).

**Example:**
```
Input:  low = 100, high = 300
Output: [123, 234]
```

**My understanding:** All sequential digit numbers come from sliding a window across `"123456789"`. Window size = number of digits. Collect numbers that fall within `[low, high]`.

**Key insight:** Fixed window sliding on the string `"123456789"`. Two loops — outer loop increases window size from `lowLen` to `highLen`, inner loop slides across the string.

**What tripped me up:**
- Inner loop condition is `i <= str.Length - lowLen` not `<` — otherwise last window is missed
- `lowLen++` must be outside the for loop (after it ends), not inside it
- `Substring(i, lowLen)` — second param is length, not end index

**Final answer (C#):**
```csharp
List<int> res = new();
int lowLen = low.ToString().Length;
int highLen = high.ToString().Length;
string str = "123456789";

while (lowLen <= highLen)
{
    for (int i = 0; i <= str.Length - lowLen; i++)
    {
        string strNum = str.Substring(i, lowLen);
        int num = int.Parse(strNum);

        if (num >= low && num <= high)
            res.Add(num);
    }
    lowLen++;
}

return res;
```

**Complexity:** O(1) — at most 36 sequential digit numbers exist (fixed search space).

---

## Height Checker

**Problem:** Count how many people are NOT standing where they'd be if the line were sorted by height.

**Example:**
```
Input:  heights = [1, 1, 4, 2, 1, 3]
Sorted:           [1, 1, 1, 2, 3, 4]
Output: 3  // indexes 2, 4, 5 differ
```

**My understanding:** Compare the array against its sorted version, count positions that differ.

**Lesson learned: READ THE CONSTRAINTS FIRST.** Heights are 1–100 — a small value range unlocks the counting trick. Constraints are part of the problem: small range → counting arrays, huge n → brute force will TLE, tiny n → brute force is fine.

**Way 1 — sort a copy, compare:**
```csharp
public int HeightChecker(int[] heights)
{
    int[] sorted = (int[])heights.Clone();
    Array.Sort(sorted);

    int mismatch = 0;

    for (int i = 0; i < heights.Length; i++)
    {
        if (heights[i] != sorted[i])
            mismatch++;
    }

    return mismatch;
}
```
O(n log n) — general tool, works for any values.

**Way 2 — counting (no sort at all):**
```csharp
public int HeightChecker(int[] heights)
{
    int[] heightToFreq = new int[101]; // heights 1-100, index = height, slot 0 unused

    foreach (var height in heights)
        heightToFreq[height]++;       // tally: heightToFreq[1] = 3 means three people of height 1

    int mismatch = 0;
    int currHeight = 0;

    for (int i = 0; i < heights.Length; i++)
    {
        // skip heights nobody has → currHeight lands on smallest height still in stock
        while (heightToFreq[currHeight] == 0)
            currHeight++;

        // currHeight is what sorted[i] WOULD be — compare without ever sorting
        if (currHeight != heights[i])
            mismatch++;

        heightToFreq[currHeight]--;   // one person of that height used up
    }

    return mismatch;
}
```
O(n) — the tally IS the sorted array stored compactly ("three 1s, then a 2, ..."); phase 2 deals it out smallest-first. This is counting sort.

**Key insights:**
- Array size 101 so index 100 exists (`new int[101]` = indexes 0..100); slot 0 wasted on purpose — cheaper than `height-1` math everywhere
- Array vs Dictionary as counter: dict has NO order — phase 2 needs smallest→largest, array indexes give that for free. Rule: small dense int keys → array as map; strings/sparse keys → dictionary. Same trick as the 26-letter anagram counter

---

## Find Target Indices After Sorting Array

**Problem:** Return all indices where `target` sits in the sorted version of the array, in increasing order.

**Example:**
```
Input:  nums = [1, 2, 5, 2, 3], target = 2
Sorted: [1, 2, 2, 3, 5] → 2s at indices [1, 2]
```

**Way 1 — sort and scan:**
```csharp
public IList<int> TargetIndices(int[] nums, int target)
{
    Array.Sort(nums);   // no Clone needed! answer refers to the SORTED array,
                        // original order is never needed again

    List<int> res = new();

    for (int i = 0; i < nums.Length; i++)
    {
        if (nums[i] == target)
            res.Add(i);
    }

    return res;
}
```

**Rule learned: clone before sorting only if the original order is still needed afterwards.** 1051/1331 answers referred to original positions → clone. Here the answer is defined on the sorted array → sort in place.

**Way 2 — no sorting at all (O(n)):** in sorted order all targets form one consecutive block, so two counts determine the whole answer:
- `lessCount` = elements < target → where the block **starts** (they'd fill the indices before it)
- `equalCount` = elements == target → how **many** indices to output

```csharp
int lessCount = 0, equalCount = 0;

foreach (var n in nums)
{
    if (n < target) lessCount++;
    else if (n == target) equalCount++;
}

List<int> res = new();
for (int i = 0; i < equalCount; i++)
    res.Add(lessCount + i);   // block starts at lessCount, one index per match

return res;
```

**Trace:** `[5, 1, 5, 3, 5]`, target 5 → lessCount = 2, equalCount = 3 → sorted would be `[1, 3, 5, 5, 5]` → output [2, 3, 4] ✓

**What tripped me up:**
- `res.Add(lessCount++)` also works but repurposes the variable (post-increment: emits current value, then bumps). `lessCount + i` keeps the meaning intact — clearer
- Don't expect to invent the counting trick on the spot — it's a collected pattern. The tell: answer depends only on sorted *positions*, not on actually touching the sorted array

**Complexity:** Way 1 O(n log n), Way 2 O(n) single pass + output loop.

---

## Longest Repeating Character Replacement

**Problem:** Given a string `s` and integer `k`, find the length of the longest substring containing the same letter after replacing at most `k` characters.

**Example:**
```
Input:  s = "AABABBA", k = 1
Output: 4
```

**My understanding:** Find the longest window where replacements needed <= k. Replacements needed = window size - count of most frequent char.

**Key insight:** Track frequency of each char using `int[26]`. Shrink when `(window size - maxFreq) > k`.

**What tripped me up:**
- Forgot to decrement freq when shrinking — used `++` instead of `--`
- `int[26]` is cleaner than dict for letter-only problems — no ContainsKey needed

**Final answer (C#):**
```csharp
int[] freq = new int[26];
int maxFreq = 0, max = 0, left = 0, right = 0;

while (right < s.Length)
{
    freq[s[right] - 'A']++;
    maxFreq = Math.Max(maxFreq, freq[s[right] - 'A']);

    while ((right - left + 1) - maxFreq > k)
    {
        freq[s[left] - 'A']--;
        left++;
    }

    max = Math.Max(max, right - left + 1);
    right++;
}

return max;
```

**Complexity:** O(n) — single pass.

---

## Max Consecutive Ones III

**Problem:** Given a binary array and integer `k`, return the maximum consecutive 1s if you can flip at most `k` zeros.

**Example:**
```
Input:  nums = [1,1,1,0,0,0,1,1,1,1,0], k = 2
Output: 6
```

**My understanding:** Find the longest window with at most `k` zeros. No need to actually flip anything — just track zero count in window.

**Key insight:** Simpler than character replacement — just count zeros, shrink when `zeroCount > k`.

**What I learned:**
- Don't modify the array — track conceptually
- When shrinking, only decrement `zeroCount` if `nums[left] == 0`

**Final answer (C#):**
```csharp
int left = 0, right = 0, max = 0, zeroCount = 0;

while (right < nums.Length)
{
    if (nums[right] == 0) zeroCount++;

    while (zeroCount > k)
    {
        if (nums[left] == 0) zeroCount--;
        left++;
    }

    max = Math.Max(max, right - left + 1);
    right++;
}

return max;
```

**Complexity:** O(n) — single pass.

---

## Find Greatest Common Divisor of Array

**Problem:** Return the GCD of the smallest and largest numbers in the array.

**Example:**
```
Input:  nums = [2, 5, 6, 9, 10]
Output: 2  // gcd(2, 10)
```

**My understanding:** Find min and max in one scan, then GCD = biggest number that divides both. Brute force: test every candidate from 1 to min, keep the last (biggest) one that divides both.

**The `%` rule that tripped me up (3 attempts!):** `a % b == 0` means "**b divides a** evenly" — candies % kids, remainder zero = shared perfectly. The thing doing the dividing goes on the RIGHT. My condition kept testing `mx % mn` — the loop variable `i` (the actual candidate) appeared nowhere in it.

**Divisor table for gcd(4, 8):**
```
i | 4 % i | 8 % i | divides both?
1 |   0   |   0   | yes
2 |   0   |   0   | yes
3 |   1   |   2   | no
4 |   0   |   0   | yes   → last winner = GCD = 4
```
The table headers ARE the code: `mn % i == 0 && mx % i == 0`.

**Final answer (C#):**
```csharp
public int FindGCD(int[] nums)
{
    int mn = nums[0], mx = 0;   // mx = 0 only safe because constraints say nums[i] >= 1

    for (int i = 0; i < nums.Length; i++)
    {
        mn = Math.Min(mn, nums[i]);
        mx = Math.Max(mx, nums[i]);
    }

    int gcd = 0;

    for (int i = 1; i <= mn; i++)   // <= mn, not < — mn itself can be the GCD
    {
        if (mx % i == 0 && mn % i == 0) gcd = i;
    }

    return gcd;
}
```

**Bonus — Euclid's algorithm (collected pattern, O(log) instead of O(n)):**
```csharp
while (b != 0)
{
    int temp = b;   // same save/overwrite/shift shuffle as linked list next/curr/prev
    b = a % b;
    a = temp;
}
return a;           // gcd(a, b) = gcd(b, a % b) until b hits 0
```

**Lessons learned:**
- Read the condition OUT LOUD as a sentence before submitting — "if max is divisible by min" doesn't mention `i` at all; would have caught the bug instantly. Rushing kept the same bug alive 3 rounds
- Loop range `[1, mn]` inclusive — stopping at `< mn` misses the case where min divides max

**Complexity:** O(n + mn) brute force; O(n + log(mn)) with Euclid.

---

## Maximum Product of Three Numbers

**Problem:** Return the maximum product of any three numbers in the array.

**Example:**
```
Input:  nums = [-10, -10, 1, 2, 3]
Output: 300   // (-10) * (-10) * 3, NOT 1 * 2 * 3 = 6
```

**My understanding:** Two candidates only — sort first, then it's four index reads:
1. Three largest: `arr[n-1] * arr[n-2] * arr[n-3]`
2. Two smallest (most negative) × largest: `arr[0] * arr[1] * arr[n-1]`

Return the bigger one. That's it.

**Why two negatives beat three positives:** negative × negative = big positive, then × the largest positive = even bigger. Always check if the two most-negative numbers produce a better product than the top three.

**Why `arr[n-1]` (not `arr[n-2]`) as the third multiplier in p2:** you want to maximize, so always pick the biggest available multiplier — that's the last element after sorting.

**What tripped me up:**
- First instinct was two pointers — doesn't fit here, no target to home in on, just two specific combinations to compare
- Easy to forget negative × negative = positive; "take the three largest" is wrong when the array has large negatives

**Final answer (C#):**
```csharp
public int MaximumProduct(int[] nums)
{
    Array.Sort(nums);
    int n = nums.Length;

    int p1 = nums[n-1] * nums[n-2] * nums[n-3];   // three largest
    int p2 = nums[0] * nums[1] * nums[n-1];         // two most-negative × largest

    return Math.Max(p1, p2);
}
```

**Complexity:** O(n log n) — sort dominates.

---

## Pattern: Dictionary with List as Value

Both problems use the same pattern:

```csharp
// initialize if key doesn't exist
if (!dict.ContainsKey(key))
    dict[key] = new List<T>();

// always add — never put this in else
dict[key].Add(value);
```

Rule: **always update the dict regardless of whether a match was found.**

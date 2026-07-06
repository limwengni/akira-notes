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

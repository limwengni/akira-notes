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

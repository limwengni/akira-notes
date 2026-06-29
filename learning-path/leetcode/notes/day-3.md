# Day 3 Notes - Hash Maps

**Goal:** Understand when O(1) lookup changes everything.

**Focus:** When you find yourself doing nested loops, ask "can a hash map remove one of these loops?"

| Problem | Difficulty | Link |
|---|---|---|
| Two Sum (redo with hash map) | Easy | [leetcode.com/problems/two-sum](https://leetcode.com/problems/two-sum) |
| Valid Anagram (redo with hash map) | Easy | [leetcode.com/problems/valid-anagram](https://leetcode.com/problems/valid-anagram) |
| First Unique Character | Easy | [leetcode.com/problems/first-unique-character-in-a-string](https://leetcode.com/problems/first-unique-character-in-a-string) |
| First Letter to Appear Twice | Easy | [leetcode.com/problems/first-letter-to-appear-twice](https://leetcode.com/problems/first-letter-to-appear-twice) |

---

## Two Sum (hash map)

**Problem:** Given an array of integers `nums` and an integer `target`, return the indices of the two numbers that add up to `target`. Exactly one solution exists.

**My understanding:** For each number, compute `target - nums[i]` (the complement). If the complement is already in the dictionary, we found the pair — return both indexes. If not, store the current number and its index for future lookups.

**Key insight:** Store `number → index` as key-value so that looking up a complement gives back its index instantly. Storing `index → number` would require scanning all values to find a match, which defeats the purpose.

**Pseudocode:**
```
Dictionary<int, int> dict = new();

for int i = 0; i < nums.Length; i++:
    if dict.ContainsKey(target - nums[i])
        return new int[]{ dict[target - nums[i]], i }
    dict.TryAdd(nums[i], i)

return new int[]{}
```

**What I learned:**
- Dictionary key is the number, value is its index — `dict[number]` instantly returns the index
- Check complement first before adding current number — avoids using the same element twice
- `TryAdd` instead of `Add` — `Add` throws exception on duplicate keys, `TryAdd` silently skips
- `ContainsKey` just checks existence, `dict[key]` gets the value — both needed here
- `TryGetValue(key, out value)` combines both steps into one, but `ContainsKey` + `dict[key]` works fine too
- Dictionary grows with input → O(n) space, but buys O(n) time vs O(n²) for the nested loop approach

**Final answer (C#):**
```csharp
public int[] TwoSum(int[] nums, int target) {
    Dictionary<int, int> dict = new();

    for (int i = 0; i < nums.Length; i++) {
        if (dict.ContainsKey(target - nums[i]))
            return new int[] { dict[target - nums[i]], i };
        dict.TryAdd(nums[i], i);
    }

    return new int[] { };
}
```

**Complexity:** O(n) time — one pass. O(n) space — dictionary grows with input size.

**vs Day 1 approach:** Day 1 was O(n²) time, O(1) space. Hash map trades space for speed.

---

## Valid Anagram (hash map)

**Problem:** Given two strings `s` and `t`, return `true` if `t` is an anagram of `s`, `false` otherwise.

**My understanding:** Count character frequencies from `s` into a dictionary. Then for each character in `t`, decrement its count — if the key doesn't exist, `t` has a character `s` doesn't, return false. Remove keys when count hits 0 so any leftover character in `t` gets caught immediately.

**Pseudocode:**
```
if s.Length != t.Length return false;

Dictionary<char, int> dict = new();

for int i = 0; i < s.Length; i++:
    if dict.ContainsKey(s[i]) dict[s[i]]++;
    else dict.TryAdd(s[i], 1);

for int i = 0; i < t.Length; i++:
    if !dict.ContainsKey(t[i]) return false;
    dict[t[i]]--;
    if dict[t[i]] == 0 dict.Remove(t[i]);

return true;
```

**What I learned:**
- `if ContainsKey → ++, else TryAdd(1)` — the else is required, otherwise TryAdd runs every iteration even after incrementing
- After the early return check, the second `ContainsKey` is redundant — you already know the key exists, just decrement directly
- Remove on zero is a clean trick — if `t` later sees that character again, `ContainsKey` returns false and catches the extra
- Dictionary size is bounded by unique characters in `s` — technically O(1) for lowercase only, but generally stated as O(n)

**Final answer (C#):**
```csharp
public bool IsAnagram(string s, string t) {
    if (s.Length != t.Length) return false;

    Dictionary<char, int> dict = new();

    for (int i = 0; i < s.Length; i++) {
        if (dict.ContainsKey(s[i]))
            dict[s[i]]++;
        else dict.TryAdd(s[i], 1);
    }

    for (int i = 0; i < t.Length; i++) {
        if (!dict.ContainsKey(t[i])) return false;

        dict[t[i]]--;
        if (dict[t[i]] == 0) dict.Remove(t[i]);
    }

    return true;
}
```

**Complexity:** O(n) time — two passes. O(n) space — dictionary size scales with unique characters in `s`.

---

## First Unique Character

**Problem:** Given a string `s`, find the first non-repeating character and return its index. If none exists, return `-1`.

**My understanding:** First pass — build a dictionary storing each character's index. If a duplicate is found, overwrite the value with `-1` to mark it as non-unique. Second pass — loop over `s` again and return `i` for the first character whose dictionary value is not `-1`.

**Key insight:** Loop over `s` in the second pass, not the dictionary. Dictionaries don't guarantee reliable ordering, but `s` always preserves original order. The index is already stored as the value, so `dict[s[i]] != -1` means it's unique and `i` is its position.

**Pseudocode:**
```
Dictionary<char, int> dict = new();

for int i = 0; i < s.Length; i++:
    if !dict.ContainsKey(s[i]) dict.TryAdd(s[i], i);
    else dict[s[i]] = -1; // mark as duplicate

for int i = 0; i < s.Length; i++:
    if dict[s[i]] != -1 return i;

return -1;
```

**What I learned:**
- Store index as value, `-1` as a sentinel for duplicates
- Don't loop over the dictionary to find order — loop over `s` instead, dictionary doesn't guarantee insertion order reliably
- Don't modify a dictionary while iterating it — causes runtime errors
- Second loop over `s` is clean because the index is already `i`

**Final answer (C#):**
```csharp
public int FirstUniqChar(string s) {
    Dictionary<char, int> dict = new();

    for (int i = 0; i < s.Length; i++) {
        if (!dict.ContainsKey(s[i]))
            dict.TryAdd(s[i], i);
        else
            dict[s[i]] = -1;
    }

    for (int i = 0; i < s.Length; i++) {
        if (dict[s[i]] != -1) return i;
    }

    return -1;
}
```

**Complexity:** O(n) time — two passes. O(n) space — dictionary bounded by unique characters, max 26 for lowercase, technically O(1) for this problem.

---

## First Letter to Appear Twice

**Problem:** Given a string `s` of lowercase English letters, return the first letter to appear twice. The problem guarantees at least one repeated letter exists.

**My understanding:** Loop through the string tracking seen characters in a HashSet. The moment a character is already in the set, it's the first duplicate — return it immediately. No need to store indexes, just existence.

**Why HashSet not Dictionary:** Don't need to store any value alongside the character — just need to know if we've seen it before. HashSet is cleaner for existence-only tracking.

**Pseudocode:**
```
HashSet<char> seen = new();

for int i = 0; i < s.Length; i++:
    if seen.Contains(s[i]) return s[i];
    else seen.Add(s[i]);

return ' '; // never reached, problem guarantees a repeat exists
```

**What I learned:**
- Single pointer is enough — no need for two pointers here
- Return immediately on first duplicate found — no need to finish the loop
- `return ' '` at the bottom satisfies C# compiler (all paths must return), but will never execute
- HashSet over Dictionary when you only need existence, not a stored value

**Final answer (C#):**
```csharp
public char RepeatedCharacter(string s) {
    HashSet<char> seen = new();

    for (int i = 0; i < s.Length; i++) {
        if (seen.Contains(s[i])) return s[i];
        else seen.Add(s[i]);
    }

    return ' ';
}
```

**Complexity:** O(n) time — one pass. O(n) space — HashSet grows with input, max 26 for lowercase so technically O(1).

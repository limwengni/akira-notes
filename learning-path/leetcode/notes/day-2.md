# Day 2 Notes - Strings

**Goal:** Get comfortable with string manipulation.

**Focus:** Strings are close to character arrays. Most beginner problems are about comparing, counting, or cleaning characters.

| Problem | Difficulty | Link |
|---|---|---|
| Reverse String | Easy | [leetcode.com/problems/reverse-string](https://leetcode.com/problems/reverse-string) |
| Valid Palindrome | Easy | [leetcode.com/problems/valid-palindrome](https://leetcode.com/problems/valid-palindrome) |
| Valid Anagram | Easy | [leetcode.com/problems/valid-anagram](https://leetcode.com/problems/valid-anagram) |

---

## Reverse String

**Problem:** Write a function that reverses a string. The input is given as an array of characters `s`. You must do it in-place with O(1) extra memory.

**My understanding:** Swap characters from both ends moving inward until the two pointers meet in the middle.

**My first attempt (pseudocode):**
```
// Wrong approach — two separate loops
for int i = 0; i < s.Length; i++
for int j = s.Length-1; j >= 0; j--
// This swaps everything twice and ends up back to original
```

**What I learned:**
- Two separate loops going opposite directions cancel each other out — everything gets swapped back
- One `while` loop with two pointers moving toward each other stops at the middle — correct
- O(1) memory means only fixed extra variables (`left`, `right`, `temp`) — no new array created
- `Array.Reverse(s)` works but is a built-in cheat — interviewers won't accept it

**Final answer (C#):**
```csharp
public void ReverseString(char[] s) {
    int left = 0;
    int right = s.Length - 1;

    while (left < right) {
        char temp = s[left];

        s[left] = s[right];
        s[right] = temp;

        left++;
        right--;
    }
}
```

**Complexity:** O(n) time — one pass through half the array. O(1) space — only three extra variables.

---

## Valid Palindrome

**Problem:** A phrase is a palindrome if, after converting all uppercase letters to lowercase and removing all non-alphanumeric characters, it reads the same forward and backward. Given a string `s`, return `true` if it is a palindrome, `false` otherwise.

**My understanding:** Clean the string by skipping non-alphanumeric characters, then compare from both ends moving inward.

**My first attempt (pseudocode):**
```
if string.isnullorempty(s) return true;

int left = 0;
int right = s.Length - 1;

while left < right:
    if !char.isletterordigit(s[left]) left++;        // skip non alphanumeric char from left
    else if !char.isletterordigit(s[right]) right--;  // skip non alphanumeric char from right
    else {
        if char.tolower(s[left]) != char.tolower(s[right]) return false;
        left++;
        right--;
    }

return true;
```

**What I learned:**
- Skip non-alphanumeric characters by moving the pointer, not by cleaning the string first
- `left++` and `right--` must be inside the `else` block — only move both pointers after a valid comparison
- Same two pointer pattern as Reverse String, just with extra skip logic

**Final answer (C#):**
```csharp
public bool IsPalindrome(string s) {
    if (string.IsNullOrEmpty(s)) return true;

    int left = 0;
    int right = s.Length - 1;

    while (left < right) {
        if (!char.IsLetterOrDigit(s[left])) {
            left++;
        }
        else if (!char.IsLetterOrDigit(s[right])) {
            right--;
        }
        else {
            if (char.ToLower(s[left]) != char.ToLower(s[right]))
                return false;

            left++;
            right--;
        }
    }

    return true;
}
```

**Complexity:** O(n) time — one pass through the string. O(1) space — only two pointers, no extra string created.

---

## Valid Anagram

**Problem:** Given two strings `s` and `t`, return `true` if `t` is an anagram of `s`, `false` otherwise. An anagram uses all the same characters the same number of times, just in a different order.

**My understanding:** Sort both strings — if they're anagrams, sorted they'll look identical.

**My first attempt (pseudocode):**
```
if s.Length != t.Length return false;

char[] chars1 = s.ToCharArray();
char[] chars2 = t.ToCharArray();

Array.Sort(chars1);
Array.Sort(chars2);

return new string(chars1) == new string(chars2);
```

**What I learned:**
- If lengths differ, they can't be anagrams — early return saves work
- Sorting both and comparing is the simplest approach
- Can't compare char arrays directly — convert back to string with `new string(arr)` first
- HashMap approach (count character frequency) is more optimal but covered in Day 3

**Final answer (C#):**
```csharp
public bool IsAnagram(string s, string t) {
    if (s.Length != t.Length) return false;

    char[] c1 = s.ToCharArray();
    char[] c2 = t.ToCharArray();

    Array.Sort(c1);
    Array.Sort(c2);

    return new string(c1) == new string(c2);
}
```

**Complexity:** O(n log n) time — sorting dominates. O(n) space — two char arrays.

---

**Method 2 — Frequency Count (26-size array, lowercase only):**

**My understanding:** Use a fixed array of size 26 (one slot per letter a-z). Loop through `s` and increment, loop through `t` and decrement. The 2 loop version targets `t` specifically — if any count goes below 0, it means `t` has exceeded the count for that character, so `t` has extra. The 1 loop version increments and decrements simultaneously so counts can be positive or negative — `!= 0` catches both directions without knowing which string caused the mismatch.

**Pseudocode:**
```
if s.Length != t.Length return false;

int[] arr = new int[26];

for int i = 0; i < s.Length; i++:
    arr[s[i] - 'a']++;

for int i = 0; i < t.Length; i++:
    arr[t[i] - 'a']--;
    if arr[t[i] - 'a'] < 0 return false;

return true;
```

**What I learned:**
- `s[i] - 'a'` maps a character to index 0-25 (`'a'` = 0, `'b'` = 1, `'z'` = 25)
- `'a'` is ASCII 97, so `s[i] - 'a'` and `s[i] - 97` are the same thing — use `'a'` for readability
- Finish processing all of `s` first, then decrement for `t` — this makes the early return valid
- `< 0` catches when **t has extra characters** that s doesn't have enough of — only checks one direction
- The length check at the top covers the other direction (s having extra characters), so `< 0` is sufficient
- Both 26 and 256 array versions can be written with 2 loops (early return `< 0`) or 1 loop (check `!= 0` at end)

**Final answer (C#):**
```csharp
public bool IsAnagram(string s, string t) {
    if (s.Length != t.Length) return false;

    int[] arr = new int[26];

    for (int i = 0; i < s.Length; i++) {
        arr[s[i] - 'a']++;
    }

    for (int i = 0; i < t.Length; i++) {
        arr[t[i] - 'a']--;
        if (arr[t[i] - 'a'] < 0) return false;
    }

    return true;
}
```

**Complexity:** O(n) time — two passes. O(1) space — fixed array of size 26, never grows with input.

---

**Method 3 — Frequency Count (256-size array, full ASCII):**

**My understanding:** Same idea as method 2 but use raw ASCII values as indexes directly — no need to subtract `'a'`. Array size 256 to cover all ASCII characters. Merge both loops into one, check all zeros at the end.

**What I learned:**
- Without `- 'a'`, raw ASCII values are used as indexes — need array size 256 to avoid out of bounds
- 1 loop version: increment and decrement happen simultaneously, so counts can be positive or negative mid-loop
- `!= 0` catches both directions — positive means s had extra, negative means t had extra
- Can't do early return when using 1 loop — a temporary -1 mid-loop might get corrected later
- 256 vs 26 array size makes no real difference in memory (fixed size either way, both O(1) space)
- Use 26 when constraint says lowercase only, 256 for full ASCII, Dictionary for Unicode

**Final answer (C#):**
```csharp
public bool IsAnagram(string s, string t) {
    if (s.Length != t.Length) return false;

    int[] counts = new int[256];

    for (int i = 0; i < s.Length; i++) {
        counts[s[i]]++;
        counts[t[i]]--;
    }

    foreach (int count in counts) {
        if (count != 0) return false;
    }

    return true;
}
```

**Complexity:** O(n) time — one pass + one fixed 256 iteration. O(1) space — fixed array of size 256, never grows with input.

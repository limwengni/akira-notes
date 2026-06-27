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

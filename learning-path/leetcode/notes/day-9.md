# Day 9 Notes - Stacks and Queues

**Goal:** Learn when order of processing matters.

**Focus:** Stack = last in first out (pile of plates). Queue = first in first out (line at a counter). Valid Parentheses is the classic stack problem — if you get that one, you understand stacks.

| Problem | Difficulty | Link |
|---|---|---|
| Valid Parentheses | Easy | [leetcode.com/problems/valid-parentheses](https://leetcode.com/problems/valid-parentheses) |
| Implement Queue using Stacks | Easy | [leetcode.com/problems/implement-queue-using-stacks](https://leetcode.com/problems/implement-queue-using-stacks) |
| Min Stack | Medium | [leetcode.com/problems/min-stack](https://leetcode.com/problems/min-stack) |

---

## Valid Parentheses

**Problem:** String of `()[]{}` — return true if properly matched and nested.

**The rule (why a stack):** having matching pairs isn't enough — `([)]` has all pairs but is invalid. Nesting order matters: **whatever opened most recently must close first** (boxes inside boxes: close inner before outer). "Most recent thing handled first" = last in, first out = stack.

**Algorithm:** walk the string —
- opener → push it
- closer → the most recent unclosed opener is on top of the stack; pop it, must be the matching partner
- end → valid only if stack is empty (nothing left open)

**What tripped me up:**
- Wrote `if (match) return true` inside the loop — wrong: one good pair doesn't validate the string (`"()[["` would return true early). A match just means keep going; only a MISMATCH returns early. True is earned by surviving the whole string
- `stk == null` is not the empty check — the object is never null, an empty backpack is still a backpack. Empty = `stk.Count == 0`, checked right before Pop
- Blanket `return true` at the end misses leftovers — `"(("` survives the loop with 2 unclosed openers. End with `return stk.Count == 0`

**The three return-false exits — each catches a closer with no rightful partner:**
1. `Count == 0` before pop → closer with nothing open: `")"`
2. Mismatch → closer paired with wrong opener (nesting broken): `"(]"`, `"([)]"`
3. `Count != 0` at the end → openers never closed: `"(("`

**Final answer (C#):**
```csharp
public bool IsValid(string s)
{
    Stack<char> stk = new();

    for (int i = 0; i < s.Length; i++)
    {
        if (s[i] == '(' || s[i] == '{' || s[i] == '[')
            stk.Push(s[i]);
        if (s[i] == ')' || s[i] == '}' || s[i] == ']')
        {
            if (stk.Count == 0) return false;
            char c = stk.Pop();
            if (c == '(' && s[i] != ')') return false;
            if (c == '{' && s[i] != '}') return false;
            if (c == '[' && s[i] != ']') return false;
        }
    }

    return stk.Count == 0;
}
```

**Complexity:** O(n) time, O(n) space (worst case all openers).

**C# stack API:** `Stack<char> stk = new();` → `.Push(x)`, `.Pop()` (remove + return top), `.Peek()` (look without removing), `.Count`.

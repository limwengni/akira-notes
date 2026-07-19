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

---

## Implement Queue using Stacks

**Problem:** Build a FIFO queue using ONLY two stacks. First design problem — a class with state that survives between calls, not one method solving one input.

**Key insight: two reversals restore order.** A stack hands things back newest-first. Pour it into a second stack (pop each, push to other) and everything flips — oldest ends up on top. stackIn = waiting room (Push lands here), stackOut = serving counter (Pop/Peek served here).

**The pouring law: only pour when stackOut is EMPTY.** stackOut's contents are already in correct queue order — pouring on top of them buries the rightful front and newcomers cut the line. Trace that breaks unconditional pouring: push 1, push 2, pop (→1 ✓), push 3, pop — pour-always returns 3, guard returns 2 ✓.

**What tripped me up:**
- Poured on every Pop — the exact line-cutting bug above
- Peek didn't pour at all — `Push(1); Peek();` crashes with 1 stuck in stackIn. Peek needs the same guard+pour as Pop; only the last line differs (look vs take)
- Empty checked only stackOut — queue is empty when BOTH stacks are empty

**Final answer (C#):**
```csharp
public class MyQueue {
    private Stack<int> stackIn = new();
    private Stack<int> stackOut = new();

    public void Push(int x) {
        stackIn.Push(x);
    }

    public int Pop() {
        if (stackOut.Count == 0) {              // pouring law: only when empty
            while (stackIn.Count > 0) {
                stackOut.Push(stackIn.Pop());   // pour: reverses again → oldest on top
            }
        }
        return stackOut.Pop();
    }

    public int Peek() {
        if (stackOut.Count == 0) {
            while (stackIn.Count > 0) {
                stackOut.Push(stackIn.Pop());
            }
        }
        return stackOut.Peek();                 // only line that differs from Pop
    }

    public bool Empty() {
        return stackIn.Count == 0 && stackOut.Count == 0;
    }
}
```

**Complexity:** amortized O(1) per operation — one Pop can trigger a whole pour, but each element only ever moves twice total (in once, poured once).

**Note:** solutions using `List` + `RemoveAt(0)` pass the judge but cheat the constraint (asked for stacks only) AND are worse — `RemoveAt(0)` shifts everything left, O(n) per pop.

---

## Min Stack

**Problem:** A stack with Push, Pop, Top, GetMin — ALL O(1). No scanning allowed.

**Why one min variable fails:** when the min itself gets popped, one variable can't tell you the previous min — you'd have to rescan. The real requirement is remembering the entire HISTORY of minimums so popping just rolls back one step. A history you add to the top of and roll back from the top... is a stack.

**Design — main stack (everyone) + min stack (champions logbook):**
- **Push(x):** main always. Min-stack only if `minStk.Count == 0 || x <= minStk.Peek()`
  - `<=` not `<` — ties must be recorded: two 2s in the club need two 2s in the logbook, or popping one 2 wrongly erases a min that's still inside
  - `||` short-circuits: empty check first means `.Peek()` never runs on an empty stack (same trick as `fast != null && fast.next != null`)
- **Pop():** main always. If the popped value == min-stack top, the champion is LEAVING — retire its logbook entry; the entry below is automatically the previous min (the rollback)
- **Top():** peek main stack. **GetMin():** peek min stack. Both pure one-line reads

**Final answer (C#):**
```csharp
public class MinStack {
    Stack<int> mainStk = new();
    Stack<int> minStk = new();

    public void Push(int value) {
        if (minStk.Count == 0 || value <= minStk.Peek())
            minStk.Push(value);
        mainStk.Push(value);
    }

    public void Pop() {
        int popped = mainStk.Pop();
        if (popped == minStk.Peek())
            minStk.Pop();                 // min left the building → roll back
    }

    public int Top() {
        return mainStk.Peek();
    }

    public int GetMin() {
        return minStk.Peek();
    }
}
```

**The transferable idea:** do a little bookkeeping on every write (Push/Pop) so the expensive question (min) becomes a free read. Pay on write, free on read — shows up everywhere in real systems.

**Complexity:** all four operations O(1); O(n) extra space worst case.

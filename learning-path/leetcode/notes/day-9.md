# Day 9 Notes - Stacks and Queues

**Goal:** Learn when order of processing matters.

**Focus:** Stack = last in first out (pile of plates). Queue = first in first out (line at a counter). Valid Parentheses is the classic stack problem — if you get that one, you understand stacks.

| Problem | Difficulty | Link |
|---|---|---|
| Valid Parentheses | Easy | [leetcode.com/problems/valid-parentheses](https://leetcode.com/problems/valid-parentheses) |
| Implement Queue using Stacks | Easy | [leetcode.com/problems/implement-queue-using-stacks](https://leetcode.com/problems/implement-queue-using-stacks) |
| Min Stack | Medium | [leetcode.com/problems/min-stack](https://leetcode.com/problems/min-stack) |
| Daily Temperatures | Medium | [leetcode.com/problems/daily-temperatures](https://leetcode.com/problems/daily-temperatures) |
| Next Greater Element I | Easy | [leetcode.com/problems/next-greater-element-i](https://leetcode.com/problems/next-greater-element-i) |
| Baseball Game | Easy | [leetcode.com/problems/baseball-game](https://leetcode.com/problems/baseball-game) |
| Remove All Adjacent Duplicates in String | Easy | [leetcode.com/problems/remove-all-adjacent-duplicates-in-string](https://leetcode.com/problems/remove-all-adjacent-duplicates-in-string) |

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

---

## Daily Temperatures

**Problem:** For every day's temperature, return how many days must pass before a warmer day. If no warmer day comes later, return `0`.

**Example:**
```text
Day:          0   1   2   3   4   5   6   7
Temperature: 73  74  75  71  69  72  76  73
Answer:       1   1   4   2   1   1   0   0
```

`75` has answer `4` because its next warmer temperature is `76`, from day 2 to day 6: `6 - 2 = 4`. The answer is the number of days waited, not the temperature difference.

**Key insight:** The stack temporarily stores **day indices that are still waiting for a warmer temperature**. It stores indices instead of temperatures because an index gives both:
- the day's temperature: `temperatures[index]`
- the waiting time: `currentDay - index`

For each current day:
- While the stack is not empty and today's temperature is warmer than the temperature on the day at the top, pop that previous day and calculate its wait.
- Push the current day because it now waits for a warmer future day.
- Any indices left in the stack at the end never find a warmer day, so their answers stay at the array's default value of `0`.

**Trace:**
```text
Day 0, 73: push 0                           stack [0]
Day 1, 74: pop 0, answer[0] = 1 - 0 = 1    stack []; push 1
Day 2, 75: pop 1, answer[1] = 2 - 1 = 1    stack []; push 2
Day 3, 71: not warmer than 75; push 3       stack [2, 3]
Day 4, 69: not warmer than 71; push 4       stack [2, 3, 4]
Day 5, 72: resolve day 4 (1 day) and day 3 (2 days), then push 5
Day 6, 76: resolve day 5 and day 2; day 2 waited 6 - 2 = 4 days
```

**Final answer (C#):**
```csharp
public int[] DailyTemperatures(int[] temperatures)
{
    int[] answer = new int[temperatures.Length];
    Stack<int> stack = new();

    for (int currentDay = 0; currentDay < temperatures.Length; currentDay++)
    {
        while (stack.Count > 0 &&
               temperatures[currentDay] > temperatures[stack.Peek()])
        {
            int previousDay = stack.Pop();
            answer[previousDay] = currentDay - previousDay;
        }

        stack.Push(currentDay);
    }

    return answer;
}
```

**When to think of a stack:** some earlier items are still waiting for a future item to resolve them, and the most recent waiting item should be checked first.

**Complexity:** O(n) time because each day is pushed and popped at most once; O(n) space in the worst case.

---

## Next Greater Element I

**Problem:** For each value in `nums1`, find that value in `nums2` and return the first greater value to its right. Return `-1` if no greater value appears later. Every value in `nums1` also appears in `nums2`.

**Example:**
```text
nums1 = [4, 1, 2]
nums2 = [1, 3, 4, 2]
answer = [-1, 3, -1]
```

- `4` has only `2` to its right, so its answer is `-1`.
- The first greater value to the right of `1` is `3`.
- `2` has nothing to its right, so its answer is `-1`.

### First solution — find each value, then search right

Set each answer to `-1` by default. Once the target is found in `nums2`, keep searching past smaller values until the first greater value appears. A smaller value does **not** mean the answer is `-1`; a greater value may still appear later.

```csharp
public int[] NextGreaterElement(int[] nums1, int[] nums2)
{
    int[] ans = new int[nums1.Length];

    for (int i = 0; i < nums1.Length; i++)
    {
        ans[i] = -1;
        bool foundNumber = false;

        for (int j = 0; j < nums2.Length; j++)
        {
            if (nums1[i] == nums2[j])
            {
                foundNumber = true;
            }
            else if (foundNumber && nums2[j] > nums1[i])
            {
                ans[i] = nums2[j];
                break; // only the first greater value matters
            }
        }
    }

    return ans;
}
```

**Complexity:** O(nums1.Length × nums2.Length) time because the scan through `nums2` restarts for every value in `nums1`; O(1) extra space, excluding the returned answer.

### Better solution — monotonic stack + dictionary

Process `nums2` once. The stack stores indices of values still waiting for their next greater value. When the current value is greater than the value at the top index, pop that waiting index and record `waiting value → current value` in the dictionary.

After processing `nums2`, loop through `nums1` and look up each answer. Values missing from the dictionary never found a greater value, so return `-1` for them.

```csharp
public int[] NextGreaterElement(int[] nums1, int[] nums2)
{
    Stack<int> temp = new();
    Dictionary<int, int> compare = new();
    int[] answers = new int[nums1.Length];

    for (int i = 0; i < nums2.Length; i++)
    {
        while (temp.Count > 0 && nums2[i] > nums2[temp.Peek()])
        {
            int prev = temp.Pop();
            compare[nums2[prev]] = nums2[i];
        }

        temp.Push(i);
    }

    for (int i = 0; i < nums1.Length; i++)
    {
        if (compare.TryGetValue(nums1[i], out int greater))
            answers[i] = greater;
        else
            answers[i] = -1;
    }

    return answers;
}
```

**Why the `while` does not make this O(n²):** every `nums2` index is pushed once and popped at most once. Across the entire loop, the `while` can therefore perform at most `nums2.Length` pops.

**Complexity:** O(nums1.Length + nums2.Length) time; O(nums2.Length) extra space for the stack and dictionary.

**Pattern connection:** Daily Temperatures and Next Greater Element both keep unresolved positions in a decreasing stack. A larger current value resolves one or more earlier values. Daily Temperatures stores the distance between indices; this problem stores the greater value itself.

---

## Baseball Game

**Problem:** Process a list of score operations, then return the sum of all valid scores remaining in the record.

```text
Number → record that score
"C"    → remove the latest valid score
"D"    → record double the latest valid score
"+"    → record the sum of the latest two valid scores
```

**Example:**
```text
operations = ["5", "2", "C", "D", "+"]

"5" → [5]
"2" → [5, 2]
"C" → [5]
"D" → [5, 10]
"+" → [5, 10, 15]

answer = 5 + 10 + 15 = 30
```

**Why a stack:** every special operation uses or removes the most recent valid score. The latest score is always at the top.

**Getting the previous two scores for `"+"`:** temporarily pop the latest score so the second-latest score becomes visible, then restore the latest score before pushing their sum.

```csharp
int last = temp.Pop();
int secondLast = temp.Peek();

temp.Push(last);
temp.Push(last + secondLast);
```

**What tripped me up:** tried to parse `temp.Pop()` and `temp.Peek()`:

```csharp
int.TryParse(temp.Pop(), out int last); // wrong
```

`Stack<int>.Pop()` and `Stack<int>.Peek()` already return `int`. Parsing converts text such as `"-2"` into an integer, so only `op` needs parsing:

```text
op              → string → parse it
temp.Pop()       → int    → use directly
temp.Peek()      → int    → use directly
```

**Final answer (C#):**
```csharp
public class Solution
{
    public int CalPoints(string[] operations)
    {
        Stack<int> temp = new();
        int sum = 0;

        foreach (string op in operations)
        {
            if (op == "C")
            {
                temp.Pop();
            }
            else if (op == "D")
            {
                temp.Push(temp.Peek() * 2);
            }
            else if (op == "+")
            {
                int last = temp.Pop();
                int secondLast = temp.Peek();

                temp.Push(last);
                temp.Push(last + secondLast);
            }
            else
            {
                int.TryParse(op, out int num);
                temp.Push(num);
            }
        }

        while (temp.Count > 0)
            sum += temp.Pop();

        return sum;
    }
}
```

**Complexity:** O(n) time; O(n) space in the worst case.

---

## Remove All Adjacent Duplicates in String

**Problem:** Repeatedly remove pairs of equal adjacent characters until no such pair remains, then return the final string.

**Example:**
```text
"abbaca"
→ remove "bb" → "aaca"
→ remove "aa" → "ca"
```

**Why a stack:** the current character only needs to compare with the most recent character that survived. If they match, the pair cancels; otherwise, keep the current character for comparison with whatever comes next.

```text
Stack not empty and top == current character → Pop
Otherwise                                → Push
```

**Trace:**
```text
Input: "abbaca"

a → push          [a]
b → push          [a, b]
b → matches top   [a]
a → matches top   []
c → push          [c]
a → push          [c, a]
```

The stack now contains the right characters, but popping returns them in reverse order: `a`, then `c`. Instead of filling an array forward and calling `Array.Reverse()`, fill the array from the last index toward index `0`.

**What tripped me up:** used `stack.Count` as the loop boundary while also popping from the stack:

```csharp
for (int i = 0; i < stack.Count; i++) // wrong: Count shrinks after every Pop
    result[i] = stack.Pop();
```

If the stack starts with four items, after two pops both `i` and `stack.Count` become `2`, so the loop stops halfway. Create the result array after the stack-processing loop, then use its fixed length. Fill it backward so the stack's reversed pop order lands in the correct positions:

```csharp
char[] result = new char[stack.Count];

for (int i = result.Length - 1; i >= 0; i--)
    result[i] = stack.Pop();
```

```text
Stack bottom → [c, a] ← top
i = 1 → pop 'a' → result[1] = 'a'
i = 0 → pop 'c' → result[0] = 'c'
Result: "ca"
```

This removes the need for a separate `Array.Reverse(result)` pass.

The array must be created **after** processing the string. Before the loop, `stack.Count` is `0`; afterward, it is exactly the number of surviving characters.

**Final answer (C#):**
```csharp
public class Solution
{
    public string RemoveDuplicates(string s)
    {
        Stack<char> stack = new();

        foreach (char c in s)
        {
            if (stack.Count > 0 && stack.Peek() == c)
            {
                stack.Pop();
            }
            else
            {
                stack.Push(c);
            }
        }

        char[] result = new char[stack.Count];

        for (int i = result.Length - 1; i >= 0; i--)
            result[i] = stack.Pop();

        return new string(result);
    }
}
```

**Complexity:** O(n) time; O(n) space.

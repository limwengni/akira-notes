# Day 8 Notes - Linked Lists

**Goal:** Get comfortable with pointer manipulation.

**Focus:** Linked lists have no index access — you move by following `.next`. Draw it out on paper first. Linked List Cycle introduces the fast/slow pointer trick.

| Problem | Difficulty | Link |
|---|---|---|
| Convert Binary Number in a Linked List to Integer (warm-up) | Easy | [leetcode.com/problems/convert-binary-number-in-a-linked-list-to-integer](https://leetcode.com/problems/convert-binary-number-in-a-linked-list-to-integer) |
| Middle of the Linked List (warm-up) | Easy | [leetcode.com/problems/middle-of-the-linked-list](https://leetcode.com/problems/middle-of-the-linked-list) |
| Reverse Linked List | Easy | [leetcode.com/problems/reverse-linked-list](https://leetcode.com/problems/reverse-linked-list) |
| Merge Two Sorted Lists | Easy | [leetcode.com/problems/merge-two-sorted-lists](https://leetcode.com/problems/merge-two-sorted-lists) |
| Linked List Cycle | Easy | [leetcode.com/problems/linked-list-cycle](https://leetcode.com/problems/linked-list-cycle) |

---

## The Basic Traversal Loop

A node is a box with two things: `val` (data) and `next` (reference to the following box). The **only** way to move is:

```csharp
ListNode curr = head;
while (curr != null)
{
    // do something with curr.val
    curr = curr.next;
}
```

This loop is to linked lists what `for i = 0 to n-1` is to arrays.

---

## Convert Binary Number in a Linked List to Integer

**Problem:** Linked list of 0s and 1s is a binary number, most significant bit first. Return its decimal value.

**My understanding:** Walk the list front to back, building the number bit by bit with `x = x * 2 + val` — same concat trick as LC 3754, just base 2.

**My answer (C#):**
```csharp
public int GetDecimalValue(ListNode head)
{
    ListNode curr = head;
    int num = 0;

    while (curr != null)
    {
        num = num * 2 + curr.val;
        curr = curr.next;
    }

    return num;
}
```

**Complexity:** O(n) — single pass.

---

## Middle of the Linked List

**Problem:** Return the middle node of a linked list. If there are two middles (even length), return the **second** one.

**My understanding:** Can't binary search — no index access, no jumping to mid. The data structure decides which tools you can use. Two ways: count then walk half, or fast/slow pointers.

**Way 1 — two passes (count, then walk length/2):**
```csharp
public ListNode MiddleNode(ListNode head)
{
    ListNode temp = head;
    int length = 0;

    while (temp != null)
    {
        temp = temp.next;
        length++;
    }

    ListNode curr = head;
    for (int i = 0; i < length / 2; i++)
        curr = curr.next;

    return curr;
}
```
Integer division handles even length: 6 boxes → 6/2 = 3 steps → node 4 = second middle ✓

**Way 2 — fast/slow pointers (one pass):**
```csharp
public ListNode MiddleNode(ListNode head)
{
    ListNode slow = head, fast = head;

    while (fast != null && fast.next != null)
    {
        slow = slow.next;
        fast = fast.next.next;
    }

    return slow;
}
```

**Key insight:** fast is a racer at double speed, not a lookahead. When fast covers the whole list, slow has covered half → slow is on the middle.

**Why the loop needs BOTH checks (in that order):**
- Odd length (5 boxes): fast lands ON the last box → `fast.next == null` stops it
- Even length (6 boxes): fast steps OFF the end → `fast == null` stops it
- `fast != null` must come first so `fast.next` is never read on null

**Complexity:** both O(n). Way 2 is one pass and the fast/slow trick comes back in Linked List Cycle.

---

## Reverse Linked List

**Problem:** Reverse a singly linked list, return the new head.

**My understanding:** Flip every arrow to point backwards. Walk the list with `prev` trailing behind `curr`; at each box, save where I'm going next, then flip the arrow to point at `prev`, then move both pointers forward.

**My answer (C#):**
```csharp
public ListNode ReverseList(ListNode head)
{
    ListNode prev = null, curr = head, next;

    while (curr != null)
    {
        next = curr.next;   // save before flipping — or the rest of the list is lost
        curr.next = prev;   // flip the arrow

        prev = curr;        // both step forward
        curr = next;
    }

    return prev;
}
```

**Key insight:** return `prev`, not `curr` — curr runs one step ahead and ends on `null` (that's the exit condition); prev ends standing on the old tail = new head.

**Edge case for free:** `head == null` → loop never runs → returns `prev` which is still null → empty list reversed is empty. No special case needed.

**Complexity:** O(n) time, O(1) space.

---

## Merge Two Sorted Lists

**Problem:** Two sorted linked lists — weave them into one sorted list.

**My understanding:** Like merging two sorted piles of cards: compare the two fronts, take the smaller onto the new pile, repeat. When one pile runs out, dump the rest of the other pile on top in one go.

**What tripped me up:**
- First idea was rewiring the input lists into each other (`list1.next = list2`) — that overwrites `.next` and loses the rest of list1. Build a third list instead
- Forgot `tail = tail.next` — without it every attach overwrites the same box
- Returned `dummy` instead of `dummy.next` — that includes the fake starter box (stray 0)

**My answer (C#):**
```csharp
public ListNode MergeTwoLists(ListNode list1, ListNode list2)
{
    // dummy = keychain ring: fake starter box so tail is never null.
    // dummy never moves — it remembers where the result STARTS.
    ListNode dummy = new();

    // tail = end of the merged list so far — where the next card lands.
    ListNode tail = dummy;

    // can only compare fronts while BOTH lists still have boxes
    while (list1 != null && list2 != null)
    {
        if (list1.val < list2.val)
        {
            tail.next = list1;      // attach smaller front to the pile
            list1 = list1.next;     // that list steps forward
        }
        else
        {
            tail.next = list2;
            list2 = list2.next;
        }

        tail = tail.next;           // tail steps onto the box just attached
    }

    // one list is dead, the other has sorted leftovers still chained together.
    // attach the first leftover box and the whole chain comes along — one attach, no loop.
    tail.next = (list1 != null) ? list1 : list2;

    // return the real list, leave the fake box behind
    return dummy.next;
}
```

**Key ideas (remember these, not the code):**
- **dummy node**: solves "what do I attach the first node to when the result doesn't exist yet". Reusable in many list problems
- **tail** must advance after every attach
- **leftovers**: already sorted + chained → single attach dumps the whole remainder

**Complexity:** O(n + m) time, O(1) extra space — nodes are reused, not copied.

---

## Linked List Cycle

**Problem:** Return true if the linked list has a cycle (some node's `next` points back to an earlier node).

**Gotcha in the problem statement:** `pos` is NOT an input — it's just how the test harness builds the cycle. The function only gets `head`; the task is simply "does this list loop at all?"

**My understanding:** Fast/slow racer from Middle of the Linked List, but the exit meaning changes. Straight list → fast falls off the end (null) → no cycle. Loopy list → nothing is ever null, but fast keeps gaining on slow until it lands on the same box → cycle.

**Why fast can't jump OVER slow:** fast gains exactly 1 step per tick (slow moves 1 away, fast moves 2 closer). A gap that shrinks by exactly 1 counts down 3 → 2 → 1 → 0 — it can't skip 0. That's why 2x speed is used: at 3x the gap would shrink by 2 and could jump over.

**My answer (C#):**
```csharp
public bool HasCycle(ListNode head)
{
    ListNode slow = head;
    ListNode fast = head;

    while (fast != null && fast.next != null)
    {
        slow = slow.next;
        fast = fast.next.next;

        if (slow == fast)       // same BOX (reference compare), not same value
            return true;        // fast lapped slow → must be a loop
    }

    return false;               // fast fell off the end → straight list
}
```

**Key details:**
- Check `slow == fast` AFTER moving — they start on the same box, checking before moving would say every list has a cycle
- `slow == fast` compares references (same box), not `.val`
- Every list hits exactly one ending: meet → true, null → false

**Complexity:** O(n) time, O(1) space.

---

## Drill Log — blank-editor rewrites (2026-07-19)

Rewrote 206 + 21 cold, no peeking. Both re-submitted green.

**206 Reverse:** correct first try, re-derived the logic instead of recalling it (flip → chain breaks → save first → step). Owned.

**21 Merge:** concepts survived (compare, keychain, leftover dump) but mechanics slipped — took 4 rounds:
- Declared `tail` twice instead of `dummy` + `tail`
- Wrote `tail = list1` (move) instead of `tail.next = list1` (attach)
- Returned `tail`, then `dummy`, before landing on `dummy.next`

→ needs one more cold rep in a day or two.

**The distinction that matters (source of most list bugs):**
- `x.next = y` → **attach**: draws an arrow between boxes
- `x = y` → **move**: just repoints my hand, connects nothing

**Also learned:**
- `new ListNode()` works because the constructor has default params (`val=0, next=null`); dummy's value is irrelevant — any value, still `return dummy.next`
- Value ≠ box: wiring (`.next`, returns, node `==`) is about boxes, never the values inside

---

## Pattern: Build a Number Digit by Digit (Horner's Method)

Turn a sequence of digits in any base into an actual number, one digit at a time:

```csharp
x = x * base + digit;   // base 10: x = x * 10 + d
                        // base 2:  x = x * 2 + bit
```

Works left to right. `x` is the **result so far**, not the digit — each step takes the x from the previous step (multiply shifts it left, new digit slides into the last spot). Like typing digits on a calculator: type `5` after `12` → display shows 12×10+5 = 125.

**Trace `101` in base 2 (x starts at 0):**
```
bit 1 → x = 0*2 + 1 = 1
bit 0 → x = 1*2 + 0 = 2
bit 1 → x = 2*2 + 1 = 5   // check: 1*4 + 0*2 + 1*1 = 5 ✓
```

**Where I used it:**
- LC 3754 (Concatenate Non-Zero Digits): base 10, skip the zeros
- LC 1290 (Binary in Linked List to Integer): base 2, do NOT skip zeros — a 0 bit still shifts

**What tripped me up:**
- Thought each digit was computed separately then added — no, one running variable, carries over every step
- No string→int conversion needed at all — the loop builds the number directly
- Watch overflow: a long digit sequence can outgrow `int` — check constraints, may need `long`

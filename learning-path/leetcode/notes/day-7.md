# Day 7 Notes - Binary Search

**Goal:** Understand how to search in O(log n) instead of O(n).

**Focus:** Always ask — can I cut the search space in half? Binary search only works on sorted data. The key is getting `left`, `right`, and `mid` right without off-by-one errors.

| Problem | Difficulty | Link |
|---|---|---|
| Binary Search | Easy | [leetcode.com/problems/binary-search](https://leetcode.com/problems/binary-search) |
| Search Insert Position | Easy | [leetcode.com/problems/search-insert-position](https://leetcode.com/problems/search-insert-position) |
| First Bad Version | Easy | [leetcode.com/problems/first-bad-version](https://leetcode.com/problems/first-bad-version) |

---

## What is O(log n)?

The work grows with the **number of times you can halve n**, not with n itself. Each check throws away half the remaining elements: 1,000,000 → 500,000 → 250,000 → ... → 1 is only ~20 checks (2²⁰ ≈ 1,000,000). A billion elements is ~30 checks.

---

## Binary Search

**Problem:** Sorted array of distinct integers, return the index of `target`, or `-1` if not present. Must be O(log n).

**My understanding:** Check the middle. The array is sorted, so comparing target to the middle tells you which half the answer must be in — throw the other half away.

**The rule that took me 3 tries:** the comparison and the move point the **same way**:
- `nums[mid] < target` → mid too small → answer is to the **right** → `left = mid + 1`
- `nums[mid] > target` → mid too big → answer is to the **left** → `right = mid - 1`

The `+1`/`-1` always points *away* from mid, because mid is already checked.

**What tripped me up:**
- Had the branches backwards (twice, in different ways) — moved `right` when the target was bigger, dragging the search toward the small numbers. Trace `[1,3,5,7,9]` target 7: wrong version does right=1, then right=-1, returns -1 on a target that exists
- Used `while (left < right)` — fails on `[5]` target 5: left=0, right=0, loop never runs. When `left == right` there's still one unchecked element, so it must be `left <= right`
- Added `left++; right++` after the branches — the branches already move the correct boundary; shifting both afterwards corrupts the range

**Final answer (C#):**
```csharp
int left = 0, right = nums.Length - 1;

while (left <= right) {
    int mid = left + (right - left) / 2;
    if (nums[mid] == target) return mid;
    else if (nums[mid] < target) {
        left = mid + 1;
    } else {
        right = mid - 1;
    }
}

return -1;
```

**Complexity:** O(log n) — halves the search space every iteration.

---

## Overflow-safe mid: `left + (right - left) / 2`

`(left + right) / 2` breaks when the sum exceeds `int.MaxValue` (2,147,483,647) — it silently wraps negative. The JDK's own binary search had this bug for years.

The safe form divides **only the gap**, then walks that half-distance from the left wall:
1. `right - left` → width of the search space (always fits — both walls fit and left <= right)
2. `/ 2` → half the width
3. `left +` → start at the left wall, walk halfway across

**Careful with parentheses:** `(left + (right - left)) / 2` simplifies to `right / 2` — wrong. No outer parens: division binds tighter than addition, so `left + (right - left) / 2` reads as "left plus half the gap." Sanity check: left=4, right=10 → gap 6, half 3, mid 7. ✅

Same value as `(left + right) / 2`, drop-in replacement — use it in every binary search, always, so overflow is a bug class that never happens.

---

## Search Insert Position

**Problem:** Same sorted array setup, but if target isn't found, return the index where it **would be inserted** to keep the array sorted.

**Key insight:** It's binary search with a one-line difference — `return left` instead of `return -1`.

**Why `left` is the insertion point:** when the loop ends, everything discarded on the low side was `< target` (only way `left` moves up) and everything from `left` onward is `> target` (only way `right` drops below it). So `left` sits exactly on the boundary — the first position whose value exceeds target. Works in both miss directions: target smaller than everything → left stays 0; bigger than everything → left ends at Length.

**Final answer (C#):**
```csharp
int left = 0, right = nums.Length - 1;

while (left <= right) {
    int mid = left + (right - left) / 2;
    if (nums[mid] == target) return mid;
    else if (nums[mid] < target) {
        left = mid + 1;
    } else {
        right = mid - 1;
    }
}

return left;
```

**Complexity:** O(log n).

---

## First Bad Version

**Problem:** Versions 1..n, shaped `[good, good, bad, bad]`. API `IsBadVersion(v)` returns true/false. Find the **first** bad version with as few API calls as possible.

**Two twists vs plain binary search:**
1. No array — search the range 1..n, "comparing" means calling the API. So `left = 1, right = n` (not 0 and n-1 — version 0 doesn't exist, version n does)
2. Finding a bad version isn't the end — the *first* bad one might be earlier. So mark it as a **candidate** and keep searching left

The candidate is the same "carry the best answer so far" trick as `maxProfit` and `min = int.MaxValue`.

**What tripped me up:**
- Started with `left = 0, right = n - 1` out of habit — versions are 1-indexed
- Moved the wrong wall in the bad branch (`left = mid - 1` — expands the range, can loop forever)
- Declared `candidate` but never assigned it (same bug as forgetting the `max` update)
- Wrapped the mid formula as `(left + (right - left)) / 2` = `right / 2`
- Wanted an `n == 1` guard — unnecessary: left=1, right=1 runs one iteration, IsBadVersion(1) must be true (a bad version is guaranteed), returns 1. **When boundaries and branches are correct, binary search needs no special cases.**

**Final answer (C#):**
```csharp
int left = 1, right = n;
int candidate = -1;

while (left <= right) {
    int mid = left + (right - left) / 2;
    if (IsBadVersion(mid)) {
        candidate = mid;
        right = mid - 1;
    } else {
        left = mid + 1;
    }
}

return candidate;
```

**Complexity:** O(log n) API calls.

---

## The two templates

**Template 1 — `<=` with candidate (my default):** range may shrink past the answer, even to empty, because the answer is saved in a variable before evicting mid. Works unchanged for exact search, insert position, and first/leftmost problems.

**Template 2 — `<` boundary variant:**
```csharp
int i = 1, j = n;
while (i < j) {
    int m = i + (j - i) / 2;
    if (IsBadVersion(m)) j = m;      // m stays in range — it might be the answer
    else i = m + 1;
}
return i;
```
The range *never stops containing the answer* — squeeze to one element and that survivor is it. The range **is** the candidate.

Load-bearing details (change any one and it breaks):
- `while (i < j)` not `<=` — with `<=`, when i==j and bad, `j = m` changes nothing → infinite loop
- `j = m` not `m - 1` — m might be the answer, `m - 1` throws it away
- mid rounds down, so m < j whenever i < j → `j = m` always shrinks → terminates

Caveats: only fits "find first/leftmost X" shapes, assumes the answer exists in the range (for plain search it needs a final `nums[i] == target` check), and its failure mode is an infinite loop instead of a wrong answer.

Both are O(log n) — LeetCode runtime differences between them are timing noise. **Judge solutions by complexity class, not the ms readout.** Decision: drill Template 1 until automatic; revisit Template 2 at Day 10 review. Mixing pieces of the two is the classic way binary search goes wrong.

---

## What Tripped Me Up (summary)

- Branch directions flipped on me three times — fixed by tracing on paper, not by re-editing. Rule: comparison and movement point the same way (`<` → go right, `>` → go left)
- `left <= right`, otherwise single-element ranges never get checked
- `left + (right - left) / 2` always — halve the gap, not the sum; watch the parentheses
- Candidate declared but never assigned — third time this "forgot to update the tracker" bug appeared (max in Longest Substring, now this)
- Binary search is a strong candidate for a cold re-attempt on Day 10

# Day 4 Notes - Two Pointers

**Goal:** Learn to use two pointers to avoid O(n²) solutions.

**Focus:** Two pointers usually means one at the start and one at the end, or both moving forward. Works especially well on sorted arrays and in-place modification problems.

| Problem | Difficulty | Link |
|---|---|---|
| Valid Palindrome | Easy | [leetcode.com/problems/valid-palindrome](https://leetcode.com/problems/valid-palindrome) |
| Merge Sorted Array | Easy | [leetcode.com/problems/merge-sorted-array](https://leetcode.com/problems/merge-sorted-array) |
| Move Zeroes | Easy | [leetcode.com/problems/move-zeroes](https://leetcode.com/problems/move-zeroes) |

---

## Valid Palindrome

Already solved in Day 2. See [day-2.md](day-2.md) for full notes and solution.

**Pattern:** Two pointers from both ends moving inward, skipping non-alphanumeric characters.

---

## Merge Sorted Array

**Problem:** Given two sorted arrays `nums1` and `nums2`, merge `nums2` into `nums1` in-place. `nums1` has extra space at the end (zeros) to hold `nums2`'s elements. `m` and `n` are the number of actual elements in each array.

**My understanding:** Use 3 pointers — `p1` at the last real element of `nums1`, `p2` at the last element of `nums2`, `p` at the very last position of `nums1`. Fill from the back comparing both arrays, placing the larger value at `p` and decrementing the winning pointer.

**Key insight:** Fill from the back so you never overwrite elements you still need. If you filled from the front, you'd have to shift elements to make room.

**Pseudocode:**
```
int p1 = m - 1;
int p2 = n - 1;
int p = m + n - 1;

while p2 >= 0:
    if p1 >= 0 && nums1[p1] > nums2[p2]:
        nums1[p] = nums1[p1];
        p1--;
    else:
        nums1[p] = nums2[p2];
        p2--;
    p--;
```

**What I learned:**
- Fill from the back — avoids shifting elements and overwriting values you still need
- Loop condition is `p2 >= 0` — if `p2` runs out, remaining `nums1` elements are already in place
- Guard `p1 >= 0` before accessing `nums1[p1]` — `p1` can go out of bounds if `nums2` has larger elements than all of `nums1`

**Final answer (C#):**
```csharp
public void Merge(int[] nums1, int m, int[] nums2, int n) {
    int p1 = m - 1;
    int p2 = n - 1;
    int p = m + n - 1;

    while (p2 >= 0) {
        if (p1 >= 0 && nums1[p1] > nums2[p2]) {
            nums1[p] = nums1[p1];
            p1--;
        } else {
            nums1[p] = nums2[p2];
            p2--;
        }
        p--;
    }
}
```

**Complexity:** O(n) time — one pass through both arrays. O(1) space — in-place, no new array allocated.

---

## Move Zeroes

**Problem:** Given an integer array `nums`, move all `0`s to the end while maintaining the relative order of non-zero elements. Do it in-place.

**My understanding:** Two pointers both starting at 0. `p1` scans for non-zero elements, `p2` tracks where the next non-zero should be placed. When `p1` finds a non-zero, copy it to `p2` then zero out `p1` — but only if `p1 != p2`.

**Key insight:** When `p1 == p2` there are no zeros before the current element — they're in sync. Zeroing out `nums[p1]` when `p1 == p2` would wipe a valid value.

**Pseudocode:**
```
int p1 = 0;
int p2 = 0;

while p1 < nums.Length:
    if nums[p1] == 0:
        p1++;
    else:
        nums[p2] = nums[p1];
        if p1 != p2: nums[p1] = 0;
        p2++;
        p1++;
```

**What I learned:**
- `p2` is the write pointer — always points to where the next non-zero should go
- Only zero out `nums[p1]` when `p1 != p2` — if they're the same index, you'd wipe the value you just wrote
- Example: `[1,2,3]` with no zeros — `p1` and `p2` stay in sync the whole time, no swapping needed

**Final answer (C#):**
```csharp
public void MoveZeroes(int[] nums) {
    int p1 = 0;
    int p2 = 0;

    while (p1 < nums.Length) {
        if (nums[p1] == 0) {
            p1++;
        } else {
            nums[p2] = nums[p1];
            if (p1 != p2)
                nums[p1] = 0;
            p2++;
            p1++;
        }
    }
}
```

**Complexity:** O(n) time — one pass. O(1) space — in-place, no new array allocated.

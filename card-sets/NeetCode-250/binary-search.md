---
deck: "NeetCode 250::Binary Search"
topic: "NeetCode 250 — Binary Search"
tags: [ankicardmaker, neetcode250, binary-search]
note_type: Basic
created: 2026-09-09
---

# NeetCode 250 — Binary Search

Story front hides the technique; back reveals the mapping, approach, and complexity.

## 1. Binary Search  ·  _Easy_

**Scenario:** A clerk has a card catalog sorted by number and must find whether a specific number is filed. Instead of flipping through every card, she opens to the middle, sees whether her target is lower or higher, and discards the half that can't contain it, repeating. Where is the target, or is it absent?

- **Maps to:** Classic binary search on a sorted array (Binary Search).
- **Model it:** Locate a target value in a sorted sequence, or report it's missing.
- **Approach & variations:**
  - Maintain low and high bounds over the sorted range.
  - Check the middle: equal means found; smaller target means search the left half; larger means the right half.
  - Halve the search interval each step until the bounds cross.
  - Compute mid as low + (high - low)/2 to avoid overflow.
- **Time:** O(log n) — the interval halves every step.
- **Space:** O(1) — a few index variables.

## 2. Search Insert Position  ·  _Easy_

**Scenario:** A librarian keeps books shelved in strict numeric order. Given a new book's number, she must say exactly which slot it belongs in — its position if it's already shelved, otherwise the slot where it would slide in to keep the order. Which index is that, found without scanning every book?

- **Maps to:** Binary search for the lower bound (Search Insert Position).
- **Model it:** In a sorted array, return the index of the target or where it would be inserted to stay sorted.
- **Approach & variations:**
  - Binary-search for the first position whose value is >= the target.
  - If found equal, that's the index; if not, the crossing point is the insertion slot.
  - Low ends at the correct insertion index when the interval empties.
  - Handles targets smaller than all (index 0) or larger than all (index n).
- **Time:** O(log n) — halving the interval each step.
- **Space:** O(1) — index bounds only.

## 3. Guess Number Higher Or Lower  ·  _Easy_

**Scenario:** A friend has picked a secret whole number between 1 and some upper limit. Each time you name a guess, she only tells you 'too high,' 'too low,' or 'correct.' Using as few guesses as possible, how do you home in on her number?

- **Maps to:** Binary search over the answer range using a comparator (Guess Number Higher or Lower).
- **Model it:** Find a hidden number in [1, n] given a feedback function that says higher/lower/equal.
- **Approach & variations:**
  - Keep low and high bounds on the possible number; guess the midpoint.
  - 'Too high' discards the midpoint and everything above; 'too low' discards it and everything below.
  - Repeat until the feedback says 'correct.'
  - Use low + (high - low)/2 for the midpoint to avoid overflow.
- **Time:** O(log n) — each guess halves the candidate range.
- **Space:** O(1) — just the two bounds.

## 4. Sqrt(x)  ·  _Easy_

**Scenario:** A gardener wants the side length of the largest whole-number square tile whose area does not exceed a given plot area. Fractions are rounded down — she needs the biggest whole side whose square still fits. Without a calculator's root button, how does she pin down that whole number?

- **Maps to:** Binary search on the answer for the integer square root (Sqrt(x)).
- **Model it:** Return the floor of the square root of a nonnegative integer.
- **Approach & variations:**
  - The answer lies in [0, x]; binary-search a candidate side.
  - Compare the candidate squared against x: too big shrinks the upper bound, otherwise it's a feasible side, raise the lower bound.
  - Keep the largest side whose square is <= x.
  - Compare with mid <= x/mid or use 64-bit products to avoid overflow.
- **Time:** O(log x) — halving the candidate range.
- **Space:** O(1) — a few numbers.

## 5. Search a 2D Matrix  ·  _Medium_

**Scenario:** A stamp album has pages laid out as a grid: within each row the values increase left to right, and every value on a row is smaller than the first value on the next row down. So reading the whole grid row by row gives one long increasing sequence. Given a value, is it somewhere in the album, without scanning cell by cell?

- **Maps to:** Binary search treating the grid as one sorted list (Search a 2D Matrix).
- **Model it:** Search a fully sorted row-major matrix for a target in logarithmic time.
- **Approach & variations:**
  - Treat the m×n grid as a single sorted list of length m*n.
  - Binary-search over flat indices, mapping index to (row, col) as (i / n, i % n).
  - Compare and discard half each step exactly like a 1D search.
  - Alternatively binary-search rows for the band, then within that row.
- **Time:** O(log(m*n)) — one binary search over all cells.
- **Space:** O(1) — index arithmetic only.

## 6. Koko Eating Bananas  ·  _Medium_

**Scenario:** A tortoise faces several heaps of lettuce and has a fixed number of hours before the caretaker returns. Each hour it commits to a single heap and nibbles up to a chosen fixed amount, stopping early if that heap runs out but never switching heaps mid-hour. What is the smallest steady nibbling rate that still finishes every heap in time?

- **Maps to:** Binary search on the answer (minimum feasible rate) (Koko Eating Bananas).
- **Model it:** Find the smallest per-hour eating speed such that total hours needed <= the deadline.
- **Approach & variations:**
  - The rate lives in [1, largest heap]; feasibility is monotonic — a higher rate never needs more hours.
  - For a candidate rate, sum ceil(heap / rate) over all heaps in one O(n) pass.
  - Binary-search the smallest rate whose total hours <= the deadline.
  - Same template as capacity-to-ship-within-D-days.
- **Time:** O(n log(maxHeap)) — an O(n) feasibility check over log(range) guesses.
- **Space:** O(1) — a few accumulators.

## 7. Capacity to Ship Packages Within D Days  ·  _Medium_

**Scenario:** Parcels sit on a dock in a fixed order and must be loaded onto a single ferry that makes one crossing per day, for a fixed number of days. Parcels must ship in their given order without reshuffling, and each day's load can't exceed the ferry's weight limit. What is the smallest weight limit that clears every parcel within the allotted days?

- **Maps to:** Binary search on the answer (minimum feasible capacity) (Capacity to Ship Packages Within D Days).
- **Model it:** Find the least ship capacity so packages, kept in order, fit into <= D day-loads.
- **Approach & variations:**
  - Capacity must be at least the heaviest parcel and at most the total weight — a monotonic range.
  - For a candidate capacity, greedily fill days in order, starting a new day when the next parcel would overflow; count days.
  - Binary-search the smallest capacity whose day count <= D.
  - Order is fixed, so the greedy pass is a clean O(n) feasibility check.
- **Time:** O(n log(sum)) — an O(n) check over log(weight range) guesses.
- **Space:** O(1) — running load and day counter.

## 8. Find Minimum In Rotated Sorted Array  ·  _Medium_

**Scenario:** A ranked leaderboard was originally sorted from low to high, but someone lifted a chunk off the top and moved it to the front, so it now increases, drops once, then increases again. All entries are distinct. Find the single lowest entry without scanning the whole board.

- **Maps to:** Binary search for the rotation pivot (Find Minimum in Rotated Sorted Array).
- **Model it:** In a rotated sorted array of distinct values, locate the minimum (the pivot).
- **Approach & variations:**
  - Compare the middle to the rightmost element to tell which half holds the drop.
  - If mid > right, the minimum is strictly to the right of mid; move low past mid.
  - Otherwise the minimum is at mid or to its left; move high to mid.
  - When the bounds converge they land on the minimum.
- **Time:** O(log n) — each step discards half.
- **Space:** O(1) — index bounds.

## 9. Search In Rotated Sorted Array  ·  _Medium_

**Scenario:** A wheel of distinct numbers was arranged in increasing order, then spun so the sequence starts partway through — it climbs, wraps around past the top back to the bottom, and climbs again. Given a target number, find its position on the wheel in as few checks as possible, or say it's absent.

- **Maps to:** Modified binary search on a rotated sorted array (Search in Rotated Sorted Array).
- **Model it:** Find a target's index in a rotated sorted array of distinct values in O(log n).
- **Approach & variations:**
  - At each step one half around the midpoint is still sorted — detect which by comparing mid to the left end.
  - If the target lies within that sorted half's value range, search there; otherwise search the other half.
  - Halve the interval each step just like ordinary binary search.
  - Distinct values guarantee the sorted-half test is unambiguous.
- **Time:** O(log n) — a single modified binary search.
- **Space:** O(1) — index bounds.

## 10. Search In Rotated Sorted Array II  ·  _Medium_

**Scenario:** Same spun wheel of numbers that climbs, wraps, and climbs again — but now duplicate numbers are allowed, so the value at the midpoint can equal the values at both ends and hide which side is sorted. Given a target, just report whether it appears anywhere on the wheel.

- **Maps to:** Binary search with duplicate handling (Search in Rotated Sorted Array II).
- **Model it:** Decide if a target exists in a rotated sorted array that may contain duplicates.
- **Approach & variations:**
  - Try the same sorted-half detection as the distinct version.
  - When mid equals both endpoints, you can't tell which half is sorted, so shrink both ends inward by one and retry.
  - That ambiguous step degrades the worst case but is still correct.
  - Return true on an exact match, false when the interval empties.
- **Time:** O(log n) average, O(n) worst case when many duplicates force linear shrinking.
- **Space:** O(1) — index bounds.

## 11. Time Based Key Value Store  ·  _Medium_

**Scenario:** An archivist logs, for each labeled folder, a series of stamped snapshots — each snapshot has a timestamp and a value, and snapshots for a folder always arrive with increasing timestamps. Later, asked for a folder's value 'as of' some moment, she must return the value from the latest snapshot at or before that moment, or nothing if none exists yet.

- **Maps to:** Per-key sorted timestamps searched by binary search (Time Based Key Value Store).
- **Model it:** Support set(key, value, time) and get(key, time) returning the value with the greatest time <= the query.
- **Approach & variations:**
  - Store each key's snapshots as a list appended in increasing time order.
  - On get, binary-search that list for the rightmost timestamp <= the query time.
  - Return that snapshot's value, or empty if every stored time is later.
  - Set is O(1) amortized since timestamps arrive sorted.
- **Time:** O(1) set, O(log m) get — binary search over a key's m snapshots.
- **Space:** O(total entries) — all snapshots retained.

## 12. Split Array Largest Sum  ·  _Hard_

**Scenario:** A row of chores with time costs must be assigned, in their given order, to a fixed number of workers so that each worker takes a consecutive block of chores. The finish time is set by whichever worker has the heaviest block. Partition the row into that many consecutive blocks so the heaviest block's total is as small as possible.

- **Maps to:** Binary search on the answer (minimize the maximum block) (Split Array Largest Sum).
- **Model it:** Split the array into k contiguous parts minimizing the largest part's sum.
- **Approach & variations:**
  - The answer lies in [max single value, total sum] and feasibility is monotonic.
  - For a candidate cap, greedily fill consecutive blocks, starting a new one when adding the next chore would exceed the cap; count blocks.
  - A candidate is feasible if the block count is <= the worker count.
  - Binary-search the smallest feasible cap (equivalent to a DP but far faster).
- **Time:** O(n log(sum)) — an O(n) greedy check over log(range) guesses.
- **Space:** O(1) — running block sum and count.

## 13. Median of Two Sorted Arrays  ·  _Hard_

**Scenario:** Two ranked queues of contestants, each already ordered by score, need their combined middle score — the median had they merged into one ranked line. You must find it far faster than actually merging the two queues. What is the combined median?

- **Maps to:** Binary search for a partition of the smaller array (Median of Two Sorted Arrays).
- **Model it:** Find the median of the union of two sorted arrays in logarithmic time.
- **Approach & variations:**
  - Binary-search a cut position in the shorter array; the other cut is fixed so the left side holds exactly half the total.
  - Check the boundary condition: each side's left maxima must not exceed the other side's right minima.
  - Adjust the cut left or right until balanced, then read the median from the four boundary values.
  - Handle odd/even total length and empty-side sentinels of -inf / +inf.
- **Time:** O(log(min(m, n))) — binary search over the smaller array's cut.
- **Space:** O(1) — only boundary values.

## 14. Find in Mountain Array  ·  _Hard_

**Scenario:** A trail's elevation strictly rises to a single summit and then strictly falls. You can only ask 'what's the height at position i?' and such peeks are costly, so you must use few. Given a target height, return the earliest position along the trail whose height matches it, or report it's not on the trail.

- **Maps to:** Three binary searches: find the peak, then each slope (Find in Mountain Array).
- **Model it:** In an array that increases then decreases, find the leftmost index equal to the target with few accesses.
- **Approach & variations:**
  - Binary-search the summit by comparing each midpoint to its right neighbor (rising vs falling).
  - Binary-search the ascending side (normal order) for the target first — it yields the earliest index.
  - If not found there, binary-search the descending side (reversed comparison).
  - Cache or minimize peeks since accesses are the limited resource.
- **Time:** O(log n) — three binary searches, each logarithmic.
- **Space:** O(1) — index bounds only.

---
deck: "NeetCode 250::Sliding Window"
topic: "NeetCode 250 — Sliding Window"
tags: [ankicardmaker, neetcode250, sliding-window]
note_type: Basic
created: 2026-09-09
---

# NeetCode 250 — Sliding Window

Story front hides the technique; back reveals the mapping, approach, and complexity.

## 1. Contains Duplicate II  ·  _Easy_

**Scenario:** A gallery guard walks past a long row of paintings, one per step. He worries about forgeries: two identical paintings hung close together would be embarrassingly obvious to visitors. He only cares if a matching pair sits within K steps of each other along the row. Is there any such nearby matching pair?

- **Maps to:** Fixed-width sliding window with a set of seen values (Contains Duplicate II).
- **Model it:** Given values in order and a distance K, decide if two equal values appear at indices no more than K apart.
- **Approach & variations:**
  - Keep a set of the last K values seen; slide it forward one step at a time.
  - At each position, if the current value is already in the set, a nearby duplicate exists.
  - When the window exceeds K, drop the value that just fell off the left end.
  - A plain map of value -> last index also works: check if current index minus stored index <= K.
- **Time:** O(n) — each value is added and removed from the window once.
- **Space:** O(min(n, K)) — the set holds at most K recent values.

## 2. Best Time to Buy And Sell Stock  ·  _Easy_

**Scenario:** A trader sees the daily prices of a coin listed left to right in calendar order. She may buy on one day and sell on a strictly later day, exactly once. She cannot sell before she buys and cannot travel back in time. What is the largest profit she can lock in, or nothing if prices only fall?

- **Maps to:** Track running minimum while scanning (Best Time to Buy and Sell Stock).
- **Model it:** Given a sequence of prices, maximize price[j] - price[i] for some i < j.
- **Approach & variations:**
  - Sweep left to right keeping the cheapest price seen so far (the best buy day).
  - At each day compute today's price minus that minimum and keep the largest such gap.
  - If no positive gap ever appears, the answer is 0 (never trade).
  - Think of it as the widest 'valley then peak' where the valley precedes the peak.
- **Time:** O(n) — a single pass over the prices.
- **Space:** O(1) — just the running minimum and best profit.

## 3. Longest Substring Without Repeating Characters  ·  _Medium_

**Scenario:** A jeweler strings beads from a spool in the exact order they come off. She wants the longest unbroken run she can cut out such that no bead color repeats within that run. As soon as a stretch would reuse a color, it's ruined. How long is the longest all-distinct stretch?

- **Maps to:** Variable-size sliding window with last-seen positions (Longest Substring Without Repeating Characters).
- **Model it:** Find the longest contiguous span of the sequence containing no repeated element.
- **Approach & variations:**
  - Grow a window by advancing the right edge one bead at a time.
  - Remember each color's most recent position; on a repeat, jump the left edge to just past the earlier copy.
  - Track the maximum window length seen along the way.
  - Never move the left edge backward, so each pointer only advances.
- **Time:** O(n) — each edge sweeps forward at most n steps.
- **Space:** O(min(n, alphabet)) — positions for the distinct colors in the window.

## 4. Longest Repeating Character Replacement  ·  _Medium_

**Scenario:** A tiler lays colored tiles in a fixed line and wants the longest solid-colored stretch he can achieve. He is allowed to repaint at most K tiles anywhere within a chosen stretch to make it one uniform color. Which contiguous stretch, after up to K repaints, gives the longest single-color run?

- **Maps to:** Sliding window tracking the most frequent element's count (Longest Repeating Character Replacement).
- **Model it:** Find the longest window where (window length) minus (count of its most common element) <= K.
- **Approach & variations:**
  - Expand the window and count colors inside it; track the highest single-color count.
  - The tiles needing repaint equal window size minus that highest count; that must stay <= K.
  - If it exceeds K, shrink from the left until the window is valid again.
  - The best window width found is the answer; the max-count need not be recomputed exactly to stay correct.
- **Time:** O(n) — each edge advances at most n times over a fixed-size color count.
- **Space:** O(1) — a fixed tally of at most 26 colors.

## 5. Permutation In String  ·  _Medium_

**Scenario:** A locksmith has a small bag of lettered tiles and a long ribbon of letters. He wants to know if somewhere along the ribbon there is an unbroken segment using exactly his bag's tiles — same letters, same quantities — just possibly shuffled in order. Does such a matching window exist anywhere on the ribbon?

- **Maps to:** Fixed-length sliding window comparing letter counts (Permutation In String).
- **Model it:** Decide if any substring of length |s1| in s2 has the same character multiset as s1.
- **Approach & variations:**
  - Tally the letter counts needed by the bag.
  - Slide a window the same width as the bag along the ribbon, maintaining its letter tally.
  - Compare tallies at each step; a match means a permutation is present.
  - Maintain a 'matched letters' counter to compare in O(1) instead of scanning 26 slots each step.
- **Time:** O(n) — one pass with constant-size tally comparisons.
- **Space:** O(1) — two fixed 26-letter tallies.

## 6. Minimum Size Subarray Sum  ·  _Medium_

**Scenario:** A dockworker loads crates onto a conveyor that presents them in a fixed order, each with a weight. He needs to grab a run of consecutive crates whose combined weight is at least a target quota, and he wants the shortest such run so he handles as few crates as possible. What's the fewest consecutive crates that meet the quota?

- **Maps to:** Variable-size sliding window over positive values (Minimum Size Subarray Sum).
- **Model it:** Find the shortest contiguous subarray whose sum is >= the target.
- **Approach & variations:**
  - Extend the window to the right, adding weights until the running sum reaches the quota.
  - Once satisfied, shrink from the left while it still meets the quota, recording the smallest width.
  - Because weights are positive, removing from the left only lowers the sum — the window is monotone.
  - If the total never reaches the quota, the answer is 0.
- **Time:** O(n) — each crate enters and leaves the window once.
- **Space:** O(1) — a running sum and two edges.

## 7. Find K Closest Elements  ·  _Medium_

**Scenario:** Houses stand along a straight road at increasing mile markers. A mail carrier parks at a chosen milepost X and wants the K houses nearest to her, returned in road order. Ties go to the house with the smaller milepost. Which K houses does she pick?

- **Maps to:** Binary search for the window's left edge, or two-pointer shrink (Find K Closest Elements).
- **Model it:** In a sorted array, return the K elements with smallest distance to X, in sorted order.
- **Approach & variations:**
  - The answer is a contiguous window of K sorted values — only its start position is unknown.
  - Binary-search the left edge: compare X - arr[mid] against arr[mid+k] - X to decide which side is closer.
  - Alternatively shrink from both ends, dropping whichever endpoint is farther (ties drop the right).
  - Return the K values in place; they are already in order.
- **Time:** O(log(n-k) + k) — binary search for the edge, then copy K values.
- **Space:** O(1) beyond the K-element output.

## 8. Minimum Window Substring  ·  _Hard_

**Scenario:** A collector walks a fixed line of stalls left to right, each selling one kind of stamp. She has a shopping list demanding certain stamps in certain quantities. She wants the shortest unbroken run of stalls she can visit that together supply every stamp on her list (extras allowed). What's the shortest qualifying run of stalls?

- **Maps to:** Variable-size sliding window with a need-count (Minimum Window Substring).
- **Model it:** Find the shortest substring of s that contains all characters of t with required multiplicities.
- **Approach & variations:**
  - Tally required counts, then expand the right edge, decrementing needs as stamps are collected.
  - Track how many distinct requirements are fully met; when all are met the window is valid.
  - While valid, shrink from the left to minimize width, recording the best, then break validity and grow again.
  - Return the smallest valid window, or empty if the list is never fully covered.
- **Time:** O(n + m) — each stall is entered and left once; m to build the need tally.
- **Space:** O(m) — counts for the distinct required stamps.

## 9. Sliding Window Maximum  ·  _Hard_

**Scenario:** A surveyor drives past a row of hills of known heights. Through a viewfinder that frames exactly K consecutive hills at a time, she slides the frame one hill forward at each stop, from the start of the row to the end. At every stop she notes the tallest hill currently in frame. List those peak heights, one per stop.

- **Maps to:** Monotonic decreasing deque of candidate maxima (Sliding Window Maximum).
- **Model it:** For every window of K consecutive elements, report the maximum.
- **Approach & variations:**
  - Keep a double-ended queue of indices whose heights are in decreasing order — the front is the current max.
  - Before adding a new hill, pop smaller heights off the back; they can never be the max while it stands.
  - Pop the front when its index falls out of the window's left edge.
  - After the first full window, record the front's height at each step.
- **Time:** O(n) — each index is pushed and popped at most once.
- **Space:** O(k) — the deque holds at most one window of candidates.

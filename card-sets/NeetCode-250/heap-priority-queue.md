---
deck: "NeetCode 250::Heap / Priority Queue"
topic: "NeetCode 250 — Heap / Priority Queue"
tags: [ankicardmaker, neetcode250, heap-priority-queue]
note_type: Basic
created: 2026-09-09
---

# NeetCode 250 — Heap / Priority Queue

Story front hides the technique; back reveals the mapping, approach, and complexity.

## 1. Kth Largest Element In a Stream  ·  _Easy_

**Scenario:** A fishing dock weighs every catch as it comes in, one fish at a time, forever. After each new fish is weighed, the harbor master must instantly announce the weight of the Kth-heaviest fish caught so far this season. New fish keep arriving; the answer must stay current after every single one.

- **Maps to:** Min-heap of fixed size K (Kth Largest Element in a Stream).
- **Model it:** Maintain a running structure that returns the Kth largest value after each insertion into a stream.
- **Approach & variations:**
  - Keep a min-heap holding only the K largest seen so far; its smallest element (the root) is the Kth largest.
  - On each new value: push it, then if the heap exceeds size K pop the smallest.
  - The root is always the answer, in `O(log K)` per query.
- **Time:** O(log K) per add — one push and at most one pop on a heap capped at size K.
- **Space:** O(K) — the heap never holds more than K elements.

## 2. Last Stone Weight  ·  _Easy_

**Scenario:** A pile of rocks sits by a smashing machine. Each round the two heaviest rocks are chosen and slammed together: if equal weight they both vaporize, otherwise the lighter is destroyed and the heavier shrinks by the lighter's weight, returning to the pile. Repeat until at most one rock remains. What does the survivor weigh, or zero if none is left?

- **Maps to:** Max-heap, repeated extraction of the two largest (Last Stone Weight).
- **Model it:** Repeatedly remove the two maximum values, push back their difference, until one or none remain.
- **Approach & variations:**
  - Build a max-heap of all weights.
  - Pop the two biggest; if they differ push back the difference.
  - Continue until size <= 1; answer is the remaining weight or 0.
- **Time:** O(n log n) — up to n rounds, each doing a constant number of O(log n) heap operations.
- **Space:** O(n) — the heap stores all stones.

## 3. K Closest Points to Origin  ·  _Medium_

**Scenario:** A drone hovers over a flat field where scattered tents each have a map coordinate. Base camp sits at coordinate zero-zero. The pilot must pick out the K tents nearest to base camp (straight-line distance), in any order. Which K tents are closest?

- **Maps to:** Max-heap of size K on distance, or quickselect (K Closest Points to Origin).
- **Model it:** Find the K points with smallest squared distance to the origin from a list of coordinates.
- **Approach & variations:**
  - Compare by squared distance `x*x + y*y` — no square roots needed.
  - Keep a max-heap of size K: push each point, pop the farthest when size exceeds K; the heap ends holding the K closest.
  - Alternatively quickselect partitions the K nearest in expected O(n).
- **Time:** O(n log K) with the size-K heap; O(n) expected with quickselect.
- **Space:** O(K) for the heap (O(1) extra for in-place quickselect).

## 4. Kth Largest Element In An Array  ·  _Medium_

**Scenario:** A vineyard has harvested a big unsorted crate of grape clusters, each a different weight. The buyer doesn't want them all sorted — she only wants to know the weight of the Kth-heaviest cluster in the crate. What is it, found as fast as possible?

- **Maps to:** Quickselect (or size-K heap) for order statistic (Kth Largest Element in an Array).
- **Model it:** Return the Kth largest value in an unsorted array without fully sorting it.
- **Approach & variations:**
  - Quickselect: partition around a pivot, recurse only into the side containing the Kth position.
  - Kth largest equals the (n-K)th smallest index after partitioning.
  - A min-heap of size K also works in O(n log K); full sort is O(n log n).
- **Time:** O(n) expected with quickselect (O(n^2) worst case); O(n log K) with a heap.
- **Space:** O(1) for in-place quickselect; O(K) for the heap variant.

## 5. Task Scheduler  ·  _Medium_

**Scenario:** A machine stamps parts, and identical stamps need a fixed cooldown of N idle minutes between two uses of the same die before it can be reused. Each minute the machine either stamps one part or sits idle. Given a batch listing how many parts of each die type are needed, what is the fewest total minutes to stamp them all?

- **Maps to:** Greedy with max-heap by remaining count (Task Scheduler).
- **Model it:** Schedule tasks so identical tasks are at least N slots apart, minimizing total time slots.
- **Approach & variations:**
  - Always run the most-frequent still-available task; a max-heap keyed on remaining count picks it.
  - Process in cycles of length N+1, cooling down used tasks before re-adding them.
  - Closed form: `(maxCount-1)*(n+1) + (#tasks tied at maxCount)`, but never less than the total task count.
- **Time:** O(T) with the formula, or O(T log 26) with the heap where T is total tasks.
- **Space:** O(1) — at most 26 distinct task counts.

## 6. Design Twitter  ·  _Medium_

**Scenario:** A tiny bulletin-board town lets residents pin notes, follow each other, and unfollow. When a resident asks to read their wall, they should see the 10 most recently pinned notes drawn from themselves and everyone they follow, newest first. Design the whole town's system supporting post, follow, unfollow, and read-wall.

- **Maps to:** Hash maps plus a k-way merge with a heap on timestamps (Design Twitter).
- **Model it:** Support posting timestamped items and merging the newest 10 across a user's own feed and followees' feeds.
- **Approach & variations:**
  - Store per-user tweet lists (with a global increasing timestamp) and a follow set per user.
  - For the feed, heap-merge the tail of each followed user's list, popping the 10 newest.
  - Follow/unfollow just edit the set; posting appends with the next timestamp.
- **Time:** getNews O(F log F + 10 log F) merging F followed feeds; post/follow/unfollow O(1).
- **Space:** O(users + tweets + follow-edges) for the stored maps.

## 7. Single Threaded CPU  ·  _Medium_

**Scenario:** A one-window bakery counter serves customers who each arrive at a stated minute and need a known number of minutes to serve. The clerk, whenever free, serves the waiting customer with the shortest job (ties broken by who has been waiting longest by ticket number); if nobody is waiting yet, the clerk waits for the next arrival. In what order are customers served?

- **Maps to:** Sort by arrival, then a min-heap on (duration, index) (Single-Threaded CPU).
- **Model it:** Simulate a processor picking the shortest available task by processing time, breaking ties by original index.
- **Approach & variations:**
  - Sort tasks by arrival time, keeping original indices.
  - Advance a clock; push all tasks that have arrived into a min-heap keyed on (processingTime, index).
  - Pop the smallest to run; if the heap is empty, jump the clock to the next arrival.
- **Time:** O(n log n) — sorting plus each task pushed and popped once from the heap.
- **Space:** O(n) — the heap can hold all pending tasks.

## 8. Reorganize String  ·  _Medium_

**Scenario:** A florist arranges a row of flowers using only the blossoms she has in stock, some colors more plentiful than others. She wants a line-up where no two neighboring flowers share the same color. Can she build such a row, and if so give one valid arrangement?

- **Maps to:** Greedy placement with a max-heap by remaining frequency (Reorganize String).
- **Model it:** Rearrange characters so no two adjacent are equal, or report it is impossible.
- **Approach & variations:**
  - Count each character; if any count exceeds `(n+1)/2` it is impossible.
  - Repeatedly place the most-frequent available character that isn't the one just placed (max-heap on count, holding the previous back one step).
  - Decrement and re-add the previous character after each placement.
- **Time:** O(n log k) — n placements, each an O(log k) heap operation over k distinct chars.
- **Space:** O(k) — counts and heap over the distinct characters.

## 9. Longest Happy String  ·  _Medium_

**Scenario:** A candy shop threads beads of three colors onto a string but the machine jams if three beads of the same color ever touch in a row. Given limited supplies of each color, build the longest possible string that never has three identical beads in a row. What string results (any valid longest one)?

- **Maps to:** Greedy with a max-heap by remaining count and a run-length guard (Longest Happy String).
- **Model it:** Build the longest string from a/b/c with given caps such that no character appears three times consecutively.
- **Approach & variations:**
  - Max-heap on remaining counts; always try the most plentiful color.
  - If the last two placed are already that color, use the next-most-plentiful instead; if none, stop.
  - Decrement and push back colors that still have supply.
- **Time:** O(n log 3) ≈ O(n) — n total beads placed, each a constant-size heap operation.
- **Space:** O(1) — heap over only three colors.

## 10. Car Pooling  ·  _Medium_

**Scenario:** A shuttle van with a fixed number of seats drives one-way along a straight road, never reversing. It has a list of pickup requests, each stating how many riders board at one mile-marker and get off at a later one. Can the van complete the whole route without ever exceeding its seat count?

- **Maps to:** Sweep-line via a min-heap on drop-off (or a difference array over stops) (Car Pooling).
- **Model it:** Check that concurrent passenger load never exceeds capacity across overlapping pickup/drop-off intervals.
- **Approach & variations:**
  - Sort trips by start location; use a min-heap keyed on drop-off to release seats as the van passes each marker.
  - Add boarders, first popping everyone who has already gotten off; if load exceeds capacity, fail.
  - A difference array over the fixed route (bucket +riders at start, -riders at end, prefix-sum) does it in O(n).
- **Time:** O(n log n) with the heap; O(n + maxLocation) with the difference array.
- **Space:** O(n) for the heap, or O(maxLocation) for the difference array.

## 11. Find Median From Data Stream  ·  _Hard_

**Scenario:** A weigh station logs truck weights one after another without end. At any moment an inspector may ask for the current middle weight of everything logged so far — the middle value if the count is odd, or the average of the two middle values if even. Support adding weights and answering the middle-value query at any time.

- **Maps to:** Two heaps: a max-heap of the lower half and a min-heap of the upper half (Find Median from Data Stream).
- **Model it:** Maintain a running median over a stream, supporting O(log n) insert and O(1) median query.
- **Approach & variations:**
  - Keep the smaller half in a max-heap and the larger half in a min-heap.
  - On insert, push to one side then rebalance so their sizes differ by at most one.
  - Median is the larger heap's root, or the average of both roots when sizes are equal.
- **Time:** addNum O(log n) per insertion; findMedian O(1).
- **Space:** O(n) — every value is stored across the two heaps.

## 12. IPO  ·  _Hard_

**Scenario:** A startup begins with a small amount of cash and may launch at most K projects, one after another, never returning a finished project's payout until choosing the next. Each project needs a minimum upfront capital to start and, once done, adds a pure profit to the bank. Pick up to K projects to maximize the final bank balance.

- **Maps to:** Two-structure greedy: sort by capital, max-heap on profit of affordable projects (IPO).
- **Model it:** Do at most K projects, each requiring capital <= current funds, to maximize accumulated capital.
- **Approach & variations:**
  - Sort projects by required capital ascending.
  - Each round, add all now-affordable projects to a max-heap keyed on profit, then take the single most profitable one.
  - Repeat up to K times; if the heap empties, stop early.
- **Time:** O(n log n) — sort plus each project pushed/popped once from the heap.
- **Space:** O(n) — the profit heap may hold all affordable projects.

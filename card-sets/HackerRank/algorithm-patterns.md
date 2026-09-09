---
deck: "HackerRank"
topic: "Algorithm & data-structure patterns (HackerRank / interview scenarios)"
tags: [ankicardmaker, hackerrank, algorithms, patterns]
note_type: Basic
created: 2026-09-09
---

# HackerRank — Algorithm & Data-Structure Patterns

Each card gives a **scenario** on the front. On the back: the pattern/data structure,
the variations needed to adapt it, and the time/space complexity **with the reason**.

## 1. Two pointers (opposite ends).

**Scenario:** You're given an array of integers **sorted in ascending order** and a target value. Return the indices of the two numbers that add up to the target. You must do it in constant extra space.

- **Pattern:** Two pointers (opposite ends).
- **Approach & variations:**
  - Place `lo` at the start and `hi` at the end.
  - If `a[lo]+a[hi] > target` move `hi--`; if `< target` move `lo++`; if equal, return.
  - Works only because the array is sorted — on an unsorted array use a hash map instead (O(n) time, O(n) space).
- **Time:** O(n) — each pointer sweeps the array at most once.
- **Space:** O(1) — only two index variables.

## 2. Variable-size sliding window + hash map of last-seen index.

**Scenario:** Given a string, find the length of the **longest substring without repeating characters**.

- **Pattern:** Variable-size sliding window + hash map of last-seen index.
- **Approach & variations:**
  - Expand `right` one char at a time; keep a map char→last index.
  - When a repeat is inside the window, jump `left` to `lastIndex+1`.
  - Track the max window width seen.
  - Variation: to return the substring itself, store the best `left`/`right`.
- **Time:** O(n) — each character enters and leaves the window at most once.
- **Space:** O(min(n, |alphabet|)) — map holds at most one entry per distinct character.

## 3. Fixed-size sliding window.

**Scenario:** Given an array of integers and a number <code>k</code>, find the **maximum sum of any contiguous subarray of length exactly k**.

- **Pattern:** Fixed-size sliding window.
- **Approach & variations:**
  - Sum the first `k` elements, then slide: add the incoming element, subtract the outgoing one.
  - No need to re-sum each window — that's the whole trick vs. the O(n·k) brute force.
  - Variation: for 'at most k' or 'at least k' problems switch to a variable window.
- **Time:** O(n) — one pass, O(1) work per slide.
- **Space:** O(1) — a single running sum.

## 4. Fast & slow pointers (Floyd's cycle detection).

**Scenario:** Determine whether a **singly linked list contains a cycle**, using constant extra memory (you cannot use a hash set of visited nodes).

- **Pattern:** Fast & slow pointers (Floyd's cycle detection).
- **Approach & variations:**
  - Advance `slow` by 1 and `fast` by 2 each step.
  - If they ever meet, there's a cycle; if `fast` hits null, there isn't.
  - Variation: to find the cycle's **start**, reset one pointer to head and advance both by 1 until they meet again.
- **Time:** O(n) — fast pointer laps slow within one cycle length.
- **Space:** O(1) — two pointers, no visited set.

## 5. Binary search on the answer.

**Scenario:** A ship must deliver all packages (given as an array of weights, in order) within <code>D</code> days. Find the **minimum ship capacity** that makes this possible.

- **Pattern:** Binary search on the answer.
- **Approach & variations:**
  - The answer lies in `[max(weight), sum(weights)]`.
  - For a candidate capacity, greedily count days needed (a monotonic feasibility check).
  - Binary-search the smallest capacity whose day-count ≤ D.
  - Same shape as 'Koko eating bananas', 'split array largest sum' — search the value space, not an index.
- **Time:** O(n · log(sum − max)) — feasibility is O(n), run log(range) times.
- **Space:** O(1) — a few counters.

## 6. Breadth-first search (BFS) on an unweighted grid.

**Scenario:** Given a grid of <code>0</code> (open) and <code>1</code> (wall), find the length of the **shortest path** from top-left to bottom-right moving 4-directionally.

- **Pattern:** Breadth-first search (BFS) on an unweighted grid.
- **Approach & variations:**
  - BFS explores by distance, so the first time you reach the target is the shortest path.
  - Use a queue of cells; mark visited on enqueue to avoid re-processing.
  - Variation: weighted edges → Dijkstra; need the actual path → store parent pointers.
- **Time:** O(V + E) = O(rows·cols) — each cell and edge visited once.
- **Space:** O(rows·cols) — visited grid + queue in the worst case.

## 7. Flood fill via DFS/BFS (or Union-Find).

**Scenario:** Given a 2-D grid of <code>'1'</code> (land) and <code>'0'</code> (water), count the **number of islands** (connected land regions, 4-directional).

- **Pattern:** Flood fill via DFS/BFS (or Union-Find).
- **Approach & variations:**
  - Scan every cell; on unvisited land, flood-fill the whole island and increment the count.
  - Mark cells visited (or sink them to '0') so each is counted once.
  - Variation: Union-Find shines when land is added incrementally ('number of islands II').
- **Time:** O(rows·cols) — every cell visited a constant number of times.
- **Space:** O(rows·cols) — recursion/stack or visited set in the worst case.

## 8. Backtracking (DFS over the decision tree with undo).

**Scenario:** Given a collection of **distinct integers, return all possible permutations**.

- **Pattern:** Backtracking (DFS over the decision tree with undo).
- **Approach & variations:**
  - Build a partial arrangement; at each depth try every unused element.
  - Recurse, then **undo** the choice (mark unused) before the next branch.
  - Prune early for constrained variants (N-Queens: skip attacked squares; combinations: enforce non-decreasing picks).
- **Time:** O(n · n!) — n! permutations, O(n) to copy each out.
- **Space:** O(n) — recursion depth / used-set (excluding the output list).

## 9. 1-D dynamic programming (Fibonacci recurrence).

**Scenario:** You are climbing a staircase of <code>n</code> steps, taking **1 or 2 steps** at a time. How many **distinct ways** can you reach the top?

- **Pattern:** 1-D dynamic programming (Fibonacci recurrence).
- **Approach & variations:**
  - `ways(i) = ways(i-1) + ways(i-2)`.
  - Memoize top-down, or build bottom-up.
  - Only the last two values matter → roll them in two variables for O(1) space.
  - Same skeleton as 'house robber' with a different transition.
- **Time:** O(n) — each subproblem solved once.
- **Space:** O(1) — two rolling variables (O(n) if you keep the full table).

## 10. 2-D dynamic programming over the two string prefixes.

**Scenario:** Given two strings, find the **minimum number of insert/delete/replace edits** to turn one into the other (edit distance).

- **Pattern:** 2-D dynamic programming over the two string prefixes.
- **Approach & variations:**
  - `dp[i][j]` = edits to convert first i chars → first j chars.
  - Match → carry `dp[i-1][j-1]`; else 1 + min(insert, delete, replace).
  - Variation: LCS / min-window alignment share this grid; you can compress to two rows for O(min) space.
- **Time:** O(m·n) — fill each table cell once in O(1).
- **Space:** O(m·n), reducible to O(min(m,n)) with rolling rows.

## 11. 0/1 Knapsack dynamic programming.

**Scenario:** Given item weights and values and a knapsack capacity <code>W</code>, maximize total value with **each item used at most once**.

- **Pattern:** 0/1 Knapsack dynamic programming.
- **Approach & variations:**
  - `dp[c]` = best value at capacity c; process items outer, capacity inner.
  - Iterate capacity **downward** so each item is used at most once (upward = unbounded knapsack).
  - Variation: 'subset sum' / 'partition equal subset' are boolean knapsacks.
- **Time:** O(n·W) — pseudo-polynomial (depends on the numeric W).
- **Space:** O(W) — the 1-D rolling array.

## 12. Greedy — sort by end time.

**Scenario:** Given intervals of start/end times, find the **maximum number of non-overlapping intervals** you can keep (or the minimum to remove).

- **Pattern:** Greedy — sort by end time.
- **Approach & variations:**
  - Sort by earliest finishing time; always keep the interval that ends soonest.
  - Skip any interval that starts before the last kept one's end.
  - The exchange argument proves greedy is optimal here.
  - Variation: sort by **start** for merging intervals or a min-heap for meeting-room count.
- **Time:** O(n log n) — dominated by the sort.
- **Space:** O(1) beyond the sort (O(n) if the sort isn't in place).

## 13. Min-heap of size k (partial selection).

**Scenario:** From a large stream/array of numbers, return the <code>k</code> **largest elements** (order doesn't matter).

- **Pattern:** Min-heap of size k (partial selection).
- **Approach & variations:**
  - Keep a min-heap of the k biggest seen; push each element, pop when size > k.
  - The heap's root is the k-th largest — the admission threshold.
  - Variation: k **closest** points → heap keyed by distance; exact k-th only → Quickselect in O(n) average.
- **Time:** O(n log k) — n pushes, each O(log k).
- **Space:** O(k) — the heap holds only k elements.

## 14. Union-Find (Disjoint Set Union).

**Scenario:** Given <code>n</code> nodes and a list of undirected edges, count the **number of connected components** (or detect a redundant edge that forms a cycle).

- **Pattern:** Union-Find (Disjoint Set Union).
- **Approach & variations:**
  - `union` each edge's endpoints; `find` with path compression.
  - Use union by rank/size to keep trees shallow.
  - Components = number of distinct roots; an edge whose endpoints already share a root is a cycle.
  - Prefer DSU over DFS when edges arrive incrementally.
- **Time:** O(E · α(n)) — near-constant inverse-Ackermann per operation.
- **Space:** O(n) — parent and rank arrays.

## 15. Topological sort (Kahn's BFS on in-degree, or DFS).

**Scenario:** You must finish <code>n</code> courses; some have prerequisites given as directed pairs. Return a **valid order to take them**, or detect that none exists.

- **Pattern:** Topological sort (Kahn's BFS on in-degree, or DFS).
- **Approach & variations:**
  - Kahn: start from in-degree-0 nodes, remove them, decrement neighbors, repeat.
  - If you output fewer than n nodes, there's a cycle → no valid order.
  - DFS variant: push nodes on post-order, reverse at the end; a gray node revisited = cycle.
- **Time:** O(V + E) — each node and edge processed once.
- **Space:** O(V + E) — adjacency list + in-degree array/queue.

## 16. Monotonic (decreasing) stack.

**Scenario:** For each element in an array, find the **next element to its right that is greater** (or −1 if none). E.g. 'days until a warmer temperature'.

- **Pattern:** Monotonic (decreasing) stack.
- **Approach & variations:**
  - Push indices; before pushing i, pop every index whose value < a[i] — a[i] is their answer.
  - The stack stays decreasing from bottom to top.
  - Variation: nearest smaller, largest rectangle in histogram, and trapping rain water all use monotonic stacks.
- **Time:** O(n) — each index is pushed and popped at most once.
- **Space:** O(n) — the stack in the worst (sorted) case.

## 17. Trie (prefix tree).

**Scenario:** Build a structure that stores a dictionary of words and supports fast **prefix lookups / autocomplete** ('does any word start with …').

- **Pattern:** Trie (prefix tree).
- **Approach & variations:**
  - Each node has child links per character and an end-of-word flag.
  - Insert/search walk one node per character — independent of how many words are stored.
  - Variation: add DFS from a prefix node for autocomplete; a '.' wildcard needs branching search.
- **Time:** Build O(total characters); query O(L) for a word of length L.
- **Space:** O(total characters) — one node chain per unique prefix.

## 18. Dijkstra's algorithm (min-heap / priority queue).

**Scenario:** Given a graph with **non-negative weighted edges**, find the shortest distance from a source to every other node.

- **Pattern:** Dijkstra's algorithm (min-heap / priority queue).
- **Approach & variations:**
  - Repeatedly pop the closest unfinalized node and relax its neighbors.
  - A min-heap keyed by tentative distance gives the next node to finalize.
  - Variation: negative edges → Bellman-Ford; unweighted → plain BFS; A* adds a heuristic.
- **Time:** O(E log V) — each edge may trigger a heap push.
- **Space:** O(V) — distance array + heap entries.

## 19. Prefix sum + hash map of prefix-sum counts.

**Scenario:** Given an array of integers and a target <code>k</code>, count the **number of contiguous subarrays whose sum equals k** (values may be negative).

- **Pattern:** Prefix sum + hash map of prefix-sum counts.
- **Approach & variations:**
  - Running sum `S`; a subarray ending here sums to k iff a previous prefix equalled `S − k`.
  - Store counts of each prefix sum in a map; add `map[S−k]` to the answer.
  - The map (not a sliding window) is required because negatives break monotonicity.
  - Seed the map with `{0:1}` for subarrays starting at index 0.
- **Time:** O(n) — one pass, O(1) map operations.
- **Space:** O(n) — up to n distinct prefix sums.

## 20. Sort by start, then sweep and merge.

**Scenario:** Given a list of intervals, **merge all overlapping intervals** into the minimal set of disjoint intervals.

- **Pattern:** Sort by start, then sweep and merge.
- **Approach & variations:**
  - Sort intervals by start time.
  - Keep the current merged interval; if the next starts ≤ current end, extend the end; otherwise emit and start a new one.
  - Variation: 'insert interval' skips the full sort; 'employee free time' merges across people with a heap.
- **Time:** O(n log n) — the sort dominates the linear sweep.
- **Space:** O(n) — the output list (O(log n)/O(n) sort overhead).

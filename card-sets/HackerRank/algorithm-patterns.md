---
deck: "HackerRank"
topic: "Real-world scenarios that map to algorithm/data-structure patterns"
tags: [ankicardmaker, hackerrank, algorithms, patterns, story]
note_type: Basic
created: 2026-09-09
---

# HackerRank — Scenario Patterns (story fronts)

**Front:** a plain-language, non-technical story (monkeys, trains, parties).
**Your job:** figure out which algorithm/data structure it maps to.
**Back:** the mapping, how to model it, the approach + variations, and time/space with the why.

## 1. Two pointers on a sorted sequence.

**Scenario:** A monkey has a row of banana bunches laid out from the smallest bunch on the left to the biggest on the right. It wants a feast of exactly **N** bananas by grabbing **exactly two** bunches. What's the fastest way to find such a pair without trying every combination?

- **Maps to:** Two pointers on a sorted sequence.
- **Model it:** The bunches are a sorted array; you want two values summing to a target N.
- **Approach & variations:**
  - Start one finger on the smallest bunch, one on the largest.
  - If their sum is too big, move the right finger left; too small, move the left finger right; equal → found.
  - Only works because it's sorted — if the bunches were in random order you'd need a hash set (O(n) time, O(n) space) instead.
- **Time:** O(n) — the two fingers only ever move inward, sweeping the row once.
- **Space:** O(1) — just two positions.

## 2. Variable-size sliding window + last-seen map.

**Scenario:** A conductor walks past a train, noting each wagon's color in order. He wants the **longest run of consecutive wagons** in which no color repeats.

- **Maps to:** Variable-size sliding window + last-seen map.
- **Model it:** Wagons are a sequence; find the longest window with all-distinct elements.
- **Approach & variations:**
  - Extend the window one wagon at a time, remembering the last position of each color.
  - When a color repeats inside the window, jump the window's left edge past that earlier copy.
  - Track the widest window seen.
  - Variation: 'at most K distinct colors' just changes the shrink condition.
- **Time:** O(n) — each wagon is entered and left by the window at most once.
- **Space:** O(min(n, #colors)) — the map holds one entry per distinct color in the window.

## 3. Fixed-size sliding window.

**Scenario:** At a carnival there's a long row of prize stalls, each worth some tickets. Your pass lets you play **exactly 4 stalls in a row**. Which 4 adjacent stalls win the most tickets?

- **Maps to:** Fixed-size sliding window.
- **Model it:** Stalls are an array; find the max sum of every contiguous block of size 4.
- **Approach & variations:**
  - Add up the first 4 stalls, then slide: add the next stall, subtract the one you left behind.
  - That reuse is the trick — no re-adding the whole block each step.
  - Variation: unknown/variable block length turns this into a two-pointer variable window.
- **Time:** O(n) — one pass, constant work per slide.
- **Space:** O(1) — a single running total.

## 4. Fast & slow pointers (cycle detection).

**Scenario:** A treasure hunter follows clues: each clue points to the next hiding spot. She worries the clues secretly **loop back on themselves forever**. With no notebook to record where she's been, how can she tell she's trapped in a loop?

- **Maps to:** Fast & slow pointers (cycle detection).
- **Model it:** Each clue→next is a linked list; detect whether it cycles.
- **Approach & variations:**
  - Send two hunters: one moves one clue per step, the other two clues per step.
  - If the fast one ever lands on the slow one, the clues loop; if it reaches a dead end, they don't.
  - Variation: to find **where** the loop starts, reset one hunter to the first clue and step both by one until they meet.
- **Time:** O(n) — the fast pointer catches up within one loop length.
- **Space:** O(1) — no visited list, just two walkers.

## 5. Binary search on the answer.

**Scenario:** A monkey faces several piles of bananas and has **H hours** before the zookeeper returns. It picks an eating speed and eats that many bananas per hour from a single pile (finishing early if a pile runs out). What is the **slowest speed** that still clears every pile in time?

- **Maps to:** Binary search on the answer.
- **Model it:** The unknown is a speed value in a range; feasibility (finishes in H hours?) is monotonic in speed.
- **Approach & variations:**
  - Speed lives in [1, biggest pile]. Higher speed is never worse, so 'fits in H hours' flips once.
  - For a guessed speed, add up hours needed (ceil of pile/speed) — an O(n) check.
  - Binary-search the smallest speed whose hours ≤ H.
  - Same shape as 'minimum ship capacity in D days' or 'split array to minimize largest sum'.
- **Time:** O(n · log(maxPile)) — an O(n) check run log(range) times.
- **Space:** O(1) — a few counters.

## 6. Breadth-first search (BFS) on an unweighted graph.

**Scenario:** A courier must cross a walled city from the front gate to the palace, moving only along open streets (some are blocked). What's the **fewest street-segments** in any route that gets there?

- **Maps to:** Breadth-first search (BFS) on an unweighted graph.
- **Model it:** The city is a grid/graph; find the shortest hop-count from source to target.
- **Approach & variations:**
  - BFS explores outward in rings of equal distance, so the target is first reached by a shortest route.
  - Use a queue; mark each cell visited when you enqueue it.
  - Variation: if streets had different travel costs you'd need Dijkstra; to recover the route, store where you came from.
- **Time:** O(V + E) — every reachable spot and connection is examined once.
- **Space:** O(V) — the visited set and the queue.

## 7. Flood fill via DFS/BFS (or Union-Find).

**Scenario:** A ranger looks down at a valley: patches of dry ground separated by water. Two dry cells belong to the same landmass if they touch edge-to-edge. **How many separate landmasses** are there?

- **Maps to:** Flood fill via DFS/BFS (or Union-Find).
- **Model it:** The map is a grid; count connected components of 'land' cells.
- **Approach & variations:**
  - Scan every cell; when you hit unvisited land, flood-fill its entire landmass and add one to the count.
  - Mark filled cells so each is counted once.
  - Variation: if land appears one cell at a time over the day, Union-Find handles the merges efficiently.
- **Time:** O(rows·cols) — each cell is touched a constant number of times.
- **Space:** O(rows·cols) — recursion/queue or a visited grid in the worst case.

## 8. Backtracking (depth-first search with undo).

**Scenario:** A photographer wants to seat 5 friends on a bench and try **every possible left-to-right ordering** for the shot. How does she generate all of them without missing or repeating any?

- **Maps to:** Backtracking (depth-first search with undo).
- **Model it:** You need all permutations of a set — explore a decision tree, choosing one unused person per seat.
- **Approach & variations:**
  - Fill seats left to right; at each seat try every friend not yet seated.
  - Recurse to the next seat, then **undo** the choice before trying the next friend.
  - Prune for constrained cousins: N-Queens skips attacked squares, 'combinations' forbids going backwards to avoid repeats.
- **Time:** O(n · n!) — n! orderings, O(n) to record each.
- **Space:** O(n) — the recursion depth / who's-seated marker.

## 9. 1-D dynamic programming (Fibonacci recurrence).

**Scenario:** A frog climbs a staircase of **n** steps, hopping either 1 or 2 steps at a time. In **how many distinct ways** can it reach the top?

- **Maps to:** 1-D dynamic programming (Fibonacci recurrence).
- **Model it:** Ways to reach step i = ways to reach i−1 plus ways to reach i−2.
- **Approach & variations:**
  - Each step's count is the sum of the previous two.
  - Build upward from the bottom (or memoize downward).
  - Only the last two counts matter → keep two variables for O(1) space.
  - Same engine as 'house robber' with a different transition rule.
- **Time:** O(n) — each step's count computed once.
- **Space:** O(1) with two rolling values (O(n) if you keep the whole table).

## 10. 2-D dynamic programming (edit distance).

**Scenario:** An autocorrect wants to turn one typed word into the intended word using the fewest single-letter fixes — each fix **adds**, **removes**, or **changes** one letter. What's the minimum number of fixes?

- **Maps to:** 2-D dynamic programming (edit distance).
- **Model it:** Compare prefixes of the two words; dp[i][j] = edits to align the first i and first j letters.
- **Approach & variations:**
  - If the current letters match, carry the diagonal value; otherwise 1 + min(add, remove, change).
  - Fill a grid of (len A + 1) × (len B + 1).
  - Variation: 'longest common subsequence' and sequence alignment use the same grid; you can compress it to two rows for O(min) space.
- **Time:** O(m·n) — one O(1) computation per grid cell.
- **Space:** O(m·n), reducible to O(min(m,n)) with rolling rows.

## 11. 0/1 Knapsack dynamic programming.

**Scenario:** A burglar's bag holds at most **W** kilograms. Each item in the house has a weight and a resale value, and there's only one of each. Which items maximize the total value carried out?

- **Maps to:** 0/1 Knapsack dynamic programming.
- **Model it:** Choose a subset of weighted/valued items under a capacity to maximize value; each item taken 0 or 1 times.
- **Approach & variations:**
  - dp[c] = best value achievable with capacity c; loop items on the outside, capacity on the inside.
  - Sweep capacity **downward** so each item is used at most once (sweeping upward allows reuse = unbounded knapsack).
  - Variation: 'can we hit exactly this total?' (subset-sum / equal partition) is the boolean version.
- **Time:** O(n·W) — pseudo-polynomial; scales with the numeric capacity.
- **Space:** O(W) — the 1-D rolling array.

## 12. Greedy — sort by finish time.

**Scenario:** A single tennis court gets many booking requests, each with a start and end time. The manager wants to accept **as many bookings as possible** with no overlaps. Which does he keep?

- **Maps to:** Greedy — sort by finish time.
- **Model it:** Intervals with start/end; pick the max set of mutually non-overlapping ones.
- **Approach & variations:**
  - Sort bookings by earliest end time; always keep the one that frees the court soonest.
  - Skip any booking that starts before the last kept one ends.
  - An exchange argument proves this greedy choice is optimal.
  - Variation: sort by **start** to merge busy periods, or use a min-heap to count simultaneous meetings/rooms.
- **Time:** O(n log n) — the sort dominates the linear scan.
- **Space:** O(1) beyond the sort (O(n) if the sort isn't in place).

## 13. Min-heap of size k (streaming top-K).

**Scenario:** Contestants stream onto a talent-show stage one after another, each with a score. At any moment the host must be ready to name the **top 3 scorers so far** — without re-sorting everyone each time.

- **Maps to:** Min-heap of size k (streaming top-K).
- **Model it:** Maintain the k largest of a stream; the heap's smallest element is the cutoff.
- **Approach & variations:**
  - Keep a min-heap holding the best 3; push each new score, and if the heap grows past 3, pop the smallest.
  - The root is the current 3rd place — the bar to beat.
  - Variation: 'k closest / k most frequent' just changes the key; needing only the exact k-th → Quickselect, O(n) average.
- **Time:** O(n log k) — n insertions, each O(log k).
- **Space:** O(k) — the heap holds only k items.

## 14. Union-Find (Disjoint Set Union).

**Scenario:** At a mixer, people introduce one another. If Ann knows Bo and Bo knows Cy, then all three count as one friend-circle. As introductions keep happening, **how many separate friend-circles** remain?

- **Maps to:** Union-Find (Disjoint Set Union).
- **Model it:** People are nodes, introductions are edges; count connected components as edges are added.
- **Approach & variations:**
  - Each introduction unions two people's groups; a find (with path compression) tells you a person's group leader.
  - Use union by size/rank to keep the trees shallow.
  - Circles remaining = number of distinct leaders; an introduction between people already in one circle changes nothing.
  - Union-Find beats re-running DFS because the introductions arrive incrementally.
- **Time:** O(E · α(n)) — near-constant (inverse-Ackermann) per operation.
- **Space:** O(n) — leader and rank arrays.

## 15. Topological sort (Kahn's BFS, or DFS post-order).

**Scenario:** A chef has many dishes, and some must be prepped before others (the sauce before the pasta, the dough before the pie). Find an **order to cook everything** so every prerequisite is done first — or report that the requirements form an impossible loop.

- **Maps to:** Topological sort (Kahn's BFS, or DFS post-order).
- **Model it:** Dishes are nodes, 'must come before' are directed edges; produce a linear order of a DAG.
- **Approach & variations:**
  - Kahn: repeatedly cook any dish with no unmet prerequisites, then remove it and relax the dishes waiting on it.
  - If you can't place every dish, a cycle exists → impossible.
  - DFS variant: emit dishes in finish order and reverse; revisiting an in-progress dish signals a cycle.
- **Time:** O(V + E) — each dish and dependency handled once.
- **Space:** O(V + E) — the dependency lists plus the queue/in-degree counts.

## 16. Monotonic (decreasing) stack.

**Scenario:** Every day a shopkeeper writes down the temperature. For each day she wants to know: **how many days until it gets warmer** than that day (0 if it never does)?

- **Maps to:** Monotonic (decreasing) stack.
- **Model it:** For each element, find the distance to the next strictly greater element on its right.
- **Approach & variations:**
  - Walk left to right keeping a stack of days still waiting for a warmer day (temperatures decreasing down the stack).
  - When today beats the day on top of the stack, pop it and record the day-gap — today is its answer.
  - Variation: 'next greater element', 'largest rectangle in a histogram', and 'trapping rain water' all lean on a monotonic stack.
- **Time:** O(n) — each day is pushed and popped at most once.
- **Space:** O(n) — the stack, when temperatures only fall.

## 17. Trie (prefix tree).

**Scenario:** A phone's contact search narrows the list the instant you type each new letter of a name. With thousands of contacts, how do you store them so **matching a typed prefix** is effectively instant?

- **Maps to:** Trie (prefix tree).
- **Model it:** Store strings so lookup cost depends on the query length, not how many strings you have.
- **Approach & variations:**
  - Each node holds one link per next letter plus an 'is a full name here' flag.
  - Typing walks one node per letter; the subtree under that node is every completion.
  - Variation: DFS from the prefix node for autocomplete suggestions; a wildcard '.' forces you to branch across children.
- **Time:** Build O(total letters); each prefix query O(L) for a length-L prefix.
- **Space:** O(total letters) — one node chain per shared prefix.

## 18. Dijkstra's algorithm (min-heap).

**Scenario:** A delivery driver wants the **cheapest-toll route** from the depot to every neighborhood. Roads connect neighborhoods and each road charges a different (never negative) toll.

- **Maps to:** Dijkstra's algorithm (min-heap).
- **Model it:** Weighted graph with non-negative edges; shortest-cost path from one source to all nodes.
- **Approach & variations:**
  - Always finalize the nearest not-yet-settled neighborhood, then relax its outgoing roads.
  - A min-heap keyed by cheapest-known cost hands you that next node.
  - Variation: negative tolls → Bellman-Ford; all tolls equal → plain BFS; want one target fast → A* with a heuristic.
- **Time:** O(E log V) — each road can trigger a heap update.
- **Space:** O(V) — best-cost array plus heap entries.

## 19. Prefix sums + a hash map of counts.

**Scenario:** A cashier logs the day's gains and losses in the order they happen. The manager asks: **how many continuous stretches of the day** netted exactly **$k** (gains and losses can both occur)?

- **Maps to:** Prefix sums + a hash map of counts.
- **Model it:** Count contiguous subarrays summing to k, where values may be negative.
- **Approach & variations:**
  - Track a running total; a stretch ending now nets k exactly when some earlier running total equalled (now − k).
  - Keep a map of how often each running total has appeared; add map[now − k] to the answer.
  - Because losses (negatives) break monotonicity, a sliding window won't work — the map is essential.
  - Seed the map with total 0 seen once, for stretches starting at the very beginning.
- **Time:** O(n) — one pass with O(1) map operations.
- **Space:** O(n) — up to n distinct running totals stored.

## 20. Sort by start, then sweep and merge.

**Scenario:** A shared calendar is full of overlapping busy blocks (10–11, 10:30–12, 14–15, …). Produce the **merged list of busy periods** so no two overlap.

- **Maps to:** Sort by start, then sweep and merge.
- **Model it:** Intervals that may overlap; collapse them into the minimal set of disjoint intervals.
- **Approach & variations:**
  - Sort blocks by start time.
  - Hold the current merged block; if the next starts at or before its end, stretch the end, else emit it and open a new one.
  - Variation: inserting one block into an already-sorted set skips the sort; 'free time across many calendars' merges with a heap.
- **Time:** O(n log n) — the sort dominates the single merge pass.
- **Space:** O(n) — the output list.

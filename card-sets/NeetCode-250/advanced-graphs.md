---
deck: "NeetCode 250::Advanced Graphs"
topic: "NeetCode 250 — Advanced Graphs"
tags: [ankicardmaker, neetcode250, advanced-graphs]
note_type: Basic
created: 2026-09-09
---

# NeetCode 250 — Advanced Graphs

Story front hides the technique; back reveals the mapping, approach, and complexity.

## 1. Path with Minimum Effort  ·  _Medium_

**Scenario:** A hiker crosses a grid of cells, each with an elevation, from the top-left to the bottom-right, stepping between adjacent cells. The strain of a route is its single biggest up-or-down elevation jump between consecutive cells. Find the route whose biggest jump is as small as possible, and report that smallest possible biggest-jump.

- **Maps to:** Minimax path via Dijkstra or binary search + connectivity (Path with Minimum Effort).
- **Model it:** Minimize the maximum edge weight (absolute height difference) along a path from corner to corner.
- **Approach & variations:**
  - Dijkstra-style: the cost of reaching a cell is the max jump so far; always expand the frontier cell with the smallest such max.
  - Alternatively binary-search the threshold and check with a flood fill whether corners connect using only jumps <= threshold.
  - Union-find over edges sorted by difference also works (add edges until corners join).
- **Time:** O(rows*cols*log(rows*cols)) — Dijkstra over grid cells with a heap.
- **Space:** O(rows*cols) — the cost grid and heap.

## 2. Network Delay Time  ·  _Medium_

**Scenario:** A signal is sent from one relay station and travels along one-way wires, each with a known travel time, to other stations. It fans out along all wires at once. How long until every station has received the signal — or report that some station can never be reached?

- **Maps to:** Single-source shortest paths (Network Delay Time / Dijkstra).
- **Model it:** Find the maximum over all nodes of the shortest-path distance from the source; infinity if any is unreachable.
- **Approach & variations:**
  - Run Dijkstra from the source to get each station's earliest arrival time.
  - The answer is the largest of those times; if any station stays unreached, return -1.
  - Bellman-Ford also works and handles the same directed weighted edges (needed if negatives existed).
- **Time:** O(E log V) — Dijkstra with a binary heap.
- **Space:** O(V + E) — adjacency plus distance array and heap.

## 3. Reconstruct Itinerary  ·  _Hard_

**Scenario:** You hold a stack of one-way plane tickets, each naming a departure and arrival airport. Starting from a fixed home airport, you must use every single ticket exactly once to form one continuous trip. Among all trips that use all tickets, produce the one that reads earliest alphabetically when the airport codes are listed in order.

- **Maps to:** Eulerian path with lexical greedy (Reconstruct Itinerary / Hierholzer).
- **Model it:** Find an Eulerian path using every directed edge once, choosing the lexicographically smallest sequence.
- **Approach & variations:**
  - Each ticket is a directed edge; you need a trail using all edges once starting at the home airport.
  - Hierholzer's algorithm: from each airport visit destinations in sorted (smallest-first) order, and append an airport to the route only after its outgoing tickets are exhausted.
  - Reverse the post-order stack to get the final itinerary.
- **Time:** O(E log E) — sorting destinations plus visiting each ticket once.
- **Space:** O(E) — adjacency lists and the route stack.

## 4. Min Cost to Connect All Points  ·  _Medium_

**Scenario:** Several houses sit at known map coordinates. You want to lay wire so every house is connected to every other (directly or through others). The cost of a direct wire between two houses is the walking-block distance between them. What is the least total wire cost to connect them all?

- **Maps to:** Minimum spanning tree (Min Cost to Connect All Points).
- **Model it:** On a complete graph with Manhattan-distance edge weights, find the minimum spanning tree's total weight.
- **Approach & variations:**
  - Prim's: grow a connected cluster, each step adding the cheapest wire from the cluster to a house outside it.
  - Kruskal's: sort all candidate wires by length and add each if it joins two separate groups (union-find), stopping at N-1 wires.
  - With N points, Prim's with a heap is natural since the graph is dense (all pairs).
- **Time:** O(N^2 log N) heap Prim's, or O(N^2) dense Prim's.
- **Space:** O(N) to O(N^2) — depending on whether edges are materialized.

## 5. Swim In Rising Water  ·  _Hard_

**Scenario:** A square pool is a grid where each cell has a wall height. Water level rises over time; at level t you may stand in any cell whose height is at most t, and you can instantly move between adjacent flooded cells. Starting top-left, wanting to reach bottom-right, what is the earliest level at which a continuous flooded route between the corners exists?

- **Maps to:** Minimax path via Dijkstra or binary search + flood fill (Swim in Rising Water).
- **Model it:** Minimize the maximum cell height along a path from corner to corner; that max is the earliest time.
- **Approach & variations:**
  - Dijkstra-style: expand the reachable cell with the smallest 'max height so far' until you pop the destination.
  - Or binary-search the level and flood-fill to test if corners connect using only cells <= level.
  - Kruskal union-find adding cells in height order until the corners join also gives the answer.
- **Time:** O(N^2 log N) — heap over the N^2 cells.
- **Space:** O(N^2) — visited/cost grid and heap.

## 6. Alien Dictionary  ·  _Hard_

**Scenario:** You are handed a list of words written in an unknown language, and you are told the list is already sorted by that language's own dictionary order. From that ordering alone, deduce the relative order of the language's letters. Output any full letter ordering consistent with the words, or report that the list contradicts itself.

- **Maps to:** Topological sort of inferred letter order (Alien Dictionary / Foreign Dictionary).
- **Model it:** Derive letter-precedence edges from adjacent word pairs, then topologically order the letters.
- **Approach & variations:**
  - For each adjacent word pair, the first differing letter gives an ordering edge earlier-letter -> later-letter.
  - Topologically sort the resulting letter graph (Kahn's or DFS) to get a valid alphabet.
  - A cycle means contradiction; also fail if a longer word precedes its own prefix.
  - Include all letters that appear, even those with no constraints.
- **Time:** O(total characters) — comparing pairs plus a topo sort over <=26 letters.
- **Space:** O(1) — bounded by the 26-letter graph (plus input).

## 7. Cheapest Flights Within K Stops  ·  _Medium_

**Scenario:** You want to travel from your home city to a destination city using one-way flights, each with a price. To keep it bearable you'll accept at most K intermediate stopovers along the way. What is the cheapest total fare for a trip from home to destination that uses no more than K stops, or is it not doable within that limit?

- **Maps to:** Bounded-hop shortest path (Cheapest Flights Within K Stops / Bellman-Ford).
- **Model it:** Find the minimum-cost path from source to destination using at most K+1 edges.
- **Approach & variations:**
  - Bellman-Ford relaxed exactly K+1 rounds, using a snapshot of distances each round so a single round can't chain multiple hops.
  - Alternatively BFS/Dijkstra tracking (city, stops-used) states, allowing revisits with fewer stops.
  - The stop limit is why plain Dijkstra alone can be wrong — cheaper-but-longer routes may be disallowed.
- **Time:** O(K * E) — K+1 relaxation rounds over all flights.
- **Space:** O(V) — distance arrays (current and previous round).

## 8. Find Critical and Pseudo Critical Edges in Minimum Spanning Tree  ·  _Hard_

**Scenario:** A town wants to connect all its buildings with the cheapest possible set of roads, each candidate road having a fixed cost. For each candidate road, classify it: 'critical' if leaving it out forces any cheapest connection plan to cost more (or become impossible), and 'important-but-optional' if it can appear in some cheapest plan but isn't forced. Report both groups.

- **Maps to:** MST edge criticality analysis (Find Critical and Pseudo-Critical Edges).
- **Model it:** Classify each edge relative to the minimum spanning tree cost: critical if excluding it raises the MST cost, pseudo-critical if it fits in some MST but isn't mandatory.
- **Approach & variations:**
  - Compute the baseline MST weight with Kruskal + union-find.
  - An edge is critical if excluding it makes the MST weight larger (or disconnected).
  - An edge is pseudo-critical if forcing it in (add it first, then Kruskal) still yields the baseline weight, but it isn't critical.
  - Index edges before sorting so you can report original positions.
- **Time:** O(E^2 * alpha) — re-run Kruskal per edge over sorted edges.
- **Space:** O(E + V) — edge list and union-find.

## 9. Build a Matrix With Conditions  ·  _Hard_

**Scenario:** You must arrange the numbers 1..k into a k-by-k grid so each number appears exactly once and the rest of the cells are blank. You're given two rule sets: one says certain numbers must sit in a higher row than certain others, the other says certain numbers must sit in a column further left than certain others. Produce any grid satisfying all rules, or report it's impossible.

- **Maps to:** Two independent topological sorts (Build a Matrix With Conditions).
- **Model it:** Order numbers vertically by the row constraints and horizontally by the column constraints via two separate topological sorts, then place each number at the intersection.
- **Approach & variations:**
  - Row conditions form a directed graph on numbers; topologically sort it to get each number's row index.
  - Column conditions likewise give a topological order for column indices.
  - If either sort hits a cycle, it's impossible; otherwise place value v at (rowRank[v], colRank[v]).
  - The two dimensions are independent, so solve them separately.
- **Time:** O(k + conditions) — two topo sorts over k nodes.
- **Space:** O(k + conditions) — two graphs plus the output grid (O(k^2)).

## 10. Greatest Common Divisor Traversal  ·  _Hard_

**Scenario:** A row of numbered tokens sits on a table. You may hop from one token to another only if the two share a common factor greater than one. Can you get from every token to every other token by some sequence of such hops?

- **Maps to:** Union-find via shared prime factors (Greatest Common Divisor Traversal).
- **Model it:** Tokens are connected if they share a prime factor; check whether the whole set forms one connected component.
- **Approach & variations:**
  - Linking every pair directly is too slow; instead union each number with its prime factors.
  - Two numbers sharing a prime end up in the same group through that prime's node.
  - After processing all numbers, everything is reachable iff all numbers belong to one group.
  - A value of 1 shares no prime, so any 1 present (with n>1) makes it impossible.
- **Time:** O(N * sqrt(maxVal)) or O(N log maxVal) with a smallest-prime sieve for factoring.
- **Space:** O(N + maxVal) — union-find over numbers and prime nodes.

---
deck: "NeetCode 250::Graphs"
topic: "NeetCode 250 — Graphs"
tags: [ankicardmaker, neetcode250, graphs]
note_type: Basic
created: 2026-09-09
---

# NeetCode 250 — Graphs

Story front hides the technique; back reveals the mapping, approach, and complexity.

## 1. Island Perimeter  ·  _Easy_

**Scenario:** A single blob of dry land sits in a shallow lake, drawn on graph paper by shading in some of the little squares. All the shaded squares touch edge-to-edge to form one connected patch with no inner ponds. You want to build a fence exactly along the waterline. How many unit fence segments do you need?

- **Maps to:** Grid scan counting exposed sides (Island Perimeter).
- **Model it:** Each filled cell in the matrix contributes to the boundary wherever it borders water or the grid edge.
- **Approach & variations:**
  - Every land cell has 4 sides; each side that faces water or off-grid is one fence segment.
  - Simplest: for each land cell add 4, then subtract 2 for every shared border with a land neighbor (counted once per pair, or subtract 1 per adjacent land side).
  - No search needed since the land is one connected blob with no lakes.
- **Time:** O(rows*cols) — one sweep over every cell.
- **Space:** O(1) — just a running total.

## 2. Verifying An Alien Dictionary  ·  _Easy_

**Scenario:** A visitor hands you an unusual alphabet where the letters run in some scrambled order you are told up front. She also gives you a list of words she claims are printed in dictionary order according to that strange alphabet. Reading down the list, is each word really no later than the one after it?

- **Maps to:** Custom-order comparison of adjacent words (Verifying an Alien Dictionary).
- **Model it:** Given a permutation of the alphabet, verify each consecutive pair of words is in lexicographic order under that ranking.
- **Approach & variations:**
  - Build a lookup from each letter to its rank in the given order.
  - Compare each neighboring pair character by character; the first differing letter decides order.
  - If words match up to the length of the shorter and the earlier word is longer, order is violated (prefix rule).
- **Time:** O(total characters) — each letter is inspected at most once across the comparisons.
- **Space:** O(1) — a fixed 26-slot rank table.

## 3. Find the Town Judge  ·  _Easy_

**Scenario:** In a village of N people, gossip says there is one special elder: everyone else trusts this elder, but the elder trusts no one. You are given a pile of slips each reading 'person A trusts person B'. Is there exactly one person who fits — trusted by all the other N-1 and trusting nobody — and if so, who?

- **Maps to:** In-degree/out-degree tally (Find the Town Judge).
- **Model it:** In a directed trust graph, find the node with in-degree N-1 and out-degree 0.
- **Approach & variations:**
  - Keep a score per person: +1 each time they are trusted, -1 each time they trust someone.
  - The judge is the unique person whose net score equals N-1.
  - Handle N=1 with no slips (that lone person is the judge).
- **Time:** O(N + E) — one pass over the trust slips plus a scan of people.
- **Space:** O(N) — one score per person.

## 4. Number of Islands  ·  _Medium_

**Scenario:** A satellite photo of the sea is laid out as a grid of squares, each either water or land. Land squares that touch side-to-side belong to the same landmass. Counting each connected chunk of land as one, how many separate islands appear in the photo?

- **Maps to:** Flood fill over a grid counting components (Number of Islands).
- **Model it:** Count connected components of land cells where adjacency is up/down/left/right.
- **Approach & variations:**
  - Scan cells; on an unvisited land cell, increment the count and flood-fill (DFS or BFS) all its connected land, marking visited.
  - Marking cells as water (or a visited set) prevents recounting.
  - Diagonal-touching would need 8-directional neighbors instead of 4.
- **Time:** O(rows*cols) — each cell is visited once.
- **Space:** O(rows*cols) worst case — recursion/queue depth for one giant island.

## 5. Max Area of Island  ·  _Medium_

**Scenario:** Same sea-photo grid of water and land squares, land touching side-to-side forming chunks. This time you don't want the number of islands — you want the size of the biggest single landmass, measured in squares. What is that largest area (0 if it's all water)?

- **Maps to:** Flood fill tracking component size (Max Area of Island).
- **Model it:** Find the maximum size among connected components of land cells with 4-directional adjacency.
- **Approach & variations:**
  - Scan cells; from each unvisited land cell, flood-fill and count the cells reached.
  - Track the running maximum of those counts.
  - Mark visited during the fill so each cell contributes to only one island's area.
- **Time:** O(rows*cols) — each cell is explored once.
- **Space:** O(rows*cols) worst case — recursion/queue for a single large island.

## 6. Clone Graph  ·  _Medium_

**Scenario:** You are shown a network of friendship circles: each person has a badge number and a list of the people they are directly linked to, and the links are mutual. Starting from one person you can reach everyone. Make a completely separate duplicate of the whole friendship network — brand-new people objects with the same numbers and the same web of links, sharing nothing with the original.

- **Maps to:** Traversal with an original-to-copy map (Clone Graph).
- **Model it:** Deep-copy a connected undirected graph, producing new nodes that mirror the neighbor structure.
- **Approach & variations:**
  - Walk the graph (DFS or BFS) from the start node.
  - Keep a map from each original node to its freshly made copy; create a copy the first time you see a node.
  - For each original, wire its copy's neighbor list to the copies of its neighbors, recursing/enqueuing unseen ones.
- **Time:** O(V + E) — every node and link is processed once.
- **Space:** O(V) — the map plus traversal frontier.

## 7. Walls And Gates  ·  _Medium_

**Scenario:** A dungeon map is a grid of rooms. Some rooms are solid rock you can't enter, some are magic gates, and the rest are empty. From an empty room you may step to an adjacent room (never through rock). For every empty room, fill in how many steps it is to the nearest gate — leave it marked unreachable if no gate can be reached.

- **Maps to:** Multi-source shortest path over a grid (Walls and Gates / Islands and Treasure).
- **Model it:** Compute each open cell's distance to the closest of several gate cells, moving 4-directionally around walls.
- **Approach & variations:**
  - Seed a queue with all gate cells at distance 0 (start from the treasures, not each empty room).
  - Expand outward level by level; the first time a room is reached records its shortest distance.
  - One combined sweep beats running a separate search from every empty room.
- **Time:** O(rows*cols) — each cell enters the frontier at most once.
- **Space:** O(rows*cols) — the frontier holds up to all cells.

## 8. Rotting Oranges  ·  _Medium_

**Scenario:** A crate is a grid of cells holding fresh fruit, rotten fruit, or empty gaps. Each minute, every rotten fruit spoils the fresh fruit directly beside it (up/down/left/right). How many minutes until no fresh fruit remains — and if some fresh fruit can never be reached, say it's impossible?

- **Maps to:** Multi-source level-by-level spread (Rotting Oranges).
- **Model it:** Simultaneous BFS from all initially rotten cells; the answer is the last level reached, contaminating fresh neighbors.
- **Approach & variations:**
  - Enqueue every rotten cell at time 0 and count fresh cells.
  - Process the frontier in waves; each wave is one minute, infecting fresh neighbors and decrementing the fresh count.
  - If fresh remain after the spread stops, return -1; else return the number of waves.
- **Time:** O(rows*cols) — each cell is enqueued at most once.
- **Space:** O(rows*cols) — the wave frontier.

## 9. Pacific Atlantic Water Flow  ·  _Medium_

**Scenario:** An island is a grid where each cell has a height. Rain on a cell flows to any equal-or-lower neighboring cell. The top and left borders drain into one ocean; the bottom and right borders drain into a second ocean. List every cell from which water can eventually reach BOTH oceans.

- **Maps to:** Reverse reachability from two borders (Pacific Atlantic Water Flow).
- **Model it:** Find cells that can reach both ocean sets, by exploring uphill from each ocean's border and intersecting.
- **Approach & variations:**
  - Instead of simulating flow from every cell, flood inward from each ocean's edges, stepping only to neighbors of equal or greater height.
  - Mark cells reachable from ocean one and, separately, from ocean two.
  - The answer is the cells marked by both floods.
- **Time:** O(rows*cols) — each cell is visited a constant number of times per ocean.
- **Space:** O(rows*cols) — two reachability marks plus frontiers.

## 10. Surrounded Regions  ·  _Medium_

**Scenario:** A board is a grid of X and O marks. An O belongs to a region of O's joined side-to-side. Any region that is completely walled in by X's — never touching the outer border — gets captured and flipped to X. Regions with at least one O on the border survive. Produce the board after all captures.

- **Maps to:** Border-anchored flood fill (Surrounded Regions).
- **Model it:** Flip every O not connected to a border O; the border-connected ones are safe.
- **Approach & variations:**
  - Flood-fill from every O sitting on the four edges, marking those O's (and their connected O's) as safe.
  - After marking, scan the board: unmarked O's are surrounded, so flip them to X; restore safe marks to O.
  - Working from the edges inward avoids mistakenly flipping open regions.
- **Time:** O(rows*cols) — each cell is examined a constant number of times.
- **Space:** O(rows*cols) worst case — flood-fill stack/queue.

## 11. Open The Lock  ·  _Medium_

**Scenario:** A padlock has four little wheels, each showing a digit 0-9 that you can nudge up or down one notch per move (9 wraps to 0). It starts at 0000 and you want it to read a target combination. But certain forbidden combinations jam the lock the instant they appear. What is the fewest single-notch moves to reach the target, or is it hopeless?

- **Maps to:** Shortest path over a state space (Open the Lock).
- **Model it:** Each 4-digit combo is a state; each move connects to 8 neighbors; find the shortest path from 0000 to target avoiding deadends.
- **Approach & variations:**
  - Treat combinations as nodes; from each, 8 moves (each wheel up or down) give neighbors.
  - BFS from 0000, skipping deadend states and already-visited ones, counting levels to the target.
  - Bidirectional BFS from both start and target speeds it up.
  - Check that 0000 itself isn't a deadend.
- **Time:** O(10^4 * 4) — bounded by all combinations times moves per state.
- **Space:** O(10^4) — visited set and frontier.

## 12. Course Schedule  ·  _Medium_

**Scenario:** A student wants to finish all N training modules. Some modules list prerequisites — 'you must complete module A before module B'. Given the full list of these before/after requirements, is it even possible to complete every module, or do the requirements loop back on themselves in a way that makes it impossible?

- **Maps to:** Cycle detection in a dependency graph (Course Schedule).
- **Model it:** Determine whether a directed graph of prerequisites is acyclic (a valid ordering exists).
- **Approach & variations:**
  - Model 'A before B' as a directed edge; a cycle means an unsatisfiable loop.
  - Peel off modules with no remaining prerequisites repeatedly (Kahn's method); if all get removed, it's possible.
  - Alternatively DFS with a recursion-stack mark to catch a back edge (cycle).
- **Time:** O(V + E) — each module and requirement processed once.
- **Space:** O(V + E) — adjacency plus in-degree/visited bookkeeping.

## 13. Course Schedule II  ·  _Medium_

**Scenario:** Same N training modules with 'do A before B' requirements, but now the student wants an actual to-do list: an order in which to take the modules so every prerequisite is satisfied before its dependent. Produce any valid order, or report that no order exists.

- **Maps to:** Topological ordering (Course Schedule II).
- **Model it:** Output a linear order of a directed acyclic graph, or empty if a cycle exists.
- **Approach & variations:**
  - Repeatedly take modules whose prerequisites are all done (in-degree zero), appending them to the order and freeing their dependents.
  - If you place all N, that's a valid order; if you stall early, a cycle blocked it — return empty.
  - A DFS post-order reversed also yields a topological order.
- **Time:** O(V + E) — each node and edge handled once.
- **Space:** O(V + E) — graph plus the output order and in-degree counts.

## 14. Graph Valid Tree  ·  _Medium_

**Scenario:** You have N employees numbered 0..N-1 and a list of direct-partnership pairs, where a partnership is mutual. For the company org to be a clean hierarchy chart, everyone must be reachable through partnerships from a single root, and there must be no redundant loops. Do these partnerships form exactly such a clean, loop-free, fully connected structure?

- **Maps to:** Connectivity + acyclicity check (Graph Valid Tree).
- **Model it:** Verify an undirected graph is fully connected and has no cycle (i.e., it is a tree).
- **Approach & variations:**
  - A tree on N nodes must have exactly N-1 edges — check this first as a quick filter.
  - Then confirm connectivity: a DFS/BFS from node 0 must reach all N, or union-find must merge all into one set without ever joining two already-linked nodes.
  - Edge count N-1 plus connected is equivalent to acyclic plus connected.
- **Time:** O(V + E) — traversal or near-linear union-find.
- **Space:** O(V + E) — adjacency plus visited/parent structures.

## 15. Course Schedule IV  ·  _Medium_

**Scenario:** Again N training modules with 'A must come before B' requirements. Now people ask yes/no questions like 'is module X a required forerunner of module Y — directly or through a chain of other modules?' Given many such queries, answer each one.

- **Maps to:** Transitive reachability / closure (Course Schedule IV).
- **Model it:** Precompute, for the prerequisite DAG, whether one node can reach another, then answer each query in O(1).
- **Approach & variations:**
  - Build reachability: for each node, the set of all modules reachable from it (its descendants).
  - Compute it via DFS/BFS from each node, or by a Floyd-Warshall-style closure over all triples.
  - Each query 'is X a prerequisite of Y' becomes 'is Y in X's reachable set'.
- **Time:** O(V*(V+E)) building reachability, then O(1) per query (or O(V^3) closure).
- **Space:** O(V^2) — the reachability table.

## 16. Number of Connected Components In An Undirected Graph  ·  _Medium_

**Scenario:** At a mixer there are N guests numbered 0..N-1 and a list of pairs who already know each other (acquaintance is mutual). People in the same knowing-circle can all be introduced around through mutual friends. How many separate social circles are there in the room?

- **Maps to:** Counting connected components (Number of Connected Components).
- **Model it:** Count connected components of an undirected graph given nodes and edges.
- **Approach & variations:**
  - Union-find: start with N singleton groups, union each acquaintance pair, count distinct roots at the end.
  - Or DFS/BFS: sweep nodes, and each time you start from an unvisited node, that's one new component; explore all it can reach.
  - Both approaches naturally handle isolated guests with no acquaintances.
- **Time:** O(V + E*alpha) union-find, or O(V + E) for DFS/BFS.
- **Space:** O(V) — parent array or visited set.

## 17. Redundant Connection  ·  _Medium_

**Scenario:** A network of N relay stations was originally wired into a clean single-loop-free layout where every station connects, using exactly N-1 cables. Then one extra cable was added, creating a single loop. You are given the cables in the order they were laid. Find the one added cable to remove so the layout is clean again — and if several qualify, name the last one laid.

- **Maps to:** Union-find cycle edge detection (Redundant Connection).
- **Model it:** In a graph that is a tree plus one edge, find the edge that closes the cycle (the last such in input order).
- **Approach & variations:**
  - Process cables in order, unioning the two endpoints.
  - The first cable whose two endpoints are already in the same group is the one closing the loop — return it.
  - Because you scan in order, that edge is the last-added redundant one by construction.
- **Time:** O(N*alpha) — near-linear union-find over the edges.
- **Space:** O(N) — parent/rank arrays.

## 18. Accounts Merge  ·  _Medium_

**Scenario:** A contact book has many entries, each a person's name followed by some email addresses. Two entries are the same real person if they share at least one email (names can repeat between different people, so names alone don't prove identity). Merge entries belonging to the same person, listing that person's name with all their emails sorted, and combine transitively — if A shares with B and B with C, all three are one.

- **Maps to:** Union-find over shared emails (Accounts Merge).
- **Model it:** Group accounts into connected components where an edge is a shared email, then collect each component's emails.
- **Approach & variations:**
  - Treat each email as a node; within one account, union all its emails together.
  - Track which name owns each email; after unioning, gather emails by their group root.
  - Sort each group's emails and prefix the owner's name; identical emails across accounts get merged automatically.
- **Time:** O(N*K*log(N*K)) — union-find over all emails plus sorting each group.
- **Space:** O(N*K) — maps from emails to groups and owners.

## 19. Evaluate Division  ·  _Medium_

**Scenario:** You know a set of exchange facts like 'one apple is worth 2 oranges' and 'one orange is worth 3 grapes'. Each fact runs both ways. Given queries such as 'how many grapes is an apple worth?', compute the value by chaining facts — and if two items have no chain connecting them, say it's unknown.

- **Maps to:** Weighted-graph path product (Evaluate Division).
- **Model it:** Build a graph where edge a->b carries ratio a/b; a query is the product of ratios along a path from one variable to another.
- **Approach & variations:**
  - Each equation a/b = k gives edges a->b (k) and b->a (1/k).
  - For each query, DFS/BFS from the numerator to the denominator, multiplying edge ratios along the way.
  - Return the accumulated product if reached, -1 if either variable is unknown or no path exists.
  - Union-find with weights, or precomputed all-pairs, also works.
- **Time:** O(Q*(V+E)) — a traversal per query.
- **Space:** O(V + E) — the ratio graph plus recursion/visited.

## 20. Minimum Height Trees  ·  _Medium_

**Scenario:** A camp has N tents connected by exactly N-1 footpaths so everyone is reachable and there are no loops. You want to place the central campfire at a tent so the walk to the farthest tent is as short as possible. Which tent (or the one or two tents) minimize that worst-case walking distance?

- **Maps to:** Iterative leaf-trimming to find graph centroid(s) (Minimum Height Trees).
- **Model it:** Find the center(s) of a tree — the roots minimizing height — which are 1 or 2 central nodes.
- **Approach & variations:**
  - Trying every tent as root is too slow; instead peel from the outside in.
  - Repeatedly remove all current leaves (degree-1 tents) layer by layer.
  - The last 1 or 2 tents remaining are the centers — the optimal campfire spots.
  - Handle N=1 and N=2 as small special cases.
- **Time:** O(V + E) — each node and edge is removed once.
- **Space:** O(V + E) — adjacency and degree counts.

## 21. Word Ladder  ·  _Hard_

**Scenario:** You start with one code word and want to reach a target code word by changing a single letter at a time, where every intermediate word must be a real word from an approved list. Same length throughout. What is the fewest number of words in the shortest such chain (counting both ends), or is it impossible?

- **Maps to:** Shortest transformation via BFS (Word Ladder).
- **Model it:** Words are nodes, one-letter differences are edges; find shortest path length from begin to end word.
- **Approach & variations:**
  - BFS level by level from the start word; the first time you reach the target gives the shortest chain length.
  - Generate neighbors by trying every letter in every position and keeping those in the word set.
  - Using wildcard patterns (e.g., h*t) as buckets speeds neighbor lookup.
  - Bidirectional BFS from both ends cuts the explored breadth.
- **Time:** O(N * L^2) — N words, each generating L positions * 26 candidates with O(L) work.
- **Space:** O(N * L) — the word set and frontier.

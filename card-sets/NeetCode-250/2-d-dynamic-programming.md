---
deck: "NeetCode 250::2-D Dynamic Programming"
topic: "NeetCode 250 — 2-D Dynamic Programming"
tags: [ankicardmaker, neetcode250, 2-d-dynamic-programming]
note_type: Basic
created: 2026-09-09
---

# NeetCode 250 — 2-D Dynamic Programming

Story front hides the technique; back reveals the mapping, approach, and complexity.

## 1. Unique Paths  ·  _Medium_

**Scenario:** A beetle starts at the top-left corner of a rectangular garden grid and wants to reach the bottom-right corner, only ever crawling one plot to the right or one plot down. How many distinct routes can it take?

- **Maps to:** 2-D grid DP counting paths (Unique Paths).
- **Model it:** Routes to a cell = routes to the cell above plus routes to the cell on the left.
- **Approach & variations:**
  - Each interior cell's count is the sum of the cell above and the cell to its left.
  - Top row and left column each have exactly one route.
  - Sweep row by row; one rolling row of counts suffices.
  - Closed form is the binomial C(m+n-2, m-1).
- **Time:** O(m*n) — one addition per cell.
- **Space:** O(n) — a single rolling row (or O(1) with the formula).

## 2. Unique Paths II  ·  _Medium_

**Scenario:** A beetle crosses a rectangular garden from top-left to bottom-right, moving only right or down, but some plots are flooded and impassable. How many distinct dry routes reach the far corner?

- **Maps to:** 2-D grid DP with blocked cells (Unique Paths II).
- **Model it:** Path count to a cell = above + left, but any blocked cell holds zero routes.
- **Approach & variations:**
  - Same additive recurrence as the open grid, but set blocked cells to 0.
  - If the start or end plot is flooded, the answer is 0.
  - Propagate the top row and left column, stopping counts at any block.
  - One rolling row keeps it space-light.
- **Time:** O(m*n) — one check and add per cell.
- **Space:** O(n) — a rolling row of counts.

## 3. Minimum Path Sum  ·  _Medium_

**Scenario:** A traveler crosses a rectangular field of tollbooths from top-left to bottom-right, paying the posted toll on every plot she steps on, and may only move right or down. What is the least total toll for the whole crossing?

- **Maps to:** 2-D grid DP minimizing accumulated cost (Minimum Path Sum).
- **Model it:** Cheapest cost to a cell = its toll plus the smaller of the cell above or the cell to the left.
- **Approach & variations:**
  - best[cell] = toll[cell] + min(best above, best left).
  - First row and column accumulate along their single approach direction.
  - Sweep row by row; a rolling row holds the previous row's bests.
  - Answer is the bottom-right accumulated cost.
- **Time:** O(m*n) — constant work per cell.
- **Space:** O(n) — one rolling row of costs.

## 4. Longest Common Subsequence  ·  _Medium_

**Scenario:** Two friends each wrote down their playlist as an ordered list of songs. Keeping each list in its own order but allowed to skip songs, they want the longest sequence of songs that appears in both lists in the same relative order. How long is it?

- **Maps to:** 2-D DP over two-string alignment (Longest Common Subsequence).
- **Model it:** LCS length of prefixes = if last songs match, 1 + LCS of both shorter; else max of dropping one from either.
- **Approach & variations:**
  - Grid indexed by prefixes of each list.
  - On a match, extend the diagonal by one; on a mismatch, take the better of up or left.
  - Order is preserved but gaps are allowed, unlike a contiguous substring.
  - Two rolling rows cut the space.
- **Time:** O(m*n) — every prefix pair filled once.
- **Space:** O(min(m,n)) — two rolling rows.

## 5. Last Stone Weight II  ·  _Medium_

**Scenario:** A quarry worker repeatedly smashes two stones together; if unequal, the lighter is destroyed and the heavier keeps the weight difference, and this continues until at most one stone remains. Choosing the smashes cleverly, what is the smallest possible final weight?

- **Maps to:** Subset-sum partition minimizing difference (Last Stone Weight II).
- **Model it:** Assigning each stone a plus or minus sign, minimize the absolute total — i.e. split into two heaps with the closest sums.
- **Approach & variations:**
  - Every sequence of smashes is equivalent to a +/- sign on each stone.
  - Minimize |sum of one heap - sum of the other|, so make one heap as close to total/2 as possible.
  - Boolean subset-sum finds the largest reachable sum <= total/2.
  - Answer is total - 2 * that best reachable sum.
- **Time:** O(n * sum) — subset-sum over stones and half-total.
- **Space:** O(sum) — a reachable-sums row.

## 6. Best Time to Buy And Sell Stock With Cooldown  ·  _Medium_

**Scenario:** A trader watches a token's daily price and may buy and later sell for profit any number of times, but only ever holds one unit at a time, and after any sale must rest a full day before buying again. What is the maximum total profit?

- **Maps to:** State-machine DP over hold/sold/rest (Best Time to Buy and Sell Stock with Cooldown).
- **Model it:** Track three daily states — holding, just-sold, and idle — with the cooldown blocking a buy the day after a sale.
- **Approach & variations:**
  - hold = max(stay holding, buy today from idle-yesterday).
  - sold = holding-yesterday + today's price.
  - rest = max(rest-yesterday, sold-yesterday), and only rest may buy next.
  - Answer is the best of sold and rest on the final day.
- **Time:** O(n) — three state updates per day.
- **Space:** O(1) — three rolling values.

## 7. Coin Change II  ·  _Medium_

**Scenario:** A cashier has unlimited coins in a few fixed denominations and wants to count how many distinct combinations of coins add up to an exact amount — where order does not matter, so two nickels then a dime is the same combination as a dime then two nickels. How many combinations are there?

- **Maps to:** Unbounded-knapsack combination counting (Coin Change II).
- **Model it:** Count unordered multisets of reusable coins summing to the amount.
- **Approach & variations:**
  - ways[amount] accumulates combinations; ways[0] = 1.
  - Loop denominations on the OUTSIDE, then amounts inward, so each coin type is fixed once.
  - That outer-coin ordering prevents counting the same set in different orders.
  - Coins are reusable, so add ways[amount - coin].
- **Time:** O(amount * coins) — each coin sweeps all amounts.
- **Space:** O(amount) — one count per sub-amount.

## 8. Target Sum  ·  _Medium_

**Scenario:** A child has a row of numbered cards and must place either a plus or a minus in front of every card, then add them all up. In how many distinct ways can the signs be chosen so the running total equals a given target?

- **Maps to:** Subset-sum reduction counting assignments (Target Sum).
- **Model it:** Choosing + or - per number to hit target reduces to: how many subsets sum to (total+target)/2.
- **Approach & variations:**
  - Let P be the plus-group sum; then P - (total-P) = target, so P = (total+target)/2.
  - If that value is non-integer or out of range, there are zero ways.
  - Count subsets summing to P with a 1-D DP over reachable sums.
  - Each number either joins P or not — a 0/1 knapsack count.
- **Time:** O(n * sum) — subset-sum counting over numbers and target sum.
- **Space:** O(sum) — a count row over reachable sums.

## 9. Interleaving String  ·  _Medium_

**Scenario:** Two dealers each hold their own ordered deck. A third deck is laid out, and you must decide whether it could have been produced by shuffling the two decks together — keeping each dealer's cards in their original order, but freely alternating whose card comes next. Could the third deck be such a merge?

- **Maps to:** 2-D DP over two-pointer interleave reachability (Interleaving String).
- **Model it:** Can prefixes of length i and j of the two sources be interleaved to form the first i+j of the target?
- **Approach & variations:**
  - ok[i][j] true if the target's next char matches source A's i-th (from ok[i-1][j]) or B's j-th (from ok[i][j-1]).
  - Total lengths must add up, else immediately false.
  - Fill a grid indexed by how many cards taken from each source.
  - One rolling row reduces space.
- **Time:** O(m*n) — every prefix pair evaluated once.
- **Space:** O(n) — a rolling row of booleans.

## 10. Stone Game  ·  _Medium_

**Scenario:** Two players face a row of an even number of treasure chests, each with a known value totaling an odd sum. They alternate turns, each turn taking a chest from either the far-left or far-right end. Both play optimally to maximize their own haul. Can the first player always guarantee a win?

- **Maps to:** Interval game DP on score difference (Stone Game).
- **Model it:** On range [i,j] the mover maximizes value taken minus the opponent's optimal result on the smaller range.
- **Approach & variations:**
  - best[i][j] = max(chest[i] - best[i+1][j], chest[j] - best[i][j-1]).
  - The value is the mover's lead; a positive best[0][n-1] means first player wins.
  - Fill by increasing interval length.
  - With an even count and odd total, the first player can in fact always force a win.
- **Time:** O(n^2) — every subinterval evaluated once.
- **Space:** O(n^2) — the interval table (reducible).

## 11. Stone Game II  ·  _Medium_

**Scenario:** Two players face a row of chest-piles, taking turns from the left end only. A running limit M starts at 1; on a turn a player must take between 1 and 2M piles from the front, and then M grows to the larger of itself and the number just taken. Both maximize their own total. What is the most the first player can secure?

- **Maps to:** Suffix-interval DP keyed on the take-limit M (Stone Game II).
- **Model it:** State is (start index, current M); the mover maximizes suffix-sum-taken minus the opponent's best from the new position and M.
- **Approach & variations:**
  - best[i][M] = max over x in 1..2M of (sum of piles i..i+x-1) + (suffixSum(i+x) - best[i+x][max(M,x)]).
  - Use suffix sums so a chosen chunk's value is O(1).
  - Fill from the end backward across all M values.
  - Answer is best[0][1].
- **Time:** O(n^3) — states (i,M) each scanning up to 2M takes.
- **Space:** O(n^2) — the (index, M) table.

## 12. Longest Increasing Path In a Matrix  ·  _Hard_

**Scenario:** A hiker crosses a field of plots each marked with an elevation and may step to an adjacent plot (up, down, left, or right) only if it is strictly higher. Starting wherever she likes, what is the greatest number of plots in a single ever-climbing walk?

- **Maps to:** Memoized DFS on a DAG of increasing moves (Longest Increasing Path in a Matrix).
- **Model it:** Longest strictly increasing path where each cell's value = 1 + max over higher neighbors.
- **Approach & variations:**
  - From each cell, the longest climb = 1 + max longest climb among strictly higher neighbors.
  - Strictly increasing edges make the graph acyclic, so memoize each cell's answer.
  - DFS with a cache (or topological order by height) avoids recomputation.
  - Global answer is the max cached value.
- **Time:** O(m*n) — each cell computed once, four neighbors each.
- **Space:** O(m*n) — the memo cache and recursion.

## 13. Distinct Subsequences  ·  _Hard_

**Scenario:** A proofreader has a long passage and a short target word. She wants to know: in how many distinct ways can she cross out some letters of the passage — keeping the rest in order — so that exactly the target word remains?

- **Maps to:** 2-D DP counting subsequence embeddings (Distinct Subsequences).
- **Model it:** Count how many subsequences of the source string equal the target string.
- **Approach & variations:**
  - ways[i][j] = ways for source prefix i to form target prefix j.
  - If letters match: ways = use-it (ways[i-1][j-1]) + skip-it (ways[i-1][j]); else just skip-it.
  - Empty target has exactly one way (delete everything).
  - A rolling row over the source cuts space.
- **Time:** O(m*n) — every prefix pair filled once.
- **Space:** O(n) — a rolling row over the target length.

## 14. Edit Distance  ·  _Medium_

**Scenario:** An editor must transform one word into another using the fewest single-letter operations, where each operation is inserting a letter, deleting a letter, or replacing one letter with another. What is the minimum number of operations?

- **Maps to:** 2-D DP over two-string alignment cost (Edit Distance / Levenshtein).
- **Model it:** Min edits between prefixes = 0 extra if last letters match, else 1 + min(insert, delete, replace).
- **Approach & variations:**
  - cost[i][j] compares prefix i of word A with prefix j of word B.
  - Matching last letters carry the diagonal cost; otherwise 1 + min(left, up, diagonal).
  - Left = delete, up = insert, diagonal = replace.
  - Base rows/columns count turning a prefix into empty (all deletes/inserts).
- **Time:** O(m*n) — every prefix pair evaluated once.
- **Space:** O(n) — two rolling rows.

## 15. Burst Balloons  ·  _Hard_

**Scenario:** A child has a row of numbered balloons and pops them one at a time. Popping a balloon earns its number times the numbers of its immediate left and right still-present neighbors (missing ends count as one), then the row closes up. In what order should she pop to earn the most coins overall?

- **Maps to:** Interval DP choosing the last balloon to pop (Burst Balloons).
- **Model it:** For a range, pick which balloon is popped LAST; its neighbors are then the fixed range boundaries.
- **Approach & variations:**
  - Pad both ends with virtual 1s.
  - best[l][r] = max over k in (l,r) of nums[l]*nums[k]*nums[r] + best[l][k] + best[k][r], treating k as the last pop.
  - Choosing the last pop fixes its neighbors as the boundaries, decoupling the subranges.
  - Fill by increasing interval width.
- **Time:** O(n^3) — every interval tries every last-pop.
- **Space:** O(n^2) — the interval table.

## 16. Regular Expression Matching  ·  _Hard_

**Scenario:** A gatekeeper checks names against a pattern that may include two wildcards: a single dot that matches any one character, and a star that means the character just before it may repeat zero or more times. Does a given name match the pattern in full?

- **Maps to:** 2-D DP over string-vs-pattern matching (Regular Expression Matching).
- **Model it:** match[i][j] = can the first i characters be matched by the first j pattern tokens, handling '.' and 'x*'.
- **Approach & variations:**
  - A dot matches any single character; a plain letter matches itself.
  - For 'x*', either skip it (zero copies) or, if the char before star matches the current letter, consume one and stay on the star.
  - Fill a grid indexed by prefixes of name and pattern.
  - Seed the empty-name row for patterns that can vanish via stars.
- **Time:** O(m*n) — every (name-prefix, pattern-prefix) pair evaluated.
- **Space:** O(m*n) — the match grid (reducible to a rolling row).

---
deck: "NeetCode 250::1-D Dynamic Programming"
topic: "NeetCode 250 — 1-D Dynamic Programming"
tags: [ankicardmaker, neetcode250, 1-d-dynamic-programming]
note_type: Basic
created: 2026-09-09
---

# NeetCode 250 — 1-D Dynamic Programming

Story front hides the technique; back reveals the mapping, approach, and complexity.

## 1. Climbing Stairs  ·  _Easy_

**Scenario:** A frog hops up a flight of steps, and each hop covers either one step or two. In how many distinct ways can it reach the very top of a staircase that is N steps tall?

- **Maps to:** Bottom-up counting with two rolling values (Climbing Stairs).
- **Model it:** Ways to reach step n = ways to reach n-1 plus ways to reach n-2, the Fibonacci recurrence.
- **Approach & variations:**
  - Each step is reachable from one-below or two-below, so add those two counts.
  - Seed with 1 way to stand at the bottom and 1 way to reach step one.
  - Keep only the last two totals and roll them forward — no full table needed.
  - This is literally the Fibonacci sequence in disguise.
- **Time:** O(n) — one pass computing each step's count once.
- **Space:** O(1) — two rolling counters.

## 2. Min Cost Climbing Stairs  ·  _Easy_

**Scenario:** A hiker climbs a staircase where standing on each step costs a posted toll, and from a step she may stride up one or two steps. She may start from either of the first two steps. What is the cheapest total toll to step past the top?

- **Maps to:** 1-D DP over minimum accumulated cost (Min Cost Climbing Stairs).
- **Model it:** Min cost to reach a step = its own toll plus the cheaper of arriving from one or two steps below.
- **Approach & variations:**
  - Cost to reach step i = toll[i] + min(reach i-1, reach i-2).
  - The goal sits just beyond the last step, so answer = min(reach last, reach second-to-last).
  - Start values are the first two tolls since either is a legal launch point.
  - Roll two variables forward instead of storing every step.
- **Time:** O(n) — each step's best arrival cost computed once.
- **Space:** O(1) — two rolling values.

## 3. N-th Tribonacci Number  ·  _Easy_

**Scenario:** A colony of rabbits grows so that each month's newborn count equals the sum of the newborns from the previous three months. Starting from 0, then 1, then 1, what is the count in month N?

- **Maps to:** Rolling 1-D recurrence over three predecessors (N-th Tribonacci Number).
- **Model it:** T(n) = T(n-1) + T(n-2) + T(n-3) with seeds 0, 1, 1.
- **Approach & variations:**
  - Like Fibonacci but summing the previous three terms instead of two.
  - Handle the tiny base cases (0, 1, 2) directly.
  - Slide a window of three values forward, one addition per month.
  - No table required — three variables suffice.
- **Time:** O(n) — one addition per term up to n.
- **Space:** O(1) — three rolling values.

## 4. House Robber  ·  _Medium_

**Scenario:** A cat burglar walks down a single row of houses, each stashing a known amount of loot, but any two houses next door to each other share an alarm that trips if both are hit. Choosing carefully, what is the most loot he can carry off?

- **Maps to:** 1-D DP with take/skip choice (House Robber).
- **Model it:** Best loot through house i = max of skipping it, or taking it plus the best through i-2.
- **Approach & variations:**
  - At each house choose max(skip = best so far, rob = this house + best two back).
  - Track two rolling bests: including the previous house and excluding it.
  - No two adjacent picks allowed, which forces the i-2 gap.
  - Answer is the better of the two rolling values at the end.
- **Time:** O(n) — one decision per house.
- **Space:** O(1) — two rolling bests.

## 5. House Robber II  ·  _Medium_

**Scenario:** A cat burglar faces houses arranged in a closed ring, each holding loot, where neighbors share an alarm — and because the ring wraps, the first and last houses are also neighbors. What is the most loot he can grab without triggering two adjacent alarms?

- **Maps to:** Linear take/skip DP run twice for the circular constraint (House Robber II).
- **Model it:** A circle means first and last conflict, so solve two lines: houses[0..n-2] and houses[1..n-1], take the max.
- **Approach & variations:**
  - Because the ends touch, you can never rob both the first and last house.
  - Run the ordinary line-robbery on the row minus the last house, then on the row minus the first.
  - Answer is the larger of the two runs.
  - Guard the single-house case where both ranges would be empty.
- **Time:** O(n) — two linear passes.
- **Space:** O(1) — rolling values per pass.

## 6. Longest Palindromic Substring  ·  _Medium_

**Scenario:** A jeweler has a long strand of colored beads and wants to cut out the single longest continuous run that reads identically forward and backward. Which stretch of beads is it?

- **Maps to:** Expand-around-center over each position (Longest Palindromic Substring).
- **Model it:** Find the longest contiguous slice of the string that is a mirror image of itself.
- **Approach & variations:**
  - Treat every bead (and every gap between two beads) as a possible mirror center.
  - Grow outward from each center while the two sides match, tracking the widest.
  - Handle odd-length (single center) and even-length (two-bead center) cases.
  - A DP table over all pairs also works but expand-around-center is simpler at O(1) space.
- **Time:** O(n^2) — n centers, each expanding up to n.
- **Space:** O(1) — just track the best start and length.

## 7. Palindromic Substrings  ·  _Medium_

**Scenario:** A jeweler examines a strand of colored beads and wants to tally every continuous run — of any length, including single beads — that reads the same in both directions. How many such runs are there in total?

- **Maps to:** Expand-around-center counting (Palindromic Substrings).
- **Model it:** Count all contiguous slices of the string that are mirror images of themselves.
- **Approach & variations:**
  - For each possible center, expand outward and increment the count on every matching pair.
  - Use both single-bead centers and between-bead centers.
  - Every successful expansion is one more valid run to add.
  - Single beads always count, giving at least n.
- **Time:** O(n^2) — n centers, each expanding up to n.
- **Space:** O(1) — a running counter.

## 8. Decode Ways  ·  _Medium_

**Scenario:** A courier receives a message written only as digits, where 1 through 26 each stand for a letter of the alphabet. Reading left to right, digits can be grouped one or two at a time into letters. In how many distinct ways can the whole string of digits be turned back into letters?

- **Maps to:** 1-D DP over decode counts with validity checks (Decode Ways).
- **Model it:** Ways to decode up to position i = ways using a valid single digit plus ways using a valid two-digit pair.
- **Approach & variations:**
  - ways[i] += ways[i-1] if the single digit is 1-9 (not a leading zero).
  - ways[i] += ways[i-2] if the two-digit pair is 10-26.
  - A lone zero that cannot pair is a dead end (zero ways).
  - Roll two counters forward; seed one way for the empty prefix.
- **Time:** O(n) — constant work per digit.
- **Space:** O(1) — two rolling counters.

## 9. Coin Change  ·  _Medium_

**Scenario:** A cashier has unlimited coins in a few fixed denominations and must pay out an exact amount using as few coins as possible. What is the fewest coins that make the amount, or is it impossible?

- **Maps to:** Unbounded-knapsack 1-D DP minimizing count (Coin Change).
- **Model it:** Fewest coins for amount a = 1 + min over denominations d of fewest coins for a-d.
- **Approach & variations:**
  - Build up best[0..amount]; best[0] = 0 coins.
  - For each amount, try every denomination and take 1 + best[amount - d].
  - Coins are reusable, so iterate amounts outward allowing repeats.
  - If no combination reaches the amount, report impossible (infinity sentinel).
- **Time:** O(amount * coins) — every amount tries every denomination.
- **Space:** O(amount) — one entry per sub-amount.

## 10. Maximum Product Subarray  ·  _Medium_

**Scenario:** A gambler walks past a row of betting tables, each multiplying his stake by a posted factor (some less than one, some negative, flipping his fortune). He must play a single unbroken run of consecutive tables. Which run multiplies his money the most?

- **Maps to:** Rolling max/min product tracking sign flips (Maximum Product Subarray).
- **Model it:** Find the contiguous slice whose product of values is largest, where negatives can flip a min into a max.
- **Approach & variations:**
  - Track both the largest and smallest running product ending here.
  - A negative factor swaps the roles of current max and min, so keep both.
  - At each table take max(value, value*prevMax, value*prevMin).
  - Update a global best each step; zeros reset the run.
- **Time:** O(n) — one pass maintaining two products.
- **Space:** O(1) — running max, min, and best.

## 11. Word Break  ·  _Medium_

**Scenario:** A scribe finds a long banner of letters with every space removed, and a dictionary of allowed words. Can the unbroken banner be sliced into a sequence of dictionary words with nothing left over?

- **Maps to:** 1-D DP over reachable break points (Word Break).
- **Model it:** Position i is reachable if some dictionary word ends exactly at i and its start was already reachable.
- **Approach & variations:**
  - breakable[i] is true if a valid word fills [j, i) and breakable[j] is true.
  - Sweep positions left to right, checking each dictionary word as a suffix.
  - Store dictionary words in a set for O(1) membership.
  - Answer is whether the end of the banner is reachable.
- **Time:** O(n^2 * L) — each cut point tests each earlier point and word length.
- **Space:** O(n) — reachability flags (plus the word set).

## 12. Longest Increasing Subsequence  ·  _Medium_

**Scenario:** A collector lines up figurines in the order she bought them, each with a height. She wants to keep the longest possible run, in that same left-to-right order (not necessarily neighbors), whose heights strictly increase. How long is that run?

- **Maps to:** Patience-sorting / binary-search DP (Longest Increasing Subsequence).
- **Model it:** Find the longest strictly increasing subsequence (order preserved, gaps allowed) of the height list.
- **Approach & variations:**
  - O(n^2): best[i] = 1 + max best[j] for earlier shorter figurines.
  - O(n log n): keep tails of increasing piles, binary-search each height into place.
  - Replace the first tail >= current height, or append if it beats all.
  - The number of piles equals the longest run's length.
- **Time:** O(n log n) — a binary search per figurine (or O(n^2) naive).
- **Space:** O(n) — the piles/tails array.

## 13. Partition Equal Subset Sum  ·  _Medium_

**Scenario:** Two siblings inherit a pile of gold bars of various weights and want to split them into two heaps of exactly equal total weight, each bar going wholly into one heap. Is a perfectly even split possible?

- **Maps to:** Subset-sum 0/1 knapsack on a boolean 1-D DP (Partition Equal Subset Sum).
- **Model it:** A fair split exists iff some subset of bars sums to exactly half the total weight.
- **Approach & variations:**
  - If the total is odd, an even split is impossible immediately.
  - Target is total/2; ask whether some subset reaches it.
  - Boolean DP: reachable[s] true if sum s is achievable; each bar used at most once.
  - Iterate sums downward per bar to avoid reusing it.
- **Time:** O(n * sum) — each bar sweeps the reachable sums.
- **Space:** O(sum) — a boolean row over half-total sums.

## 14. Combination Sum IV  ·  _Medium_

**Scenario:** A drummer wants to fill exactly N beats using notes of a few fixed durations, drawing each duration as often as he likes. Because order matters — a short-then-long pattern differs from long-then-short — how many distinct ordered sequences fill the N beats exactly?

- **Maps to:** Ordered-count unbounded DP (Combination Sum IV).
- **Model it:** Number of ordered sequences summing to target = sum over durations d of sequences summing to target-d.
- **Approach & variations:**
  - ways[t] = sum of ways[t - d] over every duration d.
  - Loop targets on the outside so different orders are counted separately.
  - Seed ways[0] = 1 (the empty sequence).
  - This counts permutations, unlike the classic combination-sum which counts sets.
- **Time:** O(target * durations) — each target tries each duration.
- **Space:** O(target) — one count per beat total.

## 15. Perfect Squares  ·  _Medium_

**Scenario:** A tiler must cover a strip of exactly N units using square tiles whose side lengths are whole numbers (so tiles cover 1, 4, 9, 16, ... units), with unlimited tiles of each size. What is the fewest tiles that sum to exactly N?

- **Maps to:** Unbounded-knapsack 1-D DP minimizing count (Perfect Squares).
- **Model it:** Fewest squares summing to n = 1 + min over squares s<=n of fewest squares for n-s.
- **Approach & variations:**
  - best[i] = 1 + min best[i - k*k] over all squares k*k <= i.
  - Squares are reusable, so this is an unbounded coin-change with square denominations.
  - Seed best[0] = 0.
  - Lagrange guarantees the answer is at most 4, but DP finds the exact minimum.
- **Time:** O(n * sqrt(n)) — each total tries every square up to it.
- **Space:** O(n) — one entry per total.

## 16. Integer Break  ·  _Medium_

**Scenario:** A farmer has a rope of whole length N and must cut it into at least two whole-length pieces, then multiply all the piece lengths together. How should he cut it so that product is as large as possible?

- **Maps to:** 1-D DP (or math) over max product of a partition (Integer Break).
- **Model it:** Best product for n = max over first cut i of i*(n-i) or i*best(n-i), requiring at least one cut.
- **Approach & variations:**
  - DP: best[n] = max over i in 1..n-1 of max(i*(n-i), i*best[n-i]).
  - The inner max chooses whether to cut the remainder further.
  - Greedy insight: break into as many 3s as possible, using 2s for the remainder.
  - Force at least one cut so n itself is not the answer.
- **Time:** O(n^2) DP — each length tries each first cut (O(n) greedy).
- **Space:** O(n) — the product table (O(1) greedy).

## 17. Stone Game III  ·  _Hard_

**Scenario:** Two rivals take turns at a row of treasure chests, each holding a known (possibly negative) value, always taking from the left end. On a turn a player scoops the next one, two, or three chests, then it is the other's turn. Both play to maximize their own total. Who ends ahead, or is it a tie?

- **Maps to:** Suffix game DP on score difference (Stone Game III).
- **Model it:** From index i, the current player maximizes (sum of next k chests) minus the opponent's best from i+k, for k in 1..3.
- **Approach & variations:**
  - Define best[i] = the score lead the mover can secure from chest i onward.
  - best[i] = max over k of prefixTake(k) - best[i+k].
  - Fill from the right end back to the start.
  - Sign of best[0] decides win/lose/tie.
- **Time:** O(n) — each index tries three take sizes.
- **Space:** O(n) — the suffix DP array (reducible to O(1)).

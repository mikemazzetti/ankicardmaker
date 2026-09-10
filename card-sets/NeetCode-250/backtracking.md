---
deck: "NeetCode 250::Backtracking"
topic: "NeetCode 250 — Backtracking"
tags: [ankicardmaker, neetcode250, backtracking]
note_type: Basic
created: 2026-09-09
---

# NeetCode 250 — Backtracking

Story front hides the technique; back reveals the mapping, approach, and complexity.

## 1. Sum of All Subsets XOR Total  ·  _Easy_

**Scenario:** A locksmith has a small ring of numbered keys. For every possible selection of keys — including the empty selection and the full ring — he combines the chosen numbers with a special 'toggle-combine' operation (bits that appear an odd number of times survive). Add up the toggle-combine result over every possible selection. What total does he get?

- **Maps to:** Backtracking over all subsets, accumulating XOR (Sum of All Subset XOR Totals).
- **Model it:** Sum the XOR of every subset of the array, including the empty subset.
- **Approach & variations:**
  - Recurse choosing include/exclude for each element, carrying the running XOR; add it at each leaf.
  - There are 2^n subsets, so brute enumeration is fine for small n.
  - Slick fact: each bit set anywhere appears in exactly half the subsets, giving `OR(all) * 2^(n-1)` in O(n).
- **Time:** O(2^n * n) enumerating subsets; O(n) with the bit-counting shortcut.
- **Space:** O(n) recursion depth (O(1) for the shortcut).

## 2. Subsets  ·  _Medium_

**Scenario:** A chef has a shelf of distinct spices and wants to write down every possible spice blend he could make — from using none of them, through every partial mix, up to using all of them. No two spices repeat on the shelf. List every distinct blend.

- **Maps to:** Backtracking / power set enumeration (Subsets).
- **Model it:** Generate the power set of a set of distinct elements.
- **Approach & variations:**
  - At each index decide include or exclude, recording the running selection at every node.
  - Because elements are distinct, no duplicate blends arise.
  - Equivalent: iterate a bitmask from 0 to 2^n-1, or grow the answer list element by element.
- **Time:** O(n * 2^n) — 2^n subsets, each up to length n to build/copy.
- **Space:** O(n) recursion depth beyond the output.

## 3. Combination Sum  ·  _Medium_

**Scenario:** A cashier has an unlimited roll of coins in a few given denominations and must make exactly a target amount. She wants every distinct set of coins that sums to the target, where a denomination may be reused any number of times, and two ways counting as the same if they use the same coins regardless of order. List them all.

- **Maps to:** Backtracking with reuse of candidates (Combination Sum).
- **Model it:** Find all multisets of candidate numbers (repeats allowed) that sum to a target.
- **Approach & variations:**
  - Recurse tracking the remaining target and a start index; from each choice you may pick the same index again to allow reuse.
  - Only move the start index forward to avoid permuted duplicates.
  - Prune when remaining goes negative; record when it hits zero.
- **Time:** O(n^(target/min)) in the worst case — exponential in the recursion depth bounded by target/smallest candidate.
- **Space:** O(target/min) recursion depth.

## 4. Combination Sum II  ·  _Medium_

**Scenario:** A cashier is handed a specific jar of coins — each physical coin usable at most once — and must find every distinct set of these coins that adds to a target amount. The jar may contain several coins of the same value, and the same combination of values must not be listed twice. Give all distinct sets.

- **Maps to:** Backtracking with sort and duplicate-skipping, no reuse (Combination Sum II).
- **Model it:** Find all subsets of a multiset (each element used once) summing to a target, without duplicate combinations.
- **Approach & variations:**
  - Sort first; recurse with a start index that always advances (each coin used at most once).
  - At the same recursion level, skip a value equal to the previous sibling to avoid duplicate sets.
  - Prune when the remaining target goes negative.
- **Time:** O(2^n) worst case — a branch per include/exclude decision over n coins.
- **Space:** O(n) recursion depth.

## 5. Combinations  ·  _Medium_

**Scenario:** A teacher must pick a committee of exactly K students from a class numbered 1 through N. Order on the committee doesn't matter, and she wants to see every possible committee she could form. List them all.

- **Maps to:** Backtracking choosing K of N (Combinations).
- **Model it:** Generate all size-K subsets of the numbers 1..N.
- **Approach & variations:**
  - Recurse with a start value, appending numbers and stopping when the selection reaches size K.
  - Advance the start so numbers are chosen in increasing order — no permutations, no repeats.
  - Prune branches that can't reach K picks with the numbers remaining.
- **Time:** O(K * C(N,K)) — C(N,K) committees, each length K to build.
- **Space:** O(K) recursion depth.

## 6. Permutations  ·  _Medium_

**Scenario:** A photographer must line up a group of distinct guests for a portrait and wants to see every possible left-to-right ordering of the whole group before choosing. No guest appears twice. List every ordering.

- **Maps to:** Backtracking building full arrangements (Permutations).
- **Model it:** Generate all orderings of a list of distinct elements.
- **Approach & variations:**
  - Recurse choosing an unused element for each position, marking it used and unmarking on backtrack.
  - A leaf at full length is one permutation.
  - Swapping elements in place is an alternative to a used-flag array.
- **Time:** O(n * n!) — n! orderings, each length n to record.
- **Space:** O(n) recursion depth plus the used marks.

## 7. Subsets II  ·  _Medium_

**Scenario:** A chef's spice shelf now has some duplicate jars of the same spice. He again wants every possible blend from none to all, but blends that use the same spices in the same amounts must not be listed twice even though duplicate jars exist. List every distinct blend.

- **Maps to:** Backtracking over subsets with duplicate-skipping after sorting (Subsets II).
- **Model it:** Generate the power set of a multiset without producing duplicate subsets.
- **Approach & variations:**
  - Sort so equal values are adjacent.
  - Recurse include/exclude with a start index; at each level skip a value equal to the previous sibling already tried.
  - Record the running selection at every node.
- **Time:** O(n * 2^n) — up to 2^n subsets, each up to length n.
- **Space:** O(n) recursion depth.

## 8. Permutations II  ·  _Medium_

**Scenario:** A photographer lines up guests for a portrait, but this time some guests are identical twins wearing the same outfit — swapping two such twins produces a line-up that looks exactly the same. She wants every visually distinct ordering, counted once each. List them.

- **Maps to:** Backtracking over permutations with duplicate pruning after sorting (Permutations II).
- **Model it:** Generate all distinct orderings of a multiset of elements.
- **Approach & variations:**
  - Sort so equal values are adjacent.
  - At each position, among equal values only use the first still-unused one (skip a duplicate whose identical predecessor is unused) to avoid repeated line-ups.
  - Mark used, recurse, and unmark on backtrack.
- **Time:** O(n * n!) worst case, fewer when duplicates prune branches.
- **Space:** O(n) recursion depth plus used marks.

## 9. Word Search  ·  _Medium_

**Scenario:** A grid of lettered tiles sits on a table. A player must trace a given word by stepping from tile to adjacent tile — up, down, left, or right — never reusing the same tile within one trace. Does the word exist somewhere as such a connected path on the board?

- **Maps to:** DFS backtracking over a grid (Word Search).
- **Model it:** Determine if a string can be formed by a path of adjacent, non-reused cells in a character grid.
- **Approach & variations:**
  - From each cell matching the first letter, DFS to neighbors that match the next letter.
  - Mark the current cell visited (e.g. temporarily overwrite it) and restore it on backtrack.
  - Succeed when the whole word is matched; fail a branch on mismatch or out of bounds.
- **Time:** O(m * n * 4^L) — a search from each cell branching up to 4 ways for word length L.
- **Space:** O(L) recursion depth (marking done in place).

## 10. Palindrome Partitioning  ·  _Medium_

**Scenario:** A jeweler has a strip of colored beads and wants to cut it into consecutive segments so that every segment reads the same forwards and backwards. She wants to enumerate every possible way to make such cuts across the whole strip. List all the ways.

- **Maps to:** Backtracking over cut positions with palindrome checks (Palindrome Partitioning).
- **Model it:** Enumerate all partitions of a string where every part is a palindrome.
- **Approach & variations:**
  - Recurse over a start index; for each end, if the prefix substring is a palindrome, take it and recurse on the rest.
  - Record a partition when the start reaches the end of the string.
  - Optionally precompute an is-palindrome table to speed the checks.
- **Time:** O(n * 2^n) — up to 2^(n-1) cut patterns, each with O(n) palindrome work.
- **Space:** O(n) recursion depth (plus O(n^2) if precomputing the palindrome table).

## 11. Letter Combinations of a Phone Number  ·  _Medium_

**Scenario:** An old landline keypad maps each number button to a little group of letters. Given a short sequence of pressed buttons, a puzzler wants to list every possible 'word' you could spell by choosing one letter from each pressed button in order. List them all.

- **Maps to:** Backtracking over a Cartesian product of per-digit letter sets (Letter Combinations of a Phone Number).
- **Model it:** Generate every string formed by picking one mapped letter per digit of the input.
- **Approach & variations:**
  - Map each digit to its letters; recurse position by position appending each candidate letter.
  - A leaf at full length is one combination.
  - Handle the empty input as producing no combinations.
- **Time:** O(4^d * d) — up to 4 letters per digit over d digits, each result length d.
- **Space:** O(d) recursion depth.

## 12. Matchsticks to Square  ·  _Medium_

**Scenario:** A crafter has a handful of sticks of various lengths and wants to lay them all end-to-end to form the four sides of a perfect square, using every stick exactly once and breaking none. Is it possible?

- **Maps to:** Backtracking assigning items to 4 equal buckets with pruning (Matchsticks to Square).
- **Model it:** Partition all sticks into exactly four groups of equal sum (the side length).
- **Approach & variations:**
  - If total isn't divisible by 4, fail; the target side is total/4.
  - Sort sticks descending and try to place each into one of four side-buckets, backtracking when a bucket overflows.
  - Prune: skip a stick longer than target, and skip buckets with equal current fill to avoid symmetric retries.
- **Time:** O(4^n) worst case, sharply cut by sorting and pruning.
- **Space:** O(n) recursion depth plus four bucket sums.

## 13. Partition to K Equal Sum Subsets  ·  _Medium_

**Scenario:** A camp counselor must split a pile of numbered tokens among exactly K children so that every child ends up holding tokens of the same total value, using every token. Can the tokens be dealt out this fairly?

- **Maps to:** Backtracking filling K equal-sum buckets with pruning (Partition to K Equal Sum Subsets).
- **Model it:** Decide if the array can be split into K subsets each summing to total/K.
- **Approach & variations:**
  - If total isn't divisible by K, or any element exceeds total/K, fail.
  - Sort descending and greedily fill one bucket to the target at a time, backtracking on failure.
  - Prune with a used mask, skip equal-value siblings, and skip a bucket you couldn't start with a given element.
- **Time:** O(K * 2^n) with memoized-mask backtracking; exponential without it.
- **Space:** O(2^n) for the visited-mask memo (O(n) recursion otherwise).

## 14. N Queens  ·  _Hard_

**Scenario:** On an N-by-N garden laid out in rows and columns, a gardener wants to place N sprinklers so that no two sprinklers share a row, a column, or either diagonal line of sight. She wants every distinct valid arrangement drawn out. Produce them all.

- **Maps to:** Backtracking row by row with column/diagonal occupancy sets (N-Queens).
- **Model it:** Place N non-attacking queens on an N×N board and return all configurations.
- **Approach & variations:**
  - Place one queen per row, trying each column that isn't already threatened.
  - Track occupied columns and both diagonals (row+col and row-col) in sets for O(1) checks.
  - Recurse to the next row; a full placement is one solution, backtracking otherwise.
- **Time:** O(N!) — roughly N choices in the first row, N-2 conflict-free in the next, and so on.
- **Space:** O(N) for the occupancy sets and recursion depth (plus output).

## 15. N Queens II  ·  _Hard_

**Scenario:** On an N-by-N garden of rows and columns, a gardener again wants N sprinklers so no two share a row, column, or diagonal line of sight — but this time she only needs to know how many distinct valid arrangements exist, not what they look like. What is the count?

- **Maps to:** Backtracking counting valid placements (N-Queens II).
- **Model it:** Count the number of ways to place N non-attacking queens on an N×N board.
- **Approach & variations:**
  - Same row-by-row placement as N-Queens, but increment a counter at each full placement instead of storing boards.
  - Track columns and both diagonals; bitmasks make the conflict checks especially fast.
  - No need to build board strings, so memory stays minimal.
- **Time:** O(N!) — the same search tree as enumerating the solutions.
- **Space:** O(N) recursion depth (constant with bitmask state).

## 16. Word Break II  ·  _Hard_

**Scenario:** A translator receives a long banner with all the spaces removed and a dictionary of allowed words. She wants every way to reinsert spaces so the whole banner splits cleanly into a sentence of dictionary words. List all such sentences.

- **Maps to:** Backtracking with memoization over suffixes (Word Break II).
- **Model it:** Enumerate all segmentations of a string into space-separated dictionary words.
- **Approach & variations:**
  - Recurse from a start index; for each dictionary-word prefix, recurse on the remainder and prepend the word to each returned sentence.
  - Memoize results per start index so shared suffixes aren't recomputed.
  - An optional word-break feasibility check first avoids exploring dead ends.
- **Time:** Exponential in the number of valid segmentations; memoization bounds repeated suffix work.
- **Space:** O(n) recursion depth plus the memo of suffix results.

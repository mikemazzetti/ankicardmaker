---
deck: "NeetCode 250::Arrays & Hashing"
topic: "NeetCode 250 — Arrays & Hashing"
tags: [ankicardmaker, neetcode250, arrays-hashing]
note_type: Basic
created: 2026-09-09
---

# NeetCode 250 — Arrays & Hashing

Story front hides the technique; back reveals the mapping, approach, and complexity.

## 1. Concatenation of Array  ·  _Easy_

**Scenario:** A street painter has a strip of numbered flags in a fixed order. A parade organizer wants a strip that is exactly twice as long: the same flags in the same order, then the whole run repeated once more right after. Produce that doubled strip.

- **Maps to:** Direct array construction / index arithmetic (Concatenation of Array).
- **Model it:** Given `nums` of length n, return an array `ans` of length 2n where `ans[i] == nums[i % n]`.
- **Approach & variations:**
  - Allocate the output and copy the input twice, or append the input to a copy of itself.
  - Equivalent one-liner: `ans[i] = nums[i % n]` for i in [0, 2n).
  - No cleverness needed — it is a warm-up in indexing.
- **Time:** O(n) — every output slot is filled once.
- **Space:** O(n) — the result holds 2n items (O(1) beyond the required output).

## 2. Contains Duplicate  ·  _Easy_

**Scenario:** A coat-check clerk receives a pile of claim tickets. She only needs to answer one yes/no question: did any single ticket number get handed in more than once during the day?

- **Maps to:** Hash set membership (Contains Duplicate).
- **Model it:** Return true if any value in the array appears at least twice.
- **Approach & variations:**
  - Sweep once, keeping seen values in a set; the moment a value is already present, answer yes.
  - Alternative: sort and check neighbors (O(n log n), O(1) extra).
  - Shortcut: compare set size to array length.
- **Time:** O(n) — one pass with O(1) set operations.
- **Space:** O(n) — the set may hold every distinct value.

## 3. Valid Anagram  ·  _Easy_

**Scenario:** Two children each spell a word using lettered fridge magnets. They want to know if one child could rearrange their own magnets to exactly spell the other's word — same magnets, just shuffled, none missing or extra.

- **Maps to:** Character frequency count (Valid Anagram).
- **Model it:** Decide whether two strings contain the same multiset of characters.
- **Approach & variations:**
  - Tally each character in the first, subtract for the second; all counts must end at zero.
  - Fast reject when lengths differ.
  - A size-26 count array works for lowercase letters; a map handles Unicode.
  - Sorting both and comparing also works (O(n log n)).
- **Time:** O(n) — count both strings once.
- **Space:** O(1) for a fixed alphabet (O(k) for k distinct characters).

## 4. Two Sum  ·  _Easy_

**Scenario:** A cashier has a row of unsorted price tags and a target total. She needs the two specific tags whose prices add up to exactly that total, and she wants their shelf positions, checking each tag only once as she goes.

- **Maps to:** Hash map of complements (Two Sum).
- **Model it:** Find indices i, j with `nums[i] + nums[j] == target` in an unsorted array.
- **Approach & variations:**
  - For each value, look up whether its needed complement (target minus it) was already seen.
  - Store value -> index as you pass; return the pair on a hit.
  - Because it is unsorted, the hash map beats two pointers here.
- **Time:** O(n) — single pass with O(1) lookups.
- **Space:** O(n) — the map of seen values.

## 5. Longest Common Prefix  ·  _Easy_

**Scenario:** A filing clerk has a stack of folder labels. She wants the longest run of starting letters that every single label shares from its very first character — the common opening they all begin with, if any.

- **Maps to:** Vertical character scan (Longest Common Prefix).
- **Model it:** Return the longest prefix string shared by all strings in the list.
- **Approach & variations:**
  - Walk column by column: compare the k-th character across all words; stop at the first mismatch or when any word ends.
  - Alternatively shrink a candidate prefix against each word.
  - Empty list or any empty word yields an empty prefix.
- **Time:** O(total characters) — worst case every character of every word is examined.
- **Space:** O(1) beyond the returned prefix.

## 6. Group Anagrams  ·  _Medium_

**Scenario:** A librarian has a cart of word cards and wants to bundle together every card whose letters can be rearranged into the same word. Cards that are letter-shuffles of one another go in one pile; each distinct pile stays separate.

- **Maps to:** Hash map keyed by a canonical signature (Group Anagrams).
- **Model it:** Partition strings into groups that share the same multiset of characters.
- **Approach & variations:**
  - Build a key per word that is identical for anagrams: its sorted letters, or a 26-length count tuple.
  - Use that key in a map from signature -> list of words.
  - Count-tuple key gives O(word length) keying vs O(len log len) for sorting.
- **Time:** O(N·K) with count keys (or O(N·K log K) sorting), N words of length up to K.
- **Space:** O(N·K) — all words stored across the groups.

## 7. Remove Element  ·  _Easy_

**Scenario:** A conveyor belt of parts passes a worker who must discard every part of one specific defective type. He can only rearrange parts on the same belt (no second belt) and afterward reports how many good parts remain packed at the front.

- **Maps to:** Two-pointer in-place overwrite (Remove Element).
- **Model it:** In place, remove all occurrences of a given value and return the count of remaining elements (order among them free).
- **Approach & variations:**
  - A write pointer marks the next 'keep' slot; a read pointer scans everything.
  - Copy each non-target value to the write slot and advance it.
  - The write index is the final kept count; leftover tail can be ignored.
- **Time:** O(n) — one scan.
- **Space:** O(1) — done in place.

## 8. Majority Element  ·  _Easy_

**Scenario:** At a town meeting everyone shouts the name of their favorite color, one after another. You are promised one color was shouted by strictly more than half the crowd. Name it, ideally without tallying every color and without writing much down.

- **Maps to:** Boyer–Moore voting (Majority Element).
- **Model it:** Return the value that appears more than n/2 times, guaranteed to exist.
- **Approach & variations:**
  - Keep a candidate and a count; matching votes increment, differing votes decrement, and a zero count adopts the next value as candidate.
  - The true majority survives because it outnumbers all others combined.
  - A hash-map tally also works but uses O(n) space.
- **Time:** O(n) — one pass.
- **Space:** O(1) — a candidate and a counter.

## 9. Design HashSet  ·  _Easy_

**Scenario:** Design a coat rack that only tracks which membership numbers are present — no duplicates, no extra data. It must support hanging a number, checking if a number is on the rack, and taking a number off, all near-instantly for any number in a huge range.

- **Maps to:** Hashing with buckets and chaining (Design HashSet).
- **Model it:** Implement add / contains / remove for integer keys without a built-in set.
- **Approach & variations:**
  - Fix a bucket count; map each key to a bucket via key mod count.
  - Each bucket is a small list; collisions chain within it.
  - For a bounded key range a plain boolean array is the simplest set.
  - Resize/rehash if load grows to keep chains short.
- **Time:** O(1) average per operation (O(n/buckets) worst case).
- **Space:** O(n) — storage grows with stored keys.

## 10. Design HashMap  ·  _Easy_

**Scenario:** Design a lost-and-found ledger where each claim number maps to one description. You can file a number with its description (overwriting any old one), look up a number's current description, and erase a number, all fast for numbers across a vast range.

- **Maps to:** Hashing with key-value buckets (Design HashMap).
- **Model it:** Implement put / get / remove for integer keys mapping to values without a built-in map.
- **Approach & variations:**
  - Bucket array indexed by key mod count; each bucket holds key-value pairs.
  - put updates in place if the key exists, else appends; get scans the bucket; remove unlinks it.
  - A direct-index array works when the key range is small and bounded.
  - Rehash when the load factor climbs.
- **Time:** O(1) average per operation (O(n/buckets) worst case).
- **Space:** O(n) — one entry per stored key.

## 11. Sort an Array  ·  _Medium_

**Scenario:** A dealer is handed a shuffled deck of numbered chips and must return them in ascending order. She may not lean on any built-in sorting helper — she has to arrange them herself, and it must stay fast even for a very large stack.

- **Maps to:** Efficient comparison sort — merge sort or heap sort (Sort an Array).
- **Model it:** Return the array sorted ascending, implementing the sort yourself in O(n log n).
- **Approach & variations:**
  - Merge sort: recursively split, then merge sorted halves (stable, O(n) extra).
  - Heap sort: build a heap and pop repeatedly (in place, O(1) extra).
  - Quicksort works but needs randomized pivots to avoid O(n²) on adversarial input.
  - Counting sort beats these when values sit in a small bounded range.
- **Time:** O(n log n) — the comparison-sort lower bound, met by merge/heap.
- **Space:** O(n) merge sort (O(1) for heap sort).

## 12. Sort Colors  ·  _Medium_

**Scenario:** A line of tiles comes in only three shades — say red, white, blue. Rearrange the line so all reds sit first, whites in the middle, blues last, doing it in a single sweep along the same line without counting shades in a first pass.

- **Maps to:** Dutch National Flag three-way partition (Sort Colors).
- **Model it:** Sort an array of only three distinct values in place in one pass.
- **Approach & variations:**
  - Keep three pointers: low boundary, current scanner, high boundary.
  - Scanner sees a red -> swap to low and advance both; a blue -> swap to high and shrink high (don't advance scanner); a white -> just advance.
  - Simpler two-pass alternative: count each shade, then overwrite.
- **Time:** O(n) — one linear scan.
- **Space:** O(1) — in-place swaps.

## 13. Top K Frequent Elements  ·  _Medium_

**Scenario:** A café logs every drink ordered all day. The manager wants the K drinks ordered most often — just those few names — without fully ranking the entire menu by popularity.

- **Maps to:** Frequency count + bucket sort (or heap) (Top K Frequent Elements).
- **Model it:** Return the K values with the highest occurrence counts in the array.
- **Approach & variations:**
  - Tally counts in a map.
  - Bucket by frequency: index i holds values seen i times; scan buckets from high to low and collect K.
  - A size-K heap over the counts is the alternative (O(n log k)).
  - Bucketing gives linear time since frequency is bounded by n.
- **Time:** O(n) with buckets (O(n log k) with a heap).
- **Space:** O(n) — counts and buckets.

## 14. Encode and Decode Strings  ·  _Medium_

**Scenario:** A courier must pack several notes — which may themselves contain any punctuation, spaces, even the delimiter you might pick — into one sealed message, then hand it off so the recipient can split it back into the exact original notes with none merged or lost.

- **Maps to:** Length-prefixed serialization (Encode and Decode Strings).
- **Model it:** Serialize a list of arbitrary strings into one string and parse it back losslessly.
- **Approach & variations:**
  - Prefix each note with its length and a separator, e.g. `5#hello`.
  - To decode, read digits up to the separator, then take exactly that many characters as the note; repeat.
  - Length prefixing is robust because content can contain any character, so no delimiter alone is safe.
- **Time:** O(total length) — each character is written and read once.
- **Space:** O(total length) — the encoded string and decoded list.

## 15. Range Sum Query 2D Immutable  ·  _Medium_

**Scenario:** A museum has a fixed grid of rooms, each with a visitor count that never changes. Guides keep asking for the total visitors inside various rectangular blocks of rooms. After a one-time setup, answer each rectangle instantly.

- **Maps to:** 2D prefix-sum table (Range Sum Query 2D Immutable).
- **Model it:** Precompute so any submatrix rectangle sum is returned in O(1).
- **Approach & variations:**
  - Build a table where entry (r,c) is the sum of everything above-and-left.
  - A rectangle sum = bottom-right − top-strip − left-strip + doubly-subtracted corner (inclusion–exclusion).
  - Works only because values are immutable; updates would need a Fenwick/segment structure.
- **Time:** O(m·n) build, O(1) per query.
- **Space:** O(m·n) — the prefix table.

## 16. Product of Array Except Self  ·  _Medium_

**Scenario:** A jeweler lines up gemstones each with a weight. For every stone she wants a tag showing the product of all the other stones' weights — everything except that stone. And her contract forbids using division to cancel out the current stone.

- **Maps to:** Prefix and suffix products (Product of Array Except Self).
- **Model it:** For each index return the product of all elements except that one, without division.
- **Approach & variations:**
  - First pass fills each slot with the running product of everything to its left.
  - Second pass multiplies in the running product of everything to its right.
  - Handle zeros naturally — the two-pass method needs no special case for them.
  - Output array can double as the prefix buffer for O(1) extra space.
- **Time:** O(n) — two linear passes.
- **Space:** O(1) extra (beyond the output array).

## 17. Valid Sudoku  ·  _Medium_

**Scenario:** An inspector reviews a partly filled nine-by-nine puzzle grid. She only checks legality of what's already written: no digit repeats within any single row, any single column, or any of the nine three-by-three blocks. She isn't solving it — just flagging conflicts.

- **Maps to:** Hash sets per row/column/box (Valid Sudoku).
- **Model it:** Verify no digit repeats within any row, column, or 3×3 sub-box of a partially filled board.
- **Approach & variations:**
  - Keep a seen-set for each of the 9 rows, 9 columns, and 9 boxes.
  - For each filled cell, compute its box index as `(r/3)*3 + c/3` and check all three sets.
  - A repeat in any set means invalid; empty cells are skipped.
- **Time:** O(1) — a fixed 81-cell board (O(n²) in grid side generally).
- **Space:** O(1) — a fixed number of small sets.

## 18. Longest Consecutive Sequence  ·  _Medium_

**Scenario:** A collector dumps a jumbled box of numbered tokens on a table. She wants the length of the longest unbroken run of consecutive numbers she could line up (like 7,8,9,10), regardless of where they sat in the pile — and she needs it fast, not by sorting the whole box.

- **Maps to:** Hash set with sequence-start detection (Longest Consecutive Sequence).
- **Model it:** Find the length of the longest run of consecutive integers present, in O(n).
- **Approach & variations:**
  - Put all values in a set.
  - A value starts a run only if value−1 is absent; from each start, walk value+1, value+2… counting length.
  - Each number is visited at most twice, keeping it linear despite the nested walk.
  - Sorting would solve it too but costs O(n log n).
- **Time:** O(n) — set lookups, each element extends a run once.
- **Space:** O(n) — the set of values.

## 19. Best Time to Buy And Sell Stock II  ·  _Medium_

**Scenario:** A trader sees a fruit's daily price for a whole season. He may buy and sell as many times as he likes, but must sell before buying again (hold at most one crate). What's the maximum total profit he can bank over the season?

- **Maps to:** Greedy sum of positive daily gains (Best Time to Buy and Sell Stock II).
- **Model it:** Maximize total profit with unlimited non-overlapping buy/sell pairs.
- **Approach & variations:**
  - Add up every upward step: whenever tomorrow's price exceeds today's, pocket the difference.
  - This captures every rising stretch, equivalent to buying at each valley and selling at each peak.
  - No lookahead or DP needed because unlimited transactions remove any tradeoff.
- **Time:** O(n) — one pass over prices.
- **Space:** O(1) — a running total.

## 20. Majority Element II  ·  _Medium_

**Scenario:** At a rally people call out team names. Any team named by more than a third of the crowd should be listed — there can be at most two such teams. Find them using barely any scratch paper.

- **Maps to:** Boyer–Moore voting for two candidates (Majority Element II).
- **Model it:** Return all values appearing more than n/3 times (at most two).
- **Approach & variations:**
  - Track two candidates with two counts; each value matches one, else decrements both, else fills an empty slot.
  - At most two values can exceed n/3, which is why two slots suffice.
  - A required second pass verifies each candidate truly exceeds n/3.
- **Time:** O(n) — two linear passes.
- **Space:** O(1) — two candidates and two counters.

## 21. Subarray Sum Equals K  ·  _Medium_

**Scenario:** A hiker logs each day's elevation gain (some days negative) in order. She wants to count how many stretches of consecutive days add up to exactly a target gain K. Days can't be reordered — only contiguous runs count.

- **Maps to:** Prefix sums with a hash map of counts (Subarray Sum Equals K).
- **Model it:** Count contiguous subarrays whose sum equals K.
- **Approach & variations:**
  - Keep a running total; a stretch summing to K exists whenever a prior running total equals current−K.
  - Store how many times each running total has occurred; add that many on each step.
  - Seed the map with total 0 seen once to catch prefixes that themselves equal K.
  - Handles negatives, unlike a sliding window.
- **Time:** O(n) — one pass with O(1) map ops.
- **Space:** O(n) — map of prefix-sum frequencies.

## 22. First Missing Positive  ·  _Hard_

**Scenario:** A hotel has rooms numbered 1, 2, 3, … A clerk holds a messy list of occupied room numbers (some junk, some huge, some repeats). She needs the smallest positive room number that is NOT occupied — using essentially only the list's own paper for scratch, no separate ledger.

- **Maps to:** Index-as-hash in-place placement (First Missing Positive).
- **Model it:** Find the smallest positive integer absent from the array using O(1) extra space.
- **Approach & variations:**
  - Treat the array as its own hash: swap each value v (when 1≤v≤n) to index v−1 until settled.
  - Then scan for the first position i whose value isn't i+1 — that's the answer.
  - Values ≤0 or >n are irrelevant and left where they fall.
  - The answer always lies in [1, n+1].
- **Time:** O(n) — each value is placed at most once via swaps.
- **Space:** O(1) — rearranges the array in place.

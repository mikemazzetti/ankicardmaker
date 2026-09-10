---
deck: "NeetCode 250::Two Pointers"
topic: "NeetCode 250 — Two Pointers"
tags: [ankicardmaker, neetcode250, two-pointers]
note_type: Basic
created: 2026-09-09
---

# NeetCode 250 — Two Pointers

Story front hides the technique; back reveals the mapping, approach, and complexity.

## 1. Reverse String  ·  _Easy_

**Scenario:** A row of lettered blocks sits on a shelf. A child must flip the whole row end-for-end so the last block becomes first, working only on that same shelf with no second shelf to borrow.

- **Maps to:** Two-pointer swap from both ends (Reverse String).
- **Model it:** Reverse a character array in place.
- **Approach & variations:**
  - One finger at each end; swap the two characters, then step both inward.
  - Stop when the fingers meet or cross.
  - In place, so no extra buffer is allocated.
- **Time:** O(n) — each character is touched once.
- **Space:** O(1) — swaps in place.

## 2. Valid Palindrome  ·  _Easy_

**Scenario:** A proofreader checks whether a phrase reads the same forward and backward, but she ignores spaces and punctuation entirely and treats capital and lowercase letters as the same. Does the cleaned phrase mirror itself?

- **Maps to:** Two pointers with filtering (Valid Palindrome).
- **Model it:** Decide if a string is a palindrome considering only alphanumerics, case-insensitively.
- **Approach & variations:**
  - A pointer at each end skips non-alphanumeric characters inward.
  - Compare the two characters lowercased; any mismatch means no.
  - Meet in the middle to confirm yes.
  - Filtering on the fly avoids building a cleaned copy.
- **Time:** O(n) — each character is examined once.
- **Space:** O(1) — two indices, no copy.

## 3. Valid Palindrome II  ·  _Easy_

**Scenario:** A proofreader checks whether a word reads the same both ways, and she's allowed to cross out at most one single letter to make it work. Can the word be a mirror image of itself with one deletion or none?

- **Maps to:** Two pointers with one allowed skip (Valid Palindrome II).
- **Model it:** Return true if the string is a palindrome after deleting at most one character.
- **Approach & variations:**
  - Close in from both ends while characters match.
  - At the first mismatch, test the substring skipping the left character OR skipping the right — either being a palindrome succeeds.
  - Only one deletion is permitted, so the branch happens just once.
- **Time:** O(n) — outer scan plus one linear verification.
- **Space:** O(1) — index-based checks, no copies.

## 4. Merge Strings Alternately  ·  _Easy_

**Scenario:** Two dancers stand in two lines. A choreographer forms one combined line by taking the front dancer of line one, then line two, then one, then two, and so on. When one line empties, the rest of the other line is appended in order.

- **Maps to:** Two-pointer interleave (Merge Strings Alternately).
- **Model it:** Build a string by alternating characters of two strings, appending the leftover tail.
- **Approach & variations:**
  - Advance an index into each string, appending one character from each per round.
  - When one runs out, append the remainder of the longer one.
  - A single loop with both indices suffices.
- **Time:** O(a + b) — every character copied once.
- **Space:** O(a + b) — the merged output.

## 5. Merge Sorted Array  ·  _Easy_

**Scenario:** A librarian has one long shelf already sorted but with empty slots at the far right, exactly enough to hold a second, smaller sorted stack. She must fold the second stack into the shelf so the whole shelf ends up sorted — filling from the right so she never overwrites a book she still needs.

- **Maps to:** Two pointers merging from the back (Merge Sorted Array).
- **Model it:** Merge two sorted arrays into the first, which has trailing space, in place.
- **Approach & variations:**
  - Start pointers at the last real element of each array and a write pointer at the very end.
  - Place the larger of the two at the write slot and step that pointer back.
  - Filling from the back avoids clobbering unmerged values in the first array.
  - Any leftover of the second array is copied down at the end.
- **Time:** O(m + n) — each element placed once.
- **Space:** O(1) — merged in place.

## 6. Remove Duplicates From Sorted Array  ·  _Easy_

**Scenario:** A row of already-alphabetized name cards has some names repeated on adjacent cards. A clerk must compact the row so each name appears once, in order, reusing the same row, then report how many unique cards fill the front.

- **Maps to:** Two-pointer in-place dedup on sorted input (Remove Duplicates From Sorted Array).
- **Model it:** Remove duplicates in place from a sorted array and return the count of uniques.
- **Approach & variations:**
  - A slow write pointer marks the last unique kept; a fast pointer scans forward.
  - When the fast value differs from the last kept, write it just after and advance the slow pointer.
  - Sortedness guarantees duplicates are adjacent, so only neighbor comparison is needed.
  - Slow index + 1 is the unique count.
- **Time:** O(n) — one scan.
- **Space:** O(1) — in place.

## 7. Two Sum II Input Array Is Sorted  ·  _Medium_

**Scenario:** A grocer has jars of coins arranged left-to-right from lightest to heaviest and wants two jars whose weights add to an exact target, reporting their positions. He wants to exploit the neat ordering rather than test every pair.

- **Maps to:** Two pointers on a sorted array (Two Sum II).
- **Model it:** Find two indices in a sorted array whose values sum to the target.
- **Approach & variations:**
  - One pointer at the lightest end, one at the heaviest.
  - Sum too big -> move the right pointer left; too small -> move the left pointer right; equal -> found.
  - Sortedness is what makes the O(n) sweep valid; unsorted would need a hash set.
- **Time:** O(n) — pointers only move inward, one sweep.
- **Space:** O(1) — two indices.

## 8. 3Sum  ·  _Medium_

**Scenario:** From a mixed bag of numbered chips (positives, negatives, zeros), a player must find every distinct trio of chips that together balance to zero. No trio should be listed twice even if different chips give the same values.

- **Maps to:** Sort + two-pointer sweep per anchor (3Sum).
- **Model it:** Find all unique triplets summing to zero.
- **Approach & variations:**
  - Sort first; fix each element as an anchor and two-pointer the rest for the needed complement.
  - Skip duplicate anchors and duplicate pointer values to keep triplets unique.
  - Break early once the anchor is positive (sum can't reach zero).
  - Sorting enables both the pointer sweep and easy dedup.
- **Time:** O(n²) — an O(n) sweep for each of n anchors (sort is O(n log n)).
- **Space:** O(1) or O(n) — ignoring output, just the sort's overhead.

## 9. 4Sum  ·  _Medium_

**Scenario:** From a bag of numbered chips a player must find every distinct group of four chips whose values add up to an exact target amount (which may be any number, not just zero). Duplicate quadruples must not be listed twice.

- **Maps to:** Sort + nested anchors + two-pointer (4Sum).
- **Model it:** Find all unique quadruples summing to a given target.
- **Approach & variations:**
  - Sort, then fix two outer anchors and two-pointer the remaining span for the target minus the pair.
  - Skip duplicate values at every level to avoid repeated quadruples.
  - Prune with running min/max bounds to cut hopeless branches.
  - Generalizes the 3Sum pattern by one more loop.
- **Time:** O(n³) — two nested anchors, each with an O(n) sweep.
- **Space:** O(1) or O(n) — beyond output, only sort overhead.

## 10. Rotate Array  ·  _Medium_

**Scenario:** A conga line of dancers must shift so that the last K dancers wrap around to the front, everyone keeping their relative order. It has to be done on the same floor without an entire spare copy of the line.

- **Maps to:** Triple reversal in place (Rotate Array).
- **Model it:** Rotate an array right by k positions in place.
- **Approach & variations:**
  - Reduce k modulo n first.
  - Reverse the whole array, then reverse the first k, then reverse the remaining n−k.
  - This lands each element in its rotated spot using only swaps.
  - A juggling/cyclic-replacement method also works in O(1) space.
- **Time:** O(n) — three linear reversals.
- **Space:** O(1) — swaps in place.

## 11. Container With Most Water  ·  _Medium_

**Scenario:** A row of vertical poles of various heights stands along a line. Choosing two poles as the sides of a rectangular tank, the water level is capped by the shorter pole and the width is their distance apart. Which two poles hold the most water?

- **Maps to:** Two pointers shrinking inward (Container With Most Water).
- **Model it:** Maximize (min of two heights) × (distance between them) over all index pairs.
- **Approach & variations:**
  - Start with the widest pair, one pointer at each end.
  - Area is limited by the shorter side, so move the shorter pointer inward — the taller side could only be wasted otherwise.
  - Track the best area as the pointers close.
  - Moving the taller side can never improve on the current width, hence the greedy choice.
- **Time:** O(n) — pointers meet after one sweep.
- **Space:** O(1) — two indices and a max.

## 12. Boats to Save People  ·  _Medium_

**Scenario:** After a flood, rescuers have canoes each with the same strict weight limit, and each canoe carries at most two people. Given everyone's weights, what's the fewest canoes needed to ferry everyone across?

- **Maps to:** Sort + greedy two pointers (Boats to Save People).
- **Model it:** Minimize boats where each holds at most two people under a weight limit.
- **Approach & variations:**
  - Sort weights; pointer at lightest and heaviest.
  - The heaviest always boards; if the lightest also fits alongside, pair them and advance both — else the heaviest goes alone.
  - Each step consumes one boat and at least the heaviest remaining person.
  - Greedy pairing of lightest-with-heaviest is provably optimal.
- **Time:** O(n log n) — dominated by the sort.
- **Space:** O(1) beyond the sort.

## 13. Trapping Rain Water  ·  _Hard_

**Scenario:** A cross-section of city rooftops of varying heights sits side by side. After a downpour, water pools in the dips between taller buildings. Given the heights, how many units of water are trapped across the whole skyline once it stops raining?

- **Maps to:** Two pointers tracking running max walls (Trapping Rain Water).
- **Model it:** Sum trapped water where each position holds min(max-left, max-right) − its own height.
- **Approach & variations:**
  - Water over a position is bounded by the tallest wall on each side.
  - Two pointers advance from both ends, moving whichever side has the smaller running max and adding that side's deficit.
  - The smaller running max is a firm bound, so its contribution is final.
  - Alternatives: precompute left/right max arrays (O(n) space), or a monotonic stack.
- **Time:** O(n) — one two-pointer pass.
- **Space:** O(1) — running maxima and a total.

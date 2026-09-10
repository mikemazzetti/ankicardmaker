---
deck: "NeetCode 250::Bit Manipulation"
topic: "NeetCode 250 — Bit Manipulation"
tags: [ankicardmaker, neetcode250, bit-manipulation]
note_type: Basic
created: 2026-09-09
---

# NeetCode 250 — Bit Manipulation

Story front hides the technique; back reveals the mapping, approach, and complexity.

## 1. Single Number  ·  _Easy_

**Scenario:** At a costume ball everyone arrived with a partner wearing the exact same mask, so every mask design shows up on precisely two guests — except one lonely person who came alone with a unique mask. Given the whole crowd streaming past, name that single unpaired mask using no notepad to tally who you've seen.

- **Maps to:** XOR fold over all elements (Single Number).
- **Model it:** Every value appears twice except one; combine all numbers with XOR and the survivor is the loner.
- **Approach & variations:**
  - XOR is its own inverse, so `x ^ x = 0` and any pair cancels.
  - XOR all values together; the duplicates annihilate and the unique one remains.
  - Order doesn't matter since XOR is commutative and associative.
  - Starting accumulator is 0 (the XOR identity).
- **Time:** O(n) — one sweep, a single XOR per guest.
- **Space:** O(1) — just the running accumulator, no tally book.

## 2. Number of 1 Bits  ·  _Easy_

**Scenario:** A hotel gives you one long row of light switches encoding a room number; each switch is either up or down. The night manager only cares how many switches are currently flipped up. Count the raised switches as fast as possible.

- **Maps to:** Popcount / bit counting (Number of 1 Bits).
- **Model it:** Count the set bits in the binary representation of the given integer.
- **Approach & variations:**
  - Simple: check the lowest bit with `n & 1`, shift right, repeat 32 times.
  - Faster (Brian Kernighan): `n &= (n - 1)` clears the lowest set bit; loop runs once per raised switch.
  - Kernighan's trick loops only k times for k set bits, not the full width.
- **Time:** O(1) — fixed 32-bit width (or O(k) set bits with Kernighan's).
- **Space:** O(1) — a single counter.

## 3. Counting Bits  ·  _Easy_

**Scenario:** A stamp collector numbers albums 0, 1, 2, up through N, and for each album wants to know how many gold stars its number needs when written in the two-symbol shorthand the club uses. Produce the star-count for every album from 0 to N without re-counting each from scratch.

- **Maps to:** DP using a lower-bit relation (Counting Bits).
- **Model it:** For each i from 0..n, output the number of set bits, reusing previously computed answers.
- **Approach & variations:**
  - Relation: `bits[i] = bits[i >> 1] + (i & 1)` — drop the last bit, add it back.
  - Alternative: `bits[i] = bits[i & (i - 1)] + 1` using the cleared-lowest-bit form.
  - Each answer is built in O(1) from a smaller, already-known one.
- **Time:** O(n) — one constant-time step per album.
- **Space:** O(n) — the output table of counts (O(1) extra beyond it).

## 4. Add Binary  ·  _Easy_

**Scenario:** Two ancient tally sticks are notched only with two kinds of marks meaning 'off' and 'on', each representing a number in a base-two folk system. Lay them right-aligned and produce a new stick whose marks represent their sum, carrying over exactly as a schoolchild adds columns by hand.

- **Maps to:** Digit-by-digit addition with carry (Add Binary).
- **Model it:** Add two binary strings and return their binary sum string.
- **Approach & variations:**
  - Walk both strings from the rightmost digit toward the left.
  - At each column sum the two digits plus the carry; the result digit is `sum % 2`, new carry is `sum / 2`.
  - Append digits then reverse, and don't forget a final leftover carry.
  - Pad implicitly by treating past-the-end digits as 0.
- **Time:** O(max(m, n)) — one pass over the longer stick.
- **Space:** O(max(m, n)) — the result string of that length.

## 5. Reverse Bits  ·  _Easy_

**Scenario:** A conveyor belt carries exactly 32 numbered tokens, each showing heads or tails, past a mirror. You must rebuild the same belt but with the token order flipped end to end — the first token's face lands in the last slot and vice versa — keeping each token's own face unchanged.

- **Maps to:** Bit reversal within a fixed width (Reverse Bits).
- **Model it:** Reverse the order of the 32 bits of an unsigned integer.
- **Approach & variations:**
  - Loop 32 times: peel the low bit of the input, push it into the result, then shift result left and input right.
  - Equivalently `result = (result << 1) | (n & 1)` each step.
  - Divide-and-conquer swap of bit halves/quarters does it in O(log w) if repeated many times.
- **Time:** O(1) — fixed 32 iterations.
- **Space:** O(1) — one result accumulator.

## 6. Missing Number  ·  _Easy_

**Scenario:** A cloakroom hands out tickets numbered 0 through N with no gaps, one per coat. At closing, all coats but one have been collected, and you hold the pile of returned tickets — one ticket fewer than were issued. Which ticket number never came back?

- **Maps to:** XOR of indices and values, or sum formula (Missing Number).
- **Model it:** Given n distinct numbers from 0..n, find the single absent one.
- **Approach & variations:**
  - XOR every index 0..n together with every value; pairs cancel and the missing number survives.
  - Alternative: expected sum `n(n+1)/2` minus the actual sum equals the gap.
  - XOR avoids the overflow risk the sum formula can hit.
  - Both are O(1) space, single pass.
- **Time:** O(n) — one sweep over the returned tickets.
- **Space:** O(1) — a single accumulator.

## 7. Sum of Two Integers  ·  _Medium_

**Scenario:** A cursed abacus has had its 'add' rail confiscated — you may only slide beads to compare positions and shift whole rows sideways. Two quantities sit on it; produce their total using nothing but these position-comparison and row-shifting moves, never the forbidden plus operation.

- **Maps to:** Addition via XOR and carry shifting (Sum of Two Integers).
- **Model it:** Compute a + b without using + or -, using only bitwise operations.
- **Approach & variations:**
  - XOR gives the sum ignoring carries; AND then left-shift gives the carries.
  - Loop: `sum = a ^ b`, `carry = (a & b) << 1`, repeat with these until carry is 0.
  - Handle language quirks (e.g. mask to 32 bits) for negatives in fixed-width languages.
- **Time:** O(1) — at most ~32 carry-propagation rounds.
- **Space:** O(1) — a couple of temporaries.

## 8. Reverse Integer  ·  _Medium_

**Scenario:** A signed odometer reading sits on the dashboard, and you want to display it with its digits written backward (keeping any leading minus). But the display case can only show numbers within a fixed range — if the flipped reading would overflow that case, it must show zero instead.

- **Maps to:** Digit reversal with overflow guard (Reverse Integer).
- **Model it:** Reverse the decimal digits of a signed 32-bit integer, returning 0 on overflow.
- **Approach & variations:**
  - Pop the last digit with `% 10`, push onto the result with `result * 10 + digit`, drop it with `/ 10`.
  - Sign carries along naturally in most languages.
  - Before each push, check against the 32-bit limits so you detect overflow before it happens.
  - Return 0 the moment the reversed value would exceed the range.
- **Time:** O(log n) — proportional to the digit count.
- **Space:** O(1) — one running result.

## 9. Bitwise AND of Numbers Range  ·  _Medium_

**Scenario:** A vault has a bank of on/off levers. You're given a first and last serial number and told: overlay the lever-patterns of every serial from first through last, and a lever stays lit only if it was lit on every single one. Report the final lever pattern without inspecting each serial individually.

- **Maps to:** Common binary prefix of the endpoints (Bitwise AND of Numbers Range).
- **Model it:** Compute the bitwise AND of all integers in [left, right].
- **Approach & variations:**
  - Any bit that ever flips across the range becomes 0 in the AND, so only the shared high prefix survives.
  - Shift both endpoints right until they're equal, counting shifts, then shift the common value back left.
  - Alternative: repeatedly clear right's lowest set bit with `right & (right - 1)` until `right <= left`.
- **Time:** O(log n) — one step per bit of width.
- **Space:** O(1) — a shift counter.

## 10. Minimum Array End  ·  _Medium_

**Scenario:** A jeweler must lay out N gemstones in strictly increasing size, and every stone must contain a fixed engraved seal x: wherever the seal has a raised dot, that stone must have a matching stud. Keep every stone as small as possible; the whole line is forced once the first stone is the seal itself. What is the size of the very last, largest stone?

- **Maps to:** Distribute a counter across the free (zero) bits of x (Minimum Array End).
- **Model it:** Build the smallest strictly increasing sequence of n values whose AND with each other all keep x's set bits; return the last element.
- **Approach & variations:**
  - Every element must be a superset of x's bits, so the set bits are fixed; only the zero-bit positions are free to vary.
  - The i-th smallest such value places the binary digits of (n-1) into x's zero-bit slots.
  - Walk the bits: fill each 0-slot of x with the next bit of (n-1), leaving x's 1-bits untouched.
  - Result is x with (n-1)'s bits scattered into its gaps.
- **Time:** O(log n + log x) — one pass over the bit positions.
- **Space:** O(1) — accumulate the answer in place.

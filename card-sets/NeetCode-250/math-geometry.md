---
deck: "NeetCode 250::Math & Geometry"
topic: "NeetCode 250 — Math & Geometry"
tags: [ankicardmaker, neetcode250, math-geometry]
note_type: Basic
created: 2026-09-09
---

# NeetCode 250 — Math & Geometry

Story front hides the technique; back reveals the mapping, approach, and complexity.

## 1. Excel Sheet Column Title  ·  _Easy_

**Scenario:** A warehouse labels shelves A, B, ... Z, then AA, AB, ... AZ, BA, and so on, exactly like a car's odometer but with 26 letters and no zero digit. Given a shelf's position number counting from 1, what is its letter label?

- **Maps to:** Base-26 conversion with a 1-based (bijective) offset (Excel Sheet Column Title).
- **Model it:** Convert a 1-based integer to its bijective base-26 letter string.
- **Approach & variations:**
  - Repeatedly subtract 1 before taking mod 26 (there's no zero digit, so it's 1-indexed).
  - That remainder maps to a letter A..Z; prepend it and divide the number by 26.
  - Continue until the number reaches zero; the built string (reversed) is the label.
- **Time:** O(log₂₆ n) — one digit produced per division.
- **Space:** O(log₂₆ n) — the output characters.

## 2. Greatest Common Divisor of Strings  ·  _Easy_

**Scenario:** Two friends each chant a repeated rhythmic phrase built by looping some shorter base phrase a whole number of times. You want the longest possible base phrase that, repeated enough times, produces each of their chants exactly. What is that longest common base phrase (if one exists)?

- **Maps to:** String GCD via concatenation test + numeric gcd of lengths (Greatest Common Divisor of Strings).
- **Model it:** Find the longest string that divides both inputs by repetition.
- **Approach & variations:**
  - A common base exists only if the two strings concatenated in both orders are equal.
  - If so, the answer's length is the numeric gcd of the two lengths.
  - Return the prefix of that length; otherwise return empty.
- **Time:** O(n + m) — the concatenation-equality check dominates.
- **Space:** O(n + m) — the concatenated strings compared.

## 3. Insert Greatest Common Divisors in Linked List  ·  _Medium_

**Scenario:** Beads with numbers are strung in a single-file chain. Between each pair of neighboring beads you must slip in one new bead whose number is the largest whole number that divides both of its neighbors evenly. Do this for every adjacent pair. What does the finished chain look like?

- **Maps to:** Linked-list traversal inserting gcd nodes between pairs (Insert Greatest Common Divisors in Linked List).
- **Model it:** For each adjacent node pair, insert a node holding their gcd.
- **Approach & variations:**
  - Walk the chain with a pointer at the current node while it has a successor.
  - Compute gcd(current.value, next.value) via the Euclidean algorithm.
  - Splice a new node with that value between current and next, then advance past the inserted node.
- **Time:** O(n log M) — n nodes, each gcd costing log of the max value.
- **Space:** O(1) — in-place pointer rewiring (excluding the required new nodes).

## 4. Transpose Matrix  ·  _Easy_

**Scenario:** A stadium's seating chart is a grid of values arranged in rows and columns. You need to flip the whole chart across its top-left-to-bottom-right diagonal, so that what was row-then-column becomes column-then-row. What does the flipped chart look like?

- **Maps to:** Matrix transpose by swapping across the main diagonal (Transpose Matrix).
- **Model it:** Produce the matrix where entry (i,j) becomes entry (j,i).
- **Approach & variations:**
  - For a square grid, swap element (i,j) with (j,i) for j > i, in place.
  - For a non-square grid, allocate a new grid with rows and columns dimensions swapped and copy across.
  - Each original position maps to its mirror across the main diagonal.
- **Time:** O(r·c) — every cell touched once.
- **Space:** O(1) in place for square, O(r·c) for a rectangular output.

## 5. Rotate Image  ·  _Medium_

**Scenario:** A square mosaic of tiles must be turned a quarter-turn clockwise, so the top row becomes the right column, and so on. You must do it by shifting tiles within the same frame, without copying the mosaic onto a second board. What is the rotated mosaic?

- **Maps to:** In-place 90° rotation via transpose + row reversal (Rotate Image).
- **Model it:** Rotate an n×n matrix 90° clockwise in place.
- **Approach & variations:**
  - Transpose the matrix (swap across the main diagonal), then reverse each row.
  - Alternatively rotate in four-cell cycles layer by layer from outside in.
  - Both avoid an extra full-size grid.
- **Time:** O(n²) — every cell moved once.
- **Space:** O(1) — rotation happens within the same grid.

## 6. Spiral Matrix  ·  _Medium_

**Scenario:** A guard walks a rectangular garden laid out as a grid of numbered plots, starting at the top-left and moving right, then down the far side, then left along the bottom, then up — always spiraling inward and never revisiting a plot. In what order does the guard step on the plots?

- **Maps to:** Boundary-shrinking spiral traversal (Spiral Matrix).
- **Model it:** List the matrix elements in clockwise spiral order.
- **Approach & variations:**
  - Keep four boundaries: top, bottom, left, right.
  - Traverse the top row left-to-right, the right column top-to-bottom, the bottom row right-to-left, the left column bottom-to-top.
  - After each edge, shrink the corresponding boundary; stop when boundaries cross.
  - Guard against a leftover single row/column at the center.
- **Time:** O(r·c) — each cell visited once.
- **Space:** O(1) — extra of the output list itself.

## 7. Set Matrix Zeroes  ·  _Medium_

**Scenario:** On a grid spreadsheet of numbers, wherever a cell holds a zero, that cell's entire row and entire column must be blanked to zero. Crucially, the original zeros should trigger the blanking, not the newly blanked cells, and you should avoid using a whole second grid. What is the final grid?

- **Maps to:** Use first row/column as in-place markers (Set Matrix Zeroes).
- **Model it:** Zero out every row and column that originally contained a zero, in place.
- **Approach & variations:**
  - First scan records which rows and columns must be zeroed; using the matrix's own first row and column as those marker flags saves space.
  - Track separately whether the first row and first column themselves need zeroing.
  - Second pass zeros interior cells whose row-marker or column-marker is set, then handle the first row/column last.
- **Time:** O(r·c) — two passes over the grid.
- **Space:** O(1) — markers stored in the grid's border cells.

## 8. Happy Number  ·  _Easy_

**Scenario:** A number game: take a whole number, replace it with the sum of the squares of its digits, and repeat. Some numbers eventually reach 1 and stay there; others fall into a repeating loop that never hits 1. Starting from a given number, does it eventually reach 1?

- **Maps to:** Cycle detection (set or Floyd's two pointers) on digit-square sums (Happy Number).
- **Model it:** Iterate the digit-square-sum function and decide whether it reaches 1 or enters a cycle.
- **Approach & variations:**
  - Repeatedly compute the sum of squares of digits.
  - Detect a loop with a seen-set, or with slow/fast pointers to use O(1) space.
  - Reaching 1 means happy; revisiting a value means a non-terminating cycle — return false.
- **Time:** O(log n) per step, bounded steps — values shrink quickly toward small cycles.
- **Space:** O(1) with two pointers (O(k) with a seen-set).

## 9. Plus One  ·  _Easy_

**Scenario:** A very large number is written one digit per card, left to right, with the most significant digit first. You need to add exactly one to this number and show the updated row of digit cards, handling any carry that ripples leftward (and possibly needs a brand-new leading card). What is the new row?

- **Maps to:** Digit-array increment with carry propagation (Plus One).
- **Model it:** Add one to a number represented as an array of digits.
- **Approach & variations:**
  - Walk from the last digit: if it's less than 9, increment and return.
  - If it's 9, set it to 0 and carry left to the next digit.
  - If every digit was 9, prepend a leading 1 (e.g. 999 -> 1000).
- **Time:** O(n) — at most one pass across the digits.
- **Space:** O(1) extra, or O(n) if a new leading digit forces a new array.

## 10. Roman to Integer  ·  _Easy_

**Scenario:** An old inscription writes quantities with letter-symbols of fixed values, largest to smallest, except that a smaller symbol placed just before a larger one means subtract it (like the notation for four or nine). Read the inscription and give its ordinary numeric value.

- **Maps to:** Left-to-right scan with subtractive-pair rule (Roman to Integer).
- **Model it:** Convert a Roman numeral string to its integer value.
- **Approach & variations:**
  - Map each symbol to its value.
  - Scan left to right; if a symbol's value is less than the next symbol's, subtract it, otherwise add it.
  - Equivalently sum all values then subtract twice each smaller-before-larger symbol.
- **Time:** O(n) — one pass over the symbols.
- **Space:** O(1) — a fixed symbol-value table.

## 11. Pow(x, n)  ·  _Medium_

**Scenario:** A biologist has a colony that multiplies by a fixed factor each generation, and wants the growth multiplier after a given whole number of generations — which might be negative, meaning going backwards in time. She wants the answer far faster than multiplying the factor by itself one generation at a time. What is the multiplier?

- **Maps to:** Fast exponentiation by squaring (Pow(x, n)).
- **Model it:** Compute x raised to the integer power n efficiently.
- **Approach & variations:**
  - Square the base and halve the exponent each step; multiply the result in when the current exponent bit is odd.
  - For a negative exponent, invert the base and use the positive magnitude.
  - Handles n via its binary representation, so log-many multiplications instead of n.
- **Time:** O(log n) — exponent halves each step.
- **Space:** O(1) iterative (O(log n) if written recursively).

## 12. Multiply Strings  ·  _Medium_

**Scenario:** Two enormous numbers are each written out digit by digit on paper strips — too big to fit in any calculator. Multiply them together using only grade-school long multiplication on the digits, and write the product as a new strip of digits. What is the product strip?

- **Maps to:** Grade-school multiplication into a positional digit buffer (Multiply Strings).
- **Model it:** Multiply two non-negative integers given as digit strings without using big-integer types.
- **Approach & variations:**
  - Allocate a result buffer of size len(a)+len(b).
  - Multiply each digit pair; digit i of a times digit j of b contributes to positions i+j and i+j+1.
  - Accumulate with carries into those positions, then strip leading zeros; handle the '0' product case.
- **Time:** O(n·m) — every digit pair multiplied once.
- **Space:** O(n + m) — the product digit buffer.

## 13. Detect Squares  ·  _Medium_

**Scenario:** A surveyor keeps dropping pins on a flat map (the same spot can get several pins over time). At any moment you may point at a spot and ask: how many axis-aligned squares can be formed using three already-placed pins together with this queried spot as the four corners, counting multiplicities from repeated pins?

- **Maps to:** Point-count map keyed by coordinate, enumerate diagonal partners (Detect Squares).
- **Model it:** Support adding points and, for a query point, counting axis-aligned squares using stored points as the other three corners.
- **Approach & variations:**
  - Store a count per exact coordinate (plus optionally points grouped by x).
  - For a query, iterate candidate diagonal-opposite points sharing neither coordinate but forming a square (equal side lengths).
  - Multiply the counts of the query's two adjacent corners and the diagonal corner, summing over all valid squares.
  - Repeated identical points multiply the counts — hence a count map, not a set.
- **Time:** add O(1); query O(n) — scanning stored points sharing the query's x.
- **Space:** O(n) — the coordinate count map.

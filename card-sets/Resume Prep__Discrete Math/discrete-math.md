---
deck: "Resume Prep::Discrete Math"
topic: "Discrete Math"
tags: [ankicardmaker, resume-prep, discrete-math]
note_type: Mixed (Basic / Basic (and reversed card) / Cloze)
created: 2026-09-09
---

# Discrete Math — Resume Prep

Source of truth for the `Resume Prep::Discrete Math` deck (14 notes). Edit here and re-push to update.

## Basic cards

1. **Q:** What is a set, in the mathematical sense?
   **A:** An unordered collection of distinct elements, with no duplicates (e.g. {1, 2, 3}).

2. **Q:** Union (A &cup; B) vs. Intersection (A &cap; B) *(reversed — tested both ways)*
   **A:** Union = elements in A <b>or</b> B (or both). Intersection = elements in <b>both</b> A and B.

3. **Q:** For the implication p &rarr; q, under what condition is it false?
   **A:** Only when p is true and q is false. In every other case (p false, regardless of q) the implication is true ("vacuously true").

4. **Q:** What is the contrapositive of "p &rarr; q", and is it logically equivalent to the original?
   **A:** The contrapositive is "&not;q &rarr; &not;p". Yes &mdash; it is always logically equivalent to the original implication, which is why proofs often prove the contrapositive instead.

5. **Q:** What are the converse and inverse of "p &rarr; q", and are they equivalent to it?
   **A:** Converse: "q &rarr; p". Inverse: "&not;p &rarr; &not;q". Neither is logically equivalent to the original implication (though they are equivalent to each other).

6. **Q:** What is the formula for the number of permutations of r items chosen from n distinct items (order matters)?
   **A:** P(n, r) = n! / (n &minus; r)!

7. **Q:** What is the formula for the number of combinations of r items chosen from n distinct items (order doesn't matter)?
   **A:** C(n, r) = n! / (r! (n &minus; r)!)

8. **Q:** What is the key question that distinguishes when to use permutations vs. combinations?
   **A:** Does order matter? If arranging "ABC" differently from "BAC" counts as a different outcome, use permutations; if not (they're the same selection), use combinations.

9. **Q:** What is the degree of a vertex in a graph?
   **A:** The number of edges incident to that vertex (for a directed graph, split into in-degree and out-degree).

10. **Q:** What is the difference between a directed graph and an undirected graph?
   **A:** In a directed graph, each edge has a direction (an ordered pair, A &rarr; B does not imply B &rarr; A). In an undirected graph, edges are bidirectional/unordered (A&mdash;B implies B&mdash;A).

11. **Q:** What does "a mod n" (a modulo n) compute?
   **A:** The remainder when integer a is divided by n; the result always lies in the range [0, n &minus; 1].

12. **Q:** What is the difference between a relation and a function, both from set A to set B?
   **A:** A relation is any subset of A &times; B (any pairing at all). A function is a relation where <b>every</b> element of A maps to <b>exactly one</b> element of B.

## Cloze cards

- A proof by induction has two parts: the {{c1::base case}} (prove the statement holds for the smallest value, e.g. n = 0 or 1) and the {{c2::inductive step}} (assume it holds for n = k, then prove it holds for n = k + 1).
- In increasing order of growth rate, common Big-O classes are: {{c1::O(1)}} constant, {{c2::O(log n)}} logarithmic, {{c3::O(n)}} linear, {{c4::O(n log n)}} linearithmic, {{c5::O(n&sup2;)}} quadratic, {{c6::O(2&sup n;)}} exponential. <!-- Back Extra: Note: the exponential term renders as O(2^n). -->

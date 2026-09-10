---
deck: "Resume Prep::Data Structures & Algorithms"
topic: "Data Structures & Algorithms"
tags: [ankicardmaker, resume-prep, dsa]
note_type: Mixed (Basic / Basic (and reversed card) / Cloze)
created: 2026-09-09
---

# Data Structures & Algorithms — Resume Prep

Source of truth for the `Resume Prep::Data Structures & Algorithms` deck (22 notes). Edit here and re-push to update.

## Basic cards

1. **Q:** What is the time complexity of accessing an element in an array by index?
   **A:** O(1) &mdash; arrays support direct address calculation (<code>base + index * elementSize</code>).

2. **Q:** What is the time complexity of inserting a new node at the <b>head</b> of a singly linked list?
   **A:** O(1) &mdash; you just repoint the head pointer, no shifting required.

3. **Q:** What is the time complexity of accessing the k-th element of a singly linked list by index?
   **A:** O(n) &mdash; there is no random access; you must traverse node-by-node from the head.

4. **Q:** Stack *(reversed — tested both ways)*
   **A:** A LIFO (Last-In, First-Out) data structure supporting <code>push</code> and <code>pop</code> from the same end.

5. **Q:** Queue *(reversed — tested both ways)*
   **A:** A FIFO (First-In, First-Out) data structure supporting <code>enqueue</code> at the back and <code>dequeue</code> from the front.

6. **Q:** What is the time and space complexity of <code>push</code>/<code>pop</code> on an array-backed stack of n elements?
   **A:** Time: O(1) per operation (amortized, due to occasional resizing). Space: O(n) total for the stack's contents.

7. **Q:** What is the average-case time complexity of lookup, insert, and delete on a hash table?
   **A:** O(1) average case &mdash; the hash function maps keys to buckets directly.

8. **Q:** What is the worst-case time complexity of a hash table lookup, and what causes it?
   **A:** O(n) &mdash; happens when many keys collide into the same bucket (e.g. a poor hash function), degrading a bucket into a linear list/chain.

9. **Q:** What are the two main strategies for resolving hash collisions?
   **A:** <b>Chaining</b> &mdash; each bucket holds a linked list (or tree) of colliding entries.<br><b>Open addressing</b> &mdash; on collision, probe for another empty slot in the table itself (e.g. linear/quadratic probing, double hashing).

10. **Q:** What is the time complexity of search, insert, and delete on a <b>balanced</b> binary search tree vs. a <b>degenerate/unbalanced</b> one (e.g. sorted-order inserts with no rebalancing)?
   **A:** Balanced: O(log n) &mdash; height stays ~log n.<br>Degenerate: O(n) &mdash; the tree collapses into a linked list.

11. **Q:** What is the time complexity of inserting into, or extracting the min/max from, a binary heap of n elements?
   **A:** O(log n) &mdash; the new/last element sifts up or down at most the height of the tree.

12. **Q:** What underlying data structure does BFS use to visit nodes, and what does DFS use?
   **A:** BFS uses a <b>queue</b> (FIFO) to explore level by level. DFS uses a <b>stack</b> (explicit, or the call stack via recursion) to explore one branch fully before backtracking.

13. **Q:** In an unweighted graph, which traversal (BFS or DFS) is guaranteed to find the shortest path between two nodes?
   **A:** BFS &mdash; it explores nodes in increasing distance from the source, so the first time it reaches a node is via a shortest path.

14. **Q:** What is the time and space complexity of BFS/DFS on a graph with V vertices and E edges (adjacency list)?
   **A:** Time: O(V + E). Space: O(V) for the visited set plus the queue/stack/recursion depth.

15. **Q:** What precondition does binary search require on its input, and what is its time complexity?
   **A:** The array must be <b>sorted</b>. Time complexity: O(log n) &mdash; each comparison halves the search space.

16. **Q:** What is quicksort's average-case and worst-case time complexity, and is it stable?
   **A:** Average: O(n log n). Worst case: O(n&sup2;) (e.g. already-sorted input with a naive pivot choice). Not stable by default (equal elements can be reordered during partitioning).

17. **Q:** What is merge sort's time complexity (best/avg/worst) and space complexity, and is it stable?
   **A:** Time: O(n log n) in all cases (always splits and merges the full input). Space: O(n) for the merge buffers. Stable &mdash; equal elements keep their relative order.

18. **Q:** What is heap sort's time and space complexity, and is it stable?
   **A:** Time: O(n log n) in all cases. Space: O(1) extra (sorts in place). Not stable &mdash; swaps during heapify can reorder equal elements.

19. **Q:** In terms of memory, what is the main tradeoff of writing an algorithm recursively instead of iteratively?
   **A:** Recursion consumes O(depth) extra space on the call stack for pending stack frames; a well-written iterative version can often do the same work in O(1) extra space.

20. **Q:** What two properties must a problem have for dynamic programming to apply?
   **A:** <b>Overlapping subproblems</b> (the same subproblems recur) and <b>optimal substructure</b> (an optimal solution is built from optimal solutions to subproblems).

## Cloze cards

- Big-O notation describes the {{c1::upper bound}} (worst-case growth rate) of an algorithm's time or space requirements as input size <code>n</code> grows.
- In a {{c1::min-heap}}, every parent node is less than or equal to its children (root is the minimum); in a {{c2::max-heap}}, every parent is greater than or equal to its children (root is the maximum). <!-- Back Extra: A heap is a complete binary tree, usually array-backed. -->

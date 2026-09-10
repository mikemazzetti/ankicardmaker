---
deck: "NeetCode 250::Trees"
topic: "NeetCode 250 — Trees"
tags: [ankicardmaker, neetcode250, trees]
note_type: Basic
created: 2026-09-09
---

# NeetCode 250 — Trees

Story front hides the technique; back reveals the mapping, approach, and complexity.

## 1. Binary Tree Inorder Traversal  ·  _Easy_

**Scenario:** A family estate branches downward, each ancestor having at most a left heir and a right heir. List everyone by this rule applied at every level: fully list the left branch, then the ancestor, then the right branch. Produce that ordering.

- **Maps to:** Inorder depth-first traversal (Binary Tree Inorder Traversal).
- **Model it:** Output the tree's values in left-root-right order.
- **Approach & variations:**
  - Recurse left, visit the node, recurse right.
  - The iterative version pushes lefts onto a stack, then pops to visit and turn right.
  - For a search tree this yields sorted order.
- **Time:** O(n) — every node visited once.
- **Space:** O(h) — recursion/stack depth equals the height.

## 2. Binary Tree Preorder Traversal  ·  _Easy_

**Scenario:** A family estate branches downward, each ancestor having at most a left and a right heir. List everyone by this rule at every level: name the ancestor first, then the whole left branch, then the whole right branch.

- **Maps to:** Preorder depth-first traversal (Binary Tree Preorder Traversal).
- **Model it:** Output the tree's values in root-left-right order.
- **Approach & variations:**
  - Visit the node, recurse left, recurse right.
  - The iterative version pushes the right child before the left onto a stack.
  - Natural for copying or top-down serialization of the structure.
- **Time:** O(n) — one visit per node.
- **Space:** O(h) — stack/recursion depth.

## 3. Binary Tree Postorder Traversal  ·  _Easy_

**Scenario:** A family estate branches downward, each ancestor having at most a left and a right heir. List everyone by this rule at every level: the whole left branch, then the whole right branch, and only then the ancestor themselves.

- **Maps to:** Postorder depth-first traversal (Binary Tree Postorder Traversal).
- **Model it:** Output the tree's values in left-right-root order.
- **Approach & variations:**
  - Recurse left, recurse right, then visit the node.
  - Iterative: reverse a modified root-right-left preorder, or use two stacks.
  - Natural for freeing/processing children before their parent.
- **Time:** O(n) — one visit per node.
- **Space:** O(h) — recursion/stack depth.

## 4. Invert Binary Tree  ·  _Easy_

**Scenario:** You have a branching family chart where everyone has at most a left and a right heir. Produce its mirror image: at every ancestor, swap the entire left branch with the entire right branch, all the way down.

- **Maps to:** Recursive subtree swap (Invert Binary Tree).
- **Model it:** Mirror a binary tree by swapping left and right children at every node.
- **Approach & variations:**
  - At each node swap its two children, then recurse into both.
  - Works with either depth-first or breadth-first order.
  - Base case: an empty spot returns itself.
- **Time:** O(n) — visits each node once.
- **Space:** O(h) — recursion depth.

## 5. Maximum Depth of Binary Tree  ·  _Easy_

**Scenario:** A branching family chart hangs from a single founder at the top, each person having at most two heirs below. How many generations deep does the longest lineage run, counting from the founder down to the most distant descendant?

- **Maps to:** Depth-first (or level) height computation (Maximum Depth of Binary Tree).
- **Model it:** Return the number of nodes on the longest root-to-leaf path.
- **Approach & variations:**
  - Depth = 1 + max(depth of left, depth of right).
  - An empty spot contributes depth 0.
  - Counting levels with a queue works equally well.
- **Time:** O(n) — every node examined.
- **Space:** O(h) — recursion stack.

## 6. Diameter of Binary Tree  ·  _Easy_

**Scenario:** In a branching family chart, pick any two people and trace the chain of relatives connecting them upward through a shared ancestor and back down. What is the largest number of steps in the longest such connecting chain found anywhere in the whole chart?

- **Maps to:** DFS returning height while tracking the best split (Diameter of Binary Tree).
- **Model it:** Find the longest path, in edges, between any two nodes of a binary tree.
- **Approach & variations:**
  - At each node the candidate path length is left height + right height.
  - Recurse returning height, updating a global maximum of that sum.
  - The best path need not pass through the top ancestor.
- **Time:** O(n) — one DFS.
- **Space:** O(h) — recursion depth.

## 7. Balanced Binary Tree  ·  _Easy_

**Scenario:** A branching family chart is 'well-proportioned' if, for every single person in it, their left lineage and right lineage never differ in depth by more than one generation. Decide whether the whole chart is well-proportioned.

- **Maps to:** Bottom-up height check (Balanced Binary Tree).
- **Model it:** Check that at every node the two subtree heights differ by at most 1.
- **Approach & variations:**
  - A DFS returns each subtree's height, or a sentinel once an imbalance is found below.
  - At each node compare left and right heights and bail out early if the gap exceeds 1.
  - Naive top-down recomputation is O(n^2); this bottom-up pass is O(n).
- **Time:** O(n) — each height computed once.
- **Space:** O(h) — recursion depth.

## 8. Same Tree  ·  _Easy_

**Scenario:** Two branching family charts are drawn on separate sheets. Decide whether they are truly identical: the same shape and the same name at every matching position, checked all the way down.

- **Maps to:** Parallel depth-first comparison (Same Tree).
- **Model it:** Determine whether two binary trees are structurally identical with equal values.
- **Approach & variations:**
  - Compare the current pair, then recurse on left-with-left and right-with-right.
  - Both empty means equal; one empty or values differing means not equal.
  - Any mismatch short-circuits to false.
- **Time:** O(n) — matching nodes visited once.
- **Space:** O(h) — recursion depth.

## 9. Subtree of Another Tree  ·  _Easy_

**Scenario:** You have a big branching family chart and a small one. Decide whether the small chart appears intact somewhere inside the big one: some person in the big chart, together with everyone below them, exactly matches the small chart in both shape and names.

- **Maps to:** DFS plus a same-tree check at each node (Subtree of Another Tree).
- **Model it:** Check whether tree t equals some subtree rooted inside tree s.
- **Approach & variations:**
  - At each node of s, run an identical-tree test against t.
  - Recurse down s until a match is found or s is exhausted.
  - Alternative: serialize both and substring-search for O(n+m).
- **Time:** O(n*m) naive — a same-tree check at each of n nodes.
- **Space:** O(h) — recursion depth.

## 10. Lowest Common Ancestor of a Binary Search Tree  ·  _Medium_

**Scenario:** In an org chart where every manager's left-hand reports carry smaller badge numbers and right-hand reports carry larger ones, two employees are named. Find their lowest common boss, the deepest manager who oversees both, using the badge-number ordering to steer your descent.

- **Maps to:** Ordered descent using the search-tree property (Lowest Common Ancestor of a BST).
- **Model it:** Find the lowest common ancestor of two nodes in a binary search tree.
- **Approach & variations:**
  - Start at the top; if both targets are smaller go left, if both are larger go right.
  - The first node where the two targets split (or that equals one target) is the answer.
  - The ordering avoids any full search.
- **Time:** O(h) — one root-to-split descent.
- **Space:** O(1) — an iterative pointer walk.

## 11. Insert into a Binary Search Tree  ·  _Medium_

**Scenario:** In a directory where each entry sends smaller keys left and larger keys right, you receive a new key guaranteed not already present. Place it so the left-smaller / right-larger rule still holds everywhere, adding it as a new bottom entry.

- **Maps to:** Search-tree insertion by descent (Insert into a BST).
- **Model it:** Insert a value into a binary search tree and return the new root.
- **Approach & variations:**
  - Descend left or right by comparing the new key to each entry.
  - When the next step is empty, attach the new entry there.
  - A plain search tree needs no rebalancing.
- **Time:** O(h) — one descent to an empty spot.
- **Space:** O(h) recursive, O(1) iterative.

## 12. Delete Node in a BST  ·  _Medium_

**Scenario:** In a directory where smaller keys go left and larger keys go right, remove a given key while keeping that ordering intact everywhere. The tricky case: the removed entry has branches on both sides, so who takes its place?

- **Maps to:** Search-tree deletion with successor swap (Delete Node in a BST).
- **Model it:** Delete a key from a binary search tree and return a still-valid root.
- **Approach & variations:**
  - Find the entry; with zero or one branch, splice it out directly.
  - With two branches, replace its value with the in-order successor (smallest on its right), then delete that successor.
  - The in-order predecessor works symmetrically.
- **Time:** O(h) — a search plus a successor find.
- **Space:** O(h) — recursion depth.

## 13. Binary Tree Level Order Traversal  ·  _Medium_

**Scenario:** A branching family chart hangs from one founder. List everyone generation by generation: the top row first, reading left to right within each generation, then the next generation, and so on.

- **Maps to:** Breadth-first traversal by levels (Binary Tree Level Order Traversal).
- **Model it:** Return node values grouped by depth level, top to bottom.
- **Approach & variations:**
  - Use a queue and finish the current level before starting the next.
  - Record each level's size so you know where it ends.
  - Enqueue the left child, then the right child.
- **Time:** O(n) — each node enqueued once.
- **Space:** O(n) — the queue can hold a full level.

## 14. Binary Tree Right Side View  ·  _Medium_

**Scenario:** You stand to the right of a branching family chart and can see, in each generation, only the person standing furthest to the right. Reading top to bottom, who do you see?

- **Maps to:** BFS taking the last node of each level (Binary Tree Right Side View).
- **Model it:** Return the rightmost node value at each depth of a binary tree.
- **Approach & variations:**
  - Level-order traverse and keep the last node seen at each level.
  - Or DFS visiting the right child first, recording the first node reached at each new depth.
  - A missing right branch falls through to a visible left one.
- **Time:** O(n) — every node visited.
- **Space:** O(n) — queue or recursion.

## 15. Construct Quad Tree  ·  _Medium_

**Scenario:** You have a square grid of black and white tiles whose side is a power of two. Compress it: if a square region is all one color, record it as a single solid block; otherwise split it into four equal quadrants and describe each the same way, recursively. Produce that nested description.

- **Maps to:** Recursive quadrant subdivision (Construct Quad Tree).
- **Model it:** Build a quad tree from an n x n grid of 0/1 cells, merging uniform regions into leaves.
- **Approach & variations:**
  - If the current square is uniform, make a solid leaf with that value.
  - Otherwise split into four sub-squares and recurse on each.
  - Merge four same-valued leaves back into one leaf.
- **Time:** O(n^2 log n) — each cell is touched at each subdivision level.
- **Space:** O(log n) recursion depth, plus the output.

## 16. Count Good Nodes In Binary Tree  ·  _Medium_

**Scenario:** Along each downward lineage in a branching chart starting from the founder, a person is 'notable' if nobody above them on that same path has a greater value. Count how many notable people the whole chart contains.

- **Maps to:** DFS carrying the max-so-far (Count Good Nodes in Binary Tree).
- **Model it:** Count nodes whose value is at least the maximum value on the path from the root to them.
- **Approach & variations:**
  - DFS downward, passing along the largest value seen so far on the path.
  - A node counts when its value is greater than or equal to that running maximum.
  - Update the maximum before recursing into the children.
- **Time:** O(n) — one DFS pass.
- **Space:** O(h) — recursion depth.

## 17. Validate Binary Search Tree  ·  _Medium_

**Scenario:** Someone claims a directory obeys the rule that everything in a person's left branch is smaller than them and everything in their right branch is larger, not just the immediate children but every descendant beneath. Verify the claim holds everywhere.

- **Maps to:** DFS with (low, high) bounds (Validate Binary Search Tree).
- **Model it:** Check whether a binary tree satisfies the global search-tree ordering property.
- **Approach & variations:**
  - Pass an allowed open interval (low, high) downward; each node must fall strictly inside.
  - Going left tightens the upper bound; going right tightens the lower bound.
  - Alternatively, an in-order traversal must be strictly increasing.
- **Time:** O(n) — each node validated once.
- **Space:** O(h) — recursion depth.

## 18. Kth Smallest Element In a Bst  ·  _Medium_

**Scenario:** In a directory where smaller keys sit left and larger keys sit right, find the entry holding the k-th smallest key, ideally without listing them all.

- **Maps to:** In-order traversal stopping at the k-th element (Kth Smallest Element in a BST).
- **Model it:** Return the k-th smallest value in a binary search tree.
- **Approach & variations:**
  - An in-order traversal yields the keys in increasing order; stop at the k-th.
  - Use an explicit stack to halt early rather than traversing everything.
  - For many repeated queries, augment each node with its subtree count.
- **Time:** O(h + k) — descend, then pop k times.
- **Space:** O(h) — stack depth.

## 19. Construct Binary Tree From Preorder And Inorder Traversal  ·  _Medium_

**Scenario:** You are given two guest lists describing the same branching seating chart. One was recorded by always naming a host before their two sub-groups; the other by naming the left sub-group, then the host, then the right sub-group. Reconstruct the exact chart.

- **Maps to:** Recursive split using the preorder root to partition the inorder list (Construct Binary Tree from Preorder and Inorder Traversal).
- **Model it:** Rebuild a binary tree from its preorder and inorder traversals.
- **Approach & variations:**
  - The next preorder value is the current root; locate it in the inorder list to split left from right.
  - The left inorder segment's size determines how much of preorder forms the left subtree; recurse.
  - A value->index map on the inorder list makes each lookup O(1).
- **Time:** O(n) — each node placed once with hashed lookups.
- **Space:** O(n) — the index map plus recursion.

## 20. House Robber III  ·  _Medium_

**Scenario:** A crime spree is planned over a branching chart of houses. Robbing a house earns its stash, but you may never rob a house together with either of the two houses directly linked just below it on the same night. Maximize the total loot across the whole chart.

- **Maps to:** Tree DP returning (rob, skip) pairs (House Robber III).
- **Model it:** Choose a maximum-sum set of tree nodes such that no chosen node is a parent of another.
- **Approach & variations:**
  - Each node returns two totals: the best if it is robbed and the best if it is skipped.
  - Robbed = value + children's skipped totals; skipped = sum of each child's better option.
  - The answer is the top node's max of its two totals.
- **Time:** O(n) — a single post-order pass.
- **Space:** O(h) — recursion depth.

## 21. Delete Leaves With a Given Value  ·  _Medium_

**Scenario:** In a branching chart, repeatedly snip off any dead-end person (nobody below them) whose value equals a target. Snipping one may expose a new dead-end above with the same value, which must then also go. Produce the final pruned chart.

- **Maps to:** Post-order pruning with cascade (Delete Leaves With a Given Value).
- **Model it:** Remove all leaves equal to target, cascading upward, from a binary tree.
- **Approach & variations:**
  - Recurse into both children first, then re-examine the current node.
  - After pruning, if the node is now a dead-end and equals target, delete it (return empty).
  - Post-order makes the upward cascade automatic in one pass.
- **Time:** O(n) — one post-order pass.
- **Space:** O(h) — recursion depth.

## 22. Binary Tree Maximum Path Sum  ·  _Hard_

**Scenario:** Along a branching chart, a 'route' is any connected chain of people that bends through at most one shared high point and never revisits anyone. Each person carries a value that may be negative. Find the route with the greatest total value anywhere in the chart.

- **Maps to:** DFS returning the best downward gain while tracking a global best (Binary Tree Maximum Path Sum).
- **Model it:** Find the maximum-sum path between any two nodes in a binary tree.
- **Approach & variations:**
  - Each node returns its best single-sided downward sum, clamped at 0.
  - At each node consider value + left gain + right gain as a route apex, updating a global maximum.
  - Return only value + the better one side upward, since a route cannot split twice.
- **Time:** O(n) — one post-order pass.
- **Space:** O(h) — recursion depth.

## 23. Serialize And Deserialize Binary Tree  ·  _Hard_

**Scenario:** You must flatten a branching family chart into a single written string you can text to a friend, such that they can rebuild the identical chart, exact shape and names and empty spots included, from your string alone. Design both the encoding and the rebuild.

- **Maps to:** Preorder encoding with empty-markers, plus a queue-driven decode (Serialize and Deserialize Binary Tree).
- **Model it:** Convert a binary tree to a string and reconstruct it losslessly.
- **Approach & variations:**
  - Preorder DFS writing each value and a marker for every empty child.
  - Rebuild by consuming tokens in the same preorder, recursing when a real value appears and stopping on markers.
  - A level-order encoding with markers works equivalently.
- **Time:** O(n) — each node written and read once.
- **Space:** O(n) — the string plus recursion/queue.

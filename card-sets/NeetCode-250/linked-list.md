---
deck: "NeetCode 250::Linked List"
topic: "NeetCode 250 — Linked List"
tags: [ankicardmaker, neetcode250, linked-list]
note_type: Basic
created: 2026-09-09
---

# NeetCode 250 — Linked List

Story front hides the technique; back reveals the mapping, approach, and complexity.

## 1. Reverse Linked List  ·  _Easy_

**Scenario:** A line of children hold hands in single file, and each child only knows who is directly ahead. You want the whole line to face the other way, so the last child becomes the leader and the leader becomes the tail. How do you flip who-holds-whom, one clasp at a time, without lining them up somewhere else?

- **Maps to:** Iterative pointer reversal (Reverse Linked List).
- **Model it:** Given a singly linked list head, reverse the next-pointers so the old tail becomes the head.
- **Approach & variations:**
  - Walk once keeping `prev`, `curr`, and a saved `next`.
  - At each node point `curr.next` back to `prev`, then advance all three.
  - Recursion works too but adds call-stack depth.
- **Time:** O(n) — a single pass over every node.
- **Space:** O(1) — three reused pointers (recursive is O(n) stack).

## 2. Merge Two Sorted Lists  ·  _Easy_

**Scenario:** Two separate single-file lines of runners are each already ordered shortest to tallest. You must weave them into one single line, still ordered shortest to tallest, without measuring anyone twice or copying the lines aside. How do you interleave them?

- **Maps to:** Two-pointer merge (Merge Two Sorted Lists).
- **Model it:** Given two sorted linked lists, splice their nodes into one sorted list.
- **Approach & variations:**
  - Use a dummy head; compare the two front nodes, attach the smaller, advance that list.
  - When one list empties, attach the remainder of the other whole.
  - Reuses existing nodes, so no new allocation is needed.
- **Time:** O(n+m) — each node visited once.
- **Space:** O(1) — pointer splicing, ignoring the output list.

## 3. Linked List Cycle  ·  _Easy_

**Scenario:** You follow a trail of signposts, each pointing to the next place to visit. You suspect the trail secretly loops back on itself, so you would wander forever. Carrying no map and remembering only where you currently stand, how do you decide whether the trail eventually loops?

- **Maps to:** Floyd's fast/slow pointers (Linked List Cycle).
- **Model it:** Detect whether a linked list contains a cycle using no extra memory.
- **Approach & variations:**
  - Move a slow walker one step and a fast walker two steps.
  - If they ever stand together a loop exists; if the fast one reaches the end, there is none.
  - A visited-set also works but costs O(n) space.
- **Time:** O(n) — the fast pointer laps the loop in linear steps.
- **Space:** O(1) — two pointers.

## 4. Reorder List  ·  _Medium_

**Scenario:** Guests are seated in one long row numbered 1,2,3,...,n. You must reseat them as first, last, second, second-last, third, third-last, alternating inward from each end. You may only change who sits next to whom, not copy the whole row elsewhere. How?

- **Maps to:** Find middle + reverse second half + merge (Reorder List).
- **Model it:** Rearrange a linked list L0->L1->...->Ln into L0->Ln->L1->Ln-1->...
- **Approach & variations:**
  - Find the middle with slow/fast pointers.
  - Reverse the second half in place.
  - Zip the two halves together, alternating one node from each.
- **Time:** O(n) — three linear passes.
- **Space:** O(1) — in-place pointer surgery.

## 5. Remove Nth Node From End of List  ·  _Medium_

**Scenario:** A conga line snakes through a hall and you must pull out exactly the person who is Nth-from-the-back. You may only walk forward from the front, and you do not know the line's length beforehand. How do you find and remove them in a single walk?

- **Maps to:** Two pointers with a fixed gap (Remove Nth Node From End of List).
- **Model it:** Delete the Nth-from-end node of a linked list in one pass.
- **Approach & variations:**
  - Advance a lead pointer N steps first.
  - Move lead and a trailing pointer together until lead hits the end; trailing now sits just before the target.
  - Use a dummy head so removing the first person is handled cleanly.
- **Time:** O(n) — a single traversal.
- **Space:** O(1) — two pointers.

## 6. Copy List With Random Pointer  ·  _Medium_

**Scenario:** You must duplicate a scavenger-hunt trail where each clue points to the next clue AND also to one arbitrary other clue somewhere in the hunt. Your copy must mirror both kinds of pointing exactly, even though the arbitrary links may jump anywhere. How?

- **Maps to:** Hash map old->new, or interleaved cloning (Copy List With Random Pointer).
- **Model it:** Deep-copy a linked list where each node has a next pointer and a random pointer to any node.
- **Approach & variations:**
  - Map each original node to its clone, then wire next/random through the map.
  - O(1)-space trick: weave clones right after originals, set randoms via `orig.next`, then unweave.
  - Handle null random pointers.
- **Time:** O(n) — a constant number of passes over the nodes.
- **Space:** O(n) with a map, or O(1) with interleaving.

## 7. Add Two Numbers  ·  _Medium_

**Scenario:** Two people each hand you a number written on a strip of tape, but with the digits laid out backwards, ones-place first. Reading each strip front to back, produce a new backwards strip that is their sum, carrying as you go. How?

- **Maps to:** Elementary addition with carry (Add Two Numbers).
- **Model it:** Two linked lists hold a number's digits in reverse order; return their sum as a linked list.
- **Approach & variations:**
  - Walk both lists together, adding matching digits plus a running carry.
  - Each new node holds sum mod 10; the carry is sum/10.
  - Continue while either list remains or the carry is nonzero.
- **Time:** O(max(n,m)) — one pass over the longer number.
- **Space:** O(max(n,m)) — the result list.

## 8. Find The Duplicate Number  ·  _Medium_

**Scenario:** In a sealed room are n+1 raffle tickets whose numbers all fall between 1 and n, so at least one number must repeat. You may not alter the tickets and may hold only a couple at a time. Treat each ticket's number as an address pointing to another ticket, and find the repeated number.

- **Maps to:** Floyd's cycle detection on value-as-index (Find the Duplicate Number).
- **Model it:** In an array of n+1 values in [1,n], find the duplicate by treating each value as a next-pointer.
- **Approach & variations:**
  - Following value->index links forms a chain that must cycle, and the cycle's entrance is the duplicate.
  - Use slow/fast to find a meeting point, then walk from the start to find the entrance.
  - Avoids modifying the tickets and uses O(1) space.
- **Time:** O(n) — linear cycle detection.
- **Space:** O(1) — two indices.

## 9. Reverse Linked List II  ·  _Medium_

**Scenario:** A single-file parade stretches down the street. You must flip the order of just the runners from the 3rd through the 7th position, leaving everyone before and after exactly where they stand, only re-linking who follows whom. How?

- **Maps to:** In-place sublist reversal (Reverse Linked List II).
- **Model it:** Reverse only the nodes of a linked list between positions left and right.
- **Approach & variations:**
  - Walk to the node just before position left, using a dummy head.
  - Reverse the segment by repeatedly moving the next node to the front of the segment.
  - Reconnect the reversed segment's ends to the untouched parts.
- **Time:** O(n) — one pass to the region and through it.
- **Space:** O(1) — reversed in place.

## 10. Design Circular Queue  ·  _Medium_

**Scenario:** You run a small valet stand with exactly k parking spots arranged in a ring. Cars enter at the tail and leave from the front; when you reach the last spot you wrap around to reuse freed early spots. Design the controls to add, remove, peek at both ends, and report full or empty.

- **Maps to:** Fixed-size ring buffer (Design Circular Queue).
- **Model it:** Implement a circular queue supporting enqueue, dequeue, front, rear, isFull, isEmpty.
- **Approach & variations:**
  - Fixed array with a head index and a running count (or head/tail with modular arithmetic).
  - Wrap indices using modulo k.
  - Full when count == k; empty when count == 0.
- **Time:** O(1) — every operation is index arithmetic.
- **Space:** O(k) — the fixed buffer.

## 11. LRU Cache  ·  _Medium_

**Scenario:** A tiny museum room can display only k artifacts. Each time a visitor views one it becomes freshest; when a new artifact arrives and the room is full, you retire whichever has gone longest without being viewed. Support instant lookup and instant retirement decisions.

- **Maps to:** Hash map + doubly linked list (LRU Cache).
- **Model it:** Build a fixed-capacity cache with O(1) get and put that evicts the least-recently-used key.
- **Approach & variations:**
  - A doubly linked list orders items by recency; a map from key to node gives O(1) access.
  - On get/put, move the node to the front (most recent).
  - When over capacity, drop the tail node and its map entry.
- **Time:** O(1) — map lookup plus constant list splicing.
- **Space:** O(k) — capacity nodes plus the map.

## 12. LFU Cache  ·  _Hard_

**Scenario:** A boutique shelf holds only k items. When it overflows you remove the item bought the fewest times ever; if several tie for fewest, you remove whichever of those went longest unbought. Support instant lookup, purchase-count updates, and eviction.

- **Maps to:** Hash maps + frequency buckets of doubly linked lists (LFU Cache).
- **Model it:** Fixed-capacity cache with O(1) get/put evicting the least-frequently-used key, breaking ties by least-recent.
- **Approach & variations:**
  - Map key->node and freq->an ordered list of nodes at that frequency.
  - On access, move the node from its freq list to freq+1 and track a running minFreq.
  - Evict from the minFreq list's least-recent end when full.
- **Time:** O(1) — constant map and list operations.
- **Space:** O(k) — nodes plus frequency structures.

## 13. Merge K Sorted Lists  ·  _Hard_

**Scenario:** You have many separate single-file lines of runners, and each line is already ordered shortest to tallest. Combine all of them into one line, still perfectly ordered, without repeatedly re-measuring everyone. What is the efficient way to keep picking who goes next?

- **Maps to:** Min-heap of list heads, or pairwise merging (Merge K Sorted Lists).
- **Model it:** Merge k sorted linked lists into one sorted list.
- **Approach & variations:**
  - Keep the current front of each list in a min-heap; pop the smallest, then push its successor.
  - Alternatively merge lists pairwise across log k rounds.
  - Both beat merging one list at a time into a growing result.
- **Time:** O(N log k) — N total nodes, each heap op is log k.
- **Space:** O(k) — heap holding one node per list.

## 14. Reverse Nodes In K Group  ·  _Hard_

**Scenario:** A single-file line of soldiers must be re-ordered in blocks of k: reverse the first k, then the next k, and so on. Any final leftover group smaller than k stays as it is. You may only re-link who follows whom. How?

- **Maps to:** Segmented in-place reversal (Reverse Nodes in k-Group).
- **Model it:** Reverse every consecutive group of k nodes in a linked list, leaving a short tail untouched.
- **Approach & variations:**
  - Check that k nodes remain; if not, stop.
  - Reverse the k-block in place and connect it to the previously reversed portion.
  - Continue from the block's new tail; a dummy head simplifies the wiring.
- **Time:** O(n) — each node is reversed once.
- **Space:** O(1) — iterative and in place.

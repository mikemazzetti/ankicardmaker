---
deck: "NeetCode 250::Greedy"
topic: "NeetCode 250 — Greedy"
tags: [ankicardmaker, neetcode250, greedy]
note_type: Basic
created: 2026-09-09
---

# NeetCode 250 — Greedy

Story front hides the technique; back reveals the mapping, approach, and complexity.

## 1. Lemonade Change  ·  _Easy_

**Scenario:** You run a lemonade stand where every cup costs exactly 5 coins. Customers arrive one at a time, each paying with a single 5-, 10-, or 20-coin piece, and you must hand back correct change immediately from only the money earlier customers gave you (you start with nothing). Serve them in order — can you make change for everyone?

- **Maps to:** Greedy cash-drawer simulation (Lemonade Change).
- **Model it:** Track counts of 5s and 10s on hand; for each bill, give change and update, failing if you ever cannot.
- **Approach & variations:**
  - A 5 needs no change; a 10 needs one 5; a 20 needs a 10+5 or three 5s.
  - For a 20, prefer giving a 10+5 over three 5s so the flexible 5s last longer.
  - If the needed change isn't available, return false.
- **Time:** O(n) — one pass over the customers, constant work each.
- **Space:** O(1) — just two running counts of bills.

## 2. Maximum Subarray  ·  _Medium_

**Scenario:** A stock trader has a ledger of daily gains and losses, one number per day. She wants to pick a single unbroken stretch of consecutive days that adds up to the largest total profit possible. What is that best total?

- **Maps to:** Running-sum greedy / Kadane's algorithm (Maximum Subarray).
- **Model it:** Find the contiguous subarray with the largest sum.
- **Approach & variations:**
  - Keep a running sum; if it ever drops below zero, reset it to zero (a negative prefix only hurts).
  - Track the best sum seen so far separately.
  - Equivalent DP: best ending here = value + max(0, best ending previous).
  - Handle all-negative input by seeding the answer with the first element, not zero.
- **Time:** O(n) — a single sweep updating two accumulators.
- **Space:** O(1) — two numbers.

## 3. Maximum Sum Circular Subarray  ·  _Medium_

**Scenario:** Numbers of daily gains and losses are written around the rim of a circular clock face, so the last day wraps back around to touch the first. Pick one unbroken run of consecutive days — possibly one that spans across the wrap point — with the largest total. What is it?

- **Maps to:** Kadane's twice, plus wraparound via total minus minimum (Maximum Sum Circular Subarray).
- **Model it:** Find the max-sum contiguous subarray in a circular array where a run may wrap around the ends.
- **Approach & variations:**
  - Non-wrapping case: ordinary max-subarray (Kadane).
  - Wrapping case: total sum minus the minimum-sum subarray (the leftover ends).
  - Answer is the max of the two, but if all numbers are negative the wrap case gives 0 wrongly — fall back to the plain max.
- **Time:** O(n) — a couple of linear Kadane passes.
- **Space:** O(1) — running sums only.

## 4. Longest Turbulent Subarray  ·  _Medium_

**Scenario:** A hiker records elevation at each step. She wants the longest continuous portion of the trail where the terrain strictly zig-zags — up then down then up, alternating with no two consecutive steps going the same direction and never staying flat. How many steps long is it?

- **Maps to:** Linear scan tracking alternating comparison sign (Longest Turbulent Subarray).
- **Model it:** Find the longest contiguous subarray whose consecutive comparisons alternate < and >.
- **Approach & variations:**
  - Track two run lengths: one ending on a rising step, one on a falling step.
  - On a rise, the up-run extends the previous down-run+1; on a fall, vice versa; equal values reset both to 1.
  - Keep the best length seen.
- **Time:** O(n) — one pass comparing adjacent pairs.
- **Space:** O(1) — two run counters.

## 5. Jump Game  ·  _Medium_

**Scenario:** A frog sits on the first of a row of lily pads. Each pad has a number telling the maximum number of pads forward the frog may leap from it (it can leap any distance up to that). Starting at the leftmost pad, can the frog possibly reach the very last pad?

- **Maps to:** Greedy farthest-reach tracking (Jump Game).
- **Model it:** Given max jump lengths per index, decide if the last index is reachable from index 0.
- **Approach & variations:**
  - Sweep left to right keeping the farthest index reachable so far.
  - If the current index ever exceeds that farthest reach, you're stuck — return false.
  - Update farthest = max(farthest, i + value); succeed if it reaches the end.
- **Time:** O(n) — one linear pass.
- **Space:** O(1) — a single reach value.

## 6. Jump Game II  ·  _Medium_

**Scenario:** A frog again starts on the first lily pad, each pad showing the maximum forward leap allowed from it, and reaching the last pad is guaranteed possible. This time it wants the fewest number of leaps to get there. How few leaps suffice?

- **Maps to:** Greedy BFS-style level expansion (Jump Game II).
- **Model it:** Find the minimum number of jumps to reach the last index given per-index max jump lengths.
- **Approach & variations:**
  - Treat reachable ranges as levels: the current jump covers [start, end].
  - As you scan the current window, track the farthest reachable next; when you hit the window's end, take a jump and extend the window to that farthest.
  - Each window boundary crossed costs one jump.
- **Time:** O(n) — one pass, each index visited once.
- **Space:** O(1) — a few boundary/reach counters.

## 7. Jump Game VII  ·  _Medium_

**Scenario:** A row of stepping stones is painted, each either solid or cracked; the first stone is solid. A frog on a solid stone may hop forward by any distance between a fixed minimum and a fixed maximum, but may only land on solid stones. Starting on the first stone, can it reach the last stone?

- **Maps to:** Reachability via sliding window / prefix count of reachable positions (Jump Game VII).
- **Model it:** Given a binary string and a [minJump, maxJump] range, decide if the last index is reachable landing only on '0's.
- **Approach & variations:**
  - A position is reachable if it's solid and some reachable position lies in the window [i-maxJump, i-minJump].
  - Use a sliding-window count (or prefix sums) of reachable flags to test that window in O(1).
  - Advance the window as i grows; answer is whether the last index is reachable.
- **Time:** O(n) — each index checks a window in amortized O(1).
- **Space:** O(n) — a reachable flag/prefix array.

## 8. Gas Station  ·  _Medium_

**Scenario:** Fuel depots are arranged in a big loop road. At each depot you can pick up a known amount of fuel, and driving from that depot to the next one burns a known amount. You have an empty tank and must complete the full loop in one direction. From which single starting depot can you make it all the way around (if any)?

- **Maps to:** Greedy total-and-running-deficit check (Gas Station).
- **Model it:** Given gas[i] and cost[i] around a circle, find the start index from which a zero-start tank never goes negative.
- **Approach & variations:**
  - If total gas < total cost, it's impossible — return -1.
  - Otherwise a unique valid start exists; sweep once tracking the running tank.
  - Whenever the tank goes negative, the start must be after the current index, so reset start to i+1 and tank to 0.
- **Time:** O(n) — a single loop around the stations.
- **Space:** O(1) — two running totals.

## 9. Hand of Straights  ·  _Medium_

**Scenario:** A card player holds a hand of numbered cards and wants to lay them all down in small groups of a fixed size, where each group must be a run of consecutive numbers (like 6-7-8). Every card must be used and no leftovers allowed. Is it possible to arrange the whole hand this way?

- **Maps to:** Greedy consumption from smallest with counts (Hand of Straights).
- **Model it:** Partition a multiset of integers into groups of size k, each k consecutive values.
- **Approach & variations:**
  - If hand size isn't divisible by the group size, fail immediately.
  - Count occurrences; repeatedly take the smallest remaining value as a run's start.
  - For that start, decrement it and the next k-1 consecutive values; if any is missing, fail.
  - A min-heap or sorted map over the distinct values keeps 'smallest remaining' cheap.
- **Time:** O(n log n) — sorting/heap over the distinct cards drives the cost.
- **Space:** O(n) — the count map of cards.

## 10. Dota2 Senate  ·  _Medium_

**Scenario:** Two rival factions sit in a fixed circular seating order and vote in repeated rounds. On each turn a member may permanently silence one member of the opposing faction, and turns proceed around the circle skipping the silenced. Play always favors banning the very next opponent who would otherwise act. Which faction ends up controlling the vote?

- **Maps to:** Two queues of indices simulating round-robin bans (Dota2 Senate).
- **Model it:** Given a string of 'R'/'D' in turn order, simulate each active member banning the nearest upcoming opponent; report the surviving party.
- **Approach & variations:**
  - Put each faction's positions in its own queue.
  - Repeatedly compare the two front indices: the smaller acts first and bans the other; the acting index goes to the back with n added (next round).
  - Continue until one queue empties — that party wins.
- **Time:** O(n) — each ban removes one member; total work is linear.
- **Space:** O(n) — two queues of indices.

## 11. Merge Triplets to Form Target Triplet  ·  _Medium_

**Scenario:** A gemcutter has several sample stones, each rated on three qualities (cut, color, clarity). He can combine any chosen subset of stones into one blended rating by taking, for each quality, the best value among the combined stones. He wants the blend to exactly match a target rating on all three qualities. Is it achievable?

- **Maps to:** Greedy filtering then per-position max (Merge Triplets to Form Target Triplet).
- **Model it:** Using element-wise max as the merge, decide if some subset of triplets merges exactly to the target triplet.
- **Approach & variations:**
  - Discard any triplet that exceeds the target in any position — it could push a value too high.
  - Among the survivors, check that each of the three positions is matched exactly by at least one triplet.
  - If all three targets are hit, the merge works.
- **Time:** O(n) — one pass over the triplets.
- **Space:** O(1) — three boolean flags.

## 12. Partition Labels  ·  _Medium_

**Scenario:** A jeweler threads a single long string of colored beads and wants to snip it into as many separate segments as possible, with one rule: all beads of any given color must end up in the same segment. Cutting cannot reorder beads. What are the lengths of the segments in this maximal chopping?

- **Maps to:** Greedy expanding window using last-occurrence (Partition Labels).
- **Model it:** Split a string into the most parts so each letter appears in only one part.
- **Approach & variations:**
  - Record the last index at which each character appears.
  - Scan left to right, extending the current segment's end to the max last-index of characters seen.
  - When the scan position reaches that end, cut — record the length and start a new segment.
- **Time:** O(n) — one pass to find last indices, one to partition.
- **Space:** O(1) — a fixed-size last-index table (alphabet).

## 13. Valid Parenthesis String  ·  _Medium_

**Scenario:** A proofreader has a line containing open and close brackets plus some wildcard blots, each blot being either an open bracket, a close bracket, or nothing at all. She may interpret each blot however she likes. Can the blots be interpreted so the whole line is perfectly balanced — every open matched by a later close?

- **Maps to:** Greedy tracking a range of possible open counts (Valid Parenthesis String).
- **Model it:** Decide if a string of '(', ')', '*' can be valid with each '*' as '(', ')', or empty.
- **Approach & variations:**
  - Maintain a low and high bound on the number of unmatched opens.
  - '(' raises both; ')' lowers both; '*' lowers low and raises high (its three options).
  - Clamp low at 0 (can't go negative); if high ever goes negative, fail. Valid iff low can reach 0 at the end.
- **Time:** O(n) — a single scan maintaining two bounds.
- **Space:** O(1) — two counters.

## 14. Candy  ·  _Hard_

**Scenario:** Children stand in a line, each with a rating for how well they behaved. You must give every child at least one candy, and any child rated strictly higher than an immediate neighbor must get more candies than that neighbor. What is the smallest total number of candies that satisfies everyone?

- **Maps to:** Two-pass greedy (left-to-right then right-to-left) (Candy).
- **Model it:** Assign minimum positive integers to a line so each strictly higher-rated neighbor gets strictly more.
- **Approach & variations:**
  - Start everyone at 1 candy.
  - Left-to-right: if a child outranks the left neighbor, give one more than that neighbor.
  - Right-to-left: if a child outranks the right neighbor, bump to max(current, rightNeighbor+1).
  - Sum the candies; the two passes satisfy both directions simultaneously.
- **Time:** O(n) — two linear sweeps.
- **Space:** O(n) — a candy count per child.

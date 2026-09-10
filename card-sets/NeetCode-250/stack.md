---
deck: "NeetCode 250::Stack"
topic: "NeetCode 250 — Stack"
tags: [ankicardmaker, neetcode250, stack]
note_type: Basic
created: 2026-09-09
---

# NeetCode 250 — Stack

Story front hides the technique; back reveals the mapping, approach, and complexity.

## 1. Baseball Game  ·  _Easy_

**Scenario:** A scorekeeper processes a list of instructions in order. Each is either a plain number to record, the word 'double' meaning record twice the last recorded number, the word 'sum' meaning record the total of the last two recorded numbers, or 'undo' meaning erase the most recent record. At the end, what is the sum of everything still on the sheet?

- **Maps to:** Stack of recorded values with push/pop operations (Baseball Game).
- **Model it:** Process operations that reference the last one or two records, then total the surviving records.
- **Approach & variations:**
  - Maintain a growing pile of recorded numbers; a plain number pushes onto it.
  - 'undo' removes the top; 'double' pushes twice the top; 'sum' pushes the top two added.
  - Each operation touches only the top one or two entries — order of records matters.
  - Sum whatever remains after all instructions.
- **Time:** O(n) — one pass, constant work per instruction.
- **Space:** O(n) — the pile can hold every recorded number.

## 2. Valid Parentheses  ·  _Easy_

**Scenario:** A ribbon of nested brackets of three shapes — round, square, and curly — comes off a printer, each either an opener or a closer. The ribbon is well-formed only if every opener is later closed by a matching-shape closer, closers come in the right nested order, and nothing is left dangling. Is this ribbon well-formed?

- **Maps to:** Stack of open brackets matched on close (Valid Parentheses).
- **Model it:** Decide if a string of brackets is properly nested and matched across three types.
- **Approach & variations:**
  - Push each opener onto a pile as you read left to right.
  - On a closer, the pile's top must be the matching opener; pop it, else it's invalid.
  - A closer with an empty pile is invalid (nothing to match).
  - Valid only if the pile is empty at the very end (no unclosed openers).
- **Time:** O(n) — each bracket is pushed and popped at most once.
- **Space:** O(n) — the pile in the worst case of all openers.

## 3. Implement Stack Using Queues  ·  _Easy_

**Scenario:** You must build a last-in-first-out tray dispenser, but the only storage you're allowed is one or more line-up lanes where items can only join at the back and leave from the front. Design push, pop-most-recent, peek-most-recent, and empty-check so that the newest item added always comes out first, using only these front-in/back-out lanes.

- **Maps to:** Simulate a LIFO stack using FIFO queue(s) (Implement Stack Using Queues).
- **Model it:** Expose stack operations while the only primitive is a first-in-first-out queue.
- **Approach & variations:**
  - One-queue trick: after enqueuing a new item, rotate the queue by moving every earlier item to the back so the newest sits at the front.
  - Then push is O(n) and pop/top are O(1) — the front is always the most recent.
  - Alternatively keep pushes O(1) and pay O(n) on pop by shuffling to the last element.
  - Empty-check just asks whether the lane has any items.
- **Time:** O(n) for the rotating operation, O(1) for the others.
- **Space:** O(n) — one lane holding all items.

## 4. Implement Queue using Stacks  ·  _Easy_

**Scenario:** You must build a first-come-first-served ticket line, but the only storage you have is spring-loaded tubes where items can only be pushed onto and popped off the top. Design join-the-back, serve-the-front, peek-the-front, and empty-check so that the oldest waiting item is always served first, using only these top-in/top-out tubes.

- **Maps to:** Simulate a FIFO queue using two LIFO stacks (Implement Queue using Stacks).
- **Model it:** Expose queue operations while the only primitive is a last-in-first-out stack.
- **Approach & variations:**
  - Keep an 'in' tube for arrivals and an 'out' tube for departures.
  - To serve or peek, if 'out' is empty, pour all of 'in' into 'out', reversing the order so the oldest is on top.
  - Push is always O(1); each item moves between tubes at most once, so pop is amortized O(1).
  - Empty means both tubes are empty.
- **Time:** Amortized O(1) per operation; a single transfer is O(n).
- **Space:** O(n) — two tubes holding all items.

## 5. Min Stack  ·  _Medium_

**Scenario:** A warehouse keeps a single spring-loaded chute where boxes are added and removed only from the top. Besides the usual add, remove-top, and read-top, the foreman needs to instantly know the lightest box currently in the chute at any moment — without digging through it. Design the chute so that lightest-box lookup is immediate.

- **Maps to:** Stack augmented with running minimums (Min Stack).
- **Model it:** Support push, pop, top, and get-minimum all in constant time.
- **Approach & variations:**
  - Alongside the main pile keep a parallel pile of running minimums.
  - On push, record min(new value, current running min) on the min pile.
  - On pop, remove from both piles together; the min pile's top is always the current minimum.
  - Alternatively store (value, min-so-far) pairs in one pile.
- **Time:** O(1) — every operation touches only the tops.
- **Space:** O(n) — the auxiliary minimum pile mirrors the main one.

## 6. Evaluate Reverse Polish Notation  ·  _Medium_

**Scenario:** A calculator reads a strip of tokens left to right. Each token is either a number or one of +, -, *, / that acts on the two most recently produced numbers (first-produced on the left of the operation), replacing them with the result. The strip is arranged so this always works out. What single number remains at the end?

- **Maps to:** Stack-based postfix expression evaluation (Evaluate Reverse Polish Notation).
- **Model it:** Evaluate an expression given in postfix order where operators follow their operands.
- **Approach & variations:**
  - Push numbers onto a pile as they appear.
  - On an operator, pop the top two, apply it with the correct operand order, and push the result.
  - Division truncates toward zero; watch operand order for subtraction and division.
  - The last remaining value on the pile is the answer.
- **Time:** O(n) — one pass, constant work per token.
- **Space:** O(n) — the pile of pending operands.

## 7. Generate Parentheses  ·  _Medium_

**Scenario:** A ribbon-maker must produce every possible well-formed ribbon of exactly N openers and N closers, where at no point reading left to right have more closers appeared than openers, and the ribbon ends balanced. List all distinct such ribbons. How do you generate them without producing malformed ones?

- **Maps to:** Backtracking with an open/close balance constraint (Generate Parentheses).
- **Model it:** Enumerate all balanced bracket strings using N pairs.
- **Approach & variations:**
  - Build left to right, tracking how many openers and closers are placed.
  - May add an opener while openers used < N; may add a closer only while closers < openers placed.
  - When the string reaches length 2N it is a valid result; record it.
  - The balance rule prunes every invalid branch, so no filtering is needed.
- **Time:** O(4^n / sqrt(n)) — the count of valid strings (Catalan number), each built in O(n).
- **Space:** O(n) recursion depth plus the output list.

## 8. Asteroid Collision  ·  _Medium_

**Scenario:** Rocks fly along a single track, each with a size and a direction — some drifting right, some left, listed in their left-to-right positions. Rightward and leftward rocks moving toward each other collide; the smaller one is destroyed, or both if equal size. Same-direction rocks never meet. Which rocks survive after all collisions settle?

- **Maps to:** Stack simulating collisions of surviving elements (Asteroid Collision).
- **Model it:** Given signed values (sign = direction, magnitude = size), resolve collisions between right-movers and following left-movers.
- **Approach & variations:**
  - Push rocks onto a pile; a collision is only possible when a leftward rock meets a rightward rock on top.
  - While the top is a rightward rock smaller than the incoming leftward rock, pop it (it's destroyed).
  - Equal sizes destroy both; if the incoming rock is destroyed, stop pushing it.
  - Rocks that survive the pile are the answer, in order.
- **Time:** O(n) — each rock is pushed and popped at most once.
- **Space:** O(n) — the survivor pile.

## 9. Daily Temperatures  ·  _Medium_

**Scenario:** A hiker logs each day's high temperature in a row by date. For every day she wants to know how many days she must wait until a strictly warmer day arrives later in the log. If no warmer day ever comes, that day's answer is zero. Produce the wait count for each day.

- **Maps to:** Monotonic decreasing stack of pending indices (Daily Temperatures).
- **Model it:** For each element find the distance to the next strictly greater element on its right.
- **Approach & variations:**
  - Scan left to right keeping a pile of days still waiting for a warmer day (temperatures decreasing down the pile).
  - When today is warmer than the pile's top, pop it and record the day gap as its answer.
  - Repeat popping while today beats the new top; then push today.
  - Days left on the pile at the end get zero.
- **Time:** O(n) — each day is pushed and popped once.
- **Space:** O(n) — the pile of unresolved days.

## 10. Online Stock Span  ·  _Medium_

**Scenario:** A trader is fed a coin's price one day at a time and can never see the future. For each new day she must immediately report, counting today and backward, the length of the longest run of consecutive most-recent days whose prices were all less than or equal to today's. Report this streak live as each price arrives.

- **Maps to:** Monotonic stack of (price, span) pairs answered online (Online Stock Span).
- **Model it:** Streaming: for each incoming value count consecutive preceding values <= it (including itself).
- **Approach & variations:**
  - Keep a pile of (price, accumulated span) with prices strictly decreasing down the pile.
  - For a new price start its span at 1, then while the top price is <= today, pop it and add its span to today's.
  - Push today with its total span and return that span immediately.
  - Each price is popped at most once, so amortized work per query is constant.
- **Time:** Amortized O(1) per query, O(n) total — each price pushed/popped once.
- **Space:** O(n) — the pile of price/span pairs.

## 11. Car Fleet  ·  _Medium_

**Scenario:** Several cars head to the same finish line on a one-lane road, each at a known starting distance from the line and a fixed top speed. A faster car catching a slower one ahead cannot pass; it slows and they travel bunched together as one group thereafter, arriving together. How many distinct groups cross the finish line?

- **Maps to:** Sort by position, compare arrival times with a stack (Car Fleet).
- **Model it:** Count clusters: process cars from nearest-to-finish backward, merging any that would catch the group ahead.
- **Approach & variations:**
  - Sort cars by starting position, closest to the finish first.
  - Compute each car's solo time to the finish = remaining distance / speed.
  - Walk from the front; a car whose time is <= the current lead group's time joins it, else it starts a new group (push its time).
  - The number of times a new lead time survives equals the fleet count.
- **Time:** O(n log n) — dominated by sorting positions.
- **Space:** O(n) — the stack of fleet lead times.

## 12. Simplify Path  ·  _Medium_

**Scenario:** A hiker is handed messy walking directions through nested rooms: names of rooms to enter, some redundant 'stay here' markers, some 'go back one room' markers, and sloppy repeated separators. Collapse this into the cleanest possible description of where she actually ends up, never backing out past the entrance. What is the tidied route?

- **Maps to:** Stack of path components (Simplify Path).
- **Model it:** Canonicalize a Unix-style path, resolving '.', '..', and redundant slashes.
- **Approach & variations:**
  - Split the route on separators, ignoring empty pieces and 'stay here' ('.') markers.
  - For a 'go back' ('..'), pop the last room if any, otherwise stay at the entrance.
  - Push any real room name onto the pile.
  - Join the surviving rooms with single separators, prefixed from the root.
- **Time:** O(n) — one pass over the components.
- **Space:** O(n) — the pile of surviving room names.

## 13. Decode String  ·  _Medium_

**Scenario:** A knitter follows a compressed pattern where a number followed by a bracketed sub-pattern means 'repeat that sub-pattern that many times,' and these repeats can nest inside one another. Expand the whole compressed pattern into the full literal sequence of stitches it describes.

- **Maps to:** Two stacks for counts and partial strings (Decode String).
- **Model it:** Expand an encoding like 3[a2[c]] into its fully repeated string, honoring nesting.
- **Approach & variations:**
  - Scan left to right building the current segment; on a digit, accumulate the full repeat number.
  - On an opener, push the current segment and the count, then start a fresh segment.
  - On a closer, pop the count and prior segment, and append the current segment repeated that many times.
  - Plain letters just extend the current segment.
- **Time:** O(total output length) — work is proportional to the expanded result.
- **Space:** O(depth + output) — nested counts and segments on the stacks.

## 14. Maximum Frequency Stack  ·  _Hard_

**Scenario:** A cluttered inbox lets you drop in tagged notes and pull one out. But pull always removes the tag that has appeared most often so far; if several tags tie for most-often, it removes whichever of those tied tags was dropped in most recently. Design push and this special pull so both are fast.

- **Maps to:** Frequency map plus stacks grouped by frequency (Maximum Frequency Stack / Freq Stack).
- **Model it:** Support push and a pop that returns the most frequent element, breaking ties by most recent.
- **Approach & variations:**
  - Track each tag's current count in a frequency map.
  - Keep a group of piles indexed by frequency level; pushing a tag places it on the pile for its new count.
  - Also track the maximum frequency present; pull takes from that top pile (naturally the most recent among ties) and lowers max if it empties.
  - Popping decrements that tag's count in the map.
- **Time:** O(1) per push and pop — map and top-of-pile operations.
- **Space:** O(n) — every pushed element is stored once across the piles.

## 15. Largest Rectangle In Histogram  ·  _Hard_

**Scenario:** A row of adjacent buildings of equal width but varying heights stands shoulder to shoulder. A window washer wants to hang the largest possible rectangular banner flat against the fronts, spanning some run of consecutive buildings, but the banner's height is capped by the shortest building it covers. What is the greatest banner area achievable?

- **Maps to:** Monotonic increasing stack of bar indices (Largest Rectangle in Histogram).
- **Model it:** Find the maximum-area rectangle bounded by consecutive bars, height limited by the shortest bar spanned.
- **Approach & variations:**
  - Keep a pile of indices with increasing heights as you scan.
  - When a shorter building appears, pop taller ones and, for each popped bar, compute its widest rectangle at that height using the new left/right bounds.
  - The right bound is the current index; the left bound is the new pile top after popping.
  - Flush the pile at the end (treat as a zero-height sentinel) and keep the maximum area.
- **Time:** O(n) — each bar is pushed and popped once.
- **Space:** O(n) — the index pile.

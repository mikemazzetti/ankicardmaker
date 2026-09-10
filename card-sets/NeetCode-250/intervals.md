---
deck: "NeetCode 250::Intervals"
topic: "NeetCode 250 — Intervals"
tags: [ankicardmaker, neetcode250, intervals]
note_type: Basic
created: 2026-09-09
---

# NeetCode 250 — Intervals

Story front hides the technique; back reveals the mapping, approach, and complexity.

## 1. Insert Interval  ·  _Medium_

**Scenario:** Your calendar already holds a tidy list of busy time-blocks that never overlap and are sorted by start time. A new busy block comes in. Slot it in so the calendar stays sorted and non-overlapping — merging it with any existing blocks it touches. What is the resulting list of blocks?

- **Maps to:** Linear merge into a sorted, disjoint interval list (Insert Interval).
- **Model it:** Insert one interval into a sorted list of disjoint intervals, merging overlaps.
- **Approach & variations:**
  - Copy all intervals ending before the new one starts (they're entirely left of it).
  - Merge every interval overlapping the new one by widening the new interval's start/end.
  - Append the merged interval, then copy the remaining intervals (entirely to its right).
- **Time:** O(n) — a single pass over the existing blocks.
- **Space:** O(n) — the output list.

## 2. Merge Intervals  ·  _Medium_

**Scenario:** A scheduler collects a messy, unsorted pile of busy time-blocks, some of which overlap or touch. Combine every group of connected blocks into single continuous blocks so none overlap anymore. What does the cleaned-up set of blocks look like?

- **Maps to:** Sort by start, then sweep-merge adjacent overlaps (Merge Intervals).
- **Model it:** Merge all overlapping intervals in an unsorted list into disjoint intervals.
- **Approach & variations:**
  - Sort intervals by start time.
  - Walk through; if the current start is <= the last kept interval's end, extend that end to the max.
  - Otherwise start a new kept interval.
  - Contrast with Insert Interval, where input is already sorted and only one interval is new.
- **Time:** O(n log n) — dominated by the sort.
- **Space:** O(n) — sort scratch plus output (O(1) extra if in place).

## 3. Non Overlapping Intervals  ·  _Medium_

**Scenario:** You've booked a pile of overlapping appointments and need a conflict-free schedule where no two remaining appointments overlap. You want to cancel as few appointments as possible. What is the fewest number you must remove?

- **Maps to:** Greedy by earliest end time, count conflicts (Non-Overlapping Intervals).
- **Model it:** Remove the minimum number of intervals so the rest are pairwise non-overlapping.
- **Approach & variations:**
  - Sort by end time; keep the interval that finishes earliest, tracking the current end.
  - If the next interval starts before that end, it conflicts — remove it (increment count).
  - Otherwise accept it and advance the end.
  - Sorting by end (not start) is the classic activity-selection maximization.
- **Time:** O(n log n) — the sort dominates.
- **Space:** O(1) — a running end value and counter (plus sort space).

## 4. Meeting Rooms  ·  _Easy_

**Scenario:** You're given a bunch of proposed meetings, each with a start and end time, all meant for a single shared room. You just need to know whether one person could attend all of them — that is, whether none of the meetings clash. Can they all coexist without overlap?

- **Maps to:** Sort by start, check adjacent overlap (Meeting Rooms).
- **Model it:** Decide if any two intervals overlap.
- **Approach & variations:**
  - Sort meetings by start time.
  - Scan adjacent pairs; if any meeting starts before the previous one ends, they overlap — return false.
  - Touching at an endpoint (one ends exactly when the next starts) is not a conflict.
- **Time:** O(n log n) — the sort dominates.
- **Space:** O(1) — just comparisons (plus sort space).

## 5. Meeting Rooms II  ·  _Medium_

**Scenario:** A conference has many talks, each with a start and end time, and overlapping talks need separate rooms. You want to rent the fewest rooms so that no two simultaneous talks share a room. What is the minimum number of rooms needed?

- **Maps to:** Min-heap of end times, or split-and-sweep of start/end events (Meeting Rooms II).
- **Model it:** Find the maximum number of intervals overlapping at any instant.
- **Approach & variations:**
  - Sort start times and end times separately.
  - Sweep a time pointer: each start needs a room; each passed end frees one.
  - The peak concurrent count is the answer.
  - Equivalent: push end times into a min-heap; if the earliest end <= current start, reuse that room, else add one.
- **Time:** O(n log n) — sorting or heap operations.
- **Space:** O(n) — the heap or the event arrays.

## 6. Meeting Rooms III  ·  _Hard_

**Scenario:** There are a fixed number of numbered meeting rooms and a list of meetings, each with a start and end. Meetings are handled in order of start time; each takes the lowest-numbered free room. If none is free, it waits and keeps its original duration, starting the moment a room frees (again preferring the lowest number). After all meetings, which room hosted the most meetings?

- **Maps to:** Two heaps: free rooms and busy (end-time, room) (Meeting Rooms III).
- **Model it:** Simulate assigning meetings to the lowest-index available room, delaying when full, and count usage per room.
- **Approach & variations:**
  - Keep a min-heap of free room indices and a min-heap of busy rooms keyed by (freeTime, index).
  - Process meetings by start; first release all rooms whose freeTime <= start into the free heap.
  - If a room is free, use the smallest index; else pop the soonest-freeing busy room, delay the meeting by that room's freeTime.
  - Tally each room's count and return the busiest (lowest index on ties).
- **Time:** O(n log n) — sort by start plus heap operations per meeting.
- **Space:** O(n + m) — heaps of meetings and rooms, counts per room.

## 7. Minimum Interval to Include Each Query  ·  _Hard_

**Scenario:** A ruler-maker has many measuring sticks, each spanning from some low mark to some high mark. For each of several query points, you want the shortest stick that fully covers that point. Report the length of that shortest covering stick for every query (or nothing if no stick covers it).

- **Maps to:** Sort queries + intervals, min-heap by interval length (Minimum Interval to Include Each Query).
- **Model it:** For each query value, find the smallest-width interval whose range contains it.
- **Approach & variations:**
  - Sort intervals by start and queries in ascending order (remember original positions).
  - Process queries in order; push all intervals whose start <= query into a min-heap keyed by width, storing their end.
  - Pop intervals whose end < query (they no longer cover it); the heap top is the shortest cover.
  - Write answers back to each query's original index.
- **Time:** O((n + q) log(n + q)) — sorting and heap operations.
- **Space:** O(n + q) — the heap and answer array.

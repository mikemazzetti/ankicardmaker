---
deck: "Resume Prep::Computer Architecture"
topic: "Computer Architecture"
tags: [ankicardmaker, resume-prep, computer-architecture]
note_type: Mixed (Basic / Basic (and reversed card) / Cloze)
created: 2026-09-09
---

# Computer Architecture — Resume Prep

Source of truth for the `Resume Prep::Computer Architecture` deck (18 notes). Edit here and re-push to update.

## Basic cards

1. **Q:** CPU (Central Processing Unit) *(reversed — tested both ways)*
   **A:** The hardware component that fetches, decodes, and executes instructions &mdash; the "brain" of the computer, containing the ALU, control unit, and registers.

2. **Q:** What does the ALU (Arithmetic Logic Unit) do?
   **A:** It performs arithmetic operations (add, subtract, multiply) and logic operations (AND, OR, NOT, comparisons) on data supplied by the registers.

3. **Q:** What are CPU registers, and why are they faster than any level of cache?
   **A:** Small, fixed-size storage locations built directly into the CPU that hold operands/results currently in use. They're fastest because they're on-chip with zero bus latency &mdash; no memory access at all.

4. **Q:** How do L1, L2, and L3 cache compare in size and speed?
   **A:** L1 is smallest and fastest (per-core, a few KB, ~1-4 cycles). L2 is larger and slower (per-core, few hundred KB - few MB). L3 is largest and slowest of the three (shared across cores, several MB, tens of cycles) &mdash; still far faster than RAM.

5. **Q:** What is temporal locality?
   **A:** The tendency for a recently accessed memory location to be accessed again soon (e.g. a loop counter or variable reused each iteration) &mdash; caches exploit this by keeping recently used data close.

6. **Q:** What is spatial locality?
   **A:** The tendency for memory locations near a recently accessed address to be accessed soon after (e.g. adjacent array elements) &mdash; caches exploit this by fetching whole cache lines, not single bytes.

7. **Q:** Why does traversing a 2D array in row-major order run faster than in column-major order (in a row-major language like C/Java)?
   **A:** Row-major traversal accesses contiguous memory addresses in sequence, so each fetched cache line is fully used (good spatial locality). Column-major traversal jumps by a full row's stride each step, causing a cache miss almost every access.

8. **Q:** What is pipelining in CPU design?
   **A:** Overlapping the execution of multiple instructions by splitting the instruction cycle into stages (e.g. fetch, decode, execute, writeback) so a new instruction can enter the pipeline each cycle instead of waiting for the previous one to fully finish.

9. **Q:** Stack memory (in the stack-vs-heap sense) *(reversed — tested both ways)*
   **A:** Fast, automatically managed memory for local variables and function call frames; fixed size per frame, freed automatically when the function returns; limited total size (stack overflow on deep recursion).

10. **Q:** How does heap memory differ from stack memory?
   **A:** Heap memory is for dynamically allocated objects whose lifetime isn't tied to a function call; it's manually or GC-managed, larger/more flexible, but slower to allocate/free and can lead to fragmentation or leaks.

11. **Q:** What is virtual memory / paging?
   **A:** An abstraction where each process gets its own virtual address space, mapped by the OS/MMU to physical RAM (or disk) in fixed-size chunks called pages, via a page table &mdash; giving processes isolation and the illusion of more memory than physically exists.

12. **Q:** What is a page fault?
   **A:** A trap that occurs when a process accesses a virtual page that isn't currently mapped into physical RAM, forcing the OS to load it from disk (or handle an invalid access).

13. **Q:** What is the core philosophical difference between RISC and CISC instruction set architectures?
   **A:** RISC (e.g. ARM) uses a small set of simple, fixed-length instructions that each execute in ~1 cycle, relying on the compiler to combine them &mdash; favors pipelining. CISC (e.g. x86) uses a larger set of complex, variable-length instructions that can do more per instruction, at the cost of more complex decoding.

14. **Q:** Why does an in-memory cache (e.g. Caffeine, as used to reduce DB load) dramatically improve latency compared to hitting the database every time?
   **A:** A cache hit returns data from RAM (nanoseconds) instead of round-tripping to a database over the network/disk (milliseconds) &mdash; the same principle as a CPU cache hit vs. a main-memory access, just at a different layer of the hierarchy.

## Cloze cards

- The memory hierarchy, from fastest/smallest to slowest/largest, is: {{c1::registers}} &rarr; {{c2::L1 cache}} &rarr; {{c3::L2 cache}} &rarr; {{c4::L3 cache}} &rarr; {{c5::main memory (RAM)}} &rarr; {{c6::disk/SSD}}.
- The three classic types of pipeline hazards are {{c1::structural}} (two instructions need the same hardware resource), {{c2::data}} (an instruction needs a result a prior instruction hasn't produced yet), and {{c3::control}} (a branch changes which instruction should be fetched next).
- The three classic cache miss types are {{c1::compulsory}} (first-ever access to a block, unavoidable), {{c2::capacity}} (the cache is too small to hold everything needed, so useful data gets evicted), and {{c3::conflict}} (multiple addresses map to the same cache set/line and evict each other despite free space elsewhere).
- The classic instruction cycle is: {{c1::fetch}} (get the instruction from memory), {{c2::decode}} (determine what it means / which control signals to set), {{c3::execute}} (perform the operation, e.g. in the ALU), and {{c4::writeback}} (store the result back to a register or memory).

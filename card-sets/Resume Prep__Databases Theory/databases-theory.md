---
deck: "Resume Prep::Databases Theory"
topic: "Databases Theory"
tags: [ankicardmaker, resume-prep, databases-theory]
note_type: Mixed (Basic / Basic (and reversed card) / Cloze)
created: 2026-09-09
---

# Databases Theory — Resume Prep

Source of truth for the `Resume Prep::Databases Theory` deck (19 notes). Edit here and re-push to update.

## Basic cards

1. **Q:** What does the "Atomicity" property of ACID guarantee?
   **A:** A transaction's operations either all happen or none do — no partially-applied transaction is ever left committed.

2. **Q:** What does the "Isolation" property of ACID guarantee?
   **A:** Concurrent transactions produce a result equivalent to running them one at a time in some order, up to the chosen isolation level.

3. **Q:** What does the CAP theorem state about a distributed data store?
   **A:** It can guarantee at most two of Consistency, Availability, and Partition tolerance at once — and since partitions will happen, real systems effectively trade off Consistency vs Availability.

4. **Q:** In CAP theorem terms, why must a distributed system always effectively choose partition tolerance?
   **A:** Network partitions will occur in any real distributed system, so a system that doesn't tolerate them simply fails during a partition — it isn't really an optional choice.

5. **Q:** What is the N+1 query problem?
   **A:** Fetching N parent records with one query, then issuing one additional query per parent to load related child data — N+1 total queries where a single join query would do.

6. **Q:** In a Hibernate app like the ServiceOntario project, how does JPQL's <code>JOIN FETCH</code> fix an N+1 problem?
   **A:** It eagerly loads the related entities in the same query via a join, instead of Hibernate lazily issuing a separate SELECT each time an association is accessed on a parent.

7. **Q:** Besides <code>JOIN FETCH</code>, what Hibernate setting reduces N+1-style overhead when lazy loading is kept?
   **A:** Tuning the Hibernate batch size (e.g. <code>@BatchSize</code> or <code>hibernate.default_batch_fetch_size</code>), which batches multiple lazy-load queries into fewer <code>IN</code>-clause queries.

8. **Q:** What's the main tradeoff of adding an index to a table?
   **A:** Faster reads/lookups on the indexed column(s), at the cost of slower writes (inserts/updates/deletes must also update the index) and extra storage.

9. **Q:** What's the difference between a primary key and a foreign key?
   **A:** A primary key uniquely identifies each row in its own table; a foreign key is a column referencing a primary key in another table to enforce a relationship.

10. **Q:** What is a database lock used for during a transaction?
   **A:** To prevent other transactions from concurrently reading or writing the same data in a conflicting way, protecting consistency while the transaction runs.

11. **Q:** OLTP *(reversed — tested both ways)*
   **A:** Online Transaction Processing — optimized for many short read/write transactions, e.g. an order-entry system.

12. **Q:** OLAP *(reversed — tested both ways)*
   **A:** Online Analytical Processing — optimized for complex, read-heavy aggregate queries over large historical data, e.g. a reporting warehouse.

13. **Q:** What is denormalization, and why is it sometimes used despite violating normal forms?
   **A:** Deliberately introducing redundant data (e.g. duplicating a column across tables) to reduce joins and speed up reads, trading write complexity and storage for query performance.

14. **Q:** Give a concrete example of denormalization used to avoid N+1-style per-row lookups.
   **A:** Storing a duplicated field — e.g. an order's customer name — directly on the order row instead of always joining to the customer table to fetch it.

15. **Q:** What's the difference between ordinary lock contention and a deadlock?
   **A:** Contention is transactions waiting for each other's locks and eventually proceeding; a deadlock is a cycle of transactions each waiting on a lock the other holds, which never resolves without the DB detecting it and aborting one.

## Cloze cards

- {{c1::1NF}} (First Normal Form) requires every column to hold atomic, indivisible values with no repeating groups.
- {{c1::2NF}} requires 1NF plus no partial dependency — every non-key column must depend on the entire primary key, not just part of it.
- {{c1::3NF}} requires 2NF plus no transitive dependency — non-key columns must depend only on the primary key, not on other non-key columns.
- ACID stands for {{c1::Atomicity}}, {{c2::Consistency}}, {{c3::Isolation}}, and {{c4::Durability}}.

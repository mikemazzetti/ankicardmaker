---
deck: "Resume Prep::PostgreSQL"
topic: "PostgreSQL"
tags: [ankicardmaker, resume-prep, postgresql]
note_type: Mixed (Basic / Basic (and reversed card) / Cloze)
created: 2026-09-09
---

# PostgreSQL — Resume Prep

Source of truth for the `Resume Prep::PostgreSQL` deck (20 notes). Edit here and re-push to update.

## Basic cards

1. **Q:** What does MVCC stand for in Postgres and what problem does it solve?
   **A:** Multi-Version Concurrency Control — lets readers see a consistent snapshot of data without blocking concurrent writers, so reads never need row locks.

2. **Q:** In Postgres's MVCC, what happens to a row when it's updated instead of being overwritten in place?
   **A:** A new row version is written; the old version remains (still visible to transactions whose snapshot predates it) until it's cleaned up by vacuum.

3. **Q:** B-tree index (Postgres) *(reversed — tested both ways)*
   **A:** The default index type — efficient for equality and range queries (<, <=, =, >=, >) on sortable data.

4. **Q:** GIN index (Postgres) *(reversed — tested both ways)*
   **A:** Generalized Inverted Index — efficient for indexing composite values like arrays, JSONB, and full-text search vectors.

5. **Q:** What is a partial index in Postgres and when would you use one?
   **A:** An index built with a <code>WHERE</code> clause covering only a subset of rows — useful for cheaply indexing a common filtered query, e.g. only unfinished orders.

6. **Q:** Write SQL to create a partial index on <code>orders</code> covering only unshipped orders.
   **A:** <pre><code>CREATE INDEX idx_unshipped
ON orders (created_at)
WHERE shipped = false;</code></pre>

7. **Q:** What does <code>EXPLAIN ANALYZE</code> do differently from plain <code>EXPLAIN</code>?
   **A:** It actually executes the query and reports real timings and row counts alongside the plan, instead of only the planner's estimates.

8. **Q:** Write a query that shows the real execution plan and timing for a SELECT on <code>orders</code>.
   **A:** <pre><code>EXPLAIN ANALYZE
SELECT * FROM orders WHERE customer_id = 42;</code></pre>

9. **Q:** What is Postgres's default transaction isolation level?
   **A:** Read Committed.

10. **Q:** What phenomenon does Repeatable Read prevent that Read Committed does not?
   **A:** Non-repeatable reads — under Repeatable Read, re-reading the same row twice in one transaction always returns the same value, even if another transaction committed a change in between.

11. **Q:** What does the <code>SERIAL</code> pseudo-type do when declaring a Postgres column?
   **A:** Creates an auto-incrementing integer column backed by a linked sequence — shorthand for an integer column with a <code>DEFAULT nextval()</code> on an auto-created sequence.

12. **Q:** Write SQL to create a table with an auto-incrementing primary key.
   **A:** <pre><code>CREATE TABLE users (
  id SERIAL PRIMARY KEY,
  username TEXT NOT NULL
);</code></pre>

13. **Q:** What's the advantage of <code>JSONB</code> over plain <code>JSON</code> in Postgres, and what's the tradeoff?
   **A:** JSONB stores a decomposed binary format — faster to query and indexable with GIN — but loses exact text formatting/key order; JSON stores raw text, faster to write but not indexable that way.

14. **Q:** Write a Postgres query filtering rows by a key inside a JSONB column.
   **A:** <pre><code>SELECT * FROM events
WHERE payload -&gt;&gt; 'type' = 'click';</code></pre>

15. **Q:** What does <code>VACUUM</code> do in Postgres?
   **A:** Reclaims storage from dead row versions left behind by MVCC updates/deletes, and refreshes planner statistics.

16. **Q:** Why does Postgres's MVCC design make regular <code>VACUUM</code>ing necessary?
   **A:** Updates and deletes don't remove old row versions immediately; without vacuuming, dead tuples accumulate and bloat tables and indexes.

17. **Q:** What is a CTE and what keyword introduces one in Postgres?
   **A:** A Common Table Expression — a named, temporary result set defined with <code>WITH</code>, usable like a subquery inside the main query.

18. **Q:** Write a Postgres query using a CTE to find customers whose total order amount exceeds $1000.
   **A:** <pre><code>WITH totals AS (
  SELECT customer_id, SUM(amount) AS total
  FROM orders GROUP BY customer_id
)
SELECT * FROM totals WHERE total &gt; 1000;</code></pre>

## Cloze cards

- The four standard SQL transaction isolation levels, weakest to strongest, are {{c1::Read Uncommitted}}, {{c2::Read Committed}}, {{c3::Repeatable Read}}, and {{c4::Serializable}}.
- Common Postgres constraints that enforce data integrity include {{c1::PRIMARY KEY}}, {{c2::FOREIGN KEY}}, {{c3::UNIQUE}}, {{c4::CHECK}}, and {{c5::NOT NULL}}.

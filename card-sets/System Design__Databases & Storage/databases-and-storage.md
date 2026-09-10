---
deck: "System Design::Databases & Storage"
topic: "Databases & Storage"
tags: [ankicardmaker, sd-databases]
note_type: Mixed (Basic / Basic (and reversed card) / Cloze)
created: 2026-09-10
---

# Databases & Storage — System Design

Source of truth for the `System Design::Databases & Storage` deck (21 notes). Edit here and re-push to update.

## Basic cards

1. **Q:** When should you choose a SQL (relational) database over NoSQL?
   **A:** When you need strong consistency, complex multi-table joins/transactions, and a fixed, well-understood schema.

2. **Q:** When should you choose a NoSQL database over SQL?
   **A:** When you need horizontal scalability, a flexible/evolving schema, and can relax strict consistency (e.g. massive write throughput, unstructured data).

3. **Q:** What is a key-value store best suited for? Give an example.
   **A:** Simple lookups by a unique key with no query complexity, e.g. <code>Redis</code> for caching or session storage.

4. **Q:** What is a document store best suited for? Give an example.
   **A:** Semi-structured, nested data accessed as whole records, e.g. <code>MongoDB</code> for product catalogs or user profiles.

5. **Q:** What is a column-family (wide-column) store best suited for? Give an example.
   **A:** Very high write throughput and queries over huge, sparse datasets, e.g. <code>Cassandra</code> for time-series or logging data.

6. **Q:** What is a graph database best suited for? Give an example.
   **A:** Data where relationships/traversals matter more than the entities themselves, e.g. <code>Neo4j</code> for social networks or recommendation engines.

7. **Q:** What data structure do most relational database indexes use, and why?
   **A:** A B-tree, because it keeps data sorted and supports O(log n) lookups, range scans, and ordered traversal at balanced depth.

8. **Q:** Why does adding an index speed up reads?
   **A:** It lets the DB search a sorted structure instead of scanning every row, turning an O(n) full scan into an O(log n) lookup.

9. **Q:** What is the write-side cost of adding an index?
   **A:** Every insert/update/delete must also update the index structure, which slows writes and uses extra storage.

10. **Q:** What is database normalization?
   **A:** Organizing data into related tables to eliminate redundancy, using foreign keys instead of duplicating data.

11. **Q:** What is database denormalization, and why is it used at scale?
   **A:** Deliberately duplicating data across tables/documents to avoid expensive joins, trading storage and write complexity for faster reads.

12. **Q:** ACID *(reversed — both ways)*
   **A:** Atomicity, Consistency, Isolation, Durability — the transaction guarantees of traditional relational (SQL) databases.

13. **Q:** BASE *(reversed — both ways)*
   **A:** Basically Available, Soft state, Eventually consistent — the looser guarantees typical of many NoSQL systems.

14. **Q:** What problem do read replicas solve?
   **A:** They offload read traffic from the primary/leader database by serving reads from copies, scaling read throughput.

15. **Q:** What is a downside of read replicas?
   **A:** Replication lag can cause a replica to serve stale (slightly outdated) data compared to the primary.

16. **Q:** What problem does connection pooling solve?
   **A:** It reuses a fixed set of already-open DB connections across requests instead of opening/closing a new connection per request, avoiding costly connection-setup overhead and exhausting the DB's connection limit.

17. **Q:** Why store large binary files (images, videos) in blob/object storage (e.g. S3) instead of a database?
   **A:** Databases are optimized for structured, queryable records, not large binaries; object storage is cheaper, scales better, and offloads that load from the DB.

18. **Q:** What kind of data is a time-series database (e.g. InfluxDB) optimized for?
   **A:** Data points indexed by time, like metrics or sensor readings, with efficient time-range queries and aggregation/downsampling.

19. **Q:** What is Elasticsearch typically used for in a system design?
   **A:** Full-text search and complex filtering/ranking over large datasets, using an inverted index — usually alongside, not instead of, a primary data store.

## Cloze cards

- The four main NoSQL families are {{c1::key-value}}, {{c2::document}}, {{c3::column-family (wide-column)}}, and {{c4::graph}} stores.
- Indexing speeds up {{c1::reads}} (faster lookups via a sorted structure) but slows down {{c2::writes}} (every index must be updated on each write).

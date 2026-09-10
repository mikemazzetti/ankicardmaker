---
deck: "Resume Prep::MongoDB"
topic: "MongoDB"
tags: [ankicardmaker, resume-prep, mongodb]
note_type: Mixed (Basic / Basic (and reversed card) / Cloze)
created: 2026-09-09
---

# MongoDB — Resume Prep

Source of truth for the `Resume Prep::MongoDB` deck (20 notes). Edit here and re-push to update.

## Basic cards

1. **Q:** Document (MongoDB) *(reversed — tested both ways)*
   **A:** MongoDB's basic unit of stored data — a JSON-like (BSON) record of field-value pairs.

2. **Q:** Collection (MongoDB) *(reversed — tested both ways)*
   **A:** A group of MongoDB documents, roughly analogous to a table in a relational database.

3. **Q:** What is BSON, and why does MongoDB use it instead of plain JSON on disk/wire?
   **A:** Binary JSON — a binary-encoded superset of JSON that adds types like Date and ObjectId and is faster to parse and traverse than text JSON.

4. **Q:** Write a MongoDB query to find all users older than 25 in the <code>users</code> collection.
   **A:** <pre><code>db.users.find({ age: { $gt: 25 } });</code></pre>

5. **Q:** Write a MongoDB command to insert a single new document into <code>users</code>.
   **A:** <pre><code>db.users.insertOne({
  name: "Alice",
  age: 30
});</code></pre>

6. **Q:** Write a MongoDB command to update one document, setting its <code>age</code> field.
   **A:** <pre><code>db.users.updateOne(
  { _id: id },
  { $set: { age: 31 } }
);</code></pre>

7. **Q:** What does the <code>$set</code> update operator do in MongoDB?
   **A:** Sets the value of a field (creating it if absent) without touching any other fields in the document.

8. **Q:** What is the MongoDB aggregation pipeline?
   **A:** A framework of sequential stages (e.g. <code>$match</code>, <code>$group</code>, <code>$sort</code>) that each transform documents and pass their output to the next stage — roughly SQL's WHERE/GROUP BY/HAVING chained together.

9. **Q:** Write an aggregation pipeline that totals order amount per customer.
   **A:** <pre><code>db.orders.aggregate([
  { $group: { _id: "$customerId",
              total: { $sum: "$amount" } } }
]);</code></pre>

10. **Q:** Write MongoDB syntax to create an ascending index on the <code>email</code> field of <code>users</code>.
   **A:** <pre><code>db.users.createIndex({ email: 1 });</code></pre>

11. **Q:** When should you embed a related document in MongoDB rather than reference it?
   **A:** When the related data is always accessed together with the parent, is small/bounded in size, and doesn't need independent querying — e.g. an address inside a user document.

12. **Q:** When should you reference a document in MongoDB instead of embedding it?
   **A:** When the related data is large, grows unbounded, is shared across many parents, or needs independent querying/updating — e.g. orders referencing a customer by ID.

13. **Q:** What is a MongoDB replica set?
   **A:** A group of mongod instances holding the same data set for redundancy — one primary accepts writes, and secondaries replicate from it and can serve reads or take over on failover.

14. **Q:** What is sharding in MongoDB and why is it used?
   **A:** Partitioning a collection's data across multiple servers (shards) by a shard key, to scale storage and throughput horizontally beyond one machine.

15. **Q:** How does MongoDB schema design philosophy differ from relational schema design?
   **A:** MongoDB is schema-flexible and denormalized by default — you model documents around how data is accessed together, not around eliminating redundancy the way normalized SQL tables do.

16. **Q:** In a React/Node.js/MongoDB app like Brawl Stars Western's site, why embed a user's profile settings inside their user document rather than a separate collection?
   **A:** They're always read and written together with the user and stay small and bounded — embedding avoids an extra query to join them back together.

17. **Q:** Write a MongoDB command to delete one document matching a filter.
   **A:** <pre><code>db.users.deleteOne({ _id: id });</code></pre>

18. **Q:** What does the <code>$exists</code> query operator check for in MongoDB?
   **A:** Whether a field is present (or, with <code>false</code>, absent) in the document, regardless of its value.

19. **Q:** What binary format does MongoDB store documents in on disk?
   **A:** BSON (Binary JSON).

## Cloze cards

- The MongoDB query operator {{c1::$in}} matches any value found in a given array, while {{c2::$gt}} matches values greater than a given value.

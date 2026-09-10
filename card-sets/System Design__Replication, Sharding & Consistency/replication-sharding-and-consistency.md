---
deck: "System Design::Replication, Sharding & Consistency"
topic: "Replication, Sharding & Consistency"
tags: [ankicardmaker, sd-consistency]
note_type: Mixed (Basic / Basic (and reversed card) / Cloze)
created: 2026-09-10
---

# Replication, Sharding & Consistency — System Design

Source of truth for the `System Design::Replication, Sharding & Consistency` deck (22 notes). Edit here and re-push to update.

## Basic cards

1. **Q:** What is leader-follower (single-leader) replication?
   **A:** One node (the leader) accepts all writes and propagates them to follower nodes, which serve reads.

2. **Q:** What is multi-leader replication?
   **A:** Multiple nodes each accept writes independently and replicate changes to one another, requiring conflict resolution.

3. **Q:** What is the main risk introduced by multi-leader replication?
   **A:** Write conflicts — the same data can be modified concurrently on different leaders and must be reconciled.

4. **Q:** Why might a system use asynchronous replication despite the risk of data loss?
   **A:** It gives lower write latency and higher availability, since the leader doesn't block on slow or unreachable followers.

5. **Q:** What is range-based sharding/partitioning?
   **A:** Partitioning data by contiguous ranges of the key (e.g. A-M, N-Z), which supports efficient range queries but risks hotspots.

6. **Q:** What is hash-based sharding/partitioning?
   **A:** Partitioning data by hashing the key and assigning it to a shard, spreading load evenly but losing ordered range-query locality.

7. **Q:** What problem does consistent hashing solve?
   **A:** It minimizes the number of keys that must be remapped when a node is added or removed, unlike simple modulo-based hashing.

8. **Q:** What is a hotspot in a sharded/partitioned system?
   **A:** A single shard or key that receives disproportionately high traffic, becoming a bottleneck while other shards sit idle.

9. **Q:** How can you mitigate a hotspot caused by one very popular key?
   **A:** Add randomness/salting to the key to spread its writes or reads across multiple shards, or cache it separately.

10. **Q:** In a CAP 'CP' tradeoff, what does the system favor, with an example?
   **A:** It favors consistency over availability during a partition — it rejects or blocks requests rather than return stale data (e.g. typical ZooKeeper/HBase configurations).

11. **Q:** In a CAP 'AP' tradeoff, what does the system favor, with an example?
   **A:** It favors availability over consistency during a partition — it keeps responding but may return stale data (e.g. Cassandra, DynamoDB by default).

12. **Q:** What does PACELC add to the CAP theorem?
   **A:** It notes that even without a Partition, you still face an Else tradeoff between Latency and Consistency — CAP only describes behavior during partitions.

13. **Q:** Strong consistency *(reversed — both ways)*
   **A:** Every read reflects the most recent write; all clients see the same data at the same time.

14. **Q:** Eventual consistency *(reversed — both ways)*
   **A:** Replicas may temporarily diverge after a write, but will converge to the same value once no new writes occur.

15. **Q:** In quorum-based replication, what does the condition <code>W + R &gt; N</code> guarantee?
   **A:** That every read quorum overlaps with every write quorum, so at least one node in a read has the latest write — guaranteeing read-your-writes consistency.

16. **Q:** In quorum notation, what do N, W, and R represent?
   **A:** N = total number of replicas, W = replicas that must acknowledge a write, R = replicas that must respond to a read.

17. **Q:** What is read-repair in a quorum-based system?
   **A:** When a read detects that some replicas returned stale data, it triggers a background write to update those replicas to the latest value.

18. **Q:** What is leader election, and why is it needed?
   **A:** The process by which distributed nodes agree on a new leader (e.g. via Raft or Paxos) after the current leader fails, so writes can continue.

19. **Q:** What is split-brain in a distributed system?
   **A:** A failure scenario where a network partition causes two nodes to each believe they are the leader, leading to conflicting writes.

## Cloze cards

- In {{c1::synchronous}} replication the leader waits for followers to confirm before acknowledging a write (safer, slower); in {{c2::asynchronous}} replication the leader acknowledges immediately without waiting (faster, risks data loss on leader failure).
- The CAP theorem states a distributed system can only guarantee two of three properties during a network partition: {{c1::Consistency}}, {{c2::Availability}}, and {{c3::Partition tolerance}}.
- PACELC: if there is a {{c1::Partition}}, trade off {{c2::Availability}} vs {{c3::Consistency}}; {{c4::Else}} (normal operation), trade off {{c5::Latency}} vs Consistency.

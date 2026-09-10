---
deck: "System Design::Distributed Message Queue (Kafka)"
topic: "Distributed Message Queue (Kafka)"
tags: [ankicardmaker, sd-message-queue]
note_type: Mixed (Basic / Basic (and reversed card) / Cloze)
created: 2026-09-10
---

# Distributed Message Queue (Kafka) — System Design

Source of truth for the `System Design::Distributed Message Queue (Kafka)` deck (22 notes). Edit here and re-push to update.

## Basic cards

1. **Q:** What are the core functional requirements of a distributed message queue like Kafka?
   **A:** Producers publish messages to topics; consumers subscribe and read messages, with support for multiple independent consumers reading the same stream.

2. **Q:** If a topic ingests 1M messages/sec at 1KB each, what's the raw ingestion bandwidth?
   **A:** ~1GB/sec (1M × 1KB), which drives how many partitions/brokers and how much disk throughput are needed.

3. **Q:** With 7-day retention at 1GB/sec average ingestion, roughly how much disk storage is needed before replication?
   **A:** ~604TB (1GB/sec × 86,400 sec/day × 7 days), then multiplied by the replication factor.

4. **Q:** What are the two primary client-facing operations in a Kafka-like queue's API?
   **A:** produce(topic, key, value) to publish a message, and poll()/consume(topic, partition, offset) to read messages.

5. **Q:** Why does produce() optionally take a message key rather than just a value?
   **A:** The key determines which partition the message is routed to (via hashing), so related messages (e.g. same user_id) land in the same partition and stay ordered.

6. **Q:** What is the fundamental unit of storage and parallelism within a Kafka topic?
   **A:** The partition — an ordered, append-only log of messages, each identified by a monotonically increasing offset.

7. **Q:** What three things uniquely identify a message's position for a consumer to resume reading?
   **A:** Topic, partition number, and offset within that partition.

8. **Q:** Why does splitting a topic into multiple partitions increase throughput?
   **A:** Each partition can be written to and read from independently, often on different brokers, letting producers and consumers parallelize across partitions.

9. **Q:** What does a consumer need to persist to resume reading after a crash without reprocessing or skipping messages?
   **A:** Its committed offset per partition — the position of the last successfully processed message.

10. **Q:** What guarantee does a consumer group provide when multiple consumer instances share the group?
   **A:** Each partition is consumed by exactly one consumer instance within the group at a time, so the group collectively processes each message once while scaling reads horizontally.

11. **Q:** What happens when a new consumer joins or an existing one leaves a consumer group?
   **A:** A rebalance is triggered, redistributing partition ownership across the group's remaining/new consumers.

12. **Q:** What is Kafka's ordering guarantee scope — global across a topic, or something narrower?
   **A:** Ordering is only guaranteed within a single partition, not across the whole topic.

13. **Q:** How do you guarantee all events for a given entity (e.g. one user) are processed in order?
   **A:** Use that entity's ID as the partition key so all its events hash to the same partition, preserving per-entity order.

14. **Q:** What does acks=all mean for a producer's write durability, and what does it look like configured?
   **A:** The producer waits for the write to be acknowledged by all in-sync replicas, not just the leader, before considering the write successful, maximizing durability at the cost of latency.<pre><code>acks=all
min.insync.replicas=2</code></pre>

15. **Q:** In-sync replica (ISR) *(reversed — both ways)*
   **A:** A follower replica fully caught up with the partition leader's log within a configured lag threshold, and thus eligible to be promoted to leader on failover without data loss.

16. **Q:** What becomes a bottleneck if a topic has too few partitions relative to consumer count?
   **A:** Consumer parallelism is capped at the number of partitions — extra consumer instances beyond that count sit idle.

17. **Q:** What's a common bottleneck from having a single very hot partition due to skewed key distribution?
   **A:** That partition's broker becomes a throughput/latency hotspot even though the cluster overall has capacity; mitigate with a better partitioning key or key salting.

18. **Q:** What's the tradeoff of acks=1 vs acks=all for producers?
   **A:** acks=1 (leader only) gives lower latency and higher throughput but risks losing the message if the leader fails before followers replicate it; acks=all is safer but slower.

19. **Q:** What's the tradeoff of increasing the partition count for a topic?
   **A:** More partitions increase parallelism and throughput, but add overhead: more open file handles, longer leader-election/rebalance times, more metadata.

## Cloze cards

- A message queue's key non-functional requirements are {{c1::durability}} (no message loss), {{c2::high throughput}}, {{c3::horizontal scalability}}, and {{c4::configurable ordering guarantees}}.
- Core components: {{c1::producers}} (publish messages), {{c2::brokers}} (store partitions, serve reads/writes), {{c3::consumer groups}} (coordinated parallel readers), and a {{c4::metadata/coordination service}} (e.g. a Raft-based controller) tracking partition leadership.
- Kafka-style durability relies on {{c1::replicating each partition across multiple brokers}}, electing a {{c2::leader replica}} that handles reads/writes, with {{c3::follower replicas}} that replicate the log and can be promoted if the leader fails.

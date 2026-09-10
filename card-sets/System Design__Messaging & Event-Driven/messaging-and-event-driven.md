---
deck: "System Design::Messaging & Event-Driven"
topic: "Messaging & Event-Driven"
tags: [ankicardmaker, sd-messaging]
note_type: Mixed (Basic / Basic (and reversed card) / Cloze)
created: 2026-09-10
---

# Messaging & Event-Driven — System Design

Source of truth for the `System Design::Messaging & Event-Driven` deck (21 notes). Edit here and re-push to update.

## Basic cards

1. **Q:** What is the key difference between a message queue and pub/sub?
   **A:** A queue delivers each message to exactly one consumer (point-to-point); pub/sub broadcasts each message to every subscriber of a topic.

2. **Q:** Give an example use case better suited to a message queue than pub/sub.
   **A:** Distributing work items across a pool of workers, where each task should be processed by only one worker (e.g. a background job queue).

3. **Q:** Give an example use case better suited to pub/sub than a message queue.
   **A:** Broadcasting an event (e.g. 'order placed') to multiple independent services that each need to react — email, analytics, inventory.

4. **Q:** In Kafka, what is a topic?
   **A:** A named stream/category of messages that producers write to and consumers read from.

5. **Q:** In Kafka, what is a partition?
   **A:** A topic is split into ordered, append-only partitions, each of which can be processed independently to allow parallelism.

6. **Q:** In Kafka, what is an offset?
   **A:** A sequential id marking a message's position within a partition, used by consumers to track their read progress.

7. **Q:** In Kafka, what is a consumer group?
   **A:** A set of consumers that share the work of reading a topic, where each partition is consumed by only one consumer in the group at a time.

8. **Q:** Why does Kafka only guarantee message ordering within a partition, not across a whole topic?
   **A:** Partitions are processed independently and in parallel by different consumers, so there's no global order across them — only within each partition's own sequence.

9. **Q:** Why is 'at-least-once' delivery the most common choice in practice, even though it can duplicate messages?
   **A:** It's simpler and cheaper to guarantee than exactly-once; the duplication risk is handled by making the consumer's handler idempotent.

10. **Q:** What does it mean for a message handler to be idempotent?
   **A:** Processing the same message multiple times produces the same result as processing it once, with no duplicate side effects.

11. **Q:** Give a common technique to make an operation idempotent.
   **A:** Use a unique idempotency key (e.g. request or message id), and check/record it before applying the operation, skipping it if already processed.

12. **Q:** What is a dead-letter queue (DLQ)?
   **A:** A separate queue that messages are routed to after repeatedly failing processing, so they don't block the main queue and can be inspected or retried later.

13. **Q:** What is backpressure in a messaging system?
   **A:** A mechanism that slows or pauses producers when consumers can't keep up, preventing the system from being overwhelmed.

14. **Q:** Name one way a system can apply backpressure.
   **A:** Bounded queues that block or reject new messages once full, or pull-based consumers that explicitly request a limited batch size.

15. **Q:** What is event sourcing?
   **A:** Storing all changes to application state as an immutable sequence of events, rather than just the current state, so state is derived by replaying events.

16. **Q:** What is a key benefit of event sourcing?
   **A:** A full audit log/history of how state was reached, plus the ability to rebuild or replay state as of any point in time.

17. **Q:** Why is CQRS often paired with event sourcing?
   **A:** Events from the write model naturally serve as the source of truth used to build and update optimized read-side projections.

18. **Q:** What is the tradeoff between synchronous (request/response) and asynchronous (event/message-based) service communication?
   **A:** Sync is simpler and gives an immediate result but couples services' availability and latency together; async decouples services and improves resilience/throughput but adds complexity (eventual consistency, harder debugging).

19. **Q:** Why can strict message ordering be hard to achieve at scale?
   **A:** Parallelism (multiple partitions/consumers) is needed for throughput, but processing in parallel breaks global order — ordering is usually only guaranteed per-partition or per-key.

## Cloze cards

- Message delivery semantics: {{c1::at-most-once}} (message may be lost, never duplicated), {{c2::at-least-once}} (message may be duplicated, never lost), {{c3::exactly-once}} (message delivered and processed exactly one time).
- CQRS separates the {{c1::write model}} (handles commands that change state) from the {{c2::read model}} (optimized for queries), often backed by different data stores.

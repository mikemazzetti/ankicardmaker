---
deck: "System Design::Unique ID Generator"
topic: "Unique ID Generator"
tags: [ankicardmaker, sd-id-generator]
note_type: Mixed (Basic / Basic (and reversed card) / Cloze)
created: 2026-09-10
---

# Unique ID Generator — System Design

Source of truth for the `System Design::Unique ID Generator` deck (22 notes). Edit here and re-push to update.

## Basic cards

1. **Q:** What are the core functional requirements of a unique ID generator service?
   **A:** Generate IDs that are unique across the whole distributed system, at high throughput, with low latency, for use as primary keys/identifiers.

2. **Q:** If a system needs to generate 1M new IDs/sec globally, what does this imply about the ID generation approach?
   **A:** It rules out any approach requiring a round-trip to a single central coordinator per ID (too much contention/latency); IDs must be generatable locally/independently per node.

3. **Q:** What is a UUID (v4) and what are its main pros/cons for use as a distributed ID?
   **A:** A 128-bit randomly generated identifier. Pro: generated locally with no coordination, globally unique with negligible collision odds. Con: not sortable/time-ordered, large (128 bits), and poor for DB index locality.

4. **Q:** What are the main advantages of Snowflake-style IDs over UUIDs for a high-throughput distributed system?
   **A:** Roughly time-sortable (good for DB index locality and range queries), compact (64-bit fits in a long/bigint), and generated locally per machine with no coordination needed per ID.

5. **Q:** How is the machine/worker ID portion of a Snowflake ID typically assigned to avoid collisions?
   **A:** Assigned via a coordination service (e.g., ZooKeeper) at machine startup, which hands out unique worker IDs from a fixed pool and prevents two machines from reusing the same ID.

6. **Q:** How can a ticket-server approach scale beyond one DB's throughput while keeping IDs roughly unique per server?
   **A:** Run multiple DB servers each auto-incrementing with a different starting offset and a fixed step (e.g., server 1: 1,4,7...; server 2: 2,5,8...), so their outputs never collide.

7. **Q:** What is the 'range handoff' (segment-based) approach to distributed ID generation?
   **A:** A central allocator hands each application server a contiguous block/range of IDs (e.g., 1000 at a time) to consume locally; the server requests a new range only after exhausting the current one, drastically reducing coordination frequency.

8. **Q:** What does it mean for an ID sequence to be 'monotonically increasing', and why is it desirable?
   **A:** Each newly generated ID is guaranteed larger than all previously generated IDs; desirable because it keeps DB indexes append-friendly (fast inserts) and lets IDs double as a rough creation-time ordering.

9. **Q:** What problem does clock skew (or clock drift) cause for timestamp-based ID generators like Snowflake?
   **A:** If a machine's clock jumps backward (e.g., due to NTP correction), it could generate a timestamp bit pattern lower than IDs it already issued, breaking monotonicity and risking ID collisions.

10. **Q:** When would you prefer UUIDs over Snowflake IDs, and vice versa?
   **A:** Prefer UUIDs when you need fully decentralized generation with zero coordination and don't care about sortability (e.g., client-side generated IDs). Prefer Snowflake when you need compact, roughly time-ordered, high-throughput IDs for DB primary keys.

11. **Q:** What are the main components of a standalone ID-generation service using the Snowflake approach?
   **A:** Stateless ID-generator nodes (each with an assigned worker ID), a coordination service for worker-ID assignment, and client SDKs/load balancer routing requests to any generator node.

12. **Q:** What happens when the 12-bit sequence number in a Snowflake ID (4096 values) is exhausted within a single millisecond?
   **A:** The generator must wait until the next millisecond tick before issuing more IDs, capping a single machine's throughput at 4096 IDs/ms (4.096M IDs/sec) for that worker.

13. **Q:** Why is a single database's native auto-increment column usually insufficient as the sole ID source for a large distributed system?
   **A:** It creates a single write bottleneck and single point of failure, and doesn't allow multiple independent services/regions to generate IDs concurrently without contention.

## Cloze cards

- A unique ID generator should ideally produce IDs that are {{c1::roughly sortable by time (monotonically increasing)}}, are {{c2::compact (fit in 64 bits)}}, and can be generated {{c3::without a central bottleneck/single point of failure}}.
- A dedicated ID-generation service typically exposes a simple endpoint like <pre><code>GET /v1/ids/next</code></pre> returning a {{c1::single new unique ID}}, or a batch variant <pre><code>GET /v1/ids/next?count=1000</code></pre> to {{c2::amortize network round-trips}}.
- A Snowflake-style 64-bit ID is composed of <pre><code>1 bit unused | 41 bits timestamp | 10 bits machine/worker ID | 12 bits sequence number</code></pre> — the {{c1::timestamp}} bits make IDs roughly time-sortable, and the {{c2::sequence number}} disambiguates multiple IDs generated in the same millisecond by the same machine.
- A {{c1::database ticket server}} generates unique IDs by using a single (or few) database's {{c2::auto-increment}} column as a centralized ID source, which is simple and strictly ordered but becomes a {{c3::single point of failure / throughput bottleneck}} at scale.
- Range/segment handoff trades a small amount of {{c1::ID space waste (unused IDs if a server crashes mid-range)}} for a large reduction in {{c2::coordination overhead / central-allocator load}}, since a round trip is only needed once per block instead of once per ID.
- Snowflake IDs are monotonically increasing {{c1::only within a single machine}} (since each machine's timestamp+sequence only grows), but {{c2::not strictly ordered across different machines}} because clocks and sequence counters differ per machine.
- Common mitigations for clock skew in Snowflake-style generators include {{c1::refusing to generate IDs and waiting/erroring if the clock is detected to have moved backward}}, and {{c2::using monotonic clocks or NTP with smoothing (slewing) instead of step corrections}}.
- Because each Snowflake generator node produces IDs independently using only local timestamp+sequence state, the ID generator scales {{c1::horizontally with no shared bottleneck}} — the only shared dependency is the one-time {{c2::worker-ID assignment}} at startup.
- Choosing an ID scheme is a tradeoff between {{c1::coordination cost}}, {{c2::ID size}}, and {{c3::sortability}} — UUIDs minimize coordination but sacrifice sortability and size; Snowflake balances all three; a central ticket server maximizes strict ordering but sacrifices availability/scale.

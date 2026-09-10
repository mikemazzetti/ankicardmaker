---
deck: "System Design::Distributed Key-Value Store"
topic: "Distributed Key-Value Store"
tags: [ankicardmaker, sd-kv-store]
note_type: Mixed (Basic / Basic (and reversed card) / Cloze)
created: 2026-09-10
---

# Distributed Key-Value Store — System Design

Source of truth for the `System Design::Distributed Key-Value Store` deck (20 notes). Edit here and re-push to update.

## Basic cards

1. **Q:** What are the two core client-facing operations a distributed key-value store must support?
   **A:** put(key, value) and get(key).

2. **Q:** Why do Dynamo-style KV stores favor availability over strict consistency (per CAP)?
   **A:** During a network partition, write availability matters more for workloads like a shopping cart than immediate consistency; conflicting writes are reconciled later.

3. **Q:** For 100M keys averaging 1KB each, roughly how much raw storage is needed before replication?
   **A:** ~100GB (100M × 1KB). With 3x replication, ~300GB.

4. **Q:** If a KV store serves 50,000 reads/sec and 5,000 writes/sec, what read:write ratio should the design optimize for?
   **A:** 10:1 — read-heavy, so optimize caching and read replicas.

5. **Q:** What might a vector clock look like when serialized in a PUT response, so the client can supply it on the next write?
   **A:** <pre><code>{
  "key": "user123",
  "value": "...",
  "vector_clock": {
    "nodeA": 2,
    "nodeB": 1
  }
}</code></pre>

6. **Q:** In a Dynamo-style KV store, what structure is a value stored with?
   **A:** The value itself, plus a vector clock (version metadata), stored as (key, value, vector_clock).

7. **Q:** What problem does consistent hashing solve in a distributed KV store?
   **A:** It minimizes key remapping when nodes are added or removed — only about K/N keys move instead of nearly all keys.

8. **Q:** Why do Dynamo-style systems assign multiple virtual nodes (vnodes) to each physical node on the hash ring?
   **A:** To spread load more evenly, and so that when a node fails, its keys are redistributed across many other nodes rather than overloading one neighbor.

9. **Q:** In Dynamo-style replication, how is a key's replica set chosen on the hash ring?
   **A:** The key is placed at its hash position, and the next N-1 distinct physical nodes walking clockwise around the ring also store replicas.

10. **Q:** With N=3, W=1, R=1, what consistency/availability tradeoff is being made?
   **A:** Maximizes availability and lowers latency, but sacrifices consistency — reads can return stale data since R+W ≤ N.

11. **Q:** Gossip protocol (in a distributed KV store) *(reversed — both ways)*
   **A:** A peer-to-peer mechanism where nodes periodically exchange membership/health state, so join/leave/failure information spreads through the cluster without a central coordinator.

12. **Q:** What does a vector clock entry (node, counter) capture for a value?
   **A:** Which node performed the write and how many writes that node has made to the key, letting the system detect causality between versions.

13. **Q:** When two versions of a key have vector clocks that are neither ancestor nor descendant of each other, what does the KV store do?
   **A:** It flags them as a sibling/conflict and returns both versions to the client or application to reconcile, e.g. via last-writer-wins or app-level merge logic.

14. **Q:** What KV-store mechanism repairs a replica that missed a write due to a temporary node outage, without blocking the client?
   **A:** Hinted handoff — a healthy node temporarily stores the write with a 'hint' and forwards it to the original replica once it recovers.

15. **Q:** What is a common bottleneck when a single key becomes extremely popular (a hot key) in a sharded KV store?
   **A:** That key's owning node(s) get disproportionate load, causing hotspotting even though the cluster as a whole is balanced.

16. **Q:** What is the tradeoff of increasing the replication factor N in a KV store?
   **A:** Higher durability and read availability, but more storage cost and more write coordination overhead/latency.

## Cloze cards

- A distributed KV store's core non-functional requirements are {{c1::high availability}}, {{c2::horizontal scalability}}, {{c3::low latency}}, and {{c4::eventual consistency}} (tunable).
- A minimal KV store HTTP API exposes {{c1::PUT /keys/{key}}} to write, {{c2::GET /keys/{key}}} to read, and {{c3::DELETE /keys/{key}}} to remove a value.
- The main components of a distributed KV store are {{c1::a coordinator/router node}} (routes requests), {{c2::storage nodes}} (persist key ranges), and {{c3::a membership/gossip layer}} (tracks cluster state).
- Dynamo-style quorum consistency uses three tunable parameters: {{c1::N}} (replicas), {{c2::R}} (nodes that must ack a read), and {{c3::W}} (nodes that must ack a write); strong consistency requires {{c4::R + W > N}}.

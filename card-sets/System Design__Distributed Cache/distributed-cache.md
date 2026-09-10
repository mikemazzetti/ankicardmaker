---
deck: "System Design::Distributed Cache"
topic: "Distributed Cache"
tags: [ankicardmaker, sd-distributed-cache]
note_type: Mixed (Basic / Basic (and reversed card) / Cloze)
created: 2026-09-10
---

# Distributed Cache — System Design

Source of truth for the `System Design::Distributed Cache` deck (22 notes). Edit here and re-push to update.

## Basic cards

1. **Q:** What are the core functional requirements of a distributed cache service?
   **A:** Support get/set/delete of key-value pairs with low latency, support TTL/expiration, and scale horizontally across many nodes while distributing keys evenly.

2. **Q:** If a service needs to cache 500M key-value pairs averaging 1KB each, what is the approximate total cache memory needed (before replication)?
   **A:** 500,000,000 x 1KB ~ 500 GB of memory

3. **Q:** What is the basic data model of a distributed cache, and how does it differ from a relational DB?
   **A:** Simple key-value pairs (often with a TTL) — no schema, no joins, no complex queries; optimized purely for fast point lookups by key.

4. **Q:** What are the main components in a distributed cache's high-level architecture?
   **A:** Cache client (with routing/hashing logic), a cluster of cache nodes holding data in memory, and often a coordination layer (e.g., gossip protocol or config service) tracking cluster membership.

5. **Q:** What is consistent hashing?
   **A:** A hashing scheme that maps both nodes and keys onto a fixed hash ring (e.g., 0 to 2^32-1); each key is owned by the first node found clockwise from its hash position, so adding/removing a node only remaps a small fraction of keys.

6. **Q:** Why do consistent hashing implementations use 'virtual nodes' (multiple points per physical node on the ring)?
   **A:** A single point per physical node can lead to uneven load distribution (some nodes owning much larger ring arcs); virtual nodes spread each physical node's ownership across many smaller arcs, balancing load more evenly.

7. **Q:** Why does a cache need an eviction policy even when using TTLs?
   **A:** Memory is finite — even before TTLs expire, the cache may fill up and need to proactively remove entries to make room for new writes.

8. **Q:** How does LFU (Least Frequently Used) eviction differ from LRU, and when might it be preferred?
   **A:** LFU evicts the entry with the fewest total accesses (regardless of recency), which better protects consistently popular items from being evicted by a short burst of unrelated new accesses.

9. **Q:** What is a 'hot key' problem in a distributed cache?
   **A:** A single key (e.g., a viral post or celebrity profile) receives disproportionately high traffic, overloading the one node that owns it via consistent hashing, even though the rest of the cluster is underutilized.

10. **Q:** Describe the cache-aside (lazy loading) pattern for reads.
   **A:** On a read: check the cache first; on a hit, return the cached value; on a miss, read from the database, then populate the cache with that value before returning it to the caller.

11. **Q:** What is a cache stampede (thundering herd), and how can it be prevented?
   **A:** When a popular cached key expires, many concurrent requests simultaneously miss the cache and hit the database at once; prevented with request coalescing (only one request refetches, others wait) or staggered/jittered TTLs.

12. **Q:** What consistency tradeoff do distributed caches typically accept, and why?
   **A:** Eventual consistency between cache and database (a write to the DB may take a moment to invalidate/update the cache) — acceptable because caches optimize for speed, and most applications tolerate briefly stale reads.

## Cloze cards

- A distributed cache prioritizes {{c1::very low latency (sub-millisecond to low-millisecond)}} and {{c1::high throughput}} over strict durability — cache data is often treated as {{c2::disposable/reconstructible from the source of truth}}.
- A distributed cache client typically talks to the cluster via simple operations: <pre><code>GET key
SET key value TTL
DEL key</code></pre> where {{c1::TTL}} lets entries expire automatically without explicit deletion.
- Naively sharding keys with <pre><code>hash(key) % N</code></pre> works until the cluster resizes (N changes) — then {{c1::almost all keys remap to different nodes}}, causing a massive cache miss storm.
- With consistent hashing, adding or removing one node out of N remaps only about {{c1::1/N of the keys}} on average, instead of remapping nearly all keys as with modulo hashing.
- To tolerate node failure, a distributed cache typically replicates each key to the next {{c1::N-1 nodes clockwise on the hash ring}} (its 'preference list'), so losing one node doesn't lose that key's data.
- {{c1::LRU (Least Recently Used)}} eviction removes the entry that hasn't been accessed for the {{c1::longest time}}, based on the assumption that recently accessed items are more likely to be accessed again soon.
- Hot keys are commonly mitigated by {{c1::replicating the hot key's value onto multiple nodes/local caches so reads are load-balanced}}, or by adding a {{c2::random suffix (key sharding) so a single logical key is split across several physical keys}}.
- In {{c1::write-through}} caching, writes go to the cache and the database synchronously (safer, slower); in {{c2::write-back (write-behind)}} caching, writes go to the cache immediately and are flushed to the database asynchronously later (faster, riskier on cache failure).
- As traffic grows, a distributed cache's bottleneck shifts from any single node's CPU/memory to {{c1::network bandwidth and connection count}} on hot nodes, addressed by {{c2::adding more nodes (with consistent hashing) and/or client-side local caching}}.
- Distributed caches usually keep data purely {{c1::in-memory}} (optionally with limited disk persistence for faster restart), trading {{c2::durability guarantees}} for the speed benefits of avoiding disk I/O on the hot path.

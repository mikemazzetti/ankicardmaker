---
deck: "System Design::Caching & CDN"
topic: "Caching & CDN"
tags: [ankicardmaker, sd-caching]
note_type: Mixed (Basic / Basic (and reversed card) / Cloze)
created: 2026-09-10
---

# Caching & CDN — System Design

Source of truth for the `System Design::Caching & CDN` deck (22 notes). Edit here and re-push to update.

## Basic cards

1. **Q:** Why introduce a cache in a system?
   **A:** To reduce latency and load on the primary data store by serving frequently accessed data from faster storage.

2. **Q:** Cache hit *(reversed — both ways)*
   **A:** A request that finds the requested data already present in the cache.

3. **Q:** Cache miss *(reversed — both ways)*
   **A:** A request for data not found in the cache, requiring a fetch from the slower underlying source.

4. **Q:** In the cache-aside (lazy-loading) pattern, who is responsible for populating the cache on a miss?
   **A:** The application: it reads from the cache, and on a miss it reads from the DB and writes the result into the cache itself.

5. **Q:** In read-through caching, who populates the cache on a miss?
   **A:** The cache itself — it sits in front of the DB and transparently loads missing data, so the application only ever talks to the cache.

6. **Q:** What is write-through caching?
   **A:** Writes go to the cache and the underlying DB synchronously as one operation, keeping the cache always consistent with the DB but adding write latency.

7. **Q:** What is write-back (write-behind) caching?
   **A:** Writes go to the cache immediately and are asynchronously flushed to the DB later, giving low write latency but risking data loss if the cache fails before flushing.

8. **Q:** Cache-aside vs read-through: what's the key difference in responsibility?
   **A:** In cache-aside the application manages loading the cache on a miss; in read-through the cache layer manages it transparently.

9. **Q:** Why is TTL-based eviction useful even alongside LRU/LFU?
   **A:** It guarantees data won't stay stale forever, bounding how out-of-date a cached value can get.

10. **Q:** Why is cache invalidation considered a hard problem?
   **A:** It's difficult to guarantee every cached copy of a piece of data is updated or removed exactly when the underlying data changes, especially across distributed caches and concurrent writes.

11. **Q:** What is a 'thundering herd' (cache stampede)?
   **A:** When a popular cached key expires or is evicted and many concurrent requests simultaneously miss the cache and hammer the backend to recompute the same value.

12. **Q:** What is a local (in-process) cache?
   **A:** A cache stored in a single application instance's own memory — very fast, but not shared across instances and lost on restart.

13. **Q:** What is a distributed cache, and give an example technology?
   **A:** A cache shared across multiple application instances over the network, e.g. Redis or Memcached.

14. **Q:** What is one key architectural difference between Redis and Memcached?
   **A:** Redis supports rich data structures and persistence/replication; Memcached is a simpler, purely in-memory key-value cache.

15. **Q:** What is the main tradeoff of a local cache vs a distributed cache?
   **A:** Local caches are faster with no network hop but cause inconsistency across instances; distributed caches stay consistent across instances but add network latency.

16. **Q:** What is a CDN's primary purpose?
   **A:** To cache and serve content from servers geographically close to the user, reducing latency and offloading the origin server.

17. **Q:** What is 'edge caching'?
   **A:** Storing copies of content at edge servers distributed near end users, rather than only at a central origin, so requests are served from the nearest location.

18. **Q:** What does 'cache consistency' refer to?
   **A:** How closely the data in a cache matches the current true state of the underlying data source.

19. **Q:** Name a core tradeoff in cache consistency design.
   **A:** Stronger consistency (always fresh) typically costs more latency and invalidation overhead; weaker (eventual) consistency is faster but can serve stale data.

## Cloze cards

- The four common cache read/write patterns are {{c1::cache-aside}}, {{c2::read-through}}, {{c3::write-through}}, and {{c4::write-back}}.
- Common cache eviction policies: {{c1::LRU}} (evicts the least recently used item), {{c2::LFU}} (evicts the least frequently used item), and {{c3::TTL}} (expires items after a fixed time regardless of usage).
- Cache stampedes can be mitigated with techniques like {{c1::locking/mutex around the recompute}}, {{c2::early or probabilistic refresh before expiry}}, or {{c3::serving stale data while recomputing in the background}}.

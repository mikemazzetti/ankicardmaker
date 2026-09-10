---
deck: "Resume Prep::Redis"
topic: "Redis"
tags: [ankicardmaker, resume-prep, redis]
note_type: Mixed (Basic / Basic (and reversed card) / Cloze)
created: 2026-09-09
---

# Redis — Resume Prep

Source of truth for the `Resume Prep::Redis` deck (18 notes). Edit here and re-push to update.

## Basic cards

1. **Q:** What kind of data store is Redis, and what roles is it commonly used for?
   **A:** An in-memory key-value data store, optionally persisted to disk — commonly used as a cache, message broker, or fast primary store for counters/sessions.

2. **Q:** Write a Redis command to set a key with a 60-second expiry.
   **A:** <pre><code>SET session:123 "data" EX 60</code></pre>

3. **Q:** What does TTL stand for in Redis, and what does the <code>TTL</code> command return?
   **A:** Time To Live — returns the remaining seconds until a key expires (<code>-1</code> if it has no expiry, <code>-2</code> if the key doesn't exist).

4. **Q:** Describe the cache-aside (lazy-loading) caching pattern.
   **A:** On read, check the cache first; on a miss, fetch from the source of truth (e.g. the DB), then write the result into the cache before returning it.

5. **Q:** In cache-aside, what must the application do on a write to keep the cache from serving stale data?
   **A:** Invalidate (or update) the corresponding cache entry right after writing to the source of truth.

6. **Q:** What Redis command publishes a message to a channel in pub/sub?
   **A:** <code>PUBLISH channel message</code> (subscribers use <code>SUBSCRIBE channel</code>).

7. **Q:** What's the key limitation of Redis pub/sub compared to a durable message queue?
   **A:** Messages aren't persisted — a subscriber that isn't connected at publish time never receives that message.

8. **Q:** RDB persistence (Redis) *(reversed — tested both ways)*
   **A:** Point-in-time binary snapshots of the whole dataset saved to disk at configured intervals.

9. **Q:** AOF persistence (Redis) *(reversed — tested both ways)*
   **A:** Append-only file logging every write operation, replayed on restart to rebuild the dataset.

10. **Q:** Why is <code>INCR</code> atomic in Redis, and why does that matter for counters?
   **A:** Redis executes each command as one indivisible step, so <code>INCR</code> reads and writes the counter atomically — avoiding lost updates from concurrent clients incrementing the same key.

11. **Q:** Write a Redis command to atomically increment a page-view counter.
   **A:** <pre><code>INCR pageviews:home</code></pre>

12. **Q:** Which Redis data type is best suited for a leaderboard ranked by score, and why?
   **A:** Sorted set (<code>ZSET</code>) — each member has a score, and Redis keeps members ordered for fast range and rank queries.

13. **Q:** Write a Redis command to add a player's score to a leaderboard sorted set.
   **A:** <pre><code>ZADD leaderboard 1500 "player1"</code></pre>

14. **Q:** When would you choose Redis as the primary data store rather than only a cache?
   **A:** When the workload needs very low-latency reads/writes on data that fits in memory and can tolerate Redis's persistence/durability tradeoffs — e.g. session stores, rate limiters, real-time counters.

15. **Q:** What Redis command retrieves and removes the first element of a list, useful for a queue?
   **A:** <code>LPOP</code> (or <code>BLPOP</code> for a blocking pop).

16. **Q:** What's the difference between <code>EXPIRE</code> and <code>PERSIST</code> in Redis?
   **A:** <code>EXPIRE</code> sets a TTL so the key auto-deletes after that time; <code>PERSIST</code> removes any existing TTL, making the key permanent again.

17. **Q:** Write a Redis command storing a hash of a user's name and age under one key.
   **A:** <pre><code>HSET user:1 name "Alice" age "30"</code></pre>

## Cloze cards

- Redis's core data types include {{c1::string}}, {{c2::hash}}, {{c3::list}}, {{c4::set}}, and {{c5::sorted set}}.

---
deck: "System Design::Rate Limiter"
topic: "Rate Limiter"
tags: [ankicardmaker, sd-rate-limiter]
note_type: Mixed (Basic / Basic (and reversed card) / Cloze)
created: 2026-09-10
---

# Rate Limiter — System Design

Source of truth for the `System Design::Rate Limiter` deck (21 notes). Edit here and re-push to update.

## Basic cards

1. **Q:** Why should a rate limiter fail open (allow traffic) rather than fail closed (block all traffic) if its backing store goes down?
   **A:** The rate limiter is a protective add-on, not the core business logic; failing closed would take down the entire service over a limiter outage, which is worse than temporarily allowing excess traffic.

2. **Q:** If an API serves 100K requests/sec across many clients, roughly how many rate-limit checks/sec must the limiter perform?
   **A:** About 100,000 checks/sec, one per incoming request, since each must be validated against its client's limit before being served.

3. **Q:** Why is a rate limiter's storage footprint small even at huge request volume (e.g. millions of clients)?
   **A:** It only stores a small counter/timestamp state per client key, not the request history itself; e.g. 10M clients x ~50 bytes ≈ 500MB, easily fitting in memory.

4. **Q:** What HTTP headers does a rate limiter typically return to inform the client of its limit status?
   **A:** <pre><code>X-RateLimit-Limit: 100
X-RateLimit-Remaining: 42
X-RateLimit-Reset: 1699999999</code></pre>

5. **Q:** What HTTP status code should a rate limiter return when a client exceeds its quota?
   **A:** 429 Too Many Requests.

6. **Q:** Why is Redis a common backing store for a distributed rate limiter?
   **A:** It is in-memory (low latency), supports atomic increment/expire operations (INCR, EXPIRE) needed to update counters safely under concurrency, and can be shared across multiple stateless application servers.

7. **Q:** How does the token bucket algorithm work?
   **A:** A bucket holds tokens up to a max capacity, refilled at a fixed rate; each request consumes one token, and requests are rejected when the bucket is empty, allowing short bursts up to the bucket capacity.

8. **Q:** How does the leaky bucket algorithm work?
   **A:** Requests enter a fixed-size queue processed at a constant output rate, like water leaking from a bucket at a steady rate; if the queue is full, new requests are dropped, smoothing bursts into a steady rate.

9. **Q:** What is the key difference in output traffic shape between token bucket and leaky bucket?
   **A:** Token bucket allows bursty output up to the bucket size as long as tokens are available; leaky bucket enforces a strictly smooth, constant output rate regardless of input burstiness.

10. **Q:** What problem does the fixed window counter algorithm have at window boundaries?
   **A:** A client can send a full quota of requests right before a window ends and another full quota right after it resets, effectively doubling the allowed rate in a short burst spanning the boundary.

11. **Q:** How does the sliding window counter (weighted) algorithm approximate sliding-log accuracy more cheaply?
   **A:** It keeps counts for the current and previous fixed windows, then computes a weighted estimate based on how far into the current window we are (previous_count x overlap_fraction + current_count), using far less memory than storing every timestamp.

12. **Q:** In a distributed rate limiter backed by Redis, why must the counter increment-and-check be atomic?
   **A:** Multiple application servers can process concurrent requests from the same client simultaneously; without an atomic operation (e.g. a Lua script or INCR+EXPIRE), a race condition could let the counter under-count and allow more requests through than the limit permits.

13. **Q:** Sketch a minimal Redis Lua script for atomic token-bucket rate limiting.
   **A:** <pre><code>local tokens = redis.call('GET', key)
if tokens == false then
  redis.call('SET', key, limit-1, 'EX', window)
  return 1
elseif tonumber(tokens) &gt; 0 then
  redis.call('DECR', key)
  return 1
else
  return 0
end</code></pre>

14. **Q:** What is the main scaling bottleneck of a centralized Redis-backed rate limiter as request volume grows into the millions/sec?
   **A:** The single Redis instance (or a hot key) becomes a throughput/latency bottleneck since every request requires a round trip to check and update the shared counter; mitigated by sharding counters by client key across a Redis cluster.

15. **Q:** What is the core tradeoff between sliding window log (accurate) and fixed window counter (cheap) rate limiting?
   **A:** Sliding window log gives precise, smooth rate limiting but uses much more memory since it stores every timestamp; fixed window counter is cheap and simple but allows boundary-burst abuse, so sliding window counter (weighted) is often chosen as a middle ground.

16. **Q:** Why is rate limiting sometimes applied at multiple levels (e.g. per-user, per-IP, and global) rather than a single rule?
   **A:** Different abuse patterns need different granularity: per-user limits stop a single account from overwhelming the system, per-IP limits catch unauthenticated or distributed abuse, and a global limit protects overall backend capacity regardless of source.

## Cloze cards

- Core functional requirements for a rate limiter: {{c1::limit requests per client}} to a configured threshold, {{c2::reject or throttle}} excess requests, and {{c3::return an appropriate response}} (e.g. HTTP 429) when limited.
- Key non-functional requirements: the limiter must add {{c1::minimal latency}}, must be {{c2::highly available}} (an outage shouldn't take down the whole system), and must work correctly across {{c3::multiple distributed servers}}.
- A basic rate-limit counter record stores a {{c1::client/API key}}, a {{c2::current request count}}, and a {{c3::window start timestamp or expiry}}.
- A rate limiter can be deployed as {{c1::middleware in the application server}}, as a {{c2::separate service/gateway}} in front of backends, or {{c3::within a client library}}; a standalone service is preferred for consistency across many backend services.
- The sliding window log algorithm stores a {{c1::timestamp for every request}} and counts entries within the trailing window, giving {{c2::perfect accuracy}} at the cost of {{c3::high memory usage}} per client.

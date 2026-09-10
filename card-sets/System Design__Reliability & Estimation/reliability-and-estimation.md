---
deck: "System Design::Reliability & Estimation"
topic: "Reliability & Estimation"
tags: [ankicardmaker, sd-reliability]
note_type: Mixed (Basic / Basic (and reversed card) / Cloze)
created: 2026-09-10
---

# Reliability & Estimation — System Design

Source of truth for the `System Design::Reliability & Estimation` deck (22 notes). Edit here and re-push to update.

## Basic cards

1. **Q:** What does 'three nines' (99.9%) availability translate to in downtime per year?
   **A:** About 8.76 hours of downtime per year.

2. **Q:** What does 'five nines' (99.999%) availability translate to in downtime per year?
   **A:** About 5.26 minutes of downtime per year.

3. **Q:** Why is an SLO typically set stricter than the corresponding SLA?
   **A:** To leave a safety margin, so the team notices and fixes problems internally before the customer-facing SLA is actually breached.

4. **Q:** What is redundancy in system design?
   **A:** Running duplicate components (servers, replicas, data centers) so that if one fails, others can take over without a service outage.

5. **Q:** What is failover?
   **A:** The automatic process of switching to a redundant/standby component when the active one fails.

6. **Q:** What is graceful degradation?
   **A:** Under failure or overload, a system keeps its core functionality working by disabling or simplifying non-essential features rather than failing completely.

7. **Q:** What problem does a circuit breaker solve?
   **A:** It stops a service from repeatedly calling a downstream dependency that is failing, failing fast instead and giving the dependency time to recover.

8. **Q:** What are the three states of a circuit breaker?
   **A:** Closed (calls flow normally), Open (calls fail immediately without trying), and Half-Open (a few test calls are let through to check for recovery).

9. **Q:** Why use exponential backoff when retrying a failed request?
   **A:** Increasing the wait time between retries avoids overwhelming an already struggling downstream service with a retry storm.

10. **Q:** Why should retry backoff usually include random jitter?
   **A:** Without jitter, many clients retry at the exact same intervals in sync, causing repeated synchronized traffic spikes (a 'thundering herd').

11. **Q:** What does a request timeout protect against?
   **A:** A slow or unresponsive dependency holding a caller's resources (threads/connections) indefinitely, which could cascade into resource exhaustion.

12. **Q:** What is the bulkhead pattern?
   **A:** Isolating resources (e.g. thread pools or connection pools) per dependency or service, so one failing dependency can't exhaust resources needed by others.

13. **Q:** How does the token bucket rate-limiting algorithm work?
   **A:** Tokens are added to a bucket at a fixed rate up to a max capacity; each request consumes a token, and requests are rejected/delayed once the bucket is empty — this allows short bursts.

14. **Q:** How does the leaky bucket rate-limiting algorithm work?
   **A:** Requests enter a fixed-size queue and are processed ('leak out') at a constant rate, smoothing bursty traffic into a steady output rate.

15. **Q:** What is an idempotency key used for in an API?
   **A:** A client-supplied unique id attached to a request so that if the request is retried (e.g. after a timeout), the server can detect the duplicate and avoid double-processing it (e.g. double-charging a payment).

16. **Q:** In back-of-envelope estimation, how do you roughly estimate QPS from daily active users?
   **A:** <code>(daily active users &times; actions per user per day) / 86,400 seconds</code>, often multiplied by a peak-factor (e.g. 2-3x) to get peak QPS. Note: a day has about 86,400 seconds (~10^5), a useful constant to memorize.

17. **Q:** What is the difference between a liveness and a readiness health check?
   **A:** Liveness asks 'is the process still running/not deadlocked' (restart it if failing); readiness asks 'is the service ready to accept traffic' (remove it from the load balancer if failing, without necessarily restarting it).

18. **Q:** Why is monitoring with alerting important beyond just logging?
   **A:** Logs require someone to go look; monitoring with alerts proactively notifies the team when a metric crosses a threshold, enabling faster incident response.

## Cloze cards

- {{c1::SLA}} (Service Level Agreement) is the external contract/promise made to customers; {{c2::SLO}} (Service Level Objective) is the internal target a team aims for; {{c3::SLI}} (Service Level Indicator) is the actual measured metric.
- Token bucket allows {{c1::bursts}} of traffic up to the bucket size, while leaky bucket enforces a {{c2::constant, smoothed}} output rate regardless of burstiness.
- Rough powers-of-two/ten memory sizes for estimation: {{c1::1 KB}} &asymp; 10^3 bytes, {{c2::1 MB}} &asymp; 10^6 bytes, {{c3::1 GB}} &asymp; 10^9 bytes, {{c4::1 TB}} &asymp; 10^12 bytes.
- Latency numbers worth memorizing: L1 cache reference &asymp; 1 ns, main memory reference &asymp; 100 ns, round trip within the same data center &asymp; 0.5 ms, and a round trip {{c1::across the US/continent}} &asymp; tens of ms (roughly 40-60 ms).

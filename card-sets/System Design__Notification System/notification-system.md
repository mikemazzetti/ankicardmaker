---
deck: "System Design::Notification System"
topic: "Notification System"
tags: [ankicardmaker, sd-notification]
note_type: Mixed (Basic / Basic (and reversed card) / Cloze)
created: 2026-09-10
---

# Notification System — System Design

Source of truth for the `System Design::Notification System` deck (20 notes). Edit here and re-push to update.

## Basic cards

1. **Q:** Why does a notification system typically favor at-least-once delivery over at-most-once, despite the risk of duplicates?
   **A:** Losing a notification, such as a security alert or OTP, is usually worse than a user occasionally receiving a duplicate; at-least-once delivery combined with idempotency-based dedup gives the best of both.

2. **Q:** If a system must fan out a broadcast to 50M users within 10 minutes, what sustained throughput is required?
   **A:** 50M / 600s ≈ 83,000 notifications/sec sustained throughput.

3. **Q:** Why is notification storage for delivery logs usually much larger in volume than the notification content itself?
   **A:** Every send generates a log/status record per user and channel; e.g. one broadcast to 50M users across 2 channels creates 100M log rows, dwarfing the shared notification template's storage size.

4. **Q:** What would a typical internal API call to trigger a notification look like?
   **A:** <pre><code>POST /notifications/send
{ userId, type, channel, templateId, data }
-&gt; returns notificationId, status: queued</code></pre>

5. **Q:** What endpoint would let a client fetch a user's notification preferences?
   **A:** <code>GET /users/{userId}/notification-preferences</code>, returning which channels (push/email/SMS) the user allows for each notification type.

6. **Q:** Why store user notification preferences as a separate table/service rather than embedding them in every notification request?
   **A:** Preferences change independently of individual sends and are read on nearly every notification; a dedicated, cacheable preference store avoids duplicating and re-validating the same data across every request.

7. **Q:** Why does a notification system place a message queue between the API layer and the channel-specific senders rather than sending synchronously?
   **A:** Sending is often slow or rate-limited by third-party providers; queuing decouples request acceptance from delivery, allows retries, and smooths bursty traffic across available worker capacity.

8. **Q:** In a fanout-on-write approach, what happens immediately when a notification is triggered?
   **A:** The system immediately writes or queues a delivery job for every target recipient at trigger time; fast to read/deliver later, but expensive up front for very large recipient lists such as millions of followers.

9. **Q:** What is fanout-on-read, and when is it preferred over fanout-on-write?
   **A:** Recipients are computed or resolved at delivery time rather than precomputed; preferred for extremely large or dynamic audiences, such as a broadcast to all users matching some condition, where precomputing every job upfront would be too costly.

10. **Q:** Why does each channel (push, email, SMS) typically get its own dedicated queue and worker pool rather than sharing one?
   **A:** Each channel has different throughput limits, latency characteristics, and third-party rate limits, such as APNs vs. Twilio; isolating queues prevents a slow or rate-limited channel from backing up delivery for the others.

11. **Q:** What retry strategy is typically used when a third-party gateway temporarily fails to deliver a notification?
   **A:** Exponential backoff with a capped number of retries, after which the notification is marked failed and optionally routed to a dead-letter queue for investigation.

12. **Q:** How is a notification typically deduplicated when at-least-once delivery causes the same message to be processed twice?
   **A:** Each notification is assigned an idempotency key, such as notificationId; the worker checks a dedup store like Redis with a TTL before sending, and skips sending if that key was already processed.

13. **Q:** Why must the dedup check-and-mark operation be atomic in a distributed notification worker pool?
   **A:** Multiple worker instances could pull the same retried job concurrently; without an atomic check-and-set (e.g. Redis SETNX), a race condition could let two workers both pass the dedup check and send duplicate notifications.

14. **Q:** What is the main scaling bottleneck when fanning out a single notification to tens of millions of users at once?
   **A:** Third-party gateway rate limits, such as APNs/FCM throughput caps, and queue/worker throughput; mitigated by batching, rate-limiting outbound calls per provider, and horizontally scaling worker pools.

15. **Q:** What is the tradeoff between fanout-on-write and fanout-on-read for notifications?
   **A:** Fanout-on-write gives fast, precomputed delivery but costs heavy upfront write load for huge audiences; fanout-on-read saves upfront cost but adds latency and complexity at delivery time since recipients must be resolved on demand.

## Cloze cards

- Core functional requirements for a notification system: send notifications via {{c1::multiple channels}} (push, email, SMS), support {{c2::user opt-in/preferences}}, and provide {{c3::delivery tracking}}.
- Key non-functional requirements: {{c1::high throughput}} (bursts of millions of notifications), {{c2::low latency}} for time-sensitive alerts, {{c3::reliability}} (no lost notifications), and {{c4::avoiding duplicate delivery}}.
- A notification record typically stores {{c1::notificationId}}, {{c2::userId}}, {{c3::channel}}, {{c4::status (queued/sent/delivered/failed)}}, and {{c5::timestamp}}.
- Core components of a notification system: {{c1::notification service/API}}, {{c2::message queue}} for buffering, {{c3::per-channel workers}} (push/email/SMS), {{c4::third-party gateways}} (APNs/FCM, SES, Twilio), and {{c5::preference/opt-out store}}.
- A typical multi-channel fanout pipeline: {{c1::trigger event}} -&gt; {{c2::look up user preferences}} -&gt; {{c3::filter enabled channels}} -&gt; {{c4::enqueue one job per channel}} -&gt; {{c5::channel worker delivers via third-party gateway}}.

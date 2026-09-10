---
deck: "System Design::Ticketmaster Booking"
topic: "Ticketmaster Booking"
tags: [ankicardmaker, sd-ticketmaster]
note_type: Mixed (Basic / Basic (and reversed card) / Cloze)
created: 2026-09-10
---

# Ticketmaster Booking — System Design

Source of truth for the `System Design::Ticketmaster Booking` deck (22 notes). Edit here and re-push to update.

## Basic cards

1. **Q:** What are the core functional requirements of a Ticketmaster-like booking system?
   **A:** Browse events/venues, view real-time seat availability, reserve/hold seats temporarily, and complete payment to confirm a booking.

2. **Q:** For a popular on-sale event with 1M users trying to book 50,000 seats in the first minute, what does this imply about system design?
   **A:** A massive, short-lived traffic spike (thundering herd) requiring queuing/rate-limiting in front of the booking service, since only 5% of users can succeed.

3. **Q:** If checkout takes an average of 3 minutes and a venue has 20,000 seats, how many holds could be active concurrently in the worst case?
   **A:** Up to 20,000 concurrent holds — the system must be able to track that many temporary reservations at once.

4. **Q:** What are the key sequential API calls a client makes to book a seat?
   **A:** GET /events/{id}/seats (view availability) → POST /reservations (hold a seat) → POST /payments (pay), after which the hold is converted to a confirmed booking.

5. **Q:** Why does POST /reservations return a reservation_id and expiry time rather than immediately confirming the booking?
   **A:** The seat is only temporarily held pending payment; the client needs the hold's ID and expiry to complete checkout within the time window.

6. **Q:** What states can a seat be in within the booking system's data model?
   **A:** Available, held (reserved), and booked (sold/confirmed).

7. **Q:** What fields does a seat 'hold' record need beyond seat ID and state?
   **A:** The user/session ID holding it, and an expiry timestamp for when the hold auto-releases.

8. **Q:** What race condition must a booking system prevent when two users click the same seat simultaneously?
   **A:** Double-booking — both requests reading 'available' before either write completes, so both proceed to reserve the same seat.

9. **Q:** What database technique lets only one of two simultaneous requests for the same seat succeed, using a conditional update?
   **A:** Optimistic concurrency control — a conditional UPDATE that only affects a row if it's still available; the loser gets zero rows updated and retries or fails.<pre><code>UPDATE seats
SET state = 'held', held_by = ?, expires_at = ?
WHERE seat_id = ? AND state = 'available';</code></pre>

10. **Q:** What's the alternative pessimistic approach to prevent double-booking, and its downside?
   **A:** Acquire a distributed lock (e.g. via Redis SETNX or a DB row lock) on the seat before reserving; simpler to reason about, but creates contention/latency and risks deadlocks or stuck locks if a client crashes mid-hold.

11. **Q:** Why is a distributed lock (e.g. Redis-based) typically given a short TTL when used for seat holds?
   **A:** So that if the holding client crashes or never completes checkout, the lock/hold automatically expires instead of permanently blocking the seat.

12. **Q:** Hold timer (seat reservation) *(reversed — both ways)*
   **A:** A time window (e.g. 5-10 minutes) during which a seat is reserved for one user to complete payment, before it is automatically released back to available.

13. **Q:** What mechanism actually releases an expired hold back to 'available' at scale, without polling every seat?
   **A:** A TTL-based expiry (e.g. Redis key expiration) or a delayed job/message scheduled at hold-creation time that flips the seat state back when it fires.

14. **Q:** Why is eventual consistency generally unacceptable for seat inventory state, unlike many other system-design domains?
   **A:** Selling the same physical seat to two people is a direct, visible business/customer failure, so seat state needs strong (linearizable) consistency, at least within a venue/event.

15. **Q:** How can seat-level locking be scaled without a single giant lock table becoming a bottleneck?
   **A:** Shard the lock/inventory store by event/venue (and possibly by section), so contention is isolated per hot event rather than global.

16. **Q:** Why must payment confirmation, not the initial hold, be the trigger that finalizes a booking?
   **A:** The hold only reserves the seat provisionally; the booking should only become permanent once payment actually succeeds, avoiding charging for seats not actually secured.

17. **Q:** What's the primary bottleneck during a flash on-sale for a single popular event?
   **A:** Extreme write contention on a small set of hot rows (that event's seats/inventory counters), far exceeding the normal per-second traffic the database can handle.

18. **Q:** What's a common mitigation for the thundering-herd problem at ticket on-sale time?
   **A:** A virtual waiting room / queue in front of the booking service that admits users at a controlled rate, smoothing the spike.

19. **Q:** What's the tradeoff of a longer seat-hold timer (e.g. 15 min) vs a shorter one (e.g. 3 min)?
   **A:** Longer holds give users more comfortable checkout time but reduce seat availability/throughput during high demand; shorter holds free seats faster but risk more checkout failures and abandoned carts.

20. **Q:** What's the tradeoff of pessimistic locking vs optimistic concurrency control for seat reservation?
   **A:** Pessimistic locking gives simpler correctness guarantees but can hurt throughput under contention and risks stuck locks; optimistic control scales better under low contention but requires retry logic and can waste work on conflicts.

## Cloze cards

- Key non-functional requirements: {{c1::strong consistency for seat state}} (no double-booking), {{c2::high availability}} during on-sale spikes, and {{c3::low latency}} seat-map reads.
- Core components: a {{c1::seat inventory/availability service}} (source of truth on seat state), a {{c2::reservation/booking service}} (manages holds), a {{c3::payment service}}, and a {{c4::queue/rate-limiter}} in front to throttle traffic during on-sales.

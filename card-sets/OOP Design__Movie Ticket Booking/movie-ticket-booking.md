---
deck: "OOP Design::Movie Ticket Booking"
topic: "Movie Ticket Booking"
tags: [ankicardmaker, ood-movie-booking]
note_type: Mixed (Basic / Basic (and reversed card) / Cloze)
created: 2026-09-10
---

# Movie Ticket Booking — OOP Design

Source of truth for the `OOP Design::Movie Ticket Booking` deck (19 notes). Edit here and re-push to update.

## Basic cards

1. **Q:** In an OOD interview, what are the 3 core functional requirements for a Movie Ticket Booking system?
   **A:** 1) Browse movies/shows by theater, date, and time. 2) Select and reserve specific seats for a show. 3) Complete payment to confirm the booking, with seats correctly released if payment fails or times out.

2. **Q:** Seat (Movie Ticket Booking) *(reversed — both ways)*
   **A:** A bookable unit within a Screen, identified by row/column, with a SeatType (e.g. REGULAR, PREMIUM, RECLINER) and a per-Show SeatStatus (AVAILABLE, LOCKED, BOOKED).

3. **Q:** Why must seat reservation in a movie booking system rely on concurrency control / locking rather than plain read-then-write?
   **A:** Multiple users can try to book the same seat for the same show at nearly the same instant; without locking, two threads could both read 'AVAILABLE', both proceed, and both charge a customer for the same physical seat (double-booking).

4. **Q:** Compare pessimistic vs optimistic locking for reserving a seat, and when you'd prefer each.
   **A:** Pessimistic locking acquires a lock (DB row lock or distributed lock) before letting anyone read/modify the seat, blocking contenders — simpler correctness, more contention overhead; good under high contention. Optimistic locking reads a version number, and the update only commits if the version hasn't changed (compare-and-swap), retrying on conflict — less blocking, better throughput when contention is low.

5. **Q:** Why does a seat lock need an expiry (TTL), e.g. 'held for 10 minutes'?
   **A:** If a user locks a seat and then abandons checkout (closes the tab, connection drops), the seat must not stay locked forever — a TTL automatically releases it back to AVAILABLE so other users can book it.

6. **Q:** In a single-database design, what SQL mechanism implements pessimistic seat locking?
   **A:** <code>SELECT ... FOR UPDATE</code> on the seat row inside a transaction — it blocks other transactions from reading/locking that same row until the current transaction commits or rolls back.

7. **Q:** In a distributed/multi-instance booking service, what tool is commonly used to implement a seat lock across service instances?
   **A:** A distributed lock via Redis (e.g. SET seat:id NX with a TTL, or the Redlock algorithm) — NX ensures only one instance can acquire the lock, and the TTL provides automatic expiry if the holder crashes.

8. **Q:** Edge case: a seat lock expires (TTL hits zero) at the exact moment the user submits payment. What must the booking flow do?
   **A:** Before confirming, re-validate that the lock is still held by this user's session; if it expired, reject the confirmation and prompt the user to reselect seats rather than charging them for a seat that may now belong to someone else.

9. **Q:** Edge case: payment succeeds but the confirm-booking step (marking seats BOOKED) fails or times out. How do you avoid losing money or double-selling the seat?
   **A:** Use a transaction/saga: only mark seats BOOKED after payment confirmation, and if that step fails, retry it idempotently (keyed by payment/booking id) rather than re-charging; if it can't be reconciled automatically, refund and release the seats.

10. **Q:** Why is BookingManager often implemented as a Singleton (or a single coordinating service) in this design?
   **A:** Seat-lock state for a given show must be checked and mutated consistently from one authoritative place; a single coordinating manager (or a shared lock store like Redis) prevents different parts of the app from making conflicting concurrent decisions about the same seat.

11. **Q:** What core fields does a Booking object typically carry?
   **A:** Booking id, user, show reference, list of seat ids, total price, BookingStatus (e.g. PENDING, CONFIRMED, CANCELLED), and a payment reference.

12. **Q:** Why is Factory a reasonable pattern for creating Payment objects (credit card, wallet, UPI) in a booking checkout flow?
   **A:** The checkout code just needs a PaymentMethod that can charge(amount); a PaymentFactory maps a payment-type enum to the right concrete implementation, so adding a new payment method doesn't touch the checkout logic.

13. **Q:** Edge case: how should the system prevent a single user from locking an unreasonable number of seats (e.g. scripted seat-hoarding)?
   **A:** Cap the number of seats a single lock/session can hold per show (e.g. max 10), enforced server-side at the lock-acquisition step, independent of any client-side UI limit.

14. **Q:** Implement seat locking in Java using a per-seat ReentrantLock with tryLock and a timeout.
   **A:** <pre><code>class SeatLockManager {
    private final Map&lt;String, ReentrantLock&gt; locks = new ConcurrentHashMap&lt;&gt;();

    boolean lockSeat(String seatId, long timeoutMs) throws InterruptedException {
        ReentrantLock lock = locks.computeIfAbsent(
            seatId, id -&gt; new ReentrantLock()
        );
        return lock.tryLock(timeoutMs, TimeUnit.MILLISECONDS);
    }

    void unlockSeat(String seatId) {
        ReentrantLock lock = locks.get(seatId);
        if (lock != null &amp;&amp; lock.isHeldByCurrentThread()) {
            lock.unlock();
        }
    }
}</code></pre>

15. **Q:** Implement a Redis-based distributed seat lock in Python using SET NX with a TTL.
   **A:** <pre><code>import redis
import uuid

r = redis.Redis()

def try_lock_seat(seat_id, ttl_seconds=600):
    token = str(uuid.uuid4())
    acquired = r.set(
        f"seat_lock:{seat_id}", token,
        nx=True, ex=ttl_seconds
    )
    return token if acquired else None

def release_seat(seat_id, token):
    # only release if we still own the lock
    if r.get(f"seat_lock:{seat_id}") == token.encode():
        r.delete(f"seat_lock:{seat_id}")</code></pre>

16. **Q:** Implement a Java confirmBooking() method that atomically checks the seat lock is still valid before marking seats BOOKED.
   **A:** <pre><code>public Booking confirmBooking(String userId, List&lt;String&gt; seatIds, Payment payment) {
    for (String seatId : seatIds) {
        if (!seatLockManager.isLockedBy(seatId, userId)) {
            throw new SeatLockExpiredException(seatId);
        }
    }
    PaymentResult result = payment.charge();
    if (!result.isSuccess()) {
        throw new PaymentFailedException(result.getReason());
    }
    for (String seatId : seatIds) {
        seatRepository.markBooked(seatId);
        seatLockManager.unlockSeat(seatId);
    }
    return bookingRepository.save(new Booking(userId, seatIds, result));
}</code></pre>

17. **Q:** Implement a Python background job that scans for and releases expired seat locks (for a design not using a TTL-native store).
   **A:** <pre><code>def release_expired_locks(lock_store, now):
    expired = [
        seat_id for seat_id, lock in lock_store.items()
        if lock.expires_at &lt;= now
    ]
    for seat_id in expired:
        del lock_store[seat_id]
        seat_repository.mark_available(seat_id)
    return expired</code></pre>

## Cloze cards

- A {{c1::Show}} represents one scheduled screening: it links a {{c2::Movie}} to a {{c3::Screen}} at a specific start time, and owns the seat-availability state for that screening.
- SeatStatus for a given show typically has three states: {{c1::AVAILABLE}}, {{c2::LOCKED}} (temporarily held during checkout), and {{c3::BOOKED}} (payment confirmed).

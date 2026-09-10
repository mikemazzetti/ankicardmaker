---
deck: "OOP Design::Ride-Sharing (Uber)"
topic: "Ride-Sharing (Uber)"
tags: [ankicardmaker, ood-ride-sharing]
note_type: Mixed (Basic / Basic (and reversed card) / Cloze)
created: 2026-09-10
---

# Ride-Sharing (Uber) — OOP Design

Source of truth for the `OOP Design::Ride-Sharing (Uber)` deck (20 notes). Edit here and re-push to update.

## Basic cards

1. **Q:** What core use cases should an OOD interview design for a ride-sharing system like Uber cover?
   **A:** A Rider requests a trip, the system matches a nearby Driver, tracks the trip lifecycle in real time, computes the fare (with surge pricing), and processes payment at completion.

2. **Q:** What is the responsibility of the Trip (Ride) class?
   **A:** Aggregates one ride's lifecycle: the Rider, matched Driver, pickup/dropoff Locations, status, route, and final fare — it's the central record tying everything else together.

3. **Q:** How do Rider and Driver relate to a common base class in the design?
   **A:** Both typically extend a shared User/Account class (name, contact, rating, payment method), with Driver adding a Vehicle and availability status, and Rider adding saved payment info.

4. **Q:** What relationship exists between Trip and Location in the class model?
   **A:** Composition/association: a Trip references two Locations (pickup and dropoff) as value objects (latitude/longitude), and a Driver's Vehicle also has a live current Location updated during the trip.

5. **Q:** Which design pattern fits selecting how to match riders to drivers, and why?
   **A:** Strategy: encapsulate matching logic (nearest-driver, least-idle-time, highest-rated) in interchangeable MatchingStrategy implementations so the algorithm can be swapped without changing the Trip request flow.

6. **Q:** Which design pattern fits computing fare with surge pricing that varies by demand/time/zone, and why?
   **A:** Strategy: a PricingStrategy interface lets you plug in SurgePricing, FlatRatePricing, etc., all exposing a fare-calculation method, so Trip doesn't hardcode pricing rules.

7. **Q:** Which design pattern fits pushing a Driver's live location updates to a Rider's app during an ongoing trip, and why?
   **A:** Observer: the Driver (or a LocationTracker) is the subject; the Rider's Trip view subscribes as an observer and gets notified on each location update, rather than the Rider polling continuously.

8. **Q:** What does <code>requestRide(rider, pickup, dropoff)</code> need to do?
   **A:** Create a Trip in REQUESTED status, invoke the MatchingStrategy to find candidate Drivers within radius, and notify the closest available Driver to accept/reject.

9. **Q:** What should <code>matchDriver(trip)</code> return if no drivers are available nearby?
   **A:** It should return a no-match result (not throw silently); the system should widen the search radius or queue the request and notify the Rider of the wait, rather than leaving the Trip stuck in REQUESTED.

10. **Q:** What must <code>calculateFare(trip)</code> account for beyond base distance/time?
   **A:** The current surge multiplier for the pickup zone/time, any tolls or wait-time charges, and the Rider's applicable promotions/discounts.

11. **Q:** Edge case: two ride requests both try to match the same nearby Driver at nearly the same instant. How should the design prevent double-booking?
   **A:** The Driver's availability flag must be updated atomically as part of the match/accept operation (e.g., compare-and-swap or a DB transaction), so only the first accepted request locks the Driver; the second falls through to re-match.

12. **Q:** Edge case: a Driver accepts a Trip, then cancels before pickup. What should happen?
   **A:** Revert Trip to REQUESTED, release the Driver back to available, re-invoke the MatchingStrategy to find a new Driver, and log the cancellation against the Driver's reliability metric.

13. **Q:** Edge case: a Rider cancels after a Driver has already started heading to pickup. What should the fare logic do?
   **A:** Charge a cancellation fee based on elapsed time/distance the Driver traveled, distinct from the normal trip fare, since the Driver incurred cost with no completed ride.

14. **Q:** Edge case: GPS/location updates arrive out of order or are momentarily lost mid-trip. What should the design do?
   **A:** Timestamp each location update and only apply it if newer than the Trip's last recorded location, so stale/out-of-order packets don't corrupt the displayed route; treat prolonged loss as a tracking-degraded state, not a trip failure.

15. **Q:** Surge pricing *(reversed — both ways)*
   **A:** A multiplier applied to the base fare during high-demand/low-driver-supply periods in a given zone, computed by the PricingStrategy and shown to the Rider before they confirm the request.

16. **Q:** Implement the Strategy pattern in Java for driver matching, with a nearest-driver implementation.
   **A:** <pre><code>public interface MatchingStrategy {
    Optional&lt;Driver&gt; match(Location pickup, List&lt;Driver&gt; available);
}

public class NearestDriverStrategy implements MatchingStrategy {
    public Optional&lt;Driver&gt; match(Location pickup, List&lt;Driver&gt; available) {
        return available.stream()
            .min(Comparator.comparingDouble(
                d -&gt; d.getCurrentLocation().distanceTo(pickup)));
    }
}
</code></pre>

17. **Q:** Implement the Observer pattern in Python so a Rider's app is notified whenever a Driver's location updates.
   **A:** <pre><code>class LocationObserver:
    def on_location_update(self, driver, location):
        raise NotImplementedError

class RiderAppView(LocationObserver):
    def on_location_update(self, driver, location):
        print(f"Driver {driver.name} is now at {location}")

class Driver:
    def __init__(self, name):
        self.name = name
        self._observers = []

    def subscribe(self, observer):
        self._observers.append(observer)

    def update_location(self, location):
        self.current_location = location
        for obs in self._observers:
            obs.on_location_update(self, location)
</code></pre>

18. **Q:** Implement a Java Strategy-pattern fare calculator with a surge-pricing implementation.
   **A:** <pre><code>public interface PricingStrategy {
    double calculateFare(double distanceKm, double durationMin);
}

public class SurgePricing implements PricingStrategy {
    private final double surgeMultiplier;

    public SurgePricing(double surgeMultiplier) {
        this.surgeMultiplier = surgeMultiplier;
    }

    public double calculateFare(double distanceKm, double durationMin) {
        double base = 2.50 + 1.20 * distanceKm + 0.25 * durationMin;
        return base * surgeMultiplier;
    }
}
</code></pre>

19. **Q:** Implement a Python driver-matching helper that atomically claims a Driver to prevent two Trips matching the same Driver.
   **A:** <pre><code>import threading

class DriverPool:
    def __init__(self):
        self._lock = threading.Lock()
        self._available = set()

    def try_claim(self, driver_id):
        with self._lock:
            if driver_id in self._available:
                self._available.remove(driver_id)
                return True
            return False

    def release(self, driver_id):
        with self._lock:
            self._available.add(driver_id)
</code></pre>

## Cloze cards

- A Trip's status typically moves through {{c1::REQUESTED}}, {{c2::ACCEPTED}}, {{c3::ONGOING}}, and finally {{c4::COMPLETED}} (or {{c5::CANCELLED}}).

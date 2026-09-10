---
deck: "OOP Design::Airline Reservation"
topic: "Airline Reservation"
tags: [ankicardmaker, ood-airline]
note_type: Mixed (Basic / Basic (and reversed card) / Cloze)
created: 2026-09-10
---

# Airline Reservation — OOP Design

Source of truth for the `OOP Design::Airline Reservation` deck (20 notes). Edit here and re-push to update.

## Basic cards

1. **Q:** In an airline reservation system, what three entities does a Booking (reservation) typically link together?
   **A:** A Passenger, a Flight, and a Seat (plus payment/fare info).

2. **Q:** Why does an airline reservation system model Flight and Aircraft as separate classes?
   **A:** Flight defines the route/schedule (origin, destination, flight number, departure/arrival time); Aircraft is the physical plane assigned to that scheduled flight, so seat maps and capacity can vary per assignment (e.g. a substitute plane).

3. **Q:** What core class represents the physical layout of seats on a specific aircraft, including class zones (Economy/Business/First)?
   **A:** SeatMap (owned by Aircraft or Flight), composed of individual Seat objects.

4. **Q:** What is the responsibility of the Itinerary class?
   **A:** Aggregates one or more Flight legs (for connecting/multi-city trips) into a single trip a Passenger books together.

5. **Q:** Passenger *(reversed — both ways)*
   **A:** Class holding traveler identity/contact info, frequent-flyer number, and their list of Bookings.

6. **Q:** Booking (Reservation) *(reversed — both ways)*
   **A:** Class linking a Passenger to a Flight and Seat, holding fare, status, and payment reference.

7. **Q:** What enum would you use to model cabin/fare classes on a flight, and name its typical values?
   **A:** SeatClass (or CabinClass): ECONOMY, PREMIUM_ECONOMY, BUSINESS, FIRST.

8. **Q:** Which design pattern fits modeling a Booking's lifecycle (Pending -&gt; Confirmed -&gt; CheckedIn -&gt; Cancelled) and why?
   **A:** The State pattern: each status becomes a state object encapsulating which transitions are legal, avoiding scattered if/else on a status enum and preventing illegal transitions like CheckedIn -&gt; Pending.

9. **Q:** Which design pattern fits notifying passengers about flight delays, gate changes, or cancellations, and why?
   **A:** The Observer pattern: Flight is the subject; Passenger/Booking objects (or a NotificationService) subscribe as observers and get pushed updates when flight status changes, decoupling the flight from notification channels (email/SMS/push).

10. **Q:** Which design pattern fits supporting multiple fare-pricing strategies (early-bird, last-minute, dynamic demand pricing)?
   **A:** The Strategy pattern: encapsulate each pricing algorithm behind a common PricingStrategy interface so Flight/Booking can swap pricing logic without changing calling code.

11. **Q:** In the airline domain, what is the classic 'double booking' edge case and how is it usually prevented?
   **A:** Two concurrent requests both read the same seat as available and both try to book it. Prevented with a lock (e.g. synchronized method, database row lock, or optimistic locking with a version/CAS check) around the read-check-reserve sequence.

12. **Q:** Why is validating layover time an important edge case when building an Itinerary from separate Flight legs?
   **A:** If the gap between the arrival of one leg and the departure of the next is too short (below a minimum connection time), or the arrival airport differs from the next departure airport, the itinerary is invalid and should be rejected or flagged.

13. **Q:** What API method signature would you expose to find available flights, and what should it return?
   **A:** <code>List&lt;Flight&gt; searchFlights(String origin, String destination, LocalDate date)</code> &mdash; returns matching scheduled flights with seat availability, not raw Aircraft objects.

14. **Q:** Why should <code>cancelBooking(bookingId)</code> release the seat back to inventory rather than just marking the Booking cancelled?
   **A:** If the Seat's availability isn't updated, the seat stays falsely 'held', causing lost revenue (or, if availability is derived only from Bookings, requires an expensive scan of all bookings to compute availability).

15. **Q:** Java: implement a thread-safe <code>bookSeat</code> method on a <code>Flight</code> that prevents two threads from double-booking the same seat, using a lock around the check-and-reserve sequence.
   **A:** <pre><code>import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.locks.ReentrantLock;

public class Flight {
    private final ConcurrentHashMap&lt;String, Seat&gt; seats = new ConcurrentHashMap&lt;&gt;();
    private final ReentrantLock bookingLock = new ReentrantLock();

    public boolean bookSeat(String seatNumber, Passenger passenger) {
        bookingLock.lock();
        try {
            Seat seat = seats.get(seatNumber);
            if (seat == null || !seat.isAvailable()) {
                return false;
            }
            seat.setAvailable(false);
            seat.setPassenger(passenger);
            return true;
        } finally {
            bookingLock.unlock();
        }
    }
}</code></pre>

16. **Q:** Python: implement a <code>Booking</code> class with a <code>BookingStatus</code> enum and a <code>cancel()</code> method that raises if the booking is already <code>CHECKED_IN</code>.
   **A:** <pre><code>from enum import Enum, auto

class BookingStatus(Enum):
    PENDING = auto()
    CONFIRMED = auto()
    CHECKED_IN = auto()
    CANCELLED = auto()

class Booking:
    def __init__(self, passenger, flight, seat):
        self.passenger = passenger
        self.flight = flight
        self.seat = seat
        self.status = BookingStatus.PENDING

    def cancel(self):
        if self.status == BookingStatus.CHECKED_IN:
            raise ValueError("Cannot cancel a checked-in booking")
        self.status = BookingStatus.CANCELLED
        self.seat.release()</code></pre>

17. **Q:** Java: implement the Observer pattern so a <code>Flight</code> notifies registered observers when its status changes (e.g. DELAYED).
   **A:** <pre><code>import java.util.ArrayList;
import java.util.List;

interface FlightStatusObserver {
    void onStatusChanged(Flight flight, FlightStatus newStatus);
}

public class Flight {
    private FlightStatus status = FlightStatus.SCHEDULED;
    private final List&lt;FlightStatusObserver&gt; observers = new ArrayList&lt;&gt;();

    public void addObserver(FlightStatusObserver observer) {
        observers.add(observer);
    }

    public void setStatus(FlightStatus newStatus) {
        this.status = newStatus;
        for (FlightStatusObserver observer : observers) {
            observer.onStatusChanged(this, newStatus);
        }
    }
}</code></pre>

18. **Q:** Python: write a function <code>is_valid_connection(arrival, departure, min_minutes=45)</code> that checks a connecting flight's layover meets a minimum connection time.
   **A:** <pre><code>from datetime import datetime, timedelta

def is_valid_connection(arrival: datetime, departure: datetime, min_minutes: int = 45) -&gt; bool:
    layover = departure - arrival
    return layover &gt;= timedelta(minutes=min_minutes)</code></pre>

## Cloze cards

- A minimal airline reservation system must support {{c1::searching flights}} by origin/destination/date, {{c2::booking a seat}} on a flight, {{c3::cancelling}} a booking, and {{c4::checking in}} a passenger.
- The {{c1::BookingStatus}} enum typically includes values like {{c2::PENDING}}, {{c3::CONFIRMED}}, {{c4::CANCELLED}}, and {{c5::CHECKED_IN}}. <!-- Extra: Modeling status as an enum plus explicit transition rules avoids invalid state jumps (e.g. CANCELLED -&gt; CHECKED_IN). -->

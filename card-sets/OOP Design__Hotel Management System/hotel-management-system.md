---
deck: "OOP Design::Hotel Management System"
topic: "Hotel Management System"
tags: [ankicardmaker, ood-hotel]
note_type: Mixed (Basic / Basic (and reversed card) / Cloze)
created: 2026-09-10
---

# Hotel Management System — OOP Design

Source of truth for the `OOP Design::Hotel Management System` deck (20 notes). Edit here and re-push to update.

## Basic cards

1. **Q:** What core use cases should an OOD interview design for a Hotel Management System cover?
   **A:** Searching room availability by date range/type, booking/reservation, check-in and check-out, billing/invoicing, and housekeeping status tracking.

2. **Q:** What is the responsibility of the Hotel class vs. a HotelBranch class in a multi-location design?
   **A:** Hotel is the top-level entity (brand) that owns multiple HotelBranch objects; each HotelBranch owns its own Rooms, staff, and local bookings.

3. **Q:** Why model Room and RoomType as separate concepts?
   **A:** Room is a specific physical room (number, floor, branch); RoomType captures shared attributes like price, capacity, and amenities so many Rooms can reference one RoomType without duplicating data.

4. **Q:** What relationship exists between Booking and Room in the class model?
   **A:** A Booking references one (or more) Rooms for a specific date range; it's an association, not composition — the Room continues to exist independently of any particular Booking.

5. **Q:** How does an Invoice relate to a Booking?
   **A:** One Invoice is generated per completed Booking (or per stay), aggregating room charges, service charges, and taxes; composition — the Invoice's line items belong to that Booking.

6. **Q:** Which design pattern fits creating different Room subtypes (Suite, Deluxe, Standard) with type-specific setup, and why?
   **A:** Factory Method: a RoomFactory centralizes construction logic so client code calls <code>createRoom(RoomType)</code> instead of branching on type everywhere a Room is instantiated.

7. **Q:** Which design pattern fits managing a Room's status transitions (AVAILABLE → RESERVED → OCCUPIED → CLEANING), and why?
   **A:** State: each status becomes a State object with allowed-transition logic, so invalid transitions (e.g., checking in an already-OCCUPIED room) are rejected by the state itself rather than scattered if-checks.

8. **Q:** Which design pattern fits varying room pricing by season/demand, and why?
   **A:** Strategy: encapsulate pricing rules in interchangeable PricingStrategy implementations (e.g., PeakSeasonPricing, WeekdayPricing) selected at booking time.

9. **Q:** What must <code>searchRooms(startDate, endDate, roomType)</code> check to return correct availability?
   **A:** It must exclude any Room of that type with an overlapping existing Booking in the given date range, not just Rooms currently marked OCCUPIED today.

10. **Q:** What should <code>checkIn(booking)</code> validate before allowing check-in?
   **A:** That today's date falls within the booking's date range, the Room's status is RESERVED (not still OCCUPIED by a prior guest), and identity/payment hold is confirmed.

11. **Q:** What should <code>checkOut(booking)</code> trigger?
   **A:** Finalize the Invoice (add incidental charges), set Room status to UNDER_MAINTENANCE or CLEANING (not directly AVAILABLE), and close the Booking.

12. **Q:** Edge case: a guest wants to extend their stay by one night at checkout time. How should the design handle it?
   **A:** Check the Room's availability for the extra night before approving; if another Booking already reserves it, offer a room change instead of overbooking.

13. **Q:** Edge case: overbooking — two Bookings end up referencing the same Room for overlapping dates. What prevents this?
   **A:** The booking-creation path must atomically check availability and reserve the Room (e.g., a DB-level unique constraint or lock on Room+date range) so the overlap check and the reservation happen as one operation.

14. **Q:** Edge case: a Room needs emergency maintenance while it has a future Booking against it. What should the system do?
   **A:** Flag the Room UNDER_MAINTENANCE, and trigger a reassignment workflow that finds an equivalent RoomType for the affected Booking or notifies staff to contact the guest.

15. **Q:** Edge case: a guest cancels within a non-refundable window. What must Booking/Invoice logic enforce?
   **A:** The cancellation policy (a date-based rule tied to the Booking) must be checked before refunding; late cancellations should still generate a partial or full charge on the Invoice.

16. **Q:** Housekeeping status *(reversed — both ways)*
   **A:** A Room attribute (distinct from booking status) tracking whether the room is CLEAN, DIRTY, or INSPECTED — checked before a Room can move from UNDER_MAINTENANCE/CLEANING back to AVAILABLE.

17. **Q:** Implement a Java Factory Method that creates Room objects for different RoomTypes.
   **A:** <pre><code>public class RoomFactory {
    public static Room createRoom(String roomNumber, RoomType type) {
        switch (type) {
            case SUITE:
                return new Room(roomNumber, type, 2, 350.00);
            case DELUXE:
                return new Room(roomNumber, type, 2, 200.00);
            case STANDARD:
                return new Room(roomNumber, type, 1, 120.00);
            default:
                throw new IllegalArgumentException("Unknown RoomType: " + type);
        }
    }
}
</code></pre>

18. **Q:** Implement the State pattern in Python for a Room's status transitions, rejecting invalid check-ins.
   **A:** <pre><code>class RoomState:
    def check_in(self, room):
        raise Exception("Cannot check in from this state")

class Available(RoomState):
    def check_in(self, room):
        room.state = Occupied()

class Reserved(RoomState):
    def check_in(self, room):
        room.state = Occupied()

class Occupied(RoomState):
    def check_in(self, room):
        raise Exception("Room already occupied")

class Room:
    def __init__(self):
        self.state = Available()

    def check_in(self):
        self.state.check_in(self)
</code></pre>

19. **Q:** Implement a Java method that checks whether a Room is free for a requested date range against its existing Bookings.
   **A:** <pre><code>public boolean isAvailable(Room room, LocalDate start, LocalDate end) {
    for (Booking b : room.getBookings()) {
        boolean overlaps = start.isBefore(b.getEndDate())
                && end.isAfter(b.getStartDate());
        if (overlaps) {
            return false;
        }
    }
    return true;
}
</code></pre>

## Cloze cards

- A Room's status typically cycles through {{c1::AVAILABLE}}, {{c2::RESERVED}}, {{c3::OCCUPIED}}, and {{c4::UNDER_MAINTENANCE}}.

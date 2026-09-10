---
deck: "OOP Design::Parking Lot"
topic: "Parking Lot"
tags: [ankicardmaker, ood-parking-lot]
note_type: Mixed (Basic / Basic (and reversed card) / Cloze)
created: 2026-09-10
---

# Parking Lot — OOP Design

Source of truth for the `OOP Design::Parking Lot` deck (20 notes). Edit here and re-push to update.

## Basic cards

1. **Q:** When clarifying requirements for a Parking Lot System design, what key scope questions should you ask?
   **A:** How many levels/floors? What vehicle types (motorcycle, car, bus)? How is pricing calculated? Is entry/exit ticket-based or automated (e.g. license plate)? Multiple entrances/exits?

2. **Q:** What is the primary functional requirement of a Parking Lot System?
   **A:** Assign and free parking spots to vehicles, track availability per level/spot type, and calculate/collect a fee on exit.

3. **Q:** What is the responsibility of the <code>ParkingLot</code> class?
   **A:** Top-level coordinator managing all floors, entry/exit points, and overall capacity; delegates spot assignment and issues tickets.

4. **Q:** What is the responsibility of the <code>ParkingFloor</code> class?
   **A:** Manages the spots on one level of the lot; tracks which spots on that floor are free or occupied.

5. **Q:** What is the responsibility of the <code>ParkingSpot</code> class?
   **A:** Represents a single spot; knows its <code>SpotType</code> and occupied status, and holds a reference to the parked vehicle (if any).

6. **Q:** What is the responsibility of the <code>Ticket</code> class?
   **A:** Created when a vehicle enters; records the vehicle, assigned spot, and entry timestamp — used to compute the fee and free the spot on exit.

7. **Q:** What enum typically represents parking spot types in a Parking Lot design?
   **A:** <code>SpotType { MOTORCYCLE, COMPACT, LARGE, HANDICAPPED }</code>

8. **Q:** What enum typically represents vehicle types in a Parking Lot design?
   **A:** <code>VehicleType { MOTORCYCLE, CAR, BUS }</code>

9. **Q:** Is the relationship between <code>ParkingLot</code> and <code>ParkingFloor</code> composition or aggregation, and why?
   **A:** Composition — floors have no independent existence outside their lot; the lot owns their lifecycle.

10. **Q:** How should <code>Car</code>, <code>Motorcycle</code>, and <code>Bus</code> relate to a base <code>Vehicle</code> class?
   **A:** Inheritance — each subtype extends <code>Vehicle</code> and carries its own <code>VehicleType</code>, which determines which <code>SpotType</code>s it can fit.

11. **Q:** Which design pattern fits computing a parking fee that varies by vehicle type, duration, or membership tier, and why?
   **A:** Strategy — encapsulate each pricing algorithm behind a common <code>PricingStrategy</code> interface so it can be swapped without changing <code>ParkingLot</code> code.

12. **Q:** Which design pattern fits centralizing creation of the correct <code>Vehicle</code> subtype without the caller knowing the concrete class, and why?
   **A:** Factory — a <code>VehicleFactory</code> centralizes creation logic based on input (e.g. a type code), decoupling object creation from the client code.

13. **Q:** What should <code>ParkingLot.parkVehicle(vehicle)</code> return, and why?
   **A:** A <code>Ticket</code> (or null/exception if the lot is full) — it's the receipt later needed to compute the fee and free the spot on exit.

14. **Q:** What are the two main public methods on the <code>ParkingLot</code> API?
   **A:** <code>parkVehicle(vehicle)</code> — assigns a spot and issues a ticket — and <code>unparkVehicle(ticket)</code> — frees the spot and charges the fee.

15. **Q:** Tricky edge case: a motorcycle takes a large/car spot because no motorcycle spots remain — how should spot assignment handle this?
   **A:** Prefer the smallest compatible spot for the vehicle's type, but allow fallback to a larger spot when the ideal size is full — trading space efficiency for never turning a vehicle away unnecessarily.

16. **Q:** Tricky edge case: a driver loses their ticket at exit — how should the system handle it?
   **A:** Charge a fixed maximum/flat fee (or require attendant override) rather than blocking the exit indefinitely.

17. **Q:** Code the <code>ParkingSpot</code> class in Java with fields for spot type and occupied state, and methods to park and remove a vehicle.
   **A:** <pre><code>public class ParkingSpot {
    private final SpotType type;
    private boolean occupied;
    private Vehicle vehicle;

    public ParkingSpot(SpotType type) {
        this.type = type;
        this.occupied = false;
    }

    public boolean isAvailable() {
        return !occupied;
    }

    public boolean canFitVehicle(Vehicle vehicle) {
        return !occupied &amp;&amp; type.canFit(vehicle.getType());
    }

    public void parkVehicle(Vehicle vehicle) {
        if (occupied) {
            throw new IllegalStateException("Spot already occupied");
        }
        this.vehicle = vehicle;
        this.occupied = true;
    }

    public void removeVehicle() {
        this.vehicle = null;
        this.occupied = false;
    }
}</code></pre>

18. **Q:** Code a <code>park_vehicle</code> method in Python on <code>ParkingLot</code> that finds the first free compatible spot across all floors and assigns it.
   **A:** <pre><code>class ParkingLot:
    def __init__(self, floors):
        self.floors = floors  # list[ParkingFloor]

    def park_vehicle(self, vehicle):
        for floor in self.floors:
            for spot in floor.spots:
                if spot.can_fit_vehicle(vehicle):
                    spot.park_vehicle(vehicle)
                    return Ticket(vehicle, spot)
        return None  # lot is full</code></pre>

19. **Q:** Code a <code>PricingStrategy</code> interface and an <code>HourlyPricingStrategy</code> implementation in Java.
   **A:** <pre><code>public interface PricingStrategy {
    double calculateFee(VehicleType type, long durationMinutes);
}

public class HourlyPricingStrategy implements PricingStrategy {
    private static final double RATE_PER_HOUR = 2.50;

    @Override
    public double calculateFee(VehicleType type, long durationMinutes) {
        long hours = (long) Math.ceil(durationMinutes / 60.0);
        return hours * RATE_PER_HOUR;
    }
}</code></pre>

20. **Q:** Code a <code>find_nearest_available_spot</code> helper in Python that, given a floor's list of spots and a vehicle, returns the first fitting spot or <code>None</code>.
   **A:** <pre><code>def find_nearest_available_spot(spots, vehicle):
    for spot in spots:
        if spot.can_fit_vehicle(vehicle):
            return spot
    return None</code></pre>

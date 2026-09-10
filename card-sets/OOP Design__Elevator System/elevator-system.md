---
deck: "OOP Design::Elevator System"
topic: "Elevator System"
tags: [ankicardmaker, ood-elevator]
note_type: Mixed (Basic / Basic (and reversed card) / Cloze)
created: 2026-09-10
---

# Elevator System — OOP Design

Source of truth for the `OOP Design::Elevator System` deck (18 notes). Edit here and re-push to update.

## Basic cards

1. **Q:** What scope questions should you clarify before designing an Elevator System?
   **A:** How many elevators and floors? A single bank or multiple? What dispatch/scheduling behavior is expected (nearest car, SCAN)? Capacity limits per car? Are requests external (hall calls) and/or internal (floor selection)?

2. **Q:** What is the primary functional requirement of an Elevator System design?
   **A:** Accept up/down pickup requests from floors and destination requests from inside a car, then dispatch/move the optimal elevator to serve each request efficiently.

3. **Q:** What is the responsibility of the <code>ElevatorController</code> class?
   **A:** Manages all elevator cars in the system, receives external and internal requests, and dispatches the best car to serve each request.

4. **Q:** What is the responsibility of the <code>Elevator</code> (car) class?
   **A:** Tracks its own current floor, direction, and state (idle/moving); maintains its internal destination queue and moves toward requested floors.

5. **Q:** What is the responsibility of a <code>Request</code> (hall call) class?
   **A:** Represents a single pickup request — a floor plus a desired direction — waiting to be served by an assigned elevator.

6. **Q:** What enum represents an elevator's direction of travel in this design?
   **A:** <code>Direction { UP, DOWN, IDLE }</code>

7. **Q:** What enum represents an elevator car's operational status?
   **A:** <code>ElevatorStatus { IDLE, MOVING, DOORS_OPEN, MAINTENANCE }</code>

8. **Q:** Is the relationship between <code>ElevatorController</code> and <code>Elevator</code> composition or aggregation, and why?
   **A:** Composition — the controller owns and manages the full lifecycle of its elevator cars; they don't exist independently of the system.

9. **Q:** How should different dispatch algorithms (nearest-car, SCAN/look) be represented in the class design?
   **A:** As interchangeable implementations of a common <code>SchedulingStrategy</code> interface, injected into <code>ElevatorController</code> rather than hardcoded.

10. **Q:** Which design pattern fits swapping the elevator dispatch/scheduling algorithm, and why?
   **A:** Strategy — each algorithm (nearest-car, SCAN) implements a common interface, so the controller can select or switch policy without changing its own code.

11. **Q:** Which design pattern fits an elevator car behaving differently depending on whether it's Idle, Moving, or in Maintenance, and why?
   **A:** State — encapsulate each mode's behavior in its own class, avoiding large conditionals scattered across <code>Elevator</code>'s methods.

12. **Q:** What are the two main entry-point APIs on <code>ElevatorController</code>?
   **A:** <code>requestElevator(floor, direction)</code> for an external hall call, and <code>selectFloor(elevatorId, floor)</code> for an internal destination request.

13. **Q:** What should <code>Elevator.step()</code> do on each tick of the simulation?
   **A:** Move one floor toward its next destination, update its current floor and direction, and open its doors if it has arrived at a requested stop.

14. **Q:** Tricky edge case: two hall calls request opposite directions from the same floor at the same time — how should this be handled?
   **A:** Treat them as two independent hall calls; the dispatcher assigns cars based on each car's current direction and position — an up-call should not be served by a car already moving down past that floor.

15. **Q:** Tricky edge case: the nearest elevator to a hall call is already at full capacity — what should the dispatcher do?
   **A:** Exclude full cars from dispatch consideration (or have the car skip the stop) and assign/queue the request to the next available car instead.

16. **Q:** Code an <code>Elevator</code> class in Python with <code>current_floor</code>, <code>direction</code>, and a method to add a destination and move one step.
   **A:** <pre><code>class Elevator:
    def __init__(self, id, current_floor=1):
        self.id = id
        self.current_floor = current_floor
        self.direction = "IDLE"
        self.destinations = set()

    def add_destination(self, floor):
        self.destinations.add(floor)
        if floor &gt; self.current_floor:
            self.direction = "UP"
        elif floor &lt; self.current_floor:
            self.direction = "DOWN"

    def step(self):
        if not self.destinations:
            self.direction = "IDLE"
            return
        if self.direction == "UP":
            self.current_floor += 1
        elif self.direction == "DOWN":
            self.current_floor -= 1
        if self.current_floor in self.destinations:
            self.destinations.remove(self.current_floor)</code></pre>

17. **Q:** Code a nearest-idle-car dispatch method in Java: given a list of elevators and a requested floor, return the closest idle elevator.
   **A:** <pre><code>public Elevator findNearestIdleElevator(List&lt;Elevator&gt; elevators, int requestedFloor) {
    Elevator best = null;
    int bestDistance = Integer.MAX_VALUE;

    for (Elevator elevator : elevators) {
        if (elevator.getStatus() != ElevatorStatus.IDLE) {
            continue;
        }
        int distance = Math.abs(elevator.getCurrentFloor() - requestedFloor);
        if (distance &lt; bestDistance) {
            bestDistance = distance;
            best = elevator;
        }
    }
    return best;
}</code></pre>

18. **Q:** Code a simple State pattern in Python for an elevator's Idle/Moving states, each with a <code>handle_request</code> method.
   **A:** <pre><code>from abc import ABC, abstractmethod

class ElevatorState(ABC):
    @abstractmethod
    def handle_request(self, elevator, floor):
        ...

class IdleState(ElevatorState):
    def handle_request(self, elevator, floor):
        elevator.add_destination(floor)
        elevator.state = MovingState()

class MovingState(ElevatorState):
    def handle_request(self, elevator, floor):
        elevator.add_destination(floor)</code></pre>

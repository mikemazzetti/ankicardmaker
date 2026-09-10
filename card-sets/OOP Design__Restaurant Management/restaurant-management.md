---
deck: "OOP Design::Restaurant Management"
topic: "Restaurant Management"
tags: [ankicardmaker, ood-restaurant]
note_type: Mixed (Basic / Basic (and reversed card) / Cloze)
created: 2026-09-10
---

# Restaurant Management — OOP Design

Source of truth for the `OOP Design::Restaurant Management` deck (17 notes). Edit here and re-push to update.

## Basic cards

1. **Q:** In an OOD interview, what are the 3 core functional requirements for a Restaurant Management system?
   **A:** 1) Reserve/seat tables and track their status. 2) Take orders, route them to the kitchen, and track preparation status. 3) Generate and settle a bill for a table, supporting splits.

2. **Q:** MenuItem (Restaurant Management) *(reversed — both ways)*
   **A:** A single orderable dish or drink with a name, description, price, category, and availability flag; Menu is a collection of MenuItems, often grouped by category.

3. **Q:** Why is Observer a good fit for notifying the kitchen display when a new order is placed?
   **A:** The Order/Waiter code that places an order shouldn't need to know about every kitchen display or printer subscribed to it; the Kitchen registers as an observer on the OrderService and is automatically notified when a new OrderItem arrives, decoupling order-taking from kitchen display logic.

4. **Q:** Why is State a good fit for both Table status and Order/OrderItem status in this design?
   **A:** Both have a small set of statuses with rules about which transitions are legal (e.g. you can't seat a RESERVED table as OCCUPIED without check-in; you can't mark an item SERVED before it's READY) — State encapsulates each status's allowed transitions instead of scattering conditionals.

5. **Q:** Why might Factory be used to construct MenuItem/Order objects in a restaurant system with multiple item categories (food, drink, combo)?
   **A:** A combo item might need to bundle/validate sub-items differently than a plain food item; a MenuItemFactory centralizes category-specific construction logic so the ordering flow just asks for 'an item of this type' without knowing the construction details.

6. **Q:** What core fields does an Order typically carry in a restaurant system?
   **A:** Order id, associated Table, list of OrderItems (each referencing a MenuItem + quantity + special instructions), overall OrderStatus, waiter/staff reference, and timestamps (placed, completed).

7. **Q:** Edge case: two waiters try to seat different walk-in parties at the same AVAILABLE table at nearly the same time. How do you prevent double-booking a table?
   **A:** Treat 'reserve/seat table' as an atomic state transition guarded by a lock or a compare-and-swap on TableStatus (only succeed if it's currently AVAILABLE) — the same class of concurrency problem as seat locking in a booking system, just lower-throughput.

8. **Q:** Edge case: a reservation is scheduled for 7:00 PM but the table is still OCCUPIED by a lingering earlier party. What should the system do?
   **A:** Flag the conflict to staff rather than silently double-booking; options include holding the reservation as PENDING-SEATING, offering the next available equivalent table, or notifying the host to manage the wait — the design should make this an explicit case, not an assumed happy path.

9. **Q:** Edge case: a customer wants to modify an order item after it's already been sent to the kitchen (status PREPARING). What should the system allow?
   **A:** Generally disallow silent edits to an item already PREPARING/READY; instead require an explicit cancel-and-void (with a reason, possibly requiring manager approval) plus a new order item, so the kitchen display and billing both reflect what was actually made and wasted.

10. **Q:** Edge case: how should the system support splitting a table's bill across multiple guests (by item, or evenly)?
   **A:** Model Bill as separate from Order: a Bill references a subset of OrderItems (or a share of the total) per guest, so it can support split-by-item (each guest's items summed independently) or split-evenly (total divided by N) without changing the underlying Order/OrderItem data.

11. **Q:** Edge case: what happens to table status if a reserved party never shows up (no-show)?
   **A:** The reservation should auto-expire after a grace period, releasing the table back to AVAILABLE so it isn't held indefinitely against walk-in demand; some designs also flag repeated no-shows on the customer's profile.

12. **Q:** Implement a State pattern for Table status in Java: a TableState interface and AvailableState/OccupiedState with different seat()/vacate() behavior.
   **A:** <pre><code>interface TableState {
    void seat(Table table);
    void vacate(Table table);
}

class AvailableState implements TableState {
    public void seat(Table table) {
        table.setState(new OccupiedState());
    }
    public void vacate(Table table) {
        throw new IllegalStateException("Table already available");
    }
}

class OccupiedState implements TableState {
    public void seat(Table table) {
        throw new IllegalStateException("Table already occupied");
    }
    public void vacate(Table table) {
        table.setState(new AvailableState());
    }
}</code></pre>

13. **Q:** Implement an Observer pattern in Python: a KitchenDisplay that subscribes to an OrderService and prints new items as they're placed.
   **A:** <pre><code>class OrderService:
    def __init__(self):
        self._observers = []

    def subscribe(self, observer):
        self._observers.append(observer)

    def place_item(self, order_item):
        order_item.status = "PLACED"
        for observer in self._observers:
            observer.on_new_item(order_item)

class KitchenDisplay:
    def on_new_item(self, order_item):
        print(f"NEW: {order_item.quantity}x {order_item.menu_item.name}")
        order_item.status = "PREPARING"</code></pre>

14. **Q:** Implement a Java method that atomically seats a table only if it is currently AVAILABLE, guarding against concurrent double-booking.
   **A:** <pre><code>public boolean trySeatTable(Table table, Order newOrder) {
    synchronized (table) {
        if (table.getStatus() != TableStatus.AVAILABLE) {
            return false;
        }
        table.setStatus(TableStatus.OCCUPIED);
        table.setCurrentOrder(newOrder);
        return true;
    }
}</code></pre>

15. **Q:** Implement a Python generate_split_bill() function that splits a table's order items evenly across N guests.
   **A:** <pre><code>def generate_split_bill(order, num_guests):
    subtotal = sum(
        item.menu_item.price * item.quantity
        for item in order.items
    )
    per_guest = round(subtotal / num_guests, 2)
    bills = [
        Bill(order=order, guest_index=i, amount=per_guest)
        for i in range(num_guests)
    ]
    # reconcile rounding remainder onto the first bill
    remainder = round(subtotal - per_guest * num_guests, 2)
    bills[0].amount += remainder
    return bills</code></pre>

## Cloze cards

- A {{c1::Table}} has a TableStatus of {{c2::AVAILABLE}}, {{c3::RESERVED}}, or {{c4::OCCUPIED}}, and is linked to at most one active {{c5::Order}} at a time.
- A typical OrderItem status progression is {{c1::PLACED}} → {{c2::PREPARING}} → {{c3::READY}} → {{c4::SERVED}}.

---
deck: "OOP Design::Food Delivery System"
topic: "Food Delivery System"
tags: [ankicardmaker, ood-food-delivery]
note_type: Mixed (Basic / Basic (and reversed card) / Cloze)
created: 2026-09-10
---

# Food Delivery System — OOP Design

Source of truth for the `OOP Design::Food Delivery System` deck (20 notes). Edit here and re-push to update.

## Basic cards

1. **Q:** What are the core functional requirements to clarify for a Food Delivery System OOD interview?
   **A:** 1) Customer browses a restaurant's menu and places an order. 2) Restaurant confirms/prepares the order. 3) A driver is assigned and delivers it. 4) The order's status is tracked end-to-end. 5) Payment is processed and can be refunded on cancellation/failure.

2. **Q:** What should you explicitly mark out of scope when designing a Food Delivery System in an interview?
   **A:** Real-time GPS routing/map algorithms, payment-gateway integration internals, and surge/dynamic pricing math &mdash; treat driver assignment and pricing as pluggable strategies rather than implementing the algorithms.

3. **Q:** What is the responsibility of the <code>Order</code> class?
   **A:** Holds the customer, restaurant, list of ordered <code>MenuItem</code>s with quantities, total price, and its own <code>OrderState</code>; exposes <code>advance()</code> and <code>cancel()</code> but delegates the actual transition rules to its current state object.

4. **Q:** What is the responsibility of the <code>DispatchService</code> class?
   **A:** Maintains the pool of available drivers and, using a pluggable assignment strategy, matches an order that has entered preparation to a driver, then hands off tracking of the delivery leg.

5. **Q:** What is the responsibility of the <code>Restaurant</code> class?
   **A:** Holds identity/location data and its current <code>MenuItem</code> catalog (with availability toggles), and can accept or reject an incoming <code>Order</code> based on capacity/hours.

6. **Q:** How does <code>Order</code> relate to <code>MenuItem</code>?
   **A:** Aggregation through a line-item wrapper: <code>Order</code> holds a list of <code>OrderLineItem</code> (menuItem reference + quantity + any customizations), not raw <code>MenuItem</code>s, so removing an item from the restaurant's menu later doesn't corrupt past orders.

7. **Q:** How does <code>DispatchService</code> relate to <code>Driver</code>?
   **A:** Aggregation: <code>DispatchService</code> tracks a pool of currently-available <code>Driver</code>s (drivers exist independently of dispatch, e.g. they can be off-shift); it removes a driver from the pool on assignment and returns them after delivery completes.

8. **Q:** Which design pattern fits the order lifecycle, and why?
   **A:** <b>State</b>. Each status (Placed, Confirmed, Preparing, OutForDelivery, Delivered, Cancelled) is a state object that knows which transitions are legal from it; <code>Order.advance()</code> delegates to <code>state.next(order)</code>, keeping transition rules out of a big switch statement and making illegal transitions (e.g. Delivered &rarr; Preparing) a compile-time-obvious non-option.

9. **Q:** Which design pattern fits driver assignment, and why?
   **A:** <b>Strategy</b>. A <code>DriverAssignmentStrategy</code> interface (e.g. NearestDriverStrategy, LoadBalancedStrategy) lets <code>DispatchService</code> swap the assignment algorithm &mdash; nearest driver at normal times, load-balanced during surge &mdash; without changing dispatch's calling code.

10. **Q:** What does <code>Order.advance()</code> do, and why does <code>Order</code> not implement the transition logic itself?
   **A:** It delegates to <code>state.next(this)</code>, returning the new state to assign as <code>this.state</code>. Keeping the logic in state classes (not in <code>Order</code>) means adding a new status is a new class, and each state can encapsulate side effects specific to that transition (e.g. PreparingState.next() calls DispatchService.requestDriver()).

11. **Q:** What is the shape of <code>DispatchService</code>'s core API?
   **A:** <code>requestDriver(Order order)</code> &mdash; delegates to the current <code>DriverAssignmentStrategy</code> and returns/assigns a <code>Driver</code>, raising a domain error if none is available &mdash; plus <code>setStrategy(DriverAssignmentStrategy)</code> to swap algorithms at runtime.

12. **Q:** Edge case: an assigned driver cancels mid-delivery, after pickup. How should the design handle this?
   **A:** The order stays in <code>OUT_FOR_DELIVERY</code> (not reverted to an earlier state); <code>DispatchService</code> is invoked again to find a replacement driver for the same order, and the customer is notified of the delay &mdash; the order's state machine doesn't need a new state, just a driver re-assignment at the dispatch layer.

13. **Q:** Edge case: a restaurant can't fulfill an order after it was placed (e.g. out of an ingredient). How should this be modeled?
   **A:** The restaurant transitions the order directly to <code>CANCELLED</code> from <code>PLACED</code>/<code>CONFIRMED</code> (a valid transition only from early states, enforced by the state classes), which triggers an automatic refund and a customer notification.

14. **Q:** Edge case: no drivers are available in <code>DispatchService</code>'s pool during a peak-hour rush. What should happen?
   **A:** <code>requestDriver()</code> should not throw and drop the order; instead the order is queued for retry (exponential backoff or event-driven re-trigger when a driver becomes free), and the assignment strategy can itself be swapped to one that widens the search radius during surge.

15. **Q:** (Java) Implement the <code>OrderState</code> interface and a <code>PreparingState</code> concrete implementation.
   **A:** <pre><code>public interface OrderState {
    OrderStatus getStatus();
    OrderState next(Order order);
}

public class PreparingState implements OrderState {
    @Override
    public OrderStatus getStatus() { return OrderStatus.PREPARING; }

    @Override
    public OrderState next(Order order) {
        DispatchService.getInstance().requestDriver(order);
        return new OutForDeliveryState();
    }
}</code></pre>

16. **Q:** (Python) Implement the <code>DriverAssignmentStrategy</code> interface and a <code>NearestDriverStrategy</code>.
   **A:** <pre><code>class DriverAssignmentStrategy:
    def assign(self, order, available_drivers):
        raise NotImplementedError


class NearestDriverStrategy(DriverAssignmentStrategy):
    def assign(self, order, available_drivers):
        restaurant_loc = order.restaurant.location
        return min(
            available_drivers,
            key=lambda d: distance(d.current_location, restaurant_loc),
            default=None,
        )</code></pre>

17. **Q:** (Java) Implement <code>Order.advance()</code> and <code>Order.cancel()</code> using the State pattern.
   **A:** <pre><code>public class Order {
    private OrderState state;
    private final List&lt;OrderLineItem&gt; items;

    public void advance() {
        this.state = state.next(this);
    }

    public OrderStatus getStatus() {
        return state.getStatus();
    }

    public void cancel() {
        if (state.getStatus() == OrderStatus.DELIVERED) {
            throw new IllegalStateException("Cannot cancel a delivered order");
        }
        this.state = new CancelledState();
    }
}</code></pre>

18. **Q:** (Python) Implement <code>DispatchService.request_driver()</code> with a swappable strategy and a no-drivers error.
   **A:** <pre><code>class DispatchService:
    def __init__(self, strategy):
        self.strategy = strategy
        self.available_drivers = []

    def set_strategy(self, strategy):
        self.strategy = strategy

    def request_driver(self, order):
        driver = self.strategy.assign(order, self.available_drivers)
        if driver is None:
            raise NoDriversAvailableError(order.id)
        driver.assign_order(order)
        self.available_drivers.remove(driver)
        return driver</code></pre>

## Cloze cards

- The core classes in a Food Delivery System design are {{c1::Order}}, {{c2::Restaurant}} (with a menu), {{c3::MenuItem}}, {{c4::Driver}}, and {{c5::DispatchService}} (assigns drivers to orders).
- The <code>OrderStatus</code> enum for order lifecycle is {{c1::PLACED}}, {{c2::CONFIRMED}}, {{c3::PREPARING}}, {{c4::OUT_FOR_DELIVERY}}, {{c5::DELIVERED}}, and {{c6::CANCELLED}}.

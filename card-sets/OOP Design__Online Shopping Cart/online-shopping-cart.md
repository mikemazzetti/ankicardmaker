---
deck: "OOP Design::Online Shopping Cart"
topic: "Online Shopping Cart"
tags: [ankicardmaker, ood-shopping-cart]
note_type: Mixed (Basic / Basic (and reversed card) / Cloze)
created: 2026-09-10
---

# Online Shopping Cart — OOP Design

Source of truth for the `OOP Design::Online Shopping Cart` deck (18 notes). Edit here and re-push to update.

## Basic cards

1. **Q:** In an OOD interview, what are the 3 core functional requirements for an Online Shopping Cart?
   **A:** 1) Add/remove/update-quantity of items in a cart. 2) Apply pricing rules and discounts to compute a total. 3) Check out into an Order that moves through a well-defined lifecycle (paid, shipped, delivered, cancelled).

2. **Q:** DiscountStrategy (Shopping Cart) *(reversed — both ways)*
   **A:** An interface encapsulating one discount algorithm (percentage-off, flat amount, buy-one-get-one) with an apply(cart) method that returns an adjusted total — swappable without changing checkout code.

3. **Q:** Why is Strategy a good fit for pricing/discount logic in a shopping cart?
   **A:** Different promotions (percent-off, flat-amount, tiered/bulk pricing, loyalty pricing) all compute a total from the same cart contents but with different algorithms; Strategy lets checkout call one interface method while the concrete pricing rule is chosen/swapped at runtime.

4. **Q:** Why is State a good fit for an Order's lifecycle in a shopping cart system?
   **A:** An Order's allowed operations change with its status (e.g. you can cancel a CREATED or PAID order but not a DELIVERED one); the State pattern encapsulates each status's allowed transitions in its own class instead of scattering if/switch statements on order.status everywhere.

5. **Q:** In a State-pattern Order design, what does calling order.cancel() actually do?
   **A:** It delegates to the order's current OrderState object's cancel() method; that state decides whether cancellation is legal from here (e.g. CreatedState/PaidState allow it, ShippedState throws or requires a return flow instead) and, if legal, transitions the order to CancelledState.

6. **Q:** What core fields does a CartItem typically carry, separate from the Product itself?
   **A:** A reference to the Product, the selected quantity, and often a price-at-add-time snapshot (so later product price changes don't silently alter an existing cart).

7. **Q:** Tricky edge case: discount stacking — what question must the design answer before applying two active discounts to the same cart?
   **A:** Whether discounts combine at all (some coupons are 'not combinable'), and if they do, in what order — e.g. is a percentage-off applied to the original price or to the price after a flat discount already reduced it? The order changes the final total.

8. **Q:** Give a concrete example of how discount order matters: $100 item, 20% off coupon, then $15 flat-off coupon, applied in different orders.
   **A:** Percent first, then flat: (100 * 0.8) - 15 = $65. Flat first, then percent: (100 - 15) * 0.8 = $68. The two orders yield different totals — the design must define and enforce one canonical order (usually percentage first, or defined by discount priority).

9. **Q:** How can a Decorator (or an ordered list of DiscountStrategy objects) cleanly implement stacked discounts?
   **A:** Wrap/chain each applicable discount around the base price calculation in a defined priority order, each stage taking the previous stage's output as its input — the cart doesn't need special-case logic for 'two discounts at once', it just applies the ordered pipeline.

10. **Q:** Edge case: two customers add the last unit of a product to their carts at nearly the same time. What must checkout guard against?
   **A:** An inventory race condition where both checkouts succeed and oversell the item; guard with an atomic decrement-if-available operation (or a DB row lock/optimistic version check) on inventory at checkout time, not just at add-to-cart time.

11. **Q:** Edge case: a product's price changes while it's sitting in a user's cart. What should checkout do?
   **A:** Typically re-validate against the current live price at checkout (not the price when added), and show the user a clear price-change notice if it differs — silently charging a stale price is a common correctness bug in interview designs.

12. **Q:** Edge case: what should happen if a coupon code is applied and then expires before the user completes checkout?
   **A:** Re-validate coupon validity (expiry, usage limits, minimum-spend rules) at the moment of checkout/payment, not just when it was entered — an expired coupon must be rejected or removed with the total recalculated before payment is charged.

13. **Q:** Implement a PricingStrategy interface in Java plus a PercentageDiscountStrategy.
   **A:** <pre><code>interface PricingStrategy {
    double calculateTotal(Cart cart);
}

class PercentageDiscountStrategy implements PricingStrategy {
    private final double percentOff;

    PercentageDiscountStrategy(double percentOff) {
        this.percentOff = percentOff;
    }

    public double calculateTotal(Cart cart) {
        double subtotal = cart.getItems().stream()
            .mapToDouble(item -&gt; item.getPrice() * item.getQuantity())
            .sum();
        return subtotal * (1 - percentOff / 100.0);
    }
}</code></pre>

14. **Q:** Implement a Python State pattern for Order status: an OrderState base class and CreatedState/ShippedState with different cancel() behavior.
   **A:** <pre><code>class OrderState:
    def cancel(self, order):
        raise NotImplementedError

class CreatedState(OrderState):
    def cancel(self, order):
        order.status = CancelledState()

class ShippedState(OrderState):
    def cancel(self, order):
        raise InvalidTransitionError(
            "Cannot cancel a shipped order; start a return instead"
        )

class CancelledState(OrderState):
    def cancel(self, order):
        raise InvalidTransitionError("Already cancelled")

class Order:
    def __init__(self):
        self.status = CreatedState()

    def cancel(self):
        self.status.cancel(self)</code></pre>

15. **Q:** Implement an ordered discount-stacking pipeline in Java that applies a list of DiscountStrategy objects in priority order.
   **A:** <pre><code>interface DiscountStrategy {
    double apply(double price);
}

class DiscountPipeline {
    private final List&lt;DiscountStrategy&gt; discounts;

    DiscountPipeline(List&lt;DiscountStrategy&gt; discounts) {
        this.discounts = discounts; // caller supplies priority order
    }

    double applyAll(double subtotal) {
        double price = subtotal;
        for (DiscountStrategy discount : discounts) {
            price = discount.apply(price);
        }
        return Math.max(price, 0.0);
    }
}</code></pre>

16. **Q:** Implement a Python checkout() function that atomically reserves inventory (decrement-if-available) before creating the order.
   **A:** <pre><code>def checkout(cart, inventory_repo, order_repo):
    reserved = []
    try:
        for item in cart.items:
            ok = inventory_repo.decrement_if_available(
                item.product_id, item.quantity
            )
            if not ok:
                raise OutOfStockError(item.product_id)
            reserved.append(item)
        return order_repo.create(cart)
    except OutOfStockError:
        for item in reserved:
            inventory_repo.increment(item.product_id, item.quantity)
        raise</code></pre>

## Cloze cards

- A {{c1::Cart}} holds a list of {{c2::CartItem}} objects (product + quantity); calculating its total is delegated to a pluggable {{c3::PricingStrategy}} rather than hard-coded in the Cart itself.
- OrderStatus in a shopping-cart's State pattern typically progresses: {{c1::CREATED}} → {{c2::PAID}} → {{c3::SHIPPED}} → {{c4::DELIVERED}}, with {{c5::CANCELLED}} reachable from the earlier states.

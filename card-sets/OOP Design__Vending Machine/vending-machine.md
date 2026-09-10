---
deck: "OOP Design::Vending Machine"
topic: "Vending Machine"
tags: [ankicardmaker, ood-vending-machine]
note_type: Mixed (Basic / Basic (and reversed card) / Cloze)
created: 2026-09-10
---

# Vending Machine — OOP Design

Source of truth for the `OOP Design::Vending Machine` deck (18 notes). Edit here and re-push to update.

## Basic cards

1. **Q:** What scope questions should you clarify before designing a Vending Machine System?
   **A:** What products/inventory does it stock? What payment types are accepted (cash, card, mobile)? Does it dispense change? Are there multiple slots per product and a restocking flow?

2. **Q:** What is the primary functional requirement of a Vending Machine design?
   **A:** Let a user select a product, accept payment, verify sufficient inventory and funds, dispense the product, and return change if applicable.

3. **Q:** What is the responsibility of the <code>VendingMachine</code> class?
   **A:** Top-level coordinator holding the current state, inventory, and balance; delegates behavior for each user action to the active state object.

4. **Q:** What is the responsibility of the <code>Inventory</code> class?
   **A:** Tracks product slots, quantities, and prices; checks stock availability and decrements it when a product is dispensed.

5. **Q:** What is the responsibility of the <code>Product</code> class?
   **A:** Represents an item for sale — holds its id/name and price.

6. **Q:** What is the responsibility of a <code>PaymentHandler</code> class?
   **A:** Accepts inserted money, tracks the running balance, computes change owed, and validates that sufficient payment has been made.

7. **Q:** What enum represents the vending machine's operating states?
   **A:** <code>State { IDLE, HAS_MONEY, DISPENSING, SOLD_OUT }</code>

8. **Q:** What enum represents accepted coin denominations?
   **A:** <code>Coin { NICKEL, DIME, QUARTER, DOLLAR }</code>

9. **Q:** Is the relationship between <code>VendingMachine</code> and <code>Inventory</code> composition or aggregation, and why?
   **A:** Composition — the inventory has no meaning or lifecycle outside its owning machine.

10. **Q:** Which design pattern is the natural fit for a Vending Machine's core behavior, and why?
   **A:** State — the machine's response to insert-coin/select-product/dispense actions differs entirely by its current mode (Idle, HasMoney, Dispensing, SoldOut), so each mode implements a common interface instead of branching on a status flag everywhere.

11. **Q:** In the State pattern implementation of a Vending Machine, what does each concrete state class implement?
   **A:** A common <code>VendingState</code> interface (e.g. <code>insertCoin()</code>, <code>selectProduct()</code>, <code>dispense()</code>, <code>refund()</code>) — each state defines only the behavior valid for that mode and transitions the machine to the next state.

12. **Q:** What are the main public methods on the <code>VendingMachine</code> API?
   **A:** <code>insertCoin(coin)</code>, <code>selectProduct(code)</code>, <code>dispense()</code>, and <code>refund()</code>.

13. **Q:** Tricky edge case: a user inserts more money than the product costs — what must <code>dispense()</code> handle?
   **A:** Compute and return correct change using available coin denominations, and fail gracefully (return the money, don't dispense) if exact change can't be made.

14. **Q:** Tricky edge case: the selected product's specific slot is empty even though other slots still have stock — what should happen?
   **A:** Track stock per slot (not just "has any product"), and on a sold-out slot refund the inserted money for that selection or prompt the user to reselect.

15. **Q:** Tricky edge case: <code>dispense()</code> is called but the hardware fails to physically release the product — what should happen?
   **A:** Don't deduct inventory or keep the payment until physical dispense is confirmed; on failure, refund the balance and flag the machine for maintenance/restock.

16. **Q:** Code a <code>VendingState</code> interface and an <code>IdleState</code> implementation in Java that transitions to <code>HasMoneyState</code> on <code>insertCoin</code>.
   **A:** <pre><code>public interface VendingState {
    void insertCoin(VendingMachine machine, Coin coin);
    void selectProduct(VendingMachine machine, String code);
    void dispense(VendingMachine machine);
}

public class IdleState implements VendingState {
    @Override
    public void insertCoin(VendingMachine machine, Coin coin) {
        machine.addBalance(coin.getValue());
        machine.setState(new HasMoneyState());
    }

    @Override
    public void selectProduct(VendingMachine machine, String code) {
        System.out.println("Insert coins before selecting a product.");
    }

    @Override
    public void dispense(VendingMachine machine) {
        System.out.println("Nothing to dispense.");
    }
}</code></pre>

17. **Q:** Code an <code>Inventory</code> class in Python storing product code to (product, quantity), with a method to dispense that checks and decrements stock.
   **A:** <pre><code>class Inventory:
    def __init__(self):
        self.slots = {}  # code -&gt; (Product, quantity)

    def add_stock(self, code, product, quantity):
        self.slots[code] = (product, quantity)

    def is_available(self, code):
        return code in self.slots and self.slots[code][1] &gt; 0

    def dispense(self, code):
        if not self.is_available(code):
            raise ValueError("Product unavailable")
        product, quantity = self.slots[code]
        self.slots[code] = (product, quantity - 1)
        return product</code></pre>

18. **Q:** Code a <code>VendingMachine.selectProduct</code> method in Java that checks inventory and sufficient balance before transitioning to a dispensing state.
   **A:** <pre><code>public void selectProduct(String code) {
    Product product = inventory.getProduct(code);
    if (product == null || !inventory.isAvailable(code)) {
        System.out.println("Product unavailable.");
        return;
    }
    if (balance &lt; product.getPrice()) {
        System.out.println("Insufficient funds.");
        return;
    }
    this.selectedProduct = product;
    setState(new DispensingState());
}</code></pre>

---
deck: "OOP Design::Coffee Maker"
topic: "Coffee Maker"
tags: [ankicardmaker, ood-coffee-maker]
note_type: Mixed (Basic / Basic (and reversed card) / Cloze)
created: 2026-09-10
---

# Coffee Maker — OOP Design

Source of truth for the `OOP Design::Coffee Maker` deck (20 notes). Edit here and re-push to update.

## Basic cards

1. **Q:** What core use cases should an OOD interview design for a smart coffee maker cover?
   **A:** Brewing multiple beverage types (espresso, latte, cappuccino) from configurable recipes, tracking ingredient inventory, customizing a drink's size/strength, and handling maintenance (cleaning/descaling).

2. **Q:** What is the responsibility of the CoffeeMachine class vs. a Recipe class?
   **A:** CoffeeMachine owns the physical subsystems (grinder, boiler, dispenser) and orchestrates brewing; Recipe is a data object describing the ingredient amounts and steps for one beverage type.

3. **Q:** Why model an InventoryManager as a separate class from CoffeeMachine?
   **A:** It isolates ingredient-stock tracking (quantities, refill, low-stock alerts) as its own concern, so CoffeeMachine just asks it 'do we have enough?' instead of managing raw stock counts itself.

4. **Q:** What relationship exists between Recipe and Ingredient in the class model?
   **A:** Composition/aggregation: a Recipe holds a list of (Ingredient, quantity) pairs describing what's needed to brew one Beverage of that type.

5. **Q:** Which design pattern fits creating the correct Beverage object for a requested type (espresso, latte, ...), and why?
   **A:** Factory Method: a BeverageFactory centralizes a <code>createBeverage(BeverageType)</code> call so new drink types can be added without changing the brewing/ordering code.

6. **Q:** Which design pattern fits letting a customer customize a drink (size, milk type, extra shot, sugar level) step by step, and why?
   **A:** Builder: a BeverageBuilder lets you chain calls like <code>withSize(...)</code>, <code>withMilk(...)</code>, <code>withExtraShot()</code> and finish with <code>build()</code>, avoiding a telescoping constructor for every combination of options.

7. **Q:** Which design pattern fits ensuring only one InventoryManager instance coordinates stock across the whole machine, and why?
   **A:** Singleton: all subsystems (grinder, boiler) must read/write the same shared ingredient counts, so a single shared instance prevents inconsistent stock views.

8. **Q:** What must <code>brew(beverageType, customization)</code> check before starting?
   **A:** That the machine isn't already mid-brew (single brewing unit), and that InventoryManager confirms every ingredient in the resolved Recipe has sufficient quantity.

9. **Q:** What should <code>refillIngredient(type, amount)</code> do?
   **A:** Increase the InventoryManager's stock count for that IngredientType and clear any low-stock alert flag for it, without needing the machine to be idle.

10. **Q:** Edge case: ingredients run out mid-brew (e.g., milk runs dry while steaming). What should the design do?
   **A:** Abort the brew cleanly, discard the partially-made beverage, refund or flag the order, and mark that IngredientType OUT_OF_STOCK so subsequent brew checks fail fast instead of starting.

11. **Q:** Edge case: two brew requests arrive while the machine is already brewing. How should the design handle the second request?
   **A:** Since there's one shared brewing unit, queue the second request (or reject with a 'busy' status) rather than interleaving two brews, which would corrupt shared subsystem state.

12. **Q:** Edge case: an ingredient is present in sufficient quantity but expired. What should the inventory check add?
   **A:** Track an expiration/best-by date per ingredient batch and fail the availability check (or warn) for expired stock even if the quantity is nonzero.

13. **Q:** Edge case: the machine needs a mandatory descale/clean cycle. How should this interact with brew requests?
   **A:** Track a maintenanceRequired flag (e.g., after N brews or a time interval) and reject new <code>brew()</code> calls with a clear status until cleaning completes, rather than silently degrading drink quality.

14. **Q:** Builder pattern *(reversed — both ways)*
   **A:** A creational pattern that separates step-by-step construction of a complex object (like a customized Beverage) from its final representation, allowing the same construction process to produce different configurations.

15. **Q:** Why is Factory Method preferred over a large if/else in <code>brew()</code> for selecting beverage type?
   **A:** It keeps the beverage-creation logic in one place (open/closed principle) — adding a new drink type means adding a new Beverage subclass and factory case, not touching every place that creates beverages.

16. **Q:** Implement a Java Factory Method for creating Beverage objects by BeverageType.
   **A:** <pre><code>public abstract class Beverage {
    public abstract List&lt;Ingredient&gt; getRecipe();
}

public class Espresso extends Beverage {
    public List&lt;Ingredient&gt; getRecipe() {
        return List.of(new Ingredient(IngredientType.WATER, 30),
                        new Ingredient(IngredientType.COFFEE_BEANS, 18));
    }
}

public class BeverageFactory {
    public static Beverage create(BeverageType type) {
        switch (type) {
            case ESPRESSO: return new Espresso();
            case LATTE: return new Latte();
            default: throw new IllegalArgumentException("Unknown type: " + type);
        }
    }
}
</code></pre>

17. **Q:** Implement the Builder pattern in Python for customizing a beverage order (size, milk, extra shot).
   **A:** <pre><code>class BeverageOrder:
    def __init__(self):
        self.size = "medium"
        self.milk = None
        self.extra_shots = 0

class BeverageBuilder:
    def __init__(self):
        self._order = BeverageOrder()

    def with_size(self, size):
        self._order.size = size
        return self

    def with_milk(self, milk_type):
        self._order.milk = milk_type
        return self

    def with_extra_shot(self):
        self._order.extra_shots += 1
        return self

    def build(self):
        return self._order

order = (BeverageBuilder()
         .with_size("large")
         .with_milk("oat")
         .with_extra_shot()
         .build())
</code></pre>

18. **Q:** Implement a thread-safe Singleton InventoryManager in Java.
   **A:** <pre><code>public class InventoryManager {
    private static volatile InventoryManager instance;
    private final Map&lt;IngredientType, Integer&gt; stock = new HashMap&lt;&gt;();

    private InventoryManager() {}

    public static InventoryManager getInstance() {
        if (instance == null) {
            synchronized (InventoryManager.class) {
                if (instance == null) {
                    instance = new InventoryManager();
                }
            }
        }
        return instance;
    }

    public synchronized boolean hasEnough(IngredientType type, int amount) {
        return stock.getOrDefault(type, 0) &gt;= amount;
    }
}
</code></pre>

19. **Q:** Implement a Python <code>brew</code> method that checks inventory for every ingredient in a Recipe before consuming them.
   **A:** <pre><code>class CoffeeMachine:
    def __init__(self, inventory):
        self.inventory = inventory
        self.busy = False

    def brew(self, recipe):
        if self.busy:
            raise RuntimeError("Machine busy")
        for ingredient, amount in recipe.items():
            if not self.inventory.has_enough(ingredient, amount):
                raise RuntimeError(f"Insufficient {ingredient}")
        self.busy = True
        try:
            for ingredient, amount in recipe.items():
                self.inventory.consume(ingredient, amount)
        finally:
            self.busy = False
</code></pre>

## Cloze cards

- A brew request typically checks these IngredientTypes before proceeding: {{c1::WATER}}, {{c2::COFFEE_BEANS}}, {{c3::MILK}}, and {{c4::SUGAR}}.

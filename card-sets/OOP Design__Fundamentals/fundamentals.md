---
deck: "OOP Design::Fundamentals"
topic: "Fundamentals"
tags: [ankicardmaker, ood-fundamentals]
note_type: Mixed (Basic / Basic (and reversed card) / Cloze)
created: 2026-09-10
---

# Fundamentals — OOP Design

Source of truth for the `OOP Design::Fundamentals` deck (24 notes). Edit here and re-push to update.

## Basic cards

1. **Q:** Why should you clarify requirements before designing any classes in an OOD interview?
   **A:** It sets the correct scope (features, scale, constraints) so you don't over- or under-engineer the design — jumping straight to classes risks solving the wrong problem.

2. **Q:** What simple technique helps you identify candidate classes from an OOD problem statement?
   **A:** Underline the nouns in the prompt — each distinct noun is a candidate class or object (e.g. "Vehicle", "Ticket", "ParkingSpot").

3. **Q:** In UML/OOD terms, what is an Association relationship?
   **A:** A general "uses-a" relationship where one object interacts with or references another, with no ownership or lifecycle dependency implied.

4. **Q:** In UML/OOD terms, what is an Aggregation relationship?
   **A:** A "has-a" relationship expressing weak ownership — the whole contains the part, but the part can exist independently and outlive the whole.

5. **Q:** In UML/OOD terms, what is a Composition relationship?
   **A:** A "has-a" relationship expressing strong ownership — the part's lifecycle is bound to the whole; when the whole is destroyed, so are its parts.

6. **Q:** On a UML class diagram, how do you visually distinguish composition from aggregation?
   **A:** A filled (solid) diamond at the "whole" end means composition; a hollow (open) diamond at the "whole" end means aggregation.

7. **Q:** What are the three compartments of a class box in a UML class diagram?
   **A:** Class name (top), attributes/fields (middle), methods/operations (bottom).

8. **Q:** SOLID — what does the Single Responsibility Principle (S) state?
   **A:** A class should have only one reason to change — i.e., one responsibility.

9. **Q:** SOLID — what does the Open/Closed Principle (O) state?
   **A:** Classes should be open for extension but closed for modification — add new behavior via new code, not by editing existing tested code.

10. **Q:** SOLID — what does the Liskov Substitution Principle (L) state?
   **A:** Objects of a subclass should be substitutable for objects of the base class without altering the correctness of the program.

11. **Q:** SOLID — what does the Interface Segregation Principle (I) state?
   **A:** Prefer several small, client-specific interfaces over one large general-purpose interface, so clients aren't forced to depend on methods they don't use.

12. **Q:** SOLID — what does the Dependency Inversion Principle (D) state?
   **A:** High-level modules should depend on abstractions, not on low-level concrete implementations — both should depend on interfaces.

13. **Q:** Strategy pattern — when should you use it in an OOD design?
   **A:** Use it when you need to select between multiple interchangeable algorithms/behaviors at runtime (e.g. pricing, sorting, dispatch policy) without conditional branching.

14. **Q:** Factory Method pattern — when should you use it?
   **A:** Use it when a class shouldn't hardcode which concrete subclass to instantiate — let a factory (or subclasses) decide, decoupling creation from use.

15. **Q:** Abstract Factory pattern — when should you use it?
   **A:** Use it when you need to create families of related objects (e.g. UI widgets for different platforms) without specifying their concrete classes.

16. **Q:** Singleton pattern — when should you use it?
   **A:** Use it when exactly one instance of a class must exist and be globally accessible (e.g. a config manager or the ParkingLot itself) — but use sparingly, it hurts testability.

17. **Q:** Observer pattern — when should you use it?
   **A:** Use it when one object's state change must automatically notify and update many dependent objects, without tightly coupling them (e.g. pub/sub, UI updates).

18. **Q:** State pattern — when should you use it?
   **A:** Use it when an object's behavior must change based on its internal state, to avoid large if/switch blocks scattered across methods (e.g. a vending machine or elevator).

19. **Q:** Decorator pattern — when should you use it?
   **A:** Use it when you need to add responsibilities to an individual object dynamically at runtime, as an alternative to subclassing every combination of features.

20. **Q:** Command pattern — when should you use it?
   **A:** Use it when you need to encapsulate a request/action as an object, to support undo/redo, queuing, logging, or parameterizing callers with different actions.

21. **Q:** Adapter pattern — when should you use it?
   **A:** Use it when you need an existing class's interface to work with client code that expects a different, incompatible interface.

22. **Q:** Code a Strategy pattern in Java for payment processing: a <code>PaymentStrategy</code> interface with <code>CreditCardStrategy</code> and <code>PayPalStrategy</code> implementations, used by a <code>Cart</code> class.
   **A:** <pre><code>public interface PaymentStrategy {
    void pay(int amount);
}

public class CreditCardStrategy implements PaymentStrategy {
    private String cardNumber;

    public CreditCardStrategy(String cardNumber) {
        this.cardNumber = cardNumber;
    }

    @Override
    public void pay(int amount) {
        System.out.println("Paid " + amount + " using Credit Card " + cardNumber);
    }
}

public class PayPalStrategy implements PaymentStrategy {
    private String email;

    public PayPalStrategy(String email) {
        this.email = email;
    }

    @Override
    public void pay(int amount) {
        System.out.println("Paid " + amount + " using PayPal account " + email);
    }
}

public class Cart {
    private PaymentStrategy paymentStrategy;

    public void setPaymentStrategy(PaymentStrategy strategy) {
        this.paymentStrategy = strategy;
    }

    public void checkout(int amount) {
        paymentStrategy.pay(amount);
    }
}</code></pre>

23. **Q:** Code an Observer pattern in Python: a <code>WeatherStation</code> subject that notifies subscribed <code>Observer</code> objects when temperature changes.
   **A:** <pre><code>from abc import ABC, abstractmethod

class Observer(ABC):
    @abstractmethod
    def update(self, temperature: float) -&gt; None:
        ...

class WeatherStation:
    def __init__(self):
        self._observers = []
        self._temperature = 0.0

    def subscribe(self, observer: Observer) -&gt; None:
        self._observers.append(observer)

    def unsubscribe(self, observer: Observer) -&gt; None:
        self._observers.remove(observer)

    def set_temperature(self, temperature: float) -&gt; None:
        self._temperature = temperature
        self._notify_all()

    def _notify_all(self) -&gt; None:
        for observer in self._observers:
            observer.update(self._temperature)

class Display(Observer):
    def update(self, temperature: float) -&gt; None:
        print(f"Display shows: {temperature}C")</code></pre>

## Cloze cards

- The four-step approach to an OOD interview: {{c1::clarify requirements and scope}} → {{c2::identify the core objects (nouns) in the problem}} → {{c3::define the relationships between those objects}} → {{c4::design the class APIs and apply relevant design patterns}}.

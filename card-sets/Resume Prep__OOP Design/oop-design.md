---
deck: "Resume Prep::OOP Design"
topic: "OOP Design"
tags: [ankicardmaker, resume-prep, oop]
note_type: Mixed (Basic / Basic (and reversed card) / Cloze)
created: 2026-09-09
---

# OOP Design — Resume Prep

Source of truth for the `Resume Prep::OOP Design` deck (19 notes). Edit here and re-push to update.

## Basic cards

1. **Q:** Single Responsibility Principle (SRP) *(reversed — tested both ways)*
   **A:** A class should have only one reason to change &mdash; it should do exactly one job.

2. **Q:** Open/Closed Principle (OCP) *(reversed — tested both ways)*
   **A:** Software entities should be open for extension but closed for modification &mdash; add new behavior via new code (e.g. subclassing/composition), not by editing existing tested code.

3. **Q:** Liskov Substitution Principle (LSP) *(reversed — tested both ways)*
   **A:** Objects of a subclass must be substitutable for objects of the superclass without breaking the correctness of the program.

4. **Q:** Interface Segregation Principle (ISP) *(reversed — tested both ways)*
   **A:** No client should be forced to depend on methods it does not use &mdash; prefer several small, specific interfaces over one large general-purpose one.

5. **Q:** Dependency Inversion Principle (DIP) *(reversed — tested both ways)*
   **A:** High-level modules should depend on abstractions, not on low-level concrete implementations; both should depend on interfaces.

6. **Q:** Why is "favor composition over inheritance" common design advice?
   **A:** Composition (has-a, holding a reference to another object) is more flexible than inheritance (is-a): it avoids deep fragile hierarchies, lets you swap behavior at runtime, and doesn't leak the parent's implementation details into the child.

7. **Q:** What is the key difference between an interface and an abstract class?
   **A:** An interface declares a contract (method signatures, no state) that a class can implement multiple of; an abstract class can hold shared state and partial implementation, but a class can extend only one.

8. **Q:** What problem does the Singleton pattern solve?
   **A:** It ensures a class has exactly one instance and provides a single global access point to it (e.g. a shared config or connection pool).

9. **Q:** How do you code a thread-safe lazy Singleton in Java?
   **A:** <pre><code>public class Singleton {
    private static volatile Singleton instance;
    private Singleton() {}

    public static Singleton getInstance() {
        if (instance == null) {
            synchronized (Singleton.class) {
                if (instance == null) {
                    instance = new Singleton();
                }
            }
        }
        return instance;
    }
}</code></pre>

10. **Q:** What problem does the Factory pattern solve?
   **A:** It centralizes object creation logic behind a method/class, so calling code depends on an abstraction instead of concrete constructors &mdash; useful when the exact subtype to create depends on runtime input.

11. **Q:** How do you code a simple Factory in Java?
   **A:** <pre><code>interface Shape { void draw(); }
class Circle implements Shape {
    public void draw() { System.out.println("circle"); }
}

class ShapeFactory {
    static Shape create(String type) {
        return switch (type) {
            case "circle" -> new Circle();
            default -> throw new IllegalArgumentException();
        };
    }
}</code></pre>

12. **Q:** What problem does the Strategy pattern solve?
   **A:** It lets you define a family of interchangeable algorithms behind a common interface and swap which one an object uses at runtime, instead of branching with if/else or subclassing per algorithm.

13. **Q:** How do you code the Strategy pattern in Java?
   **A:** <pre><code>interface DiscountStrategy {
    double apply(double price);
}
class NoDiscount implements DiscountStrategy {
    public double apply(double p) { return p; }
}
class TenPercentOff implements DiscountStrategy {
    public double apply(double p) { return p * 0.9; }
}

class Cart {
    private DiscountStrategy strategy;
    Cart(DiscountStrategy s) { this.strategy = s; }
    double total(double price) { return strategy.apply(price); }
}</code></pre>

14. **Q:** What problem does the Observer pattern solve, and give a real-world example.
   **A:** It lets one or more "observer" objects be notified automatically when a "subject" object's state changes, without the subject knowing observer details. Example: event listeners in a UI, or pub/sub messaging.

15. **Q:** What is the difference between coupling and cohesion, and which is desirable?
   **A:** <b>Coupling</b> = how much one module depends on/knows about another's internals. <b>Cohesion</b> = how closely related a single module's responsibilities are. Good design aims for <b>low coupling, high cohesion</b>.

## Cloze cards

- {{c1::Encapsulation}} is the pillar of OOP that bundles data with the methods that operate on it and restricts direct external access to that data (e.g. private fields with public getters/setters).
- {{c1::Abstraction}} is the pillar of OOP that exposes only the essential behavior of an object through a simplified interface, hiding internal implementation details.
- {{c1::Inheritance}} is the pillar of OOP that lets a class acquire fields and methods from a parent class, enabling code reuse and an is-a relationship.
- {{c1::Polymorphism}} is the pillar of OOP that lets objects of different classes be treated through a common interface, with the actual method invoked determined at runtime (or compile time for overloading).

---
deck: "OOP Design::Library Management System"
topic: "Library Management System"
tags: [ankicardmaker, ood-library]
note_type: Mixed (Basic / Basic (and reversed card) / Cloze)
created: 2026-09-10
---

# Library Management System — OOP Design

Source of truth for the `OOP Design::Library Management System` deck (20 notes). Edit here and re-push to update.

## Basic cards

1. **Q:** In an OOD interview, what should you clarify first about the Library Management System's scope before designing classes?
   **A:** The core use cases: catalog search, checkout/return of items, reservations/holds, membership limits, and fine/fee policy — plus scale (single branch vs multi-branch).

2. **Q:** Why does a Library Management System model both a Book and a BookItem class instead of just Book?
   **A:** Book holds catalog metadata shared by all copies (title, author, ISBN); BookItem represents one physical/circulating copy with its own barcode, status, and due date.

3. **Q:** What is the primary responsibility of the Library class in an LMS design?
   **A:** Acts as the top-level aggregate root: owns the catalog of Books/BookItems, coordinates search, and manages Member and Librarian accounts.

4. **Q:** What distinguishes a Librarian from a Member in the LMS class model?
   **A:** Both extend a common Account/Person base, but Librarian has extra privileges: adding/removing BookItems, managing memberships, and waiving fines.

5. **Q:** What relationship exists between Library and BookItem in the class diagram?
   **A:** Composition (one-to-many): a Library owns many BookItems, and a BookItem cannot exist independently of the Library's catalog.

6. **Q:** How do Reservation and Loan differ as classes in an LMS design?
   **A:** A Reservation records that a Member is waiting for a currently-unavailable BookItem; a Loan records that a Member currently holds a checked-out BookItem with a due date.

7. **Q:** Which design pattern fits notifying waiting members when a reserved book becomes available, and why?
   **A:** Observer: each BookItem maintains a list of Members reserved on it; when its status changes to AVAILABLE, it notifies the next Member in the reservation queue.

8. **Q:** Which design pattern fits computing overdue fines that may vary by member type or book category, and why?
   **A:** Strategy: encapsulate the fine calculation in interchangeable FineStrategy implementations (e.g., FlatRateStrategy, TieredStrategy) so the policy can change without touching Loan/Library code.

9. **Q:** What does the method <code>checkout(BookItem, Member)</code> need to validate before completing a loan?
   **A:** BookItem.status == AVAILABLE, the Member is in good standing (no unpaid fines / under loan limit), then it creates a Loan, sets BookItem.status = LOANED, and sets the due date.

10. **Q:** What should <code>returnBook(BookItem)</code> do after a member returns an item?
   **A:** Close the associated Loan, calculate any overdue fine, and update BookItem.status — to RESERVED if a hold queue exists, otherwise AVAILABLE.

11. **Q:** Edge case: two members try to reserve the same BookItem at the same instant. How should the design handle it?
   **A:** Serialize access to the reservation queue per BookItem (e.g., a lock or atomic enqueue) so only one reservation is accepted first-come-first-served; the loser stays queued behind it.

12. **Q:** Edge case: a member loses a checked-out book. What should the system do?
   **A:** Mark the BookItem status LOST, close the Loan, charge the member a replacement fee, and remove the item from the searchable catalog (or flag it for reorder).

13. **Q:** Edge case: a member wants to renew a loan that already has a reservation queue behind it. What's the correct behavior?
   **A:** Deny the renewal — items with pending reservations must be returned on the original due date so the next member in the queue can be served.

14. **Q:** ISBN *(reversed — both ways)*
   **A:** International Standard Book Number — a unique identifier for a Book's edition/title, used as the catalog lookup key (not per physical copy).

15. **Q:** Why should <code>search(query)</code> be defined on Library rather than on Book or BookItem?
   **A:** Search spans the whole catalog and needs a single entry point with an index (by title/author/ISBN); putting it on an individual Book/BookItem would have no access to the full collection.

16. **Q:** Implement the <code>checkout</code> method on a Java <code>BookItem</code> class that transitions status and records the borrower and due date.
   **A:** <pre><code>public class BookItem {
    private String barcode;
    private BookStatus status;
    private Member borrowedBy;
    private LocalDate dueDate;

    public void checkout(Member member, int loanDays) {
        if (status != BookStatus.AVAILABLE) {
            throw new IllegalStateException("Item not available: " + barcode);
        }
        this.status = BookStatus.LOANED;
        this.borrowedBy = member;
        this.dueDate = LocalDate.now().plusDays(loanDays);
    }
}
</code></pre>

17. **Q:** Implement a Python <code>Library.search</code> method that filters BookItems by title substring, case-insensitively, returning only available copies.
   **A:** <pre><code>class Library:
    def __init__(self):
        self.book_items = []

    def search(self, title_query):
        query = title_query.lower()
        return [
            item for item in self.book_items
            if query in item.book.title.lower()
            and item.status == BookStatus.AVAILABLE
        ]
</code></pre>

18. **Q:** Implement the Observer pattern in Java so a BookItem notifies the next waiting Member when it becomes available.
   **A:** <pre><code>public interface ReservationObserver {
    void onAvailable(BookItem item);
}

public class BookItem {
    private Queue&lt;ReservationObserver&gt; waitList = new LinkedList&lt;&gt;();
    private BookStatus status;

    public void reserve(ReservationObserver observer) {
        waitList.add(observer);
        status = BookStatus.RESERVED;
    }

    public void markReturned() {
        if (!waitList.isEmpty()) {
            ReservationObserver next = waitList.poll();
            status = BookStatus.RESERVED;
            next.onAvailable(this);
        } else {
            status = BookStatus.AVAILABLE;
        }
    }
}
</code></pre>

19. **Q:** Implement the Strategy pattern in Python for two interchangeable overdue-fine policies.
   **A:** <pre><code>from abc import ABC, abstractmethod

class FineStrategy(ABC):
    @abstractmethod
    def calculate(self, days_overdue):
        ...

class FlatRateFine(FineStrategy):
    def calculate(self, days_overdue):
        return 0.25 * days_overdue

class TieredFine(FineStrategy):
    def calculate(self, days_overdue):
        if days_overdue &lt;= 7:
            return 0.10 * days_overdue
        return 0.70 + 0.50 * (days_overdue - 7)

class Loan:
    def __init__(self, fine_strategy: FineStrategy):
        self.fine_strategy = fine_strategy

    def overdue_fine(self, days_overdue):
        return self.fine_strategy.calculate(days_overdue)
</code></pre>

## Cloze cards

- A BookItem's lifecycle typically moves through the status values {{c1::AVAILABLE}}, {{c2::RESERVED}}, {{c3::LOANED}}, and {{c4::LOST}}.

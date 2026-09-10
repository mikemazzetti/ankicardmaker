---
deck: "OOP Design::Amazon Locker"
topic: "Amazon Locker"
tags: [ankicardmaker, ood-amazon-locker]
note_type: Mixed (Basic / Basic (and reversed card) / Cloze)
created: 2026-09-10
---

# Amazon Locker — OOP Design

Source of truth for the `OOP Design::Amazon Locker` deck (20 notes). Edit here and re-push to update.

## Basic cards

1. **Q:** What are the core functional requirements to clarify for an Amazon Locker OOD interview?
   **A:** 1) A courier drops a package into a locker sized to fit it. 2) The system generates a pickup access code and notifies the recipient. 3) The recipient enters the code to unlock and retrieve the package. 4) Unclaimed packages expire after a pickup window. 5) A single locker bank has a fixed, mixed set of locker sizes to allocate efficiently.

2. **Q:** What should you explicitly mark out of scope when designing an Amazon Locker system in an interview?
   **A:** Physical hardware/lock mechanism details, courier route optimization, and payment/billing &mdash; focus on locker allocation, access-code lifecycle, and the size-assignment strategy.

3. **Q:** What is the responsibility of the <code>LockerBank</code> class?
   **A:** Represents one physical location: owns a fixed set of <code>Locker</code>s of mixed sizes, and exposes <code>assignLocker(Package)</code> / <code>releaseLocker(code)</code> as the entry points for courier drop-off and customer pickup.

4. **Q:** What is the responsibility of the <code>Locker</code> class?
   **A:** One physical compartment: tracks its own <code>LockerSize</code>, <code>LockerStatus</code>, the <code>Package</code> currently inside (if any), and the current access code plus its expiration; exposes <code>unlock(code)</code>.

5. **Q:** What is the responsibility of the <code>Package</code> class?
   **A:** Holds the tracking id, recipient info, and the <code>LockerSize</code> the package requires &mdash; it is a passive data object with no knowledge of which locker it ends up in.

6. **Q:** How does <code>LockerBank</code> relate to <code>Locker</code>?
   **A:** Composition: a <code>LockerBank</code> owns a fixed collection of <code>Locker</code>s (typically a mix of sizes decided at install time); lockers don't exist outside a bank and are looked up by the bank when allocating or releasing.

7. **Q:** Which design pattern fits locker-size assignment, and why?
   **A:** <b>Strategy</b>. A <code>LockerSizeAssignmentStrategy</code> interface (e.g. BestFitStrategy, FirstAvailableStrategy) lets <code>LockerBank</code> swap the allocation algorithm &mdash; best-fit to minimize wasted space vs. first-available for speed &mdash; without changing the bank's calling code.

8. **Q:** What is the shape of <code>LockerBank.assignLocker()</code>'s API and return value?
   **A:** <code>assignLocker(Package pkg)</code> filters lockers to <code>AVAILABLE</code> ones whose size is &ge; the package's required size, delegates the final pick to the assignment strategy, marks that locker <code>OCCUPIED</code>, generates an access code, and returns both the locker and the code.

9. **Q:** What must <code>Locker.unlock(code)</code> check, in order, before releasing the package?
   **A:** 1) The locker is actually <code>OCCUPIED</code> (not already empty). 2) The access code hasn't expired (raise/return an expiry-specific error, not a generic failure). 3) The entered code matches. Only then does it release the package and reset status to <code>AVAILABLE</code>.

10. **Q:** Edge case: no locker of the exact required size is available at drop-off time. What should the assignment strategy do?
   **A:** Fall back to the next size up (never a smaller one, or the package won't physically fit) &mdash; e.g. a BestFit strategy that finds no MEDIUM locker free should consider LARGE next, and only raise a <code>NoLockerAvailableException</code> if every size &ge; required is full.

11. **Q:** Edge case: a recipient never enters their access code within the pickup window (e.g. 3 days). What should happen?
   **A:** The system auto-expires the code, marks the package for return-to-sender/carrier pickup, notifies the recipient and sender, and frees the locker back to <code>AVAILABLE</code> once the carrier physically retrieves the package (status can pass through a transient <code>RESERVED</code>/pending-return state, not straight to AVAILABLE while the package is still inside).

12. **Q:** Edge case: two couriers could simultaneously try to drop packages into the same locker bank at the exact same time. How does the design prevent a double-assignment?
   **A:** <code>assignLocker()</code> must perform an atomic check-and-set on a locker's status (e.g. compare-and-swap AVAILABLE&rarr;OCCUPIED under a lock/transaction) rather than read-then-write, so two concurrent calls can never both succeed in claiming the same <code>Locker</code>.

13. **Q:** Edge case: a recipient forgets/loses their access code. What recovery path should the design support?
   **A:** Expose a <code>regenerateAccessCode(package)</code> flow gated by identity verification (e.g. re-authenticating in the retailer's app) that invalidates the old code and issues a new one with a fresh expiration, without changing the locker's contents or status.

14. **Q:** (Java) Implement the <code>LockerSizeAssignmentStrategy</code> interface and a <code>BestFitStrategy</code>.
   **A:** <pre><code>public interface LockerSizeAssignmentStrategy {
    Locker selectLocker(Package pkg, List&lt;Locker&gt; availableLockers);
}

public class BestFitStrategy implements LockerSizeAssignmentStrategy {
    @Override
    public Locker selectLocker(Package pkg, List&lt;Locker&gt; availableLockers) {
        return availableLockers.stream()
            .filter(locker -&gt; locker.getSize().ordinal() &gt;= pkg.getRequiredSize().ordinal())
            .filter(locker -&gt; locker.getStatus() == LockerStatus.AVAILABLE)
            .min(Comparator.comparing(locker -&gt; locker.getSize().ordinal()))
            .orElseThrow(() -&gt; new NoLockerAvailableException(pkg.getId()));
    }
}</code></pre>

15. **Q:** (Python) Implement <code>LockerBank.assign_locker()</code>, including random access-code generation.
   **A:** <pre><code>import random
import string

class LockerBank:
    def __init__(self, lockers, strategy):
        self.lockers = lockers
        self.strategy = strategy

    def assign_locker(self, package):
        available = [l for l in self.lockers if l.status == LockerStatus.AVAILABLE]
        locker = self.strategy.select_locker(package, available)
        code = self._generate_access_code()
        locker.status = LockerStatus.OCCUPIED
        locker.package = package
        locker.access_code = code
        return locker, code

    def _generate_access_code(self):
        return "".join(random.choices(string.digits, k=6))</code></pre>

16. **Q:** (Java) Implement <code>Locker.unlock(code)</code>, including the expired-code check.
   **A:** <pre><code>public class Locker {
    private LockerStatus status;
    private String accessCode;
    private LocalDateTime codeExpiresAt;
    private Package contents;

    public boolean unlock(String enteredCode) {
        if (status != LockerStatus.OCCUPIED) {
            return false;
        }
        if (LocalDateTime.now().isAfter(codeExpiresAt)) {
            throw new AccessCodeExpiredException();
        }
        if (!accessCode.equals(enteredCode)) {
            return false;
        }
        status = LockerStatus.AVAILABLE;
        contents = null;
        accessCode = null;
        return true;
    }
}</code></pre>

17. **Q:** (Python) Implement a fallback strategy that widens to the next larger size when the primary strategy finds nothing.
   **A:** <pre><code>class FirstAvailableFallbackStrategy(LockerSizeAssignmentStrategy):
    def __init__(self, primary_strategy):
        self.primary_strategy = primary_strategy

    def select_locker(self, package, available_lockers):
        try:
            return self.primary_strategy.select_locker(package, available_lockers)
        except NoLockerAvailableError:
            largest = max(available_lockers, key=lambda l: l.size.value, default=None)
            if largest is None:
                raise
            return largest</code></pre>

## Cloze cards

- The core classes in an Amazon Locker design are {{c1::LockerBank}} (a physical location), {{c2::Locker}} (one compartment), {{c3::Package}}, and {{c4::LockerSizeAssignmentStrategy}} (chooses which locker fits a package).
- The <code>LockerSize</code> enum is ordered {{c1::SMALL}}, {{c2::MEDIUM}}, {{c3::LARGE}}, {{c4::EXTRA_LARGE}} so sizes can be compared to find the smallest locker that still fits a package.
- The <code>LockerStatus</code> enum for a single compartment is {{c1::AVAILABLE}}, {{c2::OCCUPIED}}, {{c3::RESERVED}}, and {{c4::OUT_OF_SERVICE}}.

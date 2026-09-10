---
deck: "OOP Design::Splitwise"
topic: "Splitwise"
tags: [ankicardmaker, ood-splitwise]
note_type: Mixed (Basic / Basic (and reversed card) / Cloze)
created: 2026-09-10
---

# Splitwise — OOP Design

Source of truth for the `OOP Design::Splitwise` deck (20 notes). Edit here and re-push to update.

## Basic cards

1. **Q:** In Splitwise's domain model, what three concrete Split subtypes does the Strategy pattern typically provide?
   **A:** EqualSplit, ExactSplit, and PercentSplit &mdash; each implementing a common SplitStrategy/Split interface with a method to compute each participant's owed amount.

2. **Q:** What is the responsibility of the Expense class?
   **A:** Holds the total amount, the payer (who fronted the money), the list of participants, the chosen SplitStrategy/SplitType, and produces a list of per-user Split amounts owed.

3. **Q:** Strategy pattern *(reversed — both ways)*
   **A:** Behavioral pattern that defines a family of interchangeable algorithms (here, split-calculation methods) behind a common interface, letting the context (Expense) pick one at runtime without conditional branching.

4. **Q:** Why does the Strategy pattern fit split calculation better than a big if/else on SplitType inside Expense?
   **A:** Each split algorithm (equal/exact/percent) has different validation and math; Strategy isolates each in its own class implementing a common interface, so adding a new split type (e.g. SHARES/weighted) means adding a class, not editing Expense's logic &mdash; Open/Closed Principle.

5. **Q:** What structure represents who-owes-whom across a group, and why call it a 'balance graph'?
   **A:** A directed weighted graph where each User is a node and each edge (A -&gt; B, amount) represents A owing B that amount; implemented as e.g. <code>Map&lt;User, Map&lt;User, Double&gt;&gt;</code>. It's a graph because debts form a network, and simplification is a graph-reduction problem.

6. **Q:** What is 'debt simplification' in Splitwise, and what algorithmic approach solves it?
   **A:** Reducing the number of individual transactions needed to settle all group balances (e.g. A owes B, B owes C, C owes A nets to fewer/zero transfers). Solved as a min-cash-flow problem: compute each person's net balance, then greedily match the largest creditor with the largest debtor repeatedly.

7. **Q:** In the balance graph, how do you compute a single User's net balance (how much they're owed overall)?
   **A:** Net = total amount owed to them by everyone, minus total amount they owe everyone else (receivable - payable).

8. **Q:** What must be true of the percentages in a PercentSplit for an Expense to be valid?
   **A:** They must sum to exactly 100% across all participants (within a small floating-point epsilon); otherwise reject the expense with a validation error.

9. **Q:** What must be true of the amounts in an ExactSplit for an Expense to be valid?
   **A:** The sum of each participant's exact amount must equal the Expense's total amount (within a small epsilon for floating point).

10. **Q:** What rounding edge case occurs with EqualSplit, and how is it typically handled?
   **A:** Dividing a total like $100 among 3 people gives $33.33 repeating &mdash; the split amounts won't sum exactly to $100 in cents. Fix: compute the floor amount per person, then distribute the leftover cents one at a time to the first N participants (or the payer) so the sum matches exactly.

11. **Q:** When a User is both the payer and a participant in their own Expense, how should their own share be handled in the balance graph?
   **A:** Their own share nets against what they paid &mdash; do not record a self-edge (a user owing themselves); only create graph edges between the payer and the OTHER participants for their respective shares.

12. **Q:** What API method would settle a debt directly between two users outside of any Expense, and what does it do to the balance graph?
   **A:** <code>settleUp(User payer, User payee, double amount)</code> &mdash; reduces the edge weight from payer to payee (or adds an offsetting payment record), recording a direct payment rather than a shared expense.

13. **Q:** Why should Group maintain its own BalanceSheet rather than computing balances by replaying all Expenses on every query?
   **A:** Replaying every expense on every balance check is O(n) per query and doesn't scale; an incrementally-updated BalanceSheet (updated once per addExpense/settleUp call) makes <code>getBalance(userA, userB)</code> O(1).

14. **Q:** What API call adds a new shared expense, and what are its key parameters?
   **A:** <code>addExpense(User payer, double amount, List&lt;User&gt; participants, SplitType type, Map&lt;User, Double&gt; splitValues)</code> &mdash; splitValues holds exact amounts or percentages depending on type (unused/null for EQUAL).

15. **Q:** Why is currency/precision handling (integer cents instead of floating-point dollars) an important edge case in Splitwise-style systems?
   **A:** Floating-point arithmetic (doubles) accumulates rounding errors across many expenses, causing balances to drift from the true total; storing amounts as integer cents (or a fixed-point Decimal type) avoids this.

16. **Q:** Java: implement the Strategy pattern with an EqualSplitStrategy that distributes a total (in cents) evenly, giving any leftover cents to the first participants.
   **A:** <pre><code>import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

interface SplitStrategy {
    Map&lt;User, Long&gt; computeSplits(long totalCents, List&lt;User&gt; participants, Map&lt;User, Long&gt; inputs);
}

class EqualSplitStrategy implements SplitStrategy {
    @Override
    public Map&lt;User, Long&gt; computeSplits(long totalCents, List&lt;User&gt; participants, Map&lt;User, Long&gt; inputs) {
        int n = participants.size();
        long base = totalCents / n;
        long remainder = totalCents % n;

        Map&lt;User, Long&gt; splits = new LinkedHashMap&lt;&gt;();
        for (int i = 0; i &lt; n; i++) {
            long share = base + (i &lt; remainder ? 1 : 0);
            splits.put(participants.get(i), share);
        }
        return splits;
    }
}</code></pre>

17. **Q:** Python: write <code>validate_exact_split(total_amount, splits)</code> that raises ValueError if the split amounts don't sum to the total (allow a small float epsilon).
   **A:** <pre><code>EPSILON = 1e-6

def validate_exact_split(total_amount: float, splits: dict) -&gt; None:
    split_sum = sum(splits.values())
    if abs(split_sum - total_amount) &gt; EPSILON:
        raise ValueError(
            f"Exact splits sum to {split_sum}, expected {total_amount}"
        )</code></pre>

18. **Q:** Java: implement <code>BalanceSheet.recordDebt(debtor, creditor, amountCents)</code> that nets a new debt against any existing opposite-direction debt between the same two users.
   **A:** <pre><code>import java.util.HashMap;
import java.util.Map;

class BalanceSheet {
    private final Map&lt;User, Map&lt;User, Long&gt;&gt; owes = new HashMap&lt;&gt;();

    public void recordDebt(User debtor, User creditor, long amountCents) {
        if (debtor.equals(creditor) || amountCents == 0) return;

        long existingReverse = owes
            .getOrDefault(creditor, Map.of())
            .getOrDefault(debtor, 0L);

        if (existingReverse &gt; 0) {
            long net = existingReverse - amountCents;
            if (net &gt;= 0) {
                owes.get(creditor).put(debtor, net);
            } else {
                owes.get(creditor).remove(debtor);
                owes.computeIfAbsent(debtor, k -&gt; new HashMap&lt;&gt;())
                    .merge(creditor, -net, Long::sum);
            }
        } else {
            owes.computeIfAbsent(debtor, k -&gt; new HashMap&lt;&gt;())
                .merge(creditor, amountCents, Long::sum);
        }
    }
}</code></pre>

19. **Q:** Python: implement a greedy <code>simplify_debts(net_balances)</code> that repeatedly matches the largest creditor with the largest debtor to minimize transactions, using heaps.
   **A:** <pre><code>import heapq

def simplify_debts(net_balances: dict) -&gt; list:
    creditors = [(-amt, user) for user, amt in net_balances.items() if amt &gt; 0]
    debtors = [(amt, user) for user, amt in net_balances.items() if amt &lt; 0]
    heapq.heapify(creditors)
    heapq.heapify(debtors)

    transactions = []
    while creditors and debtors:
        neg_credit, creditor = heapq.heappop(creditors)
        debt, debtor = heapq.heappop(debtors)
        credit = -neg_credit
        settled = min(credit, -debt)

        transactions.append((debtor, creditor, settled))

        if credit - settled &gt; 1e-9:
            heapq.heappush(creditors, (-(credit - settled), creditor))
        if -debt - settled &gt; 1e-9:
            heapq.heappush(debtors, (debt + settled, debtor))

    return transactions</code></pre>

## Cloze cards

- The {{c1::SplitType}} enum has values {{c2::EQUAL}}, {{c3::EXACT}}, and {{c4::PERCENT}}, selecting which split strategy an Expense uses.

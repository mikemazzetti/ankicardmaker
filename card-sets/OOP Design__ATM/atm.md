---
deck: "OOP Design::ATM"
topic: "ATM"
tags: [ankicardmaker, ood-atm]
note_type: Mixed (Basic / Basic (and reversed card) / Cloze)
created: 2026-09-10
---

# ATM — OOP Design

Source of truth for the `OOP Design::ATM` deck (19 notes). Edit here and re-push to update.

## Basic cards

1. **Q:** What's the core scope of a "Design an ATM" OOD problem?
   **A:** Authenticate a card + PIN, support balance inquiry/withdrawal/deposit/transfer, dispense physical cash correctly, enforce account- and machine-level limits, and talk to a remote Bank service for account data.

2. **Q:** Why is the State pattern a strong fit for ATM/session behavior, and what does its State interface typically expose?
   **A:** The ATM's allowed actions and screen prompts change entirely based on its current state (idle vs. authenticated vs. mid-withdrawal); State pattern encapsulates each state's behavior in its own class instead of one large conditional. The interface typically exposes insertCard(), enterPin(pin), selectTransaction(type), and cancel() — each concrete state implements only the transitions valid from it.

3. **Q:** Which pattern fits modeling Withdraw/Deposit/Transfer/BalanceInquiry as interchangeable operations?
   **A:** Command pattern — a Transaction interface with execute() lets Session run any transaction type polymorphically, and log/undo it uniformly.

4. **Q:** CashDispenser *(reversed — both ways)*
   **A:** The hardware component responsible for tracking available bill denominations and physically dispensing a requested amount, or reporting failure if it can't make exact change.

5. **Q:** What's the relationship between ATM, Session, and BankAccount?
   **A:** ATM creates a Session once a card + PIN are authenticated; Session references the authenticated BankAccount (fetched from Bank) and orchestrates Transactions against it. ATM itself holds no account data.

6. **Q:** Why should BankAccount balance updates happen through the remote Bank service rather than being mutated locally on the ATM?
   **A:** The account is the shared source of truth across ATMs/branches, so the ATM must call Bank.withdraw()/Bank.deposit() (likely with an idempotency key) rather than mutate a local copy, to stay consistent with other channels.

7. **Q:** What does CashDispenser.dispense(amount) need to compute internally?
   **A:** The combination of available bill denominations (e.g. a greedy or DP breakdown over $20/$50/$100) that sums exactly to the requested amount, given current denomination counts.

8. **Q:** Tricky edge case: what if the requested withdrawal amount can't be made with the ATM's current denomination inventory (e.g. $30 requested but only $50 bills remain)?
   **A:** CashDispenser.dispense() must fail explicitly (return a "cannot make exact amount" result) rather than dispensing an approximate amount, and the Transaction must not debit the account when dispensing fails.

9. **Q:** Tricky edge case: what should happen after N consecutive incorrect PIN attempts?
   **A:** The Session should transition to a BLOCKED/CARD_RETAINED state, retain or eject-and-lock the card per bank policy, and require the customer to contact the bank rather than allow further attempts.

10. **Q:** Tricky edge case: how do you avoid double-dispensing or double-debiting if the ATM crashes mid-withdrawal, after debiting the account but before dispensing cash?
   **A:** Treat withdrawal as a two-phase, idempotent operation (reserve/hold funds, dispense, then commit or roll back) backed by a transaction log, so a crash mid-flow can be reconciled instead of silently losing or duplicating money.

11. **Q:** Why keep CardReader and CashDispenser as separate classes rather than methods directly on ATM?
   **A:** Single Responsibility — each models one piece of hardware with its own state and failure modes (jammed card, out of cash); ATM just orchestrates them through the Session/State machine.

12. **Q:** Java: implement an ATMState interface and an AuthenticatedState that transitions to a transaction-in-progress state.
   **A:** <pre><code>public interface ATMState {
    void insertCard(ATMContext context, Card card);
    void enterPin(ATMContext context, String pin);
    void selectTransaction(ATMContext context, TransactionType type);
    void cancel(ATMContext context);
}

public class AuthenticatedState implements ATMState {
    @Override
    public void insertCard(ATMContext context, Card card) {
        throw new IllegalStateException("Card already inserted and authenticated");
    }

    @Override
    public void enterPin(ATMContext context, String pin) {
        throw new IllegalStateException("Already authenticated");
    }

    @Override
    public void selectTransaction(ATMContext context, TransactionType type) {
        context.setState(new TransactionInProgressState(type));
    }

    @Override
    public void cancel(ATMContext context) {
        context.endSession();
    }
}</code></pre>

13. **Q:** Python: implement CashDispenser.dispense(amount) using a greedy denomination breakdown, returning None on failure.
   **A:** <pre><code>class CashDispenser:
    def __init__(self, inventory: dict):
        # e.g. {100: 5, 50: 10, 20: 20}
        self.inventory = dict(inventory)

    def dispense(self, amount: int):
        if amount % 20 != 0:
            return None
        breakdown = {}
        remaining = amount
        for denom in sorted(self.inventory, reverse=True):
            count = min(remaining // denom, self.inventory[denom])
            if count &gt; 0:
                breakdown[denom] = count
                remaining -= denom * count
        if remaining != 0:
            return None
        for denom, count in breakdown.items():
            self.inventory[denom] -= count
        return breakdown</code></pre>

14. **Q:** Java: implement a WithdrawTransaction (Command) that checks balance and daily limit before calling CashDispenser.
   **A:** <pre><code>public class WithdrawTransaction implements Transaction {
    private final BankAccount account;
    private final CashDispenser dispenser;
    private final int amount;

    public WithdrawTransaction(BankAccount account, CashDispenser dispenser, int amount) {
        this.account = account;
        this.dispenser = dispenser;
        this.amount = amount;
    }

    @Override
    public void execute() {
        if (amount &gt; account.getBalance()) {
            throw new InsufficientFundsException();
        }
        if (amount &gt; account.getRemainingDailyLimit()) {
            throw new DailyLimitExceededException();
        }
        Map&lt;Integer, Integer&gt; cash = dispenser.dispense(amount);
        if (cash == null) {
            throw new CannotDispenseExactAmountException();
        }
        account.debit(amount);
    }
}</code></pre>

15. **Q:** Python: implement a Session class orchestrating authenticate() and execute_transaction().
   **A:** <pre><code>class Session:
    def __init__(self, bank, cash_dispenser):
        self.bank = bank
        self.cash_dispenser = cash_dispenser
        self.account = None

    def authenticate(self, card, pin):
        self.account = self.bank.verify(card, pin)
        return self.account is not None

    def execute_transaction(self, transaction):
        if self.account is None:
            raise RuntimeError("Session not authenticated")
        return transaction.execute()</code></pre>

## Cloze cards

- {{c1::ATM}}, {{c2::CardReader}}, {{c3::CashDispenser}}, and {{c4::Session}} are core hardware/session classes; {{c5::BankAccount}} and {{c6::Bank}} model the account data and the remote banking service.
- The ATM's {{c1::State}} enum typically includes {{c2::IDLE, CARD_INSERTED, PIN_ENTRY, AUTHENTICATED, TRANSACTION_IN_PROGRESS, DISPENSING_CASH}}.
- Before dispensing cash, the withdrawal Transaction must check that {{c1::the requested amount does not exceed the account's available balance}}, rejecting with an error if it does — checked before ever touching the CashDispenser.
- Withdrawal must also be checked against {{c1::a per-transaction limit and a rolling daily withdrawal limit}}, which are enforced separately from the account balance check.

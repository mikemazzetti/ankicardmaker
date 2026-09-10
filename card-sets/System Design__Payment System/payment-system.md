---
deck: "System Design::Payment System"
topic: "Payment System"
tags: [ankicardmaker, sd-payment]
note_type: Mixed (Basic / Basic (and reversed card) / Cloze)
created: 2026-09-10
---

# Payment System — System Design

Source of truth for the `System Design::Payment System` deck (22 notes). Edit here and re-push to update.

## Basic cards

1. **Q:** What are the core functional requirements of a payment system?
   **A:** Process a payment from a payer to a payee, support refunds, record transaction history, and integrate with external payment service providers (PSPs) for card/bank rails.

2. **Q:** In the CAP tradeoff, which side does the core ledger/transaction path of a payment system lean toward, and why?
   **A:** Consistency — it's better to reject or delay a payment than to risk double-charging or losing money; availability is sacrificed when necessary for correctness.

3. **Q:** If a payment system processes 10M transactions/day, what is the average TPS, and why must peak capacity be provisioned much higher?
   **A:** 10,000,000 / 86,400 ~ 116 TPS average; but payments spike heavily around sales events/paydays, so peak TPS can be 10-50x average.

4. **Q:** What HTTP endpoint pattern is typical for issuing a refund, and what must it reference?
   **A:** <pre><code>POST /v1/payments/{payment_id}/refunds</code></pre> — it must reference the original payment_id and cannot exceed the original charged amount.

5. **Q:** What is the minimum set of fields a 'Payment' record needs in the data model?
   **A:** payment_id, idempotency_key, payer_account, payee_account, amount, currency, status (pending/succeeded/failed), created_at.

6. **Q:** How does a server implement idempotency for payment requests?
   **A:** Store idempotency_key with a unique constraint mapped to the resulting payment record; on a retry with the same key, look it up and return the stored response instead of re-processing.

7. **Q:** What is the double-entry ledger principle used in payment systems?
   **A:** Every transaction is recorded as at least two balanced entries — a debit from one account and a credit to another — so the sum of all entries is always zero, making the ledger self-verifying.

8. **Q:** What is reconciliation in a payment system, and why is it needed?
   **A:** Periodically comparing internal ledger records against the external PSP's/bank's records to detect and resolve mismatches caused by network failures, partial processing, or bugs.

9. **Q:** What does PCI-DSS require, and how do most systems avoid the burden of full compliance?
   **A:** PCI-DSS mandates strict security controls for anyone storing/processing raw card data; most systems avoid this by never touching raw card numbers — they use a third-party PSP (e.g., Stripe) and store only a tokenized reference.

10. **Q:** Why can't a payment spanning multiple services (e.g., debit wallet, credit merchant, notify) use a single ACID database transaction?
   **A:** Because the services/data typically live in separate databases or microservices, so no single local transaction can span all of them atomically.

11. **Q:** What is the difference between orchestration-based and choreography-based sagas?
   **A:** Orchestration: a central coordinator explicitly tells each service what step to run next. Choreography: each service publishes events and reacts to others' events, with no central coordinator.

12. **Q:** What are the main components in a high-level payment system architecture?
   **A:** API gateway, payment orchestration service, ledger/accounting service, idempotency store, PSP integration adapter, and an async event/notification pipeline.

13. **Q:** What is the typical scaling bottleneck in a payment system's core ledger, and how is it mitigated?
   **A:** Write contention on hot account rows (e.g., a popular merchant account) under high concurrency; mitigated by sharding accounts, using optimistic concurrency control, or queuing writes per account.

## Cloze cards

- A payment system must prioritize {{c1::correctness and consistency}} above all (money must never be lost or duplicated), plus {{c2::durability of records and auditability}} for compliance.
- A payment 'charge' endpoint is typically <pre><code>POST /v1/payments
{ "idempotency_key": "...", "amount": 500, "currency": "USD", "source": "..." }</code></pre> — the client must generate the {{c1::idempotency_key}} itself before the call.
- An {{c1::idempotency key}} is a unique client-generated token attached to a payment request so that if the client retries the same request (e.g., after a timeout), the server can {{c2::detect the duplicate and return the original result instead of charging twice}}.
- True exactly-once delivery is impossible over an unreliable network; payment systems instead achieve exactly-once *effect* by combining {{c1::at-least-once delivery/retries}} with {{c1::idempotency keys}} so retries are safe.
- A payment ledger is typically {{c1::append-only / immutable}} — corrections are made by adding new reversing entries, never by editing or deleting past entries, preserving a full audit trail.
- Reconciliation usually runs as a {{c1::batch job}} that diffs internal transaction records against {{c2::PSP settlement reports/statements}}, flagging discrepancies for manual or automated resolution.
- A payment system usually doesn't move money itself; it delegates actual card/bank movement to a {{c1::Payment Service Provider (PSP)}} and stores only a {{c2::token/reference ID}} returned by the PSP instead of sensitive card data.
- The {{c1::saga pattern}} handles distributed transactions as a sequence of local transactions, each with a defined {{c2::compensating action}} that undoes its effect if a later step in the sequence fails.
- Payment systems often {{c1::acknowledge a payment as 'accepted' immediately but settle/clear funds asynchronously}}, trading a small window of uncertainty for much higher throughput and responsiveness.

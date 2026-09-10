---
deck: "Resume Prep::Serverless & Event-Driven Architecture"
topic: "Serverless & Event-Driven Architecture"
tags: [ankicardmaker, resume-prep, serverless]
note_type: Mixed (Basic / Basic (and reversed card) / Cloze)
created: 2026-09-09
---

# Serverless & Event-Driven Architecture — Resume Prep

Source of truth for the `Resume Prep::Serverless & Event-Driven Architecture` deck (15 notes). Edit here and re-push to update.

## Basic cards

1. **Q:** What is "serverless" computing?
   **A:** A cloud execution model where the provider automatically provisions, scales, and manages the compute infrastructure; you deploy code (e.g., functions) and pay only for actual execution, not for idle capacity.

2. **Q:** Name two downsides of a serverless architecture.
   **A:** Cold-start latency on infrequently-invoked functions, and vendor lock-in to the provider's runtime/services plus harder local testing and debugging.

3. **Q:** What is event-driven architecture?
   **A:** A design where components communicate by producing and reacting to events (state changes) asynchronously through an intermediary, rather than calling each other directly and synchronously.

4. **Q:** Publish/subscribe (pub/sub) pattern *(reversed — tested both ways)*
   **A:** Producers publish events to a channel (topic) without knowing who is listening; any number of subscribers independently receive their own copy of each event.

5. **Q:** What is Amazon SQS, and how does it typically deliver a message?
   **A:** A message queue service; each message is normally consumed and removed by exactly one consumer (point-to-point), which decouples producers from consumers and buffers load.

6. **Q:** What is Amazon SNS, and how does its delivery model differ from SQS?
   **A:** A pub/sub notification service that pushes ("fans out") each published message to every current subscriber (e.g., multiple SQS queues, Lambdas, emails) — unlike SQS, where one message goes to one consumer.

7. **Q:** What does "idempotency" mean for a message- or event-processing handler?
   **A:** Processing the same message more than once produces the same end result as processing it exactly once, with no duplicate side effects.

8. **Q:** Why must consumers of an SQS queue be designed to be idempotent?
   **A:** SQS guarantees at-least-once delivery, so a message can be redelivered and processed more than once (e.g., if it isn't deleted before its visibility timeout expires); idempotent handling prevents duplicate effects from that redelivery.

9. **Q:** What does "at-least-once delivery" guarantee, and what does it not guarantee?
   **A:** It guarantees a message will be delivered one or more times; it does not guarantee exactly-once delivery or strict ordering (for standard SQS queues/SNS topics).

10. **Q:** What is a Dead-Letter Queue (DLQ) used for?
   **A:** Capturing messages that repeatedly fail processing (once they exceed a max receive/retry count) so they're isolated for inspection or reprocessing instead of blocking the queue or being silently lost.

11. **Q:** Choreography (event-driven microservices) *(reversed — tested both ways)*
   **A:** A coordination style where each service reacts to events independently with no central controller — the overall workflow emerges from services publishing and subscribing to events.

12. **Q:** In orchestration (as opposed to choreography), how is a multi-step workflow coordinated?
   **A:** A central orchestrator (e.g., AWS Step Functions) explicitly invokes each service in sequence and tracks and manages the workflow's state.

13. **Q:** Why must serverless functions like AWS Lambda be written to be stateless?
   **A:** Because the platform can create, reuse, or destroy execution environments at any time and route different invocations to different instances, so anything that must persist between calls has to be stored externally (e.g., DynamoDB, S3), not in memory on the instance.

## Cloze cards

- Pros of a serverless architecture: {{c1::no server management}}, {{c2::automatic scaling}}, and {{c3::pay-per-execution billing}}.
- At BMO, redesigning legacy synchronous REST APIs into an {{c1::event-driven}} architecture (API Gateway/Lambda decoupled via async events rather than direct calls) delivered an {{c2::80%}} faster runtime.

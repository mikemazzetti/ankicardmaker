---
deck: "Resume Prep::AWS SQS, EventBridge, CodeBuild & Boto3"
topic: "AWS SQS, EventBridge, CodeBuild & Boto3"
tags: [ankicardmaker, aws-messaging-ci]
note_type: Mixed (Basic / Basic (and reversed card) / Cloze)
created: 2026-09-10
---

# AWS SQS, EventBridge, CodeBuild & Boto3 — Resume Prep

Source of truth for the `Resume Prep::AWS SQS, EventBridge, CodeBuild & Boto3` deck (20 notes). Edit here and re-push to update.

## Basic cards

1. **Q:** What AWS service is a fully managed message queue used to decouple producers and consumers?
   **A:** Amazon SQS (Simple Queue Service).

2. **Q:** What is an SQS "visibility timeout"?
   **A:** The period after a consumer receives a message during which that message is hidden from other consumers, so it isn't processed twice while being worked on. If it expires before the message is deleted, the message becomes visible again for redelivery.

3. **Q:** What is an SQS Dead-Letter Queue (DLQ) used for?
   **A:** It captures messages that repeatedly fail processing (exceed maxReceiveCount) so they can be inspected/debugged later instead of looping or being silently dropped.

4. **Q:** SQS Standard queue *(reversed — both ways)*
   **A:** At-least-once delivery, best-effort ordering, nearly unlimited throughput.

5. **Q:** SQS FIFO queue *(reversed — both ways)*
   **A:** Exactly-once processing and strict message ordering, named with a .fifo suffix, with lower throughput limits than Standard.

6. **Q:** What is SQS long polling, and why use it over short polling?
   **A:** Setting <code>WaitTimeSeconds &gt; 0</code> on <code>ReceiveMessage</code> so the call waits for a message to arrive instead of returning empty immediately — reduces empty responses, API calls, and cost.

7. **Q:** Write a boto3 snippet that sends a message to an SQS queue.
   **A:** <pre><code>import boto3

sqs = boto3.client("sqs")
sqs.send_message(
    QueueUrl="https://sqs.us-east-1.amazonaws.com/123456789/orders",
    MessageBody="order-42 ready for processing"
)</code></pre>

8. **Q:** In BMO's modernization of 30+ legacy APIs, what role did SQS play in the new architecture?
   **A:** It decoupled the modernized, serverless event-driven APIs (Lambda, API Gateway, DynamoDB, CloudWatch) — buffering requests between components so producers and consumers didn't need to process synchronously in lockstep.

9. **Q:** What is Amazon EventBridge?
   **A:** A serverless event bus that routes events between AWS services, SaaS apps, and your own applications based on rules.

10. **Q:** Which two AWS services did BMO combine to architect the serverless event-driven backend that decoupled loan-submission logic from third-party credit checks?
   **A:** AWS Lambda + EventBridge.

11. **Q:** Why choose EventBridge over a plain SQS queue for routing an event to multiple different downstream consumers?
   **A:** EventBridge does content-based pattern matching and can fan an event out to many different target types at once; SQS is a single point-to-point queue consumed by one logical consumer group.

12. **Q:** What's the key architectural difference between EventBridge and SNS?
   **A:** EventBridge does rich, content-based event pattern filtering across many-to-many sources and targets (with a schema registry); SNS is simpler pub/sub topic fan-out to subscribers.

13. **Q:** What file defines the build commands (install, build, etc.) for an AWS CodeBuild project?
   **A:** buildspec.yml.

14. **Q:** List buildspec.yml's phases in execution order.
   **A:** <pre><code>install
pre_build
build
post_build</code></pre>

15. **Q:** How did BMO use AWS CodeBuild to improve build/deploy quality, and with what results?
   **A:** Ran custom Python linting/static-analysis scripts for C++ and Node.js as part of the CodeBuild pipeline, yielding 30% faster builds and 20% fewer pre-deploy defects.

16. **Q:** What is Boto3?
   **A:** The official AWS SDK for Python — lets code create, configure, and manage AWS services (S3, SQS, Lambda, DynamoDB, etc.) programmatically.

17. **Q:** In boto3, what's the difference between a client and a resource?
   **A:** A client is a low-level interface that maps 1:1 to the AWS service API (you pass raw parameters). A resource is a higher-level, object-oriented abstraction built on top of a client.

18. **Q:** What boto3 object manages credentials, region, and configuration for the API calls you make?
   **A:** <code>boto3.Session</code> — clients/resources are created from a session (or a default session if you don't create one explicitly).

19. **Q:** How does boto3 let you iterate through a multi-page (paginated) API response, e.g. listing thousands of S3 objects?
   **A:** Use a paginator: <code>paginator = client.get_paginator('list_objects_v2')</code>, then iterate <code>paginator.paginate(...)</code> — it handles the continuation tokens automatically.

## Cloze cards

- EventBridge {{c1::rules}} match event patterns and route matching events to one or more {{c2::targets}} (e.g. Lambda functions, SQS queues, Step Functions).

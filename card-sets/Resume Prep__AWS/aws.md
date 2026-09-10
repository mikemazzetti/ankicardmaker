---
deck: "Resume Prep::AWS"
topic: "AWS"
tags: [ankicardmaker, resume-prep, aws]
note_type: Mixed (Basic / Basic (and reversed card) / Cloze)
created: 2026-09-09
---

# AWS — Resume Prep

Source of truth for the `Resume Prep::AWS` deck (22 notes). Edit here and re-push to update.

## Basic cards

1. **Q:** Which four AWS services did you use at BMO to modernize 20+ legacy APIs into a serverless, event-driven architecture?
   **A:** AWS Lambda, API Gateway, DynamoDB, and CloudWatch.

2. **Q:** What is an Amazon S3 bucket?
   **A:** A container for objects (data + metadata) in S3. Bucket names must be globally unique across all of AWS, and each bucket lives in one specific region.

3. **Q:** What read consistency model does Amazon S3 provide for all requests (since Dec 2020)?
   **A:** Strong read-after-write consistency for all GET, PUT, and LIST operations, including overwrite PUTs and DELETEs.

4. **Q:** What is a Lambda "cold start"?
   **A:** The extra latency when Lambda must provision a brand-new execution environment (download code, boot the runtime, run init code) before handling an invocation, instead of reusing an already-warm environment.

5. **Q:** Lambda Provisioned Concurrency *(reversed — tested both ways)*
   **A:** A setting that keeps a specified number of Lambda execution environments initialized and ready in advance, so those invocations skip cold starts entirely — the main mitigation for cold-start latency, alongside shrinking the deployment package and avoiding heavy init-time work.

6. **Q:** What does setting "reserved concurrency" on a Lambda function do?
   **A:** It caps the maximum number of concurrent executions that function may use, guaranteeing that capacity for it while throttling any invocations above that ceiling.

7. **Q:** What is the maximum execution timeout you can configure for an AWS Lambda function?
   **A:** 15 minutes.

8. **Q:** Name common event sources that can trigger an AWS Lambda function.
   **A:** API Gateway requests, S3 object events, DynamoDB Streams, SQS queues, SNS topics, EventBridge rules, and scheduled (cron) rules.

9. **Q:** In DynamoDB, what does the partition key determine?
   **A:** It is hashed to decide which physical partition the item is stored on; it's the required part of the primary key used to route every read/write.

10. **Q:** In a DynamoDB table with a composite primary key, what does the sort key let you do?
   **A:** Store and query multiple items that share the same partition key, uniquely ordered/identified by the sort key (e.g., all orders for one customer, sorted by date).

11. **Q:** What is "single-table design" in DynamoDB?
   **A:** Modeling multiple different entity types in one DynamoDB table using generic/overloaded partition and sort key attributes, so most access patterns are satisfied with a single request, unlike a relational schema's one-table-per-entity approach.

12. **Q:** Why might you choose an eventually consistent read instead of a strongly consistent read in DynamoDB?
   **A:** It costs half the RCUs and gives lower latency/higher throughput; use it when the app can tolerate reading data that might be a moment stale right after a write.

13. **Q:** What's the main practical difference between an API Gateway REST API and an HTTP API?
   **A:** HTTP APIs are lower-latency and cheaper but support a smaller feature set (fewer integration types, no built-in usage plans/API keys, no WAF); REST APIs support the full feature set, including request validation, response caching, WAF, and usage plans.

14. **Q:** In API Gateway's Lambda proxy integration, what is the Lambda function itself responsible for that a non-proxy integration would otherwise handle?
   **A:** Parsing the raw incoming HTTP request and returning a specifically-shaped response object (statusCode, headers, body) — API Gateway performs no request/response mapping for you.

15. **Q:** How does API Gateway enforce request throttling by default?
   **A:** A token-bucket algorithm applied at the account/stage level with a steady-state rate limit and a burst limit; requests beyond that receive an HTTP 429 Too Many Requests response.

16. **Q:** What's the difference between what CloudWatch Logs and CloudWatch Metrics store?
   **A:** Logs store raw, timestamped text log events (e.g., a Lambda function's console output); Metrics store numeric time-series data (e.g., invocation count, duration, error count) used for dashboards and alarms.

17. **Q:** What does a CloudWatch Alarm do when its watched metric crosses the configured threshold for the set number of evaluation periods?
   **A:** It changes state (e.g., OK -&gt; ALARM) and can trigger an action, such as publishing to an SNS topic or invoking an Auto Scaling policy.

18. **Q:** IAM Role *(reversed — tested both ways)*
   **A:** An AWS identity with attached permission policies that can be temporarily assumed by a trusted user, service, or account, instead of using long-lived credentials — e.g., a Lambda function's execution role.

## Cloze cards

- At BMO, modernizing 20+ legacy APIs into a serverless, event-driven architecture (Lambda + API Gateway + DynamoDB) achieved a {{c1::80%}} faster runtime.
- Ordering common S3 storage classes from hottest/most expensive to coldest/cheapest: {{c1::S3 Standard}} -&gt; {{c2::S3 Standard-IA}} -&gt; {{c3::S3 Glacier Instant Retrieval}} -&gt; {{c4::S3 Glacier Deep Archive}}. <!-- Back Extra: IA = Infrequent Access. Deep Archive restores can take hours. -->
- In DynamoDB provisioned mode, one {{c1::Read Capacity Unit (RCU)}} provides one strongly consistent read per second for an item up to 4 KB, and one {{c2::Write Capacity Unit (WCU)}} provides one write per second for an item up to 1 KB. <!-- Back Extra: An eventually consistent read costs half an RCU. -->
- In DynamoDB, a {{c1::Global Secondary Index (GSI)}} can use a different partition/sort key than the base table and supports only eventually consistent reads, while a {{c2::Local Secondary Index (LSI)}} shares the base table's partition key, must be created at table-creation time, and supports strongly consistent reads.

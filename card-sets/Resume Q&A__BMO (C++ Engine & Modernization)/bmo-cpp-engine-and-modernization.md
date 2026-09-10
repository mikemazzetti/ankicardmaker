---
deck: "Resume Q&A::BMO (C++ Engine & Modernization)"
topic: "BMO (C++ Engine & Modernization)"
tags: [ankicardmaker, resume-bmo-2]
note_type: Mixed (Basic / Basic (and reversed card) / Cloze)
created: 2026-09-10
---

# BMO (C++ Engine & Modernization) — Resume Q&A

Source of truth for the `Resume Q&A::BMO (C++ Engine & Modernization)` deck (20 notes). Edit here and re-push to update.

## Basic cards

1. **Q:** What language was the high-throughput financial calculation engine written in during the May–Aug 2026 BMO internship?
   **A:** <code>C++20</code>

2. **Q:** What technology exposed the C++20 calculation engine to Python callers?
   **A:** <code>pybind11</code> bindings.

3. **Q:** How many legacy APIs did Michele modernize during the May–Aug 2026 internship?
   **A:** <b>30+</b> legacy APIs.

4. **Q:** What AWS service did Michele use for queuing/decoupling in the API modernization work?
   **A:** <code>AWS SQS</code>

5. **Q:** What did Michele build custom Python linting/static-analysis scripts to check?
   **A:** <b>C++ and Node.js</b> code.

6. **Q:** Where did the custom Python linting/static-analysis scripts run in the CI pipeline?
   **A:** On <b>AWS CodeBuild</b>.

7. **Q:** What build-speed improvement came from the custom linting/static-analysis tooling?
   **A:** <b>30% faster</b> builds.

8. **Q:** What defect-reduction resulted from the custom linting/static-analysis tooling?
   **A:** <b>20% fewer</b> pre-deploy defects.

9. **Q:** What tool did Michele build to search/filter CloudWatch logs?
   **A:** A <b>Python CLI tool</b>.

10. **Q:** What speed improvement did the Python CloudWatch-log CLI tool achieve?
   **A:** <b>40% faster</b> log retrieval.

11. **Q:** What is Michele's current title at BMO (Sep 2026–present)?
   **A:** <b>Junior Software Developer</b>.

12. **Q:** What BMO strategic initiative is Michele's Junior Developer work part of?
   **A:** <b>Ambition 2030</b>.

13. **Q:** How many branch locations does the core branch software Michele modernizes as a Junior Developer support?
   **A:** <b>1,800+</b> locations.

14. **Q:** What three languages does Michele use day-to-day as a Junior Software Developer at BMO?
   **A:** <code>Node.js</code>, <code>Python</code>, and <code>C++</code> (on AWS).

15. **Q:** What is the stated technical focus of Michele's Junior Developer role?
   **A:** <b>AI-Driven Development</b>.

16. **Q:** Interview prompt: "Tell me about a performance problem you solved."
   **A:** <b>S:</b> BMO's transaction batch-processing pipeline handled 2.5M+ account records per day and latency was a bottleneck.<br><b>T:</b> Speed up the core calculation logic without breaking existing Python-based integrations.<br><b>A:</b> Rewrote the hot path as a C++20 financial calculation engine and exposed it to the rest of the system via pybind11 bindings.<br><b>R:</b> Cut batch-processing latency by 42% at that 2.5M+ record/day scale.

17. **Q:** Interview prompt: "Describe a large-scale modernization effort you contributed to."
   **A:** <b>S:</b> BMO had 30+ legacy APIs on older, tightly-coupled infrastructure.<br><b>T:</b> Modernize them to a scalable, maintainable architecture.<br><b>A:</b> Migrated the APIs to serverless, event-driven services built on AWS Lambda, API Gateway, DynamoDB, CloudWatch, and SQS.<br><b>R:</b> 30+ APIs now run on serverless infrastructure, improving scalability and observability.

18. **Q:** Interview prompt: "Tell me about a tool you built to improve developer productivity."
   **A:** <b>S:</b> Engineers needed to manually dig through CloudWatch logs and pre-deploy code review was slow/inconsistent.<br><b>T:</b> Build tooling to speed up both log investigation and code quality checks.<br><b>A:</b> Built a Python CLI to search/filter CloudWatch logs, and custom Python linting/static-analysis scripts for C++ and Node.js running on AWS CodeBuild.<br><b>R:</b> 40% faster log retrieval; 30% faster builds and 20% fewer pre-deploy defects from the linting tooling.

## Cloze cards

- Michele engineered a high-throughput financial calculation engine in {{c1::C++20}} with {{c2::Python (pybind11)}} bindings, cutting batch-processing latency {{c3::42%}} across {{c4::2.5M+}} daily account records.
- The legacy APIs were modernized into serverless, event-driven architectures using {{c1::AWS Lambda}}, {{c2::API Gateway}}, {{c3::DynamoDB}}, {{c4::CloudWatch}}, and {{c5::AWS SQS}}.

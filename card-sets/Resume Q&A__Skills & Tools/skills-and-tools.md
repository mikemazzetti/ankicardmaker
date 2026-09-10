---
deck: "Resume Q&A::Skills & Tools"
topic: "Skills & Tools"
tags: [ankicardmaker, resume-skills]
note_type: Mixed (Basic / Basic (and reversed card) / Cloze)
created: 2026-09-10
---

# Skills & Tools — Resume Q&A

Source of truth for the `Resume Q&A::Skills & Tools` deck (22 notes). Edit here and re-push to update.

## Basic cards

1. **Q:** What Python library does Michele use for AWS scripting/automation?
   **A:** Boto3

2. **Q:** What tool does Michele use for API testing?
   **A:** Postman

3. **Q:** Which experience used C++20 for a high-throughput system?
   **A:** BMO Software Engineer Intern (May-Aug 2026) - financial calculation engine in C++20 with Python (pybind11) bindings.

4. **Q:** Which experiences used Python?
   **A:** BMO Junior SWE (Node.js/Python/C++ on AWS); BMO SWE Intern May-Aug 2026 (pybind11 bindings, linting scripts, CloudWatch CLI tool); BMO SWE Intern Jan-Apr 2026 (FastAPI SDLC PoC); COMPLIANCE360 (MS Fabric ETL pipeline); BUFFET (NLP trading pipeline).

5. **Q:** Which experiences used AWS?
   **A:** BMO Junior SWE; BMO SWE Intern May-Aug 2026 (Lambda, API Gateway, DynamoDB, CloudWatch, SQS, CodeBuild); BMO SWE Intern Jan-Apr 2026 (Angular/Node.js on AWS, Lambda + EventBridge, DynamoDB).

6. **Q:** Which experiences used Spring Boot?
   **A:** ServiceOntario SWE Intern (Spring Boot + React) and Government of Ontario SWE Intern (Java + Spring Boot eForm backend).

7. **Q:** Which experiences used React?
   **A:** ServiceOntario SWE Intern (Spring Boot + React) and BMO SWE Intern Jan-Apr 2026 (owned migration to a React SPA).

8. **Q:** Which experiences involved LLMs/NLP?
   **A:** WesternAI's TruthLens (RoBERTa fine-tuning, RAG, SHAP); BMO SWE Intern Jan-Apr 2026 (specialized LLM agents per SDLC phase); BUFFET (VADER-based NLP trading pipeline).

9. **Q:** Which experiences used serverless/event-driven architecture?
   **A:** BMO SWE Intern May-Aug 2026 (30+ legacy APIs modernized to serverless/event-driven: Lambda, API Gateway, DynamoDB, CloudWatch, SQS) and BMO SWE Intern Jan-Apr 2026 (serverless event-driven backend with Lambda + EventBridge).

10. **Q:** Judgment: which caching tool would you pick to cut upstream calls in a circuit-breaker-protected service, and why?
   **A:** Caffeine - Michele paired it with Resilience4j circuit breakers at the Government of Ontario, cutting ~25% of upstream calls.

11. **Q:** Judgment: between PostgreSQL and DynamoDB, which would you pick for a high-throughput, access-pattern-driven workload, and why?
   **A:** DynamoDB - Michele designed a DynamoDB schema at BMO (Jan-Apr 2026) that cut processing time 60%; PostgreSQL better fits relational, query-heavy needs.

12. **Q:** Judgment: which techniques would you reach for to fix N+1 query latency in a relational database, and why?
   **A:** JPQL JOIN FETCH plus tuned Hibernate batch sizes - exactly what Michele used at ServiceOntario to cut read latency 40%.

13. **Q:** Judgment: which approach would you pick for a CPU-bound, high-throughput engine that still needs Python interop, and why?
   **A:** Write the core in C++20 and expose it to Python via pybind11 bindings - Michele's approach at BMO cut batch-processing latency 42% across 2.5M+ daily records.

## Cloze cards

- Michele's core languages include {{c1::Java}}, {{c2::C#}}, {{c3::C++}}, and {{c4::Python}}.
- Michele's core languages also include {{c1::JavaScript}}, {{c2::TypeScript}}, {{c3::HTML/CSS}}, and {{c4::SQL}}.
- Backend frameworks Michele has used include {{c1::Spring Boot}}, {{c2::Hibernate}}, {{c3::FastAPI}}, and {{c4::Express}}.
- Full-stack/frontend frameworks Michele has used include {{c1::React}}, {{c2::Angular}}, and {{c3::Node.js}}.
- Data/ML frameworks Michele has used include {{c1::TensorFlow}}, {{c2::PySpark}}, and {{c3::Pandas}}.
- Michele's cloud/DevOps toolkit includes {{c1::Docker}}, {{c2::Kubernetes}}, {{c3::PostgreSQL}}, {{c4::MongoDB}}, and {{c5::Redis}}.
- The AWS services Michele lists are {{c1::S3}}, {{c2::Lambda}}, {{c3::DynamoDB}}, and {{c4::CloudWatch}}.
- Michele's testing frameworks include {{c1::JUnit}}, {{c2::Mockito}}, {{c3::Pytest}}, and {{c4::Jest}}.
- Michele's build/CI tools include {{c1::CMake}}, {{c2::Maven}}, {{c3::Jenkins}}, and {{c4::Azure DevOps}}.

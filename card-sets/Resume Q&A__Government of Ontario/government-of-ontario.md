---
deck: "Resume Q&A::Government of Ontario"
topic: "Government of Ontario"
tags: [ankicardmaker, resume-gov-ontario]
note_type: Mixed (Basic / Basic (and reversed card) / Cloze)
created: 2026-09-10
---

# Government of Ontario — Resume Q&A

Source of truth for the `Resume Q&A::Government of Ontario` deck (20 notes). Edit here and re-push to update.

## Basic cards

1. **Q:** What was Michele's role and employer for the May–Aug 2025 internship?
   **A:** <b>Software Engineering Intern at the Government of Ontario</b>.

2. **Q:** What platform did Michele build eForm back-end architecture for?
   **A:** The <b>Business Experience Platform</b>.

3. **Q:** What stack was the eForm back-end built with?
   **A:** <code>Java</code> + <code>Spring Boot</code>

4. **Q:** How much data did the Business Experience Platform's eForm back-end handle daily?
   **A:** <b>10GB+ per day</b>.

5. **Q:** How many businesses did the Business Experience Platform serve?
   **A:** <b>400,000+</b> businesses.

6. **Q:** What did Michele build to handle high-throughput input validation on the Business Experience Platform?
   **A:** A <b>validation microservice</b>.

7. **Q:** What Spring feature enabled non-blocking I/O in the validation microservice?
   **A:** <code>Spring @Async</code>

8. **Q:** What latency improvement did the @Async validation microservice achieve?
   **A:** <b>40% lower</b> latency.

9. **Q:** What resilience library did Michele use to add circuit breakers?
   **A:** <code>Resilience4j</code>

10. **Q:** What caching library did Michele pair with Resilience4j?
   **A:** <code>Caffeine</code>

11. **Q:** What reduction in upstream calls did Resilience4j + Caffeine caching achieve?
   **A:** <b>~25% fewer</b> upstream calls.

12. **Q:** Circuit breaker (Resilience4j) *(reversed — both ways)*
   **A:** A resilience pattern that stops calling a failing or slow upstream service once a failure threshold is hit, failing fast locally instead of letting the failure cascade.

13. **Q:** Caffeine cache *(reversed — both ways)*
   **A:** A high-performance in-memory Java caching library, used here to serve repeated lookups locally and reduce redundant upstream calls.

14. **Q:** Why use Spring @Async instead of a blocking call in the validation microservice?
   **A:** It frees up request-handling threads while waiting on I/O, so more validation requests can be in flight concurrently — improving throughput and latency under load.

15. **Q:** What does the eForm back-end handle within the Business Experience Platform?
   **A:** The <b>form submission/processing architecture</b> businesses use on the platform (10GB+/day across 400,000+ businesses).

16. **Q:** Interview prompt: "Tell me about a time you made a system more resilient to upstream failures."
   **A:** <b>S:</b> The Business Experience Platform's validation microservice depended on upstream services that could be slow or fail.<br><b>T:</b> Reduce load on and exposure to those upstream dependencies.<br><b>A:</b> Added Resilience4j circuit breakers to fail fast on unhealthy upstreams, plus Caffeine in-memory caching to avoid redundant calls.<br><b>R:</b> Cut upstream calls by ~25%.

17. **Q:** Interview prompt: "Tell me about optimizing a high-throughput backend service."
   **A:** <b>S:</b> The validation microservice on the Business Experience Platform needed to handle input validation for a high volume of business submissions.<br><b>T:</b> Reduce request latency without blocking server threads.<br><b>A:</b> Rebuilt the validation path using Spring @Async for non-blocking I/O.<br><b>R:</b> Achieved 40% lower latency.

18. **Q:** Interview prompt: "Describe a backend system you built that handled real scale."
   **A:** <b>S:</b> The Government of Ontario needed eForm back-end architecture for the Business Experience Platform.<br><b>T:</b> Design and build it to handle high daily volume across many businesses.<br><b>A:</b> Built the back-end in Java + Spring Boot, plus an @Async validation microservice and Resilience4j/Caffeine for resilience and efficiency.<br><b>R:</b> The platform handled 10GB+/day for 400,000+ businesses, with 40% lower validation latency and ~25% fewer upstream calls.

## Cloze cards

- Michele built the eForm back-end for the Business Experience Platform in {{c1::Java + Spring Boot}}, handling {{c2::10GB+/day}} for {{c3::400,000+}} businesses.
- Michele added {{c1::Resilience4j}} circuit breakers plus {{c2::Caffeine}} caching, cutting upstream calls by {{c3::~25%}}.

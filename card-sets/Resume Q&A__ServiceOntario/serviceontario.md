---
deck: "Resume Q&A::ServiceOntario"
topic: "ServiceOntario"
tags: [ankicardmaker, resume-serviceontario]
note_type: Mixed (Basic / Basic (and reversed card) / Cloze)
created: 2026-09-10
---

# ServiceOntario — Resume Q&A

Source of truth for the `Resume Q&A::ServiceOntario` deck (19 notes). Edit here and re-push to update.

## Basic cards

1. **Q:** What was Michele's role and employer for the Sep–Dec 2025 internship?
   **A:** <b>Software Engineering Intern at ServiceOntario</b>.

2. **Q:** What backend framework powered ServiceOntario's compliance workflows?
   **A:** <code>Spring Boot</code>

3. **Q:** What frontend framework was paired with Spring Boot at ServiceOntario?
   **A:** <code>React</code>

4. **Q:** How many residents did the ServiceOntario compliance workflows serve?
   **A:** <b>15M+</b> residents.

5. **Q:** What class of performance bug did Michele fix in ServiceOntario's compliance workflows?
   **A:** An <b>N+1 query bottleneck</b>.

6. **Q:** What JPQL technique did Michele use to fix the N+1 problem at ServiceOntario?
   **A:** <code>JOIN FETCH</code>

7. **Q:** What other Hibernate-level tuning did Michele apply alongside JOIN FETCH?
   **A:** Tuned <b>Hibernate batch sizes</b>.

8. **Q:** What read-latency improvement resulted from the N+1 fix at ServiceOntario?
   **A:** <b>40% lower</b> read latency.

9. **Q:** What accessibility standard did Michele's UI library comply with at ServiceOntario?
   **A:** <b>WCAG 2.1</b>.

10. **Q:** What language was the WCAG 2.1-compliant UI library built in?
   **A:** <code>TypeScript</code>

11. **Q:** What development-speed benefit did the TypeScript UI library provide?
   **A:** <b>30% faster</b> frontend development cycles.

12. **Q:** N+1 query problem *(reversed — both ways)*
   **A:** A performance bug where fetching a list of N records triggers one additional query per record (N extra queries) instead of a single batched/joined query.

13. **Q:** JOIN FETCH (JPQL) *(reversed — both ways)*
   **A:** A JPQL clause that eagerly loads an associated entity or collection within the same query, avoiding the extra per-row queries that cause N+1 problems.

14. **Q:** Why does tuning Hibernate batch size help alongside JOIN FETCH?
   **A:** It groups remaining lazy-load queries into fewer batched round-trips to the database, reducing overhead JOIN FETCH alone doesn't eliminate.

15. **Q:** Why build a reusable WCAG 2.1 TypeScript component library instead of styling each page individually?
   **A:** It centralizes accessible, typed components so every new screen reuses tested, compliant building blocks instead of re-implementing accessibility per page — which is what drove the 30% faster frontend cycles.

16. **Q:** Interview prompt: "Tell me about a performance problem you diagnosed and fixed."
   **A:** <b>S:</b> ServiceOntario's Spring Boot + React compliance workflows, used by 15M+ residents, had slow read paths.<br><b>T:</b> Find and fix the root cause of the read-latency issue.<br><b>A:</b> Diagnosed an N+1 query bottleneck, fixed it with JPQL JOIN FETCH to eagerly load associations in one query, and tuned Hibernate batch sizes for remaining lazy loads.<br><b>R:</b> Read latency dropped 40%.

17. **Q:** Interview prompt: "Tell me about a time you improved accessibility in a product."
   **A:** <b>S:</b> ServiceOntario's frontend needed to meet public-sector accessibility requirements while shipping features quickly.<br><b>T:</b> Provide reusable, compliant UI building blocks for the team.<br><b>A:</b> Built a WCAG 2.1-compliant TypeScript UI component library.<br><b>R:</b> Frontend development cycles got 30% faster since teams reused accessible components instead of building them from scratch.

18. **Q:** Interview prompt: "Walk me through a full-stack project you worked on at scale."
   **A:** <b>S:</b> ServiceOntario needed compliance workflows serving 15M+ residents.<br><b>T:</b> Contribute full-stack, from backend performance to frontend accessibility.<br><b>A:</b> Worked across a Spring Boot + React stack — fixed an N+1 bottleneck with JOIN FETCH and Hibernate batch tuning, and built a WCAG 2.1 TypeScript UI library.<br><b>R:</b> 40% lower read latency and 30% faster frontend cycles, on a system serving 15M+ residents.

## Cloze cards

- At ServiceOntario, Michele fixed N+1 query bottlenecks using JPQL {{c1::JOIN FETCH}} and tuned {{c2::Hibernate batch sizes}}, achieving {{c3::40%}} lower read latency.

---
deck: "Resume Q&A::Behavioral & STAR"
topic: "Behavioral & STAR"
tags: [ankicardmaker, resume-behavioral]
note_type: Mixed (Basic / Basic (and reversed card) / Cloze)
created: 2026-09-10
---

# Behavioral & STAR — Resume Q&A

Source of truth for the `Resume Q&A::Behavioral & STAR` deck (20 notes). Edit here and re-push to update.

## Basic cards

1. **Q:** For 'tell me about your biggest technical challenge,' which project fits best?
   **A:** The C++20 high-throughput financial calculation engine at BMO (Software Engineer Intern, May-Aug 2026).

2. **Q:** STAR - Situation/Task: what was the challenge with the calculation engine?
   **A:** Cut transaction batch-processing latency across 2.5M+ daily account records while keeping Python interoperability via pybind11.

3. **Q:** STAR - Action: what did Michele build to solve the calculation-engine challenge?
   **A:** Engineered the core engine in C++20 for raw performance and exposed it to Python through pybind11 bindings.

4. **Q:** STAR - Result: what was the measured outcome of the calculation-engine work?
   **A:** 42% reduction in transaction batch-processing latency across 2.5M+ daily account records.

5. **Q:** For 'tell me about a time you improved performance' (a story distinct from the C++ engine), which project fits?
   **A:** Fixing N+1 query bottlenecks at ServiceOntario.

6. **Q:** STAR - Situation: what performance problem existed at ServiceOntario?
   **A:** N+1 query bottlenecks were slowing read performance in full-stack compliance workflows serving 15M+ residents.

7. **Q:** STAR - Action: how did Michele fix the N+1 bottleneck at ServiceOntario?
   **A:** Used JPQL JOIN FETCH and tuned Hibernate batch sizes.

8. **Q:** STAR - Result: what latency improvement came from the N+1 fix?
   **A:** 40% lower read latency.

9. **Q:** For 'tell me about a time you learned something quickly,' which project fits?
   **A:** TruthLens at WesternAI - fine-tuning RoBERTa and building a RAG architecture with SHAP.

10. **Q:** STAR - Action: what new technique did Michele pick up quickly for TruthLens?
   **A:** Fine-tuning a RoBERTa transformer model and implementing a RAG (retrieval-augmented generation) pipeline with SHAP for explainable counter-evidence retrieval.

11. **Q:** STAR - Result: how accurate was the TruthLens misinformation classifier?
   **A:** 93% accuracy on real-time misinformation classification.

12. **Q:** For 'tell me about a time you led a team,' which résumé roles can Michele draw on?
   **A:** Develop for Good Site Technical Lead, WesternAI ML Developer, and leading the AI-driven SDLC PoC at BMO.

13. **Q:** STAR - what did Michele lead as Develop for Good Site Technical Lead?
   **A:** The engineering team for nonprofit LiberArte's website redesign, coordinating with management, design, and client teams to ship a responsive, accessibility-friendly site.

14. **Q:** STAR - what leadership did the AI-SDLC PoC at BMO involve?
   **A:** Led the effort to build specialized LLM agents per SDLC phase (Python + FastAPI), then presented the PoC to Directors.

15. **Q:** For 'tell me about a time you dealt with ambiguity,' which project fits?
   **A:** COMPLIANCE360 - built during the OPS Hackathon 2025, an open-ended problem to investigate Ontario business records.

16. **Q:** STAR - Action/Result: what did Michele build for COMPLIANCE360 under ambiguity, and how did it turn out?
   **A:** Built an ETL pipeline on MS Fabric in Python plus scoring algorithms to investigate business records - the team won the hackathon.

17. **Q:** For 'tell me about a high-impact project,' which experience has the widest reach, and what are the key numbers?
   **A:** BMO's Ambition 2030 modernization - technical delivery across 1,800+ branch locations; also notable: ServiceOntario (15M+ residents) and the Government of Ontario eForm platform (400,000+ businesses).

18. **Q:** For 'tell me about explaining technical work to non-technical stakeholders,' which project fits?
   **A:** The AI-driven SDLC pipeline PoC (Python + FastAPI, LLM agents per phase) that Michele presented to Directors at BMO.

19. **Q:** For 'tell me about building for resilience/reliability,' which project fits, and what was the result?
   **A:** The eForm validation microservice at the Government of Ontario - Resilience4j circuit breakers + Caffeine caching, cutting ~25% of upstream calls and preventing cascading failures.

20. **Q:** For 'tell me about a failure or what you'd do differently,' how should Michele answer using only résumé facts?
   **A:** The résumé lists no explicit failure - instead, frame a 'gap I closed': before Michele built Python linting/static-analysis scripts at BMO, builds were slower with more pre-deploy defects; naming that gap and the fix (30% faster builds, 20% fewer defects) shows self-critical improvement without inventing a failure.

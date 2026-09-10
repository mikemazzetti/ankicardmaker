---
deck: "Resume Q&A::BMO (Calculator & AI-SDLC)"
topic: "BMO (Calculator & AI-SDLC)"
tags: [ankicardmaker, resume-bmo-1]
note_type: Mixed (Basic / Basic (and reversed card) / Cloze)
created: 2026-09-10
---

# BMO (Calculator & AI-SDLC) — Resume Q&A

Source of truth for the `Resume Q&A::BMO (Calculator & AI-SDLC)` deck (20 notes). Edit here and re-push to update.

## Basic cards

1. **Q:** During the Jan–Apr 2026 BMO internship, what end-to-end web app did Michele build?
   **A:** A <b>Mortgage &amp; Loan Calculator</b> web application.

2. **Q:** What frontend framework did Michele use for the Mortgage &amp; Loan Calculator?
   **A:** <code>Angular</code>

3. **Q:** What language did Michele write the Mortgage &amp; Loan Calculator's frontend in?
   **A:** <code>TypeScript</code>

4. **Q:** What backend runtime powered the Mortgage &amp; Loan Calculator, and where did it run?
   **A:** <code>Node.js</code>, deployed on <b>AWS</b>.

5. **Q:** What AI-focused initiative did Michele lead during the Jan–Apr 2026 internship?
   **A:** An <b>AI-driven SDLC pipeline proof-of-concept (PoC)</b>.

6. **Q:** What tech stack was the AI-driven SDLC PoC built with?
   **A:** <code>Python</code> + <code>FastAPI</code>

7. **Q:** In the AI-driven SDLC PoC, how were the LLM agents organized?
   **A:** As <b>specialized LLM agents, one per project phase</b> of the SDLC.

8. **Q:** Who did Michele present the AI-driven SDLC pipeline PoC to?
   **A:** <b>Directors</b> at BMO.

9. **Q:** What backend architecture did Michele design to decouple loan submission from credit checks?
   **A:** A <b>serverless, event-driven backend</b> using <code>AWS Lambda</code> + <code>EventBridge</code>.

10. **Q:** By how much did the Lambda + EventBridge redesign reduce coupling between submission logic and credit checks?
   **A:** <b>40%</b> less coupling.

11. **Q:** What failure mode did the Lambda + EventBridge decoupling prevent?
   **A:** <b>Cascading failures</b> — a slow/failing third-party credit check could no longer take down loan submission.

12. **Q:** What frontend architecture did Michele migrate the loan/mortgage app to?
   **A:** A <b>React single-page application (SPA)</b>.

13. **Q:** What database schema did Michele design as part of the React SPA migration?
   **A:** A <b>DynamoDB</b> schema.

14. **Q:** What processing-speed improvement resulted from the React SPA + DynamoDB migration?
   **A:** <b>60% faster</b> processing.

15. **Q:** EventBridge (in the BMO Lambda backend) *(reversed — both ways)*
   **A:** An AWS event bus service used to route events between decoupled services (e.g. loan submission → credit check) instead of direct synchronous calls.

16. **Q:** Interview prompt: "Walk me through a time you improved a system's resilience to a third-party dependency."
   **A:** <b>S:</b> BMO's loan/mortgage submission flow called a third-party credit-check service directly, so a slow or failing check could cascade into submission failures.<br><b>T:</b> Decouple submission from the credit-check dependency so one failure mode couldn't take down the other.<br><b>A:</b> Architected a serverless event-driven backend using AWS Lambda + EventBridge — submission logic published events instead of calling the credit-check service synchronously.<br><b>R:</b> Reduced coupling by 40% and eliminated cascading failures between the two systems.

17. **Q:** Interview prompt: "Tell me about a time you presented technical work to senior leadership."
   **A:** <b>S:</b> During the Jan–Apr 2026 BMO internship, leadership was exploring how AI could speed up the software development lifecycle.<br><b>T:</b> Lead a proof-of-concept demonstrating an AI-driven SDLC pipeline.<br><b>A:</b> Built the PoC in Python + FastAPI, implementing specialized LLM agents assigned to different phases of the SDLC.<br><b>R:</b> Presented the working PoC directly to Directors, demonstrating a viable AI-assisted development workflow.

18. **Q:** Interview prompt: "Describe a full-stack feature you owned end to end."
   **A:** <b>S:</b> BMO needed a Mortgage &amp; Loan Calculator web app for branch/customer use.<br><b>T:</b> Build and later modernize it end to end, frontend to data layer.<br><b>A:</b> Built the app with Angular/TypeScript on Node.js/AWS, then owned migrating the frontend to a React SPA and designing a new DynamoDB schema.<br><b>R:</b> The migration made processing 60% faster while keeping the app on AWS-native infrastructure.

## Cloze cards

- The Mortgage &amp; Loan Calculator was built end-to-end using {{c1::Angular}} and {{c2::TypeScript}} on the frontend, with {{c3::Node.js}} on AWS for the backend.
- Michele architected a serverless event-driven backend with {{c1::AWS Lambda}} + {{c2::EventBridge}} to decouple submission logic from third-party credit checks, cutting coupling by {{c3::40%}} and preventing {{c4::cascading failures}}.

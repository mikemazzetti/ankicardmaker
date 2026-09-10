---
deck: "Resume Prep::Agile SDLC & AI-Driven Dev"
topic: "Agile SDLC & AI-Driven Dev"
tags: [ankicardmaker, resume-prep, agile-sdlc]
note_type: Mixed (Basic / Basic (and reversed card) / Cloze)
created: 2026-09-09
---

# Agile SDLC & AI-Driven Dev — Resume Prep

Source of truth for the `Resume Prep::Agile SDLC & AI-Driven Dev` deck (18 notes). Edit here and re-push to update.

## Basic cards

1. **Q:** What's the core difference between Waterfall and Agile as SDLC models?
   **A:** Waterfall runs the SDLC phases sequentially, with each phase fully completed and signed off before the next starts, and requirements fixed up front. Agile works in short iterative cycles (sprints), delivering working increments repeatedly and adapting requirements based on ongoing feedback.

2. **Q:** What does the Product Owner own and do in Scrum?
   **A:** Owns the product backlog — deciding and prioritizing what gets built next to maximize the value delivered, and representing stakeholder/customer needs to the team.

3. **Q:** What does the Scrum Master do (and NOT do)?
   **A:** Facilitates the Scrum process, removes blockers/impediments for the team, and shields it from outside disruption. They are a facilitator/coach, not the team's manager or task-assigner.

4. **Q:** What's the difference in purpose between a Sprint Review and a Sprint Retrospective?
   **A:** Sprint Review demos the completed increment to stakeholders to gather feedback on the product. Sprint Retrospective is an internal team-only discussion on how the process and collaboration itself can improve next sprint.

5. **Q:** What is a "sprint" in Scrum?
   **A:** A fixed-length iteration (commonly 1-4 weeks) during which a defined set of backlog items is designed, built, and turned into a working, potentially shippable increment.

6. **Q:** What format do user stories typically follow?
   **A:** <pre><code>As a &lt;role&gt;,
I want &lt;goal&gt;,
so that &lt;benefit&gt;.</code></pre>e.g. "As a customer, I want to see my loan payment estimate, so that I can budget before applying."

7. **Q:** What do story points measure in Agile estimation?
   **A:** The relative effort, complexity, and uncertainty of a task — not literal hours. Stories are sized against each other (often on a Fibonacci-like scale: 1, 2, 3, 5, 8...) so the team estimates consistently without pinning down exact time.

8. **Q:** Why is CI/CD a natural fit for Agile teams?
   **A:** Agile's goal is to ship working software frequently in small increments. CI/CD automates the build/test/merge step (Continuous Integration) and the release step (Continuous Deployment/Delivery), so each small increment can be integrated and shipped fast and reliably instead of hitting a manual release bottleneck.

9. **Q:** Beyond catching bugs, what's a primary goal of code review?
   **A:** Knowledge sharing across the team and maintaining consistent design/code-quality standards — catching architectural or design issues early, before they're baked into the codebase.

10. **Q:** In an AI-assisted SDLC (like the BMO VSCode-agent PoC), what does "specialized agents per project phase" mean?
   **A:** Instead of one generic AI assistant for everything, different agents are configured/prompted for a specific SDLC stage — e.g. a requirements-analysis agent, a code-generation agent, a test-generation agent, a code-review agent — each with instructions tailored to that phase's task.

11. **Q:** Why does prompt/instruction design matter when building an SDLC-phase AI agent (e.g. a VSCode coding agent)?
   **A:** The agent's output quality depends directly on how precisely its instructions define scope, constraints, available context, and expected output format. Vague instructions produce inconsistent or off-target results — well-designed instructions function like a spec the agent executes against.

12. **Q:** Give a concrete example of an SDLC phase (other than writing implementation code) that an AI agent can accelerate.
   **A:** e.g. generating test cases from requirements/user stories, or drafting a PR summary and flagging likely issues during code review — applying AI earlier or later in the pipeline than just code generation.

13. **Q:** What's a key risk of merging AI-generated code into a CI/CD pipeline without human review?
   **A:** The AI can produce subtly incorrect logic, security vulnerabilities, or hallucinated APIs that still pass superficial tests. Human code review remains a necessary quality gate before those changes reach production.

14. **Q:** How does Agile's iterative feedback loop map onto how AI coding agents are typically used day to day?
   **A:** Like a sprint cycle at small scale: the developer gives the agent a scoped task, reviews and tests its output, then iterates with refined prompts/instructions — rather than expecting one perfect one-shot result.

## Cloze cards

- The classic SDLC phases are: {{c1::Requirements/Planning}}, {{c2::Design}}, {{c3::Implementation}}, {{c4::Testing}}, {{c5::Deployment}}, {{c6::Maintenance}}.
- The three core Scrum roles are the {{c1::Product Owner}}, the {{c2::Scrum Master}}, and the {{c3::Development Team}}.
- The four core Scrum ceremonies are {{c1::Sprint Planning}}, the {{c2::Daily Standup}}, the {{c3::Sprint Review}}, and the {{c4::Sprint Retrospective}}.
- The three main Scrum artifacts are the {{c1::Product Backlog}}, the {{c2::Sprint Backlog}}, and the {{c3::Increment}}.

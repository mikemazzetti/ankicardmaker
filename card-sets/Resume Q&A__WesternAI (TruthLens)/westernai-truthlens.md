---
deck: "Resume Q&A::WesternAI (TruthLens)"
topic: "WesternAI (TruthLens)"
tags: [ankicardmaker, resume-westernai]
note_type: Mixed (Basic / Basic (and reversed card) / Cloze)
created: 2026-09-10
---

# WesternAI (TruthLens) — Resume Q&A

Source of truth for the `Resume Q&A::WesternAI (TruthLens)` deck (20 notes). Edit here and re-push to update.

## Basic cards

1. **Q:** What is TruthLens?
   **A:** A full-stack NLP platform built at WesternAI to proactively flag deceptive web content in real time.

2. **Q:** What was your role and timeframe on the TruthLens project?
   **A:** Machine Learning Developer at WesternAI, Jan–Aug 2026, London, ON.

3. **Q:** What accuracy did TruthLens achieve on misinformation classification?
   **A:** 93% accuracy in real-time misinformation classification.

4. **Q:** Which base model did you fine-tune for TruthLens's classifier?
   **A:** RoBERTa.

5. **Q:** Why fine-tune RoBERTa instead of training a classifier from scratch?
   **A:** RoBERTa already has strong language representations from large-scale pretraining, so fine-tuning it on the misinformation task needs far less labeled data and compute than training a model from scratch, while still reaching high task-specific accuracy (93%).

6. **Q:** What NLP architecture did TruthLens add beyond the classifier?
   **A:** A Retrieval-Augmented Generation (RAG) architecture.

7. **Q:** What does the RAG layer in TruthLens retrieve?
   **A:** Counter-evidence — supporting or refuting source material relevant to a flagged claim.

8. **Q:** Why add a RAG layer instead of relying only on the classifier's label output?
   **A:** The classifier alone only outputs a verdict; RAG retrieves real evidence so the system can show users transparent, sourced reasoning behind a flag instead of an unexplained label.

9. **Q:** What tool did you integrate into TruthLens for explainability?
   **A:** SHAP (SHapley Additive exPlanations).

10. **Q:** What does SHAP add to TruthLens?
   **A:** Transparent explainability — it attributes the classifier's decision to specific input features, supporting the RAG counter-evidence with interpretable reasoning.

11. **Q:** Why does explainability (via SHAP) matter specifically for a misinformation-flagging tool?
   **A:** Users are more likely to trust and act on a flag if they can see why content was flagged, rather than accepting an opaque black-box verdict.

12. **Q:** RAG (as used in TruthLens) *(reversed — both ways)*
   **A:** Retrieval-Augmented Generation — an architecture that retrieves supporting evidence to ground and explain a model's output.

13. **Q:** What kind of content does TruthLens analyze?
   **A:** Deceptive web content, classified in real time for misinformation.

14. **Q:** Describe the TruthLens pipeline end to end.
   **A:** Web content is classified in real time by a fine-tuned RoBERTa model; a flag triggers RAG retrieval of counter-evidence, and SHAP explains which input features drove the classification.

15. **Q:** Was TruthLens a front-end-only, back-end-only, or full-stack build?
   **A:** Full-stack — TruthLens is described as a full-stack NLP platform.

16. **Q:** STAR — Talking point: Describe the core problem TruthLens solved.
   **A:** Situation/Task: deceptive web content spreads faster than users can evaluate it. Action: fine-tuned RoBERTa for real-time misinformation classification and layered RAG + SHAP for evidence-backed, explainable flags. Result: 93% classification accuracy with transparent counter-evidence, not just a black-box label.

17. **Q:** STAR — Talking point: Why is TruthLens more trustworthy than a plain classifier?
   **A:** Action: added a RAG layer to retrieve real counter-evidence and SHAP to expose which features drove each decision. Result: users get an explainable, evidence-backed verdict instead of an opaque 93%-accurate prediction.

18. **Q:** STAR — Talking point: What technical trade-off did you navigate in the RoBERTa fine-tuning?
   **A:** Task: reach high accuracy without the cost of training a language model from scratch. Action: started from pretrained RoBERTa and fine-tuned it on the misinformation classification task. Result: 93% accuracy by leveraging RoBERTa's existing language understanding.

19. **Q:** STAR — Talking point: Summarize TruthLens's architecture in one breath for an interview.
   **A:** A full-stack NLP platform: fine-tuned RoBERTa flags deceptive content in real time at 93% accuracy, a RAG layer retrieves counter-evidence, and SHAP explains the decision — so flags are accurate and transparent, not a black box.

## Cloze cards

- TruthLens combines a fine-tuned {{c1::RoBERTa}} classifier, a {{c2::RAG}} architecture for counter-evidence retrieval, and {{c3::SHAP}} for explainability.

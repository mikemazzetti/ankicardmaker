---
deck: "Resume Q&A::BUFFET"
topic: "BUFFET"
tags: [ankicardmaker, resume-buffet]
note_type: Mixed (Basic / Basic (and reversed card) / Cloze)
created: 2026-09-10
---

# BUFFET — Resume Q&A

Source of truth for the `Resume Q&A::BUFFET` deck (20 notes). Edit here and re-push to update.

## Basic cards

1. **Q:** What is BUFFET?
   **A:** An NLP algorithmic trader project that analyzes comment sentiment to inform trading decisions.

2. **Q:** What language was the BUFFET data-ingestion pipeline built in?
   **A:** Python.

3. **Q:** How many comments did the BUFFET pipeline ingest?
   **A:** 63,000+ comments.

4. **Q:** What uptime did the BUFFET ingestion pipeline achieve?
   **A:** 99.9% uptime.

5. **Q:** What sentiment analysis model did BUFFET build on?
   **A:** VADER (Valence Aware Dictionary and sEntiment Reasoner).

6. **Q:** Why use VADER as the base sentiment model instead of training a sentiment classifier from scratch?
   **A:** VADER is a lightweight, rule-based lexicon model tuned for short, informal text and needs no training data or model training — it can be used and extended out of the box, ideal for fast iteration on high-volume comment sentiment.

7. **Q:** How did you improve VADER's accuracy for BUFFET?
   **A:** By enhancing it with a custom financial lexicon.

8. **Q:** What accuracy gain did the custom financial lexicon provide?
   **A:** +18% accuracy improvement over stock VADER.

9. **Q:** What does injecting a custom financial lexicon into VADER actually do?
   **A:** It adds finance-specific terms and their sentiment valence scores — words/phrases missing from VADER's general-purpose lexicon — so the model correctly scores financial sentiment that generic VADER would misread or ignore.

10. **Q:** Why does generic VADER underperform on financial/trading comments without customization?
   **A:** VADER's default lexicon is tuned for general social-media language and doesn't capture domain-specific financial slang and terms, so it misjudges sentiment specific to trading discussion.

11. **Q:** What operational challenge did the BUFFET Python pipeline have to manage?
   **A:** API rate limits from the data source(s) it ingested comments from.

12. **Q:** How did the pipeline maintain 99.9% uptime while respecting API rate limits?
   **A:** It was engineered to actively manage and throttle requests against the API's rate limits, avoiding being blocked or dropped while continuously ingesting comment data.

13. **Q:** What is the end goal of BUFFET's sentiment pipeline?
   **A:** To feed sentiment signals from ingested comments into algorithmic trading decisions.

14. **Q:** VADER *(reversed — both ways)*
   **A:** A lexicon/rule-based sentiment analysis tool; in BUFFET it was enhanced with a custom financial lexicon for a +18% accuracy gain.

15. **Q:** What kind of data source likely produced the 63,000+ comments for BUFFET?
   **A:** A social/community platform with public trading discussion, accessed via a rate-limited API.

16. **Q:** STAR — Talking point: Describe the BUFFET reliability challenge and how you solved it.
   **A:** Task: continuously ingest a high volume of comments (63,000+) through a rate-limited API without downtime. Action: built a Python pipeline that actively managed API rate limits. Result: sustained 99.9% uptime on ingestion.

17. **Q:** STAR — Talking point: How did you improve sentiment accuracy for financial text specifically?
   **A:** Task: generic VADER sentiment scoring didn't capture financial/trading slang. Action: built and injected a custom financial lexicon into VADER. Result: +18% accuracy improvement in sentiment classification for the trading use case.

18. **Q:** STAR — Talking point: Why was VADER the right starting point rather than a deep-learning sentiment model?
   **A:** Task: needed fast, interpretable sentiment scoring on large volumes of short comments. Action: chose rule-based VADER and extended it with a domain-specific financial lexicon rather than training a heavier model from scratch. Result: a meaningful (+18%) accuracy gain with a lightweight, explainable, easily-tunable approach.

19. **Q:** STAR — Talking point: Summarize BUFFET's technical contribution in one breath.
   **A:** A Python pipeline that reliably ingested 63,000+ comments at 99.9% uptime under API rate limits, and boosted VADER sentiment accuracy 18% with a custom financial lexicon — powering an NLP algorithmic trading signal.

## Cloze cards

- BUFFET's Python pipeline ingested {{c1::63,000+}} comments at {{c2::99.9%}} uptime while managing API rate limits, and enhanced {{c3::VADER}} sentiment with a custom {{c4::financial lexicon}} for a {{c5::+18%}} accuracy gain.

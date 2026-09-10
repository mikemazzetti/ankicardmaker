---
deck: "Resume Prep::NLP & Sentiment Analysis"
topic: "NLP & Sentiment Analysis"
tags: [ankicardmaker, resume-prep, nlp]
note_type: Mixed (Basic / Basic (and reversed card) / Cloze)
created: 2026-09-09
---

# NLP & Sentiment Analysis — Resume Prep

Source of truth for the `Resume Prep::NLP & Sentiment Analysis` deck (18 notes). Edit here and re-push to update.

## Basic cards

1. **Q:** What is tokenization in NLP?
   **A:** Splitting raw text into smaller units — typically words or subwords — called tokens, for further processing.

2. **Q:** What are "stop words", and why are they often removed?
   **A:** Very common words (e.g. "the", "is", "and") that carry little distinctive meaning; removing them reduces noise and dimensionality for many NLP tasks.

3. **Q:** Stemming (NLP) *(reversed — tested both ways)*
   **A:** Crudely chopping word endings using fixed rules/heuristics to reduce a word to a root form (e.g. "running" → "run"), without guaranteeing the result is a real word.

4. **Q:** Lemmatization (NLP) *(reversed — tested both ways)*
   **A:** Reducing a word to its dictionary base form (lemma) using vocabulary and morphological/POS analysis (e.g. "better" → "good"), producing a valid word.

5. **Q:** What's the main tradeoff between stemming and lemmatization?
   **A:** Stemming is faster but cruder (can produce non-words); lemmatization is more linguistically accurate but slower and needs more resources (vocabulary/POS info).

6. **Q:** What is the "bag-of-words" text representation?
   **A:** Representing text as an unordered vector of word counts (or presence), completely ignoring grammar and word order.

7. **Q:** What does TF-IDF stand for, and what does it down-weight?
   **A:** Term Frequency-Inverse Document Frequency; it down-weights terms that appear frequently across many documents (less distinctive) and up-weights terms frequent in one document but rare across the corpus.

8. **Q:** What is VADER in sentiment analysis?
   **A:** Valence Aware Dictionary and sEntiment Reasoner — a lexicon-and-rule-based sentiment analysis tool tuned for social-media-style text that requires no training data.

9. **Q:** What is VADER's "compound score"?
   **A:** A single normalized score from -1 (most negative) to +1 (most positive) summarizing overall sentiment, computed by summing each word's rule-adjusted valence and normalizing the total.

10. **Q:** Name three linguistic features VADER's rules explicitly account for beyond a plain word-valence lexicon.
   **A:** Negation (e.g. "not good" flips polarity), intensifiers/degree modifiers (e.g. "very good" boosts the score), and punctuation/capitalization/emoji (e.g. "!!!" or ALL CAPS amplify intensity).

11. **Q:** How do you get a VADER compound sentiment score for a string in Python?
   **A:** <pre><code>from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
analyzer = SentimentIntensityAnalyzer()
score = analyzer.polarity_scores(text)['compound']</code></pre>

12. **Q:** How do you inject a custom term into VADER's lexicon (e.g. a domain-specific finance word)?
   **A:** <code>analyzer.lexicon.update({'bullish': 2.5, 'bearish': -2.5})</code>

13. **Q:** Why add a custom financial lexicon to VADER instead of relying on its default lexicon?
   **A:** VADER's default lexicon is tuned for general social media, not finance jargon (e.g. "bullish", "short squeeze"); a custom lexicon lets it correctly score domain-specific terms, improving accuracy on financial text.

14. **Q:** In the BUFFET project, what result came from enhancing VADER with a custom financial lexicon?
   **A:** An 18% improvement in sentiment classification accuracy on financial/trading text, across 63k+ ingested comments.

15. **Q:** What does "precision" measure in a classification task?
   **A:** Of all instances predicted positive, the fraction that were actually positive — TP / (TP + FP).

16. **Q:** What does "recall" measure in a classification task?
   **A:** Of all actual positive instances, the fraction the model correctly identified — TP / (TP + FN).

17. **Q:** What is the F1 score?
   **A:** The harmonic mean of precision and recall — a single metric balancing both, useful when you need to trade off false positives against false negatives.

18. **Q:** Why choose a lexicon-based approach like VADER over a trained ML classifier for sentiment analysis?
   **A:** It needs no labeled training data, is fast and interpretable (scores trace back to specific words/rules), and performs reasonably well out-of-the-box — useful when labeled data is scarce or transparency/speed matters.

---
deck: "Resume Prep::Statistics"
topic: "Statistics"
tags: [ankicardmaker, resume-prep, statistics]
note_type: Mixed (Basic / Basic (and reversed card) / Cloze)
created: 2026-09-09
---

# Statistics — Resume Prep

Source of truth for the `Resume Prep::Statistics` deck (16 notes). Edit here and re-push to update.

## Basic cards

1. **Q:** When is the median preferred over the mean as a measure of central tendency?
   **A:** When the data is skewed or has outliers &mdash; the mean is pulled toward extreme values, while the median (the middle value) is robust to them.

2. **Q:** Mode *(reversed — tested both ways)*
   **A:** The most frequently occurring value in a data set (a data set can have zero, one, or multiple modes).

3. **Q:** What does variance measure?
   **A:** The average of the squared differences between each data point and the mean &mdash; it quantifies how spread out the data is.

4. **Q:** How is standard deviation related to variance?
   **A:** Standard deviation is the square root of the variance &mdash; it's expressed in the same units as the original data, unlike variance.

5. **Q:** Why doesn't correlation between two variables prove that one causes the other?
   **A:** Because the observed relationship could be due to a confounding variable, reverse causation, or coincidence &mdash; correlation only measures that two variables move together, not why.

6. **Q:** What does a p-value represent in hypothesis testing?
   **A:** The probability of observing data at least as extreme as what was measured, <b>assuming the null hypothesis is true</b>. A small p-value (below the significance threshold, e.g. 0.05) is evidence against the null hypothesis.

7. **Q:** What is the difference between the null hypothesis and the alternative hypothesis?
   **A:** The null hypothesis (H&#8320;) states there is no effect/difference (the default assumption). The alternative hypothesis (H&#8321;) states there is a real effect/difference, which you're testing for evidence of.

8. **Q:** What is sampling bias? Give an example.
   **A:** A systematic error where the sample isn't representative of the population, skewing results. Example: surveying only people online about internet usage habits over-represents heavy internet users.

9. **Q:** What does a 95% confidence interval mean?
   **A:** If you repeated the sampling process many times and built an interval the same way each time, about 95% of those intervals would contain the true population parameter. (It is not a 95% probability that this one interval contains the true value.)

10. **Q:** In classification, what does precision measure and how is it computed?
   **A:** Of everything the model predicted positive, how many were actually positive. Precision = TP / (TP + FP).

11. **Q:** In classification, what does recall measure and how is it computed?
   **A:** Of everything that was actually positive, how many the model correctly caught. Recall = TP / (TP + FN).

12. **Q:** What is the typical tradeoff between precision and recall?
   **A:** Raising the classification threshold tends to increase precision but decrease recall (fewer, more confident positive predictions), while lowering it increases recall but decreases precision (more positive predictions, more false alarms).

13. **Q:** What is Bayes' theorem (formula for P(A|B))?
   **A:** P(A|B) = [P(B|A) &times; P(A)] / P(B)

14. **Q:** Give the intuition for Bayes' theorem with a medical-test example.
   **A:** Even with a highly accurate test, if a disease is very rare (low prior P(disease)), most positive results are still false positives &mdash; Bayes' theorem lets you update the probability of actually having the disease given a positive result, combining the test's accuracy with the disease's base rate.

## Cloze cards

- For a normal distribution, about {{c1::68%}} of values fall within 1 standard deviation of the mean, about {{c2::95%}} within 2 standard deviations, and about {{c3::99.7%}} within 3 standard deviations. <!-- Back Extra: This is the empirical rule (68-95-99.7 rule). -->
- The F1 score is the {{c1::harmonic mean}} of precision and recall, used as a single metric when you need to balance both. <!-- Back Extra: F1 = 2 * (precision * recall) / (precision + recall) -->

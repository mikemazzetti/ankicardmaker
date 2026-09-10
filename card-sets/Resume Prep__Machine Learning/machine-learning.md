---
deck: "Resume Prep::Machine Learning"
topic: "Machine Learning"
tags: [ankicardmaker, ml]
note_type: Mixed (Basic / Basic (and reversed card) / Cloze)
created: 2026-09-10
---

# Machine Learning — Resume Prep

Source of truth for the `Resume Prep::Machine Learning` deck (20 notes). Edit here and re-push to update.

## Basic cards

1. **Q:** In reinforcement learning, what does an agent learn to do?
   **A:** Choose actions in an environment, guided by rewards and penalties it receives, so as to maximize cumulative reward over time.

2. **Q:** Why split data into training, validation, and test sets instead of just training and test?
   **A:** The validation set is used to tune hyperparameters and select between models during development without touching the test set, so the test set stays an unbiased, final estimate of how the model generalizes to unseen data.

3. **Q:** Overfitting *(reversed — both ways)*
   **A:** A model fits the training data (including its noise) too closely, resulting in high variance and poor generalization to new, unseen data.

4. **Q:** Underfitting *(reversed — both ways)*
   **A:** A model is too simple to capture the underlying pattern in the data, resulting in high bias and poor performance on both training and test data.

5. **Q:** What does gradient descent do during model training?
   **A:** It iteratively updates model parameters in the direction that most reduces the loss function, using the gradient of the loss with respect to the parameters.

6. **Q:** What does the learning rate control in gradient descent, and what happens if it's set too high?
   **A:** It controls the size of each parameter update step. If it's too high, training can become unstable and the loss can oscillate or diverge instead of converging to a minimum.

7. **Q:** What does dropout do during neural network training?
   **A:** It randomly deactivates a fraction of neurons on each forward/backward pass, preventing units from co-adapting and reducing overfitting.

8. **Q:** What is the purpose of k-fold cross-validation?
   **A:** It splits the data into k folds, trains on k-1 folds and validates on the remaining fold, rotating through all k folds, to get a more reliable estimate of model performance than a single train/validation split.

9. **Q:** Why is feature scaling (standardization/normalization) important before training many ML models?
   **A:** Algorithms based on distances or gradient magnitudes (e.g., k-means, k-NN, gradient descent, SVMs) converge faster and behave correctly when features share a comparable scale; otherwise large-scale features can dominate.

10. **Q:** What's the difference between a classification task and a regression task in supervised learning?
   **A:** Classification predicts a discrete category or class label; regression predicts a continuous numeric value.

11. **Q:** How does a random forest differ from a single decision tree?
   **A:** A random forest trains many decision trees on bootstrapped samples of the data with random subsets of features at each split, then averages (regression) or votes (classification) their predictions, reducing the overfitting a single tree is prone to.

12. **Q:** In k-means clustering, what does the algorithm iteratively update to form k clusters?
   **A:** Cluster centroids: each point is assigned to its nearest centroid, then each centroid is recomputed as the mean of its assigned points, repeating until the assignments stop changing.

13. **Q:** Write scikit-learn code that splits data into an 80/20 train/test set and fits a Logistic Regression model.
   **A:** <pre><code>from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

model = LogisticRegression()
model.fit(X_train, y_train)
score = model.score(X_test, y_test)</code></pre>

14. **Q:** At WesternAI, what classification accuracy did Michele's TruthLens model achieve for real-time misinformation detection?
   **A:** 93%

## Cloze cards

- In {{c1::supervised}} learning, a model is trained on labeled examples (input-output pairs) to learn a mapping it can apply to new, unseen inputs.
- In {{c1::unsupervised}} learning, a model finds structure or patterns (e.g., clusters) in unlabeled data, with no predefined output labels.
- {{c1::Cross-entropy loss}} is the standard loss function for classification tasks, while {{c2::Mean Squared Error (MSE)}} is the standard loss function for regression tasks.
- L1 regularization (Lasso) adds the sum of absolute weight values and tends to produce {{c1::sparse weights, some exactly zero (built-in feature selection)}}; L2 regularization (Ridge) adds the sum of squared weight values and tends to {{c2::shrink weights smoothly toward zero without eliminating them}}.
- Given confusion-matrix counts TP, TN, FP, FN: Accuracy = {{c1::(TP + TN) / (TP + TN + FP + FN)}}, Precision = {{c2::TP / (TP + FP)}}, Recall = {{c3::TP / (TP + FN)}}.
- The {{c1::F1 score}} is the harmonic mean of precision and recall. {{c2::ROC-AUC}} is the area under the ROC curve, summarizing a classifier's ability to separate classes across all thresholds. A {{c3::confusion matrix}} tabulates a classifier's True Positive, False Positive, True Negative, and False Negative counts.

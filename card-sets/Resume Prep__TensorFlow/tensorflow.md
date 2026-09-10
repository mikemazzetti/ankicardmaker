---
deck: "Resume Prep::TensorFlow"
topic: "TensorFlow"
tags: [ankicardmaker, resume-prep, tensorflow]
note_type: Mixed (Basic / Basic (and reversed card) / Cloze)
created: 2026-09-09
---

# TensorFlow — Resume Prep

Source of truth for the `Resume Prep::TensorFlow` deck (18 notes). Edit here and re-push to update.

## Basic cards

1. **Q:** What is a tensor in TensorFlow?
   **A:** A multi-dimensional array (a generalization of scalars, vectors, and matrices) with a defined dtype and shape — the core data structure TensorFlow computes on.

2. **Q:** What's the key difference between the Keras Sequential API and the Functional API?
   **A:** Sequential stacks layers in a single linear chain (one input, one output); the Functional API builds a graph of layers, allowing multiple inputs/outputs, shared layers, and non-linear topologies (e.g. branches, skip connections).

3. **Q:** How do you build a Sequential model with one hidden Dense layer (64 units, relu) and an output Dense layer (10 units, softmax)?
   **A:** <pre><code>model = tf.keras.Sequential([
    tf.keras.layers.Dense(64, activation='relu'),
    tf.keras.layers.Dense(10, activation='softmax')
])</code></pre>

4. **Q:** What three things does <code>model.compile()</code> configure?
   **A:** The optimizer, the loss function, and the metrics to track during training/evaluation.

5. **Q:** How do you compile a model for multi-class classification with the Adam optimizer?
   **A:** <code>model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])</code>

6. **Q:** How do you train a compiled model for 10 epochs on <code>X_train</code>/<code>y_train</code>?
   **A:** <code>model.fit(X_train, y_train, epochs=10, batch_size=32)</code>

7. **Q:** How does a layer like Dropout or BatchNorm behave differently in training mode versus inference mode?
   **A:** In training mode Dropout randomly zeroes units and BatchNorm uses the current batch's statistics; in inference mode Dropout is disabled (a no-op) and BatchNorm uses its learned running statistics — controlled by a <code>training</code> flag.

8. **Q:** What is overfitting?
   **A:** When a model learns the training data too specifically (including its noise), so it performs well on training data but poorly on unseen/validation data.

9. **Q:** Name two regularization techniques used in Keras/TensorFlow to reduce overfitting.
   **A:** Dropout layers and L1/L2 weight regularization (also early stopping and data augmentation).

10. **Q:** What does a Dropout layer do during training?
   **A:** It randomly sets a fraction of its input units to zero on each update, preventing the network from relying too heavily on any single neuron — reducing overfitting.

11. **Q:** What is "autodiff" (automatic differentiation) in TensorFlow?
   **A:** A technique that computes exact gradients of a computation by tracking the operations performed and applying the chain rule automatically, without hand-deriving derivatives.

12. **Q:** How do you compute gradients of a loss with respect to model weights manually using <code>tf.GradientTape</code>?
   **A:** <pre><code>with tf.GradientTape() as tape:
    predictions = model(x)
    loss = loss_fn(y, predictions)
grads = tape.gradient(loss, model.trainable_variables)</code></pre>

13. **Q:** What does an optimizer (e.g. Adam, SGD) do during training?
   **A:** It updates the model's weights using the computed gradients, in the direction that minimizes the loss function.

14. **Q:** What does the loss function measure?
   **A:** The error, or distance, between the model's predictions and the true target values — training adjusts weights to minimize it.

15. **Q:** Why use a validation set during training (e.g. via <code>validation_split</code> or <code>validation_data</code> in <code>fit()</code>)?
   **A:** To monitor performance on data the model isn't training on, each epoch — this reveals overfitting that the training loss alone wouldn't show.

16. **Q:** What's the difference between <code>model.predict(X)</code> and <code>model.evaluate(X, y)</code>?
   **A:** <code>predict()</code> just returns raw model outputs (inference only, no labels needed); <code>evaluate()</code> runs inference and computes the loss/metrics against the supplied true labels <code>y</code>.

17. **Q:** What is a "layer" in <code>tf.keras</code>, conceptually?
   **A:** A reusable, composable unit encapsulating a computation (e.g. weights plus an operation like a dense matrix multiply + activation) that can be stacked with other layers to build a model.

## Cloze cards

- In {{c1::model.fit()}}, one full pass over the entire training dataset is called an {{c2::epoch}}, while each single gradient update on a subset of data is a {{c3::batch}}/step.

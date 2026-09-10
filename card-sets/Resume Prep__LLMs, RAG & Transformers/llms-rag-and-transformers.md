---
deck: "Resume Prep::LLMs, RAG & Transformers"
topic: "LLMs, RAG & Transformers"
tags: [ankicardmaker, llm-rag]
note_type: Mixed (Basic / Basic (and reversed card) / Cloze)
created: 2026-09-10
---

# LLMs, RAG & Transformers — Resume Prep

Source of truth for the `Resume Prep::LLMs, RAG & Transformers` deck (20 notes). Edit here and re-push to update.

## Basic cards

1. **Q:** What mechanism lets a transformer weigh the relevance of every other token when encoding a given token?
   **A:** Self-attention

2. **Q:** What is a "token" in the context of an LLM?
   **A:** A basic unit of text (a word, subword, or character piece) that a language model processes as input/output, produced by a tokenizer.

3. **Q:** What is an embedding in NLP?
   **A:** A dense, fixed-length numeric vector representation of a token, word, or piece of text that captures its semantic meaning, so similar meanings map to similar vectors.

4. **Q:** How does RoBERTa differ from the original BERT?
   **A:** RoBERTa uses the same architecture as BERT but improves the training recipe: more training data, longer training, larger batches, dynamic masking, and removal of the Next Sentence Prediction (NSP) objective.

5. **Q:** What's the difference between pretraining and fine-tuning for a language model?
   **A:** Pretraining trains a model from scratch on a large, general text corpus (e.g., via masked language modeling) to learn broad language representations; fine-tuning further trains that pretrained model on a smaller, task-specific labeled dataset to specialize it.

6. **Q:** What is transfer learning?
   **A:** Reusing knowledge (weights/representations) learned by a model on one task or dataset as the starting point for a model on a different but related task, instead of training from scratch.

7. **Q:** What problem does Retrieval-Augmented Generation (RAG) solve for LLMs?
   **A:** It grounds an LLM's responses in external, up-to-date, or domain-specific knowledge retrieved at query time, rather than relying only on facts memorized during pretraining.

8. **Q:** What similarity metric is most commonly used to compare vector embeddings in similarity search?
   **A:** Cosine similarity (the cosine of the angle between two vectors).

9. **Q:** What is prompt engineering?
   **A:** The practice of designing and refining the input (instructions, examples, context) given to an LLM to reliably elicit the desired output, without changing the model's weights.

10. **Q:** What distinguishes an LLM agent from a plain single-turn LLM completion?
   **A:** An LLM agent plans and executes multi-step tasks, deciding when to call external tools/APIs or use retrieved context and take further actions, rather than just producing one response to one prompt.

11. **Q:** What does SHAP stand for, and what does it provide?
   **A:** SHapley Additive exPlanations - a model-explainability technique that assigns each input feature a contribution value toward a specific prediction, based on Shapley values from cooperative game theory.

12. **Q:** What is "hallucination" in the context of LLMs?
   **A:** When an LLM generates text that is fluent and confident but factually incorrect or unsupported by any real source.

13. **Q:** How does RAG help reduce LLM hallucination?
   **A:** By grounding the model's generation in retrieved, verifiable source documents, giving it real evidence to draw from instead of relying solely on memorized (and possibly incorrect) parameters.

14. **Q:** In WesternAI's TruthLens project, which pretrained transformer model was fine-tuned for misinformation classification?
   **A:** RoBERTa

15. **Q:** What real-time classification accuracy did TruthLens achieve for flagging deceptive/misinformation content?
   **A:** 93%

16. **Q:** What explainability technique did TruthLens integrate with its RAG pipeline to support transparent counter-evidence retrieval?
   **A:** SHAP

17. **Q:** At BMO, what Python web framework was used to build specialized LLM agents for each phase of an AI-driven SDLC pipeline PoC?
   **A:** FastAPI

## Cloze cards

- In self-attention, each token produces a {{c1::query}}, {{c2::key}}, and {{c3::value}} vector; attention weights come from comparing queries against keys, then used to weight the values.
- {{c1::Encoder-only}} transformers (e.g., BERT) are best suited for understanding tasks like classification and generating embeddings, while {{c2::decoder-only}} transformers (e.g., GPT) are best suited for autoregressive text generation.
- The RAG pipeline works in three steps: {{c1::retrieve}} relevant documents/passages from an external knowledge source, {{c2::augment}} the LLM prompt with that retrieved context, then {{c3::generate}} a response grounded in it.

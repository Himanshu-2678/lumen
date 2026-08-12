# Decision: Add Cross Encoder Reranking

## Problem

Initial hybrid retrieval sometimes returned semantically related but noisy chunks.
This affected answer grounding.

## Experiment

Added Cross Encoder reranking using:

ms-marco-MiniLM-L-6-v2

Pipeline:

Hybrid Retrieval
        ↓
Cross Encoder Reranker
        ↓
Top-k Evidence Selection
        ↓
LLM Generation


## Evaluation Dataset

- 40 questions
- 5 documents
- 35 answerable questions
- 5 unanswerable questions


## Results

| Metric | Baseline | Reranked | Change |
|---|---:|---:|---:|
| Faithfulness | 0.624 | 0.735 | +0.111 |
| Answer Relevancy | 0.795 | 0.735 | -0.060 |
| Context Precision | 0.756 | 0.762 | +0.006 |
| Refusal Accuracy | - | 1.0 | - |


## Decision

Keep cross encoder reranking.

Reason:
The improvement in faithfulness indicates better evidence grounding.
The slight reduction in answer relevancy is accepted because factual support is prioritized over broader generation.
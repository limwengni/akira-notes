# Lesson 3 - Retrieval and RAG

> 60-90 minutes - Inspect retrieved evidence before generating an answer.

**Goal:** divide documents into chunks, retrieve candidates, and keep their source identities.

**Prerequisites:** Python dictionaries, lists, sets, and functions. This example uses only the standard library.

**Focus:** retrieval-augmented generation (RAG) supplies retrieved evidence to a model when it generates an answer.

---

## The pipeline

A small RAG pipeline loads documents, splits them into chunks, retrieves relevant chunks for a question, places them in context, and asks a model to answer from that evidence.

An **embedding** is a numerical representation of content. Vector retrieval compares such representations to find related passages. This lesson uses word overlap instead, so you can understand and debug retrieval without downloading an embedding model.

Smaller chunks can improve focus but lose surrounding meaning. Overlap repeats some words between neighboring chunks so a boundary is less likely to cut away important context.

## Python example - A transparent retriever

Save this complete block as `retrieval.py` in your practice directory. The next lesson and project import it.

```python
import re

DOCUMENTS = {
    "graphs.md": (
        "Breadth-first search (BFS) uses a queue to find a path with "
        "the fewest edges in an unweighted graph."
    ),
    "pytorch.md": (
        "Autograd computes gradients. Clear gradients before each "
        "optimizer update."
    ),
    "agents.md": (
        "An agent uses a model to choose tools and uses their results "
        "to continue a task."
    ),
}
STOP_WORDS = {
    "a", "an", "and", "are", "does", "how", "i", "in", "is",
    "it", "of", "the", "to", "what", "which", "why", "with",
}

def tokens(text):
    return set(re.findall(r"[a-z0-9]+", text.lower())) - STOP_WORDS

def chunk_documents(documents, size=24, overlap=6):
    if size < 1 or not 0 <= overlap < size:
        raise ValueError("Require size > 0 and 0 <= overlap < size.")
    chunks = []
    for source, text in documents.items():
        words = text.split()
        for number, start in enumerate(range(0, len(words), size-overlap)):
            chunks.append({
                "id": f"{source}#chunk-{number}",
                "text": " ".join(words[start:start+size]),
            })
            if start + size >= len(words):
                break
    return chunks

CHUNKS = chunk_documents(DOCUMENTS)

def retrieve(question, top_k=2, chunks=None):
    if top_k < 1:
        raise ValueError("top_k must be positive.")
    query_tokens = tokens(question)
    scored = []
    corpus = CHUNKS if chunks is None else chunks
    for chunk in corpus:
        score = len(query_tokens & tokens(chunk["text"]))
        if score > 0:
            scored.append((score, chunk["id"], chunk))
    scored.sort(key=lambda item: (-item[0], item[1]))
    return [chunk for _, _, chunk in scored[:top_k]]

if __name__ == "__main__":
    for question in ["Why does BFS use a queue?", "Who won the football match?"]:
        matches = retrieve(question)
        print(question)
        for match in matches:
            print(match["id"], ":", match["text"])
        if not matches:
            print("No supporting passage found.")
```

**Expected:** the BFS question retrieves `graphs.md#chunk-0`. The football question returns no passages.

These names identify in-memory fixture documents, not files that you need to create. The mini-project shows how to load real Markdown notes.

## From retrieval to generation

This example stops at retrieval. To make a model-backed RAG system, pass the selected passages and their source IDs to a model, then ask it to answer with references to those IDs.

The [notes-assistant project](mini-project.md) first adds a deterministic extractive response, then offers a model-backed RAG extension. An extractive response quotes evidence; it does not generate a new explanation.

A positive word-overlap score means "candidate passage," not "this passage proves the answer." Similar wording can still retrieve irrelevant evidence. Retrieval and answer correctness need separate checks.

## Exercises

1. Add a short Dijkstra document and retrieve it using a question containing "Dijkstra".
2. Ask for "automatic differentiation" when the note says "autograd". Explain the keyword mismatch.
3. Make a longer document and change chunk size and overlap. Inspect the IDs and text.
4. Create five questions with expected source IDs, including two that should return no support.

**Hints:** synonyms motivate embeddings or query expansion, but either approach still needs evaluation. Examine actual chunks before increasing top_k.

## Common mistakes

- Dropping source identity during chunking.
- Retrieving something for every question even when evidence is absent.
- Assuming a citation proves that the generated claim matches the source.
- Treating retrieved document text as instructions for the application.

## Checkpoint

- [ ] I can trace a question to its retrieved chunks and source IDs.
- [ ] I can explain the difference between keyword and vector retrieval.
- [ ] I can distinguish retrieval, extraction, and model-backed generation.

Previous: [Tool calling](02-tool-calling.md). Next: [LangGraph workflows](04-langgraph-workflows.md). [Track index](README.md) | [Progress](progress.md).

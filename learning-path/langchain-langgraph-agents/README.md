# LangChain, LangGraph, RAG and AI Agents - Beginner

> Five lessons plus a mini-project - Allow 1-2 sessions per lesson and 2-4 for the project.

**Goal:** Trace a question from retrieval to answer, distinguish scripted routing from model decisions, and explain where tool arguments are checked.

## Prerequisites

Python functions, dictionaries, type hints, imports, and basic exception handling. Neural-network training is not a prerequisite.

## Setup

Use the [shared Python setup](../README.md#python-setup), then install the framework packages inside that environment:

```powershell
python -m pip install "langchain>=1,<2" "langgraph>=1,<2"
```

This track targets the v1 API families. The core lessons run offline after installation. Lesson 3 uses only the standard library. Lesson 5 has a separate, optional hosted-model example; install its provider package only if you choose that extension.

Use the [shared instructions for saving and running examples](../README.md#python-setup). Keep scripts imported by a lesson in the same practice directory.

---

## Lessons

| Order | Lesson | Focus |
|---|---|---|
| 1 | [Prompts and LangChain](01-prompts-and-langchain.md) | Compose prompts and a deterministic runnable. |
| 2 | [Tool calling](02-tool-calling.md) | Describe, validate, and execute a typed tool. |
| 3 | [Retrieval and RAG](03-retrieval-and-rag.md) | Retrieve chunks and keep source references. |
| 4 | [LangGraph workflows](04-langgraph-workflows.md) | Route shared state through explicit steps. |
| 5 | [AI agents](05-ai-agents.md) | Understand a model/tool loop and its limits. |
| 6 | [Mini-project](mini-project.md) | A notes assistant with source references, an unknown-answer path, and a small evaluation set. |

## Progress and review

Use the [progress tracker](progress.md) after every session. Completion means you can run the example, explain it, and adapt it for an exercise.

[Official LangChain documentation](https://docs.langchain.com/oss/python/langchain/overview) is the reference for framework concepts.

See the [roadmap](../ROADMAP.md) for the recommended order across tracks, or return to [all learning journeys](../README.md).

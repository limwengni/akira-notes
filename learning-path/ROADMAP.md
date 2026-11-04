# Learning Roadmap

> Plan for understanding - A session is roughly 45-90 minutes, not a deadline.

**Goal:** choose an entry point and know what to learn before moving on.

---

## Before choosing a track

You should be able to write a function, loop over a list, look up a dictionary key, import a module, and run a Python file. If those are unfamiliar, use the [Python tutorial](https://docs.python.org/3/tutorial/) alongside the first lesson.

For algebra, read `y = w * x + b` as "multiply the input by a weight, then add a bias." The neural-network lessons introduce gradients through small examples.

## Choose your route

| Your interest | Suggested order | Readiness checkpoint |
|---|---|---|
| Routing and graph algorithms | Graph lessons 1-3, then the core graph project | Explain why fewest roads can differ from fastest travel time |
| Traffic prediction and GNNs | Graph lessons 1-3, PyTorch lessons 1-5, graph lessons 4-5, then the extended graph project | Trace a node feature through aggregation and evaluate a future-time prediction |
| Building LLM applications | LangChain lessons 1-5, then the notes-assistant project | Explain which steps are scripted and which decisions a model makes |
| Understanding deep learning | PyTorch lessons 1-5, then the classifier project | Train, evaluate, save, reload, and explain a model |

Track indexes: [Graphs](graphs-routing-gnns-traffic/README.md), [LangChain and agents](langchain-langgraph-agents/README.md), [PyTorch](pytorch-deep-learning/README.md).

**Focus:** LangGraph's workflow graph and a GNN's data graph serve different purposes. Learning one does not automatically teach the other.

## A realistic rhythm

| Stage | Sessions | Evidence to keep |
|---|---|---|
| Setup and first lesson | 1-2 | A working example and a few sentences explaining it |
| Remaining lessons in one track | 4-8 | Completed exercises, including one changed input per lesson |
| Mini-project | 2-4 | A runnable script, results, and known limitations |
| Review | 1 | Rebuild one small part without copying |

A complete track often takes 8-15 sessions. The traffic/GNN route includes the PyTorch foundations, so allow extra time. Prior programming experience changes these estimates.

A useful session is 15 minutes reading, 25-50 minutes coding, and 5-10 minutes writing notes. Stay with one primary track; use another only when a prerequisite points there.

## Milestones

- [ ] **Python ready:** I can run a file and understand lists, dictionaries, functions, and imports.
- [ ] **First example explained:** I can predict its output and explain each important step.
- [ ] **Exercises attempted:** I can handle an input beyond the lesson's happy path.
- [ ] **Project completed:** I have measured behavior against a simple baseline or acceptance case.
- [ ] **Review completed:** I can explain a limitation and rebuild a small part from memory.

Use the detailed [graph tracker](graphs-routing-gnns-traffic/progress.md), [agent tracker](langchain-langgraph-agents/progress.md), or [PyTorch tracker](pytorch-deep-learning/progress.md) for session notes.

## How the tracks connect

- Graph algorithms choose paths using known edge costs. Traffic models estimate quantities that can become those costs.
- PyTorch supplies tensor operations, differentiation, and trainable layers used in the GNN lesson.
- RAG retrieves information to support an answer. An agent can choose retrieval as a tool.
- LangGraph describes how an application moves between steps. The notes-assistant project uses explicit routing before any optional model-driven behavior.
- A more complicated model or agent needs evidence of improvement. Compare with a simple baseline first.

## Completion review

Before marking a track complete, demonstrate its mini-project and answer:

1. What goes in and what comes out?
2. What assumptions does the example make?
3. Which failure case did you try?
4. What evidence supports the result?
5. What would you need before using it with real data?

Return to the [journey index](README.md).

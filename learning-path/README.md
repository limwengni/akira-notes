# Learning Paths

> Beginner-friendly tracks - Work through one main track at a time, with 45-90 minutes per session.

**Goal:** build working understanding through explanations, Python examples, exercises, and a small project.

Start with the [learning roadmap](ROADMAP.md). It explains prerequisites, suggested study routes, and when the tracks connect.

---

## Choose a track

| Track | Start here | What you will build | Progress |
|---|---|---|---|
| Graph Theory, shortest paths, GNNs, and traffic prediction | [Graphs and traffic](graphs-routing-gnns-traffic/README.md) | A traffic-aware route planner | [Tracker](graphs-routing-gnns-traffic/progress.md) |
| LangChain, LangGraph, RAG, tool calling, and AI agents | [AI application workflows](langchain-langgraph-agents/README.md) | A notes assistant with source references | [Tracker](langchain-langgraph-agents/progress.md) |
| PyTorch, neural networks, and deep learning | [PyTorch foundations](pytorch-deep-learning/README.md) | A small classifier that can be saved and reloaded | [Tracker](pytorch-deep-learning/progress.md) |

Each track contains five lessons, exercises, a mini-project, and a progress tracker. Estimates include reading and practice; projects usually need several sessions.

## How to use the lessons

1. Read the goal and prerequisites.
2. Predict what the example will do before running it.
3. Run it, then change one input and explain the result.
4. Complete the exercises. Use the hints after making an attempt.
5. Record what confused you in the tracker and revisit it next session.

**Keep it light:** getting stuck is a reason to shrink the example. A lesson is complete when you can explain the main idea and modify the code yourself.

## Python setup

Use Python 3.11 or 3.12 with a virtual environment. Check the framework's installation page if using another Python version.

From the repository root, create an optional local practice folder and environment. These commands are for PowerShell:

```powershell
python --version
New-Item -ItemType Directory -Force learning-path/practice
python -m venv learning-path/practice/.venv
learning-path/practice/.venv/Scripts/Activate.ps1
python -m pip --version
```

If PowerShell blocks activation, call the environment's interpreter directly, for example:
`learning-path/practice/.venv/Scripts/python.exe -m pip --version`.
Use that interpreter in place of `python` for installation and running examples.

On macOS/Linux, activate with `source learning-path/practice/.venv/bin/activate`.

The practice directory is a suggested workspace for your own scripts; the lessons themselves are Markdown. Keep environments, generated model files, and credentials out of commits. You can stage individual notes without adding practice outputs.

Code blocks are standalone unless a lesson explicitly says to save/import a named file or append a continuation. Run a saved example with `python path/to/example.py`.

## Other learning paths

The existing tracks live alongside these new materials:

- [LeetCode learning path](leetcode/README.md)
- [Ruby/Rails learning path](ruby/README.md)
- [Web3 learning path](web3/README.md)

Return to the [repository README](../README.md).

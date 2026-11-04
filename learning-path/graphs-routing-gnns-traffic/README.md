# Graphs, Routing, GNNs and Traffic Prediction - Beginner

> Five lessons plus a mini-project - Allow 1-2 sessions per lesson and 2-4 for the project.

**Goal:** Explain when BFS and Dijkstra disagree, fit a tiny GNN, and evaluate a traffic baseline without future information.

## Prerequisites

Python dictionaries, lists, functions, loops, and basic arithmetic. Complete lessons 1-3 first; take the PyTorch foundations before lesson 4.

## Setup

Lessons 1-3, lesson 5, and the core project use only the Python standard library. Lesson 4 and the optional GNN extension require the [PyTorch setup](../pytorch-deep-learning/README.md#setup).

Use the [shared instructions for saving and running examples](../README.md#python-setup). Keep scripts imported by a lesson in the same practice directory.

---

## Lessons

| Order | Lesson | Focus |
|---|---|---|
| 1 | [Graph foundations](01-graph-foundations.md) | Model intersections, roads, direction, and costs. |
| 2 | [BFS and DFS](02-bfs-and-dfs.md) | Explore a graph and reconstruct an unweighted shortest path. |
| 3 | [Shortest paths](03-shortest-paths.md) | Find a minimum-cost route with Dijkstra; understand A*. |
| 4 | [Graph neural networks](04-graph-neural-networks.md) | Learn from node features and neighboring nodes. |
| 5 | [Traffic prediction](05-traffic-prediction.md) | Build time windows and evaluate a forecasting baseline. |
| 6 | [Mini-project](mini-project.md) | A small traffic-aware route planner, followed by an optional GNN forecast experiment. |

## Progress and review

Use the [progress tracker](progress.md) after every session. Completion means you can run the example, explain it, and adapt it for an exercise.

[Stacks and queues practice](../leetcode/notes/day-9.md) revisits queues and stacks used in traversal.

See the [roadmap](../ROADMAP.md) for the recommended order across tracks, or return to [all learning journeys](../README.md).

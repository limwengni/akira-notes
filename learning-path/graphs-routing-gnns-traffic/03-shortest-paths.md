# Lesson 3 - Shortest Paths

> 60-90 minutes - Compare edge count with total travel time.

**Goal:** implement Dijkstra's algorithm for a graph with finite, nonnegative edge costs.

**Prerequisites:** [BFS and DFS](02-bfs-and-dfs.md), dictionaries, tuples, and functions.

**Focus:** repeatedly expand the node with the lowest known total cost.

---

## The idea

BFS explores by number of edges. Dijkstra explores by accumulated cost. A **priority queue** keeps the cheapest candidate available; Python's `heapq` provides a min-heap.

When a route to a neighbor is cheaper than the previous best, update that neighbor's distance and parent. This improvement is called **relaxation**.

An older heap entry can remain after an improvement. Skip it when its cost no longer matches the best distance.

## Python example - Cost and path

Save this complete block as `routing.py` in your practice directory. The project will import it from there. Running it directly prints the example route; importing it does not run the demo.

```python
import heapq
import math
from itertools import count

def shortest_path(graph, start, goal):
    if start not in graph or goal not in graph:
        raise ValueError("Both endpoints must be declared nodes.")

    # Validate the entire graph before any early exit.
    for neighbors in graph.values():
        for neighbor, weight in neighbors.items():
            if neighbor not in graph:
                raise ValueError("Every neighbor must be a declared node.")
            if not math.isfinite(weight) or weight < 0:
                raise ValueError("Costs must be finite and nonnegative.")

    sequence = count()
    heap = [(0.0, next(sequence), start)]
    distance = {start: 0.0}
    parent = {start: None}

    while heap:
        cost, _, current = heapq.heappop(heap)
        if cost != distance[current]:
            continue
        if current == goal:
            path = []
            node = goal
            while node is not None:
                path.append(node)
                node = parent[node]
            return cost, path[::-1]

        for neighbor, weight in graph[current].items():
            candidate = cost + weight
            if candidate < distance.get(neighbor, math.inf):
                distance[neighbor] = candidate
                parent[neighbor] = current
                heapq.heappush(
                    heap, (candidate, next(sequence), neighbor)
                )

    return math.inf, []

if __name__ == "__main__":
    roads = {
        "Home": {"Cafe": 2.0, "School": 1.0},
        "Cafe": {"Office": 5.0},
        "School": {"Park": 1.0},
        "Park": {"Office": 1.0},
        "Office": {},
        "Isolated": {},
    }
    print(shortest_path(roads, "Home", "Office"))
    print(shortest_path(roads, "Home", "Isolated"))
    print(shortest_path(roads, "Home", "Home"))
```

**Expected:**

```text
(3.0, ['Home', 'School', 'Park', 'Office'])
(inf, [])
(0.0, ['Home'])
```

The counter breaks equal-cost heap ties without comparing node names. The algorithm returns one optimal route; equal-cost alternatives need not all be returned.

**Complexity:** for a simple adjacency-list graph, the lazy-heap implementation takes O((V + E) log V) time and O(V + E) auxiliary space. The validation pass also scans all nodes and edges.

## Why negative costs break the guarantee

Dijkstra finalizes a node assuming no later route can make it cheaper. A negative edge can invalidate that assumption. Use an algorithm designed for negative edges, such as Bellman-Ford, when the problem requires them. Travel times should not be negative.

## A* in one paragraph

A* prioritizes `cost_so_far + estimated_cost_to_goal`. With a suitable heuristic it can explore fewer nodes. For the usual shortest-path guarantees, the heuristic must not overestimate remaining cost; consistency is especially useful when permanently closing nodes. Our example does not implement A*. With a zero heuristic, A* has Dijkstra's priorities.

## Exercises

1. Raise Park -> Office to 10 minutes. Predict the new fastest route before running it.
2. Add a zero-cost edge and a cycle. Confirm termination.
3. Try a negative edge, infinity, an undeclared neighbor, and an unknown endpoint. Explain each error.
4. Compare the route with BFS from lesson 2. Explain the disagreement.

**Hints:** the route through Cafe costs 7 minutes. Check all weights before starting so invalid edges cannot hide behind an early return.

## Checkpoint

- [ ] I can explain relaxation, the heap, and stale entries.
- [ ] I can distinguish invalid input from an unreachable destination.
- [ ] I can choose BFS or Dijkstra based on the meaning of edge cost.

Previous: [BFS and DFS](02-bfs-and-dfs.md). Next: [GNNs](04-graph-neural-networks.md), after the [PyTorch track](../pytorch-deep-learning/README.md). You can also start the [core project](mini-project.md). [Track index](README.md) | [Progress](progress.md).

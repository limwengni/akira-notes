# Lesson 2 - BFS and DFS

> 60-90 minutes - Trace the queue or stack by hand first.

**Goal:** explore reachable nodes and find a shortest path measured in number of edges.

**Prerequisites:** [graph foundations](01-graph-foundations.md), Python functions, and a set.

**Focus:** breadth-first search (BFS) explores in layers. Depth-first search (DFS) follows one branch before trying another.

---

## Why order matters

Imagine asking everyone one road away from Home, then everyone two roads away. That is BFS. A queue keeps the oldest unexplored node at the front.

DFS uses a stack: the newest unexplored node is next. It is useful for reachability and structural exploration, but its first route need not use the fewest roads.

The existing [stacks and queues notes](../leetcode/notes/day-9.md) explain these processing orders.

## Python example - BFS with a parent map

This standalone example assumes every neighbor is also a key in the graph.

```python
from collections import deque

roads = {
    "Home": ["Cafe", "School"],
    "Cafe": ["Office"],
    "School": ["Park"],
    "Park": ["Office"],
    "Office": [],
    "Isolated": [],
}

def bfs_path(graph, start, goal):
    if start not in graph or goal not in graph:
        raise ValueError("Both endpoints must be declared nodes.")

    queue = deque([start])
    parent = {start: None}

    while queue:
        current = queue.popleft()
        if current == goal:
            path = []
            while current is not None:
                path.append(current)
                current = parent[current]
            return path[::-1]

        for neighbor in graph[current]:
            if neighbor not in parent:
                parent[neighbor] = current
                queue.append(neighbor)

    return None

print(bfs_path(roads, "Home", "Office"))
print(bfs_path(roads, "Home", "Isolated"))
print(bfs_path(roads, "Home", "Home"))
```

**Expected:**

```text
['Home', 'Cafe', 'Office']
None
['Home']
```

The parent map does two jobs: it marks a node as discovered and remembers how we reached it. Marking discovery before enqueueing avoids repeatedly queueing a node in a cycle.

BFS guarantees the fewest edges when each edge has equal cost. It does not use travel-time weights.

## Python example - DFS reachability

Append this block to the previous example; it reuses `roads`.

```python
def dfs_reachable(graph, start):
    if start not in graph:
        raise ValueError("Start must be a declared node.")

    stack = [start]
    seen = set()
    while stack:
        current = stack.pop()
        if current in seen:
            continue
        seen.add(current)
        stack.extend(graph[current])
    return seen

print(sorted(dfs_reachable(roads, "Home")))
```

**Expected:** Cafe, Home, Office, Park, and School are reachable. Isolated is absent. Sorting makes the printed result easy to compare; it is not the DFS visit order.

**Complexity:** each traversal runs in O(V + E) time on an adjacency list over the reachable part of the graph. BFS needs O(V) auxiliary space; this simple DFS can hold duplicate stack entries, using up to O(V + E) space.

## Exercises

1. Add Office -> Home. Confirm that both searches still terminate.
2. Reverse Home's neighbor order. Can the chosen path change when there are equal-length alternatives?
3. Add Home -> Office with a 100-minute cost in a separate weighted version. Would BFS notice that cost?
4. Change BFS to return every node's distance from Home in number of edges.

**Hints:** use `distance[neighbor] = distance[current] + 1` when discovering a new node. A parent map answers "how did I get here?"; a distance map answers "how far is it?"

## Common mistakes

- Using a plain list's `pop(0)` for a large queue; `deque.popleft()` avoids shifting elements.
- Forgetting the visited/discovered check.
- Claiming DFS always gives the shortest route.
- Reporting a missing endpoint as merely unreachable; it is invalid input.

## Checkpoint

- [ ] I can trace BFS's queue and reconstruct a path.
- [ ] I can explain why visited state prevents loops.
- [ ] I know when "shortest" means fewest edges.

Previous: [Graph foundations](01-graph-foundations.md). Next: [Shortest paths](03-shortest-paths.md). [Track index](README.md) | [Progress](progress.md).

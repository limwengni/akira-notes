# Lesson 1 - Graph Foundations

> 45-60 minutes - Draw the graph before writing code.

**Goal:** describe a network as nodes, edges, and optional costs.

**Prerequisites:** Python dictionaries, lists, and loops. No graph library is needed.

**Focus:** a graph is a way to record relationships. Intersections can be nodes; roads between them can be edges.

---

## The vocabulary

| Term | Meaning | Road example |
|---|---|---|
| Node or vertex | One object in the network | An intersection |
| Edge | A connection between two nodes | A road |
| Directed edge | A connection usable in one direction | A one-way road |
| Undirected edge | A connection usable in both directions | A two-way road |
| Weight | A number attached to an edge | Travel time in minutes |
| Path | A sequence of connected nodes | Home -> School -> Park |
| Cycle | A route that returns to a previous node | A loop around a block |

A node's degree counts its connections in an undirected graph. In a directed graph, distinguish incoming and outgoing edges.

## Python example - An adjacency list

A dictionary of neighbor lists is an **adjacency list**. Every node gets a key, including nodes without outgoing roads.

This is a standalone example:

```python
roads = {
    "Home": ["Cafe", "School"],
    "Cafe": ["Office"],
    "School": ["Park"],
    "Park": ["Office"],
    "Office": [],
    "Isolated": [],
}

for place, destinations in roads.items():
    print(place, "->", destinations)

node_count = len(roads)
edge_count = sum(len(destinations) for destinations in roads.values())
print("Nodes:", node_count)
print("Directed edges:", edge_count)
print("Outgoing roads from Home:", len(roads["Home"]))
```

**Expected:** 6 nodes, 5 directed edges, and 2 outgoing roads from Home. Office can be reached but has no outgoing road; Isolated has no connections at all.

The data is directed. Home -> Cafe does not imply Cafe -> Home. To model a two-way road, explicitly add both directions. For an undirected graph stored that way, summing list lengths counts each ordinary edge twice.

## Adding costs

For routing, replace each neighbor list with a dictionary of travel times:

```python
weighted_roads = {
    "Home": {"Cafe": 2.0, "School": 1.0},
    "Cafe": {"Office": 5.0},
    "School": {"Park": 1.0},
    "Park": {"Office": 1.0},
    "Office": {},
    "Isolated": {},
}

route = ["Home", "School", "Park", "Office"]
minutes = sum(
    weighted_roads[start][end]
    for start, end in zip(route, route[1:])
)
print(minutes)  # 3.0
```

This second block is also standalone. `zip(route, route[1:])` gives each consecutive pair. A missing edge raises an error: a list of places is a valid path only when every consecutive road exists.

**Complexity:** an adjacency list takes O(V + E) space, where V is the number of nodes and E is the number of stored directed edges.

## Exercises

1. Add a node named Library and a road from School to Library. Predict the new node and edge counts.
2. Make Home-Cafe a two-way connection. Which additional dictionary entry is needed?
3. Find every node with no outgoing roads. Are they all unreachable?
4. Explain why a route with fewer roads can take more minutes.

**Hints:** iterate over `roads.items()`; reachability depends on incoming paths as well as outgoing degree. Compare the two-road route through Cafe with the three-road route through School and Park.

## Common mistakes

- Forgetting nodes with no outgoing edges.
- Assuming every edge has a reverse edge.
- Mixing kilometers, seconds, and minutes in the same weights.
- Treating a dictionary's display order as meaningful road geometry.

## Checkpoint

- [ ] I can identify nodes, edges, direction, and weights.
- [ ] I can calculate a path's total cost.
- [ ] I can explain the difference between an isolated node and a destination with no outgoing roads.

Next: [BFS and DFS](02-bfs-and-dfs.md). Return to the [track index](README.md) or update [progress](progress.md).

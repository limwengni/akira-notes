# Mini-project - A Traffic-aware Route Planner

> 2-4 sessions for the core project; allow another 2-3 for the optional GNN extension.

**Goal:** connect forecasting, evaluation, and weighted routing in a small explainable program.

**Prerequisites:** lessons 1-3 and 5. The optional extension also requires lesson 4 and the PyTorch track.

**Deliverable:** a Python script, its outputs, and a short explanation of assumptions and failures.

---

## Milestone 1 - Evaluate and route with persistence

Save the complete Dijkstra example from [lesson 3](03-shortest-paths.md) as `routing.py`. Put the following new script beside it and run it from that practice directory.

```python
from statistics import mean
from routing import shortest_path

# Each edge has six historical travel-time measurements in minutes.
histories = {
    ("Home", "Cafe"): [2, 2, 2, 2, 2, 2],
    ("Cafe", "Office"): [5, 5, 5, 5, 5, 5],
    ("Home", "School"): [1, 1, 1, 1, 8, 6],
    ("School", "Park"): [1, 1, 1, 1, 1, 1],
    ("Park", "Office"): [1, 1, 1, 1, 1, 1],
}

PLACES = ("Home", "Cafe", "School", "Park", "Office")

def as_graph(edge_costs):
    # Keep declared destinations even when all their roads are closed.
    graph = {place: {} for place in PLACES}
    for (start, end), cost in edge_costs.items():
        graph.setdefault(start, {})[end] = float(cost)
        graph.setdefault(end, {})
    return graph

# Backtest the last observed timestamp, keeping its target unseen.
errors = [
    abs(series[-2] - series[-1]) for series in histories.values()
]
print("Held-out persistence MAE:", round(mean(errors), 2))

# Forecast one step beyond the available observations.
next_costs = {edge: values[-1] for edge, values in histories.items()}
old_costs = {edge: values[0] for edge, values in histories.items()}
print("Old snapshot:", shortest_path(as_graph(old_costs), "Home", "Office"))
print("Predicted next:", shortest_path(as_graph(next_costs), "Home", "Office"))
```

**Expected:** MAE `0.4` minutes; the old snapshot chooses Home -> School -> Park -> Office at 3 minutes. The predicted next snapshot chooses Home -> Cafe -> Office at 7 minutes.

The future travel times have not been observed. This proves that the program routes using its forecasts; it does not prove the predicted route will be fastest in reality.

## Milestone 2 - Investigate failures

- Remove Park -> Office and confirm routing still works through Cafe.
- Remove both roads entering Office and expect `(inf, [])`.
- Try a negative or nonfinite cost and expect validation to reject it.
- Simulate a closure by removing an edge rather than assigning zero cost.
- Compare persistence with a mean computed from earlier observations.
- Write down the snapshot-routing assumption and the five-minute forecast horizon you chose.

## Milestone 3 - Optional GNN forecast experiment

Here the road segments become graph nodes. Two consecutive road segments are connected, so a downstream segment can receive upstream history. This is a **line-graph style representation**; it differs from using intersections as GNN nodes.

Save [lesson 4's class](04-graph-neural-networks.md) as `gnn.py`, beside `routing.py`. This complete extension trains on invented data and compares test MAE with persistence.

```python
import copy
import torch
from gnn import TinyTrafficGNN
from routing import shortest_path

torch.manual_seed(7)
edges = [
    ("Home", "Cafe"), ("Cafe", "Office"), ("Home", "School"),
    ("School", "Park"), ("Park", "Office"),
]
base = torch.tensor([2.0, 5.0, 1.0, 1.0, 1.0])
data = torch.stack([
    base + 0.3 * torch.sin(t / 5.0 + torch.arange(5))
    for t in range(80)
])  # [time, road segment]

# Row i receives from upstream road j. Diagonal starts at zero.
adjacency = torch.zeros(5, 5)
for i, (start, _) in enumerate(edges):
    for j, (_, end) in enumerate(edges):
        if end == start:
            adjacency[i, j] = 1.0

# Targets have timestamps 3..79. Divide by a fixed unit scale, not
# a statistic learned from validation/test data.
x = torch.stack([data[t-3:t].T / 10.0 for t in range(3, 80)])
y = data[3:].unsqueeze(-1) / 10.0
train_x, train_y = x[:47], y[:47]       # targets 3..49
val_x, val_y = x[47:62], y[47:62]      # targets 50..64
test_x, test_y = x[62:], y[62:]        # targets 65..79

model = TinyTrafficGNN(in_features=3)
optimizer = torch.optim.Adam(model.parameters(), lr=0.01)
best_loss, best_state = float("inf"), None
for _ in range(200):
    model.train()
    optimizer.zero_grad()
    loss = (model(train_x, adjacency) - train_y).square().mean()
    loss.backward()
    optimizer.step()
    model.eval()
    with torch.no_grad():
        val_loss = (model(val_x, adjacency) - val_y).square().mean().item()
    if val_loss < best_loss:
        best_loss = val_loss
        best_state = copy.deepcopy(model.state_dict())

model.load_state_dict(best_state)
model.eval()
with torch.no_grad():
    predicted = model(test_x, adjacency)
    learned_mae = (predicted - test_y).abs().mean().item() * 10
    persistence = test_x[:, :, -1:]
    baseline_mae = (persistence - test_y).abs().mean().item() * 10
    future_x = data[-3:].T.unsqueeze(0) / 10.0
    future_minutes = (
        model(future_x, adjacency).squeeze(0).squeeze(-1) * 10
    ).clamp_min(0.1)

graph = {node: {} for edge in edges for node in edge}
for (start, end), minutes in zip(edges, future_minutes.tolist()):
    graph[start][end] = minutes

print("Test GNN MAE, minutes:", round(learned_mae, 3))
print("Test persistence MAE, minutes:", round(baseline_mae, 3))
print("Predicted route:", shortest_path(graph, "Home", "Office"))
```

**Expected behavior:** finite MAEs and a valid route. The GNN is not guaranteed to beat persistence. Record both results. The tiny network uses three lagged values and one spatial aggregation, rather than a full temporal/recurrent architecture.

The minimum travel-time clamp is an explicit toy-model assumption. In real data, investigate invalid forecasts and closures rather than hiding them with a convenient clamp.

## Acceptance checks

- [ ] The core example produces the expected MAE and two routes.
- [ ] Unreachable destinations and invalid costs behave as documented.
- [ ] Predictions use only information available at the forecast origin.
- [ ] Units are consistent, and the route uses the intended predicted snapshot.
- [ ] If I tried the GNN, I selected weights using validation and evaluated test once afterward.
- [ ] I recorded whether the learned model beat persistence, without changing test data to improve the result.
- [ ] My notes explain that synthetic-data results do not establish real-world forecasting or routing quality.

**Write-up:** include commands, dependencies, outputs, one failed case, and a next experiment.

Previous: [Traffic prediction](05-traffic-prediction.md). Return to the [track index](README.md), [roadmap](../ROADMAP.md), or [progress tracker](progress.md).

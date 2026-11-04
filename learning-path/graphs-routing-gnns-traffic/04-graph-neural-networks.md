# Lesson 4 - Graph Neural Networks

> 60-90 minutes - Learn one message-passing layer before larger architectures.

**Goal:** combine each node's features with its neighbors' features and train a tiny graph model.

**Prerequisites:** graph lessons 1-3 and [PyTorch lessons 1-3](../pytorch-deep-learning/README.md#lessons). Install PyTorch using that track's setup.

**Focus:** a GNN learns from both values attached to nodes and the connections between them.

---

## What travels along an edge?

A **feature** is a number describing a node, such as recent travel time or queue length. A **message** is information sent from one node to a connected node.

A simple layer does three things:

1. Gather feature vectors from the node and its neighbors.
2. Aggregate them, for example by taking their mean.
3. Apply a shared trainable transformation.

All nodes use the same weights. The graph decides which information is combined.

## Shapes before code

| Symbol | Shape | Meaning |
|---|---|---|
| X | N by F | N nodes, F features per node |
| A | N by N | A[i, j] = 1 means node i receives from node j |
| H | N by hidden size | Learned node representations |
| Prediction | N by 1 | One predicted value for each node |

For this lesson, A describes a bidirectional three-node chain. Adding the identity matrix lets every node receive its own information. Row normalization makes each aggregation a mean.

## Python example - A trainable mean-aggregation GNN

Save this complete block as `gnn.py` in your practice directory. The optional project imports the class.

```python
import torch
from torch import nn

class TinyTrafficGNN(nn.Module):
    def __init__(self, in_features=2, hidden_size=8):
        super().__init__()
        self.hidden = nn.Linear(in_features, hidden_size)
        self.output = nn.Linear(hidden_size, 1)

    def forward(self, features, adjacency):
        with_self = adjacency + torch.eye(
            adjacency.shape[0],
            dtype=adjacency.dtype,
            device=adjacency.device,
        )
        mean_neighbors = with_self / with_self.sum(
            dim=1, keepdim=True
        )
        aggregated = mean_neighbors @ features
        hidden = torch.relu(self.hidden(aggregated))
        return self.output(hidden)

if __name__ == "__main__":
    torch.manual_seed(7)
    adjacency = torch.tensor([
        [0.0, 1.0, 0.0],
        [1.0, 0.0, 1.0],
        [0.0, 1.0, 0.0],
    ])
    features = torch.tensor([
        [0.2, 0.1],
        [0.6, 0.7],
        [0.9, 0.8],
    ])
    targets = torch.tensor([[0.3], [0.6], [0.8]])
    model = TinyTrafficGNN()
    optimizer = torch.optim.Adam(model.parameters(), lr=0.03)
    loss_fn = nn.MSELoss()

    initial_loss = loss_fn(model(features, adjacency), targets).item()
    for _ in range(250):
        optimizer.zero_grad()
        predictions = model(features, adjacency)
        loss = loss_fn(predictions, targets)
        loss.backward()
        optimizer.step()

    model.eval()
    with torch.no_grad():
        result = model(features, adjacency)
        print("Output shape:", tuple(result.shape))
        print("Initial MSE:", round(initial_loss, 4))
        print("Final MSE:", round(loss_fn(result, targets).item(), 4))
```

**Expected:** output shape `(3, 1)`; training should reduce MSE. Exact values depend on the PyTorch version and execution environment.

This fits three invented labels on one graph. It demonstrates trainable message passing; it does not establish forecasting accuracy. The layer uses a row-normalized mean, rather than the symmetric normalization of the original GCN paper.

## Why the graph matters

With the identity matrix as adjacency input, each node only sees itself after normalization. With the chain adjacency, it also sees connected nodes. The hidden layer learns how to use the aggregated numbers.

One message-passing layer sees one-hop neighbors. Repeated layers expand the receptive field, but too much averaging can make different nodes' representations look alike.

This dense N-by-N example favors readability. Large road networks usually need sparse graph representations and more careful modeling.

## Exercises

1. Calculate node 0's aggregated features by hand. Include its self-connection.
2. Replace adjacency with an all-zero matrix. Which information remains?
3. Add an isolated fourth node. Why does its self-connection keep the denominator nonzero?
4. Change the hidden size. Record training loss and explain why that alone does not prove better generalization.

**Hints:** node 0 averages rows 0 and 1 of X. Keep targets shaped `(N, 1)` so loss does not silently broadcast against `(N,)`.

## Checkpoint

- [ ] I can explain the N-by-F and N-by-N shapes.
- [ ] I can identify the learned parameters and the fixed graph structure.
- [ ] I understand why fitting one snapshot is different from forecasting future observations.

Further reading: [Kipf and Welling's GCN paper](https://arxiv.org/abs/1609.02907).

Previous: [Shortest paths](03-shortest-paths.md). Next: [Traffic prediction](05-traffic-prediction.md). [Track index](README.md) | [Progress](progress.md).

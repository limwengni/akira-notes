# Lesson 3 - Neural Networks

> 60-90 minutes - Learn the training loop on four examples.

**Goal:** train a small network that can represent a nonlinear decision.

**Prerequisites:** [autograd](02-autograd.md), Python classes, and tensor shapes.

**Focus:** layers learn parameters; activation functions make a stack of layers nonlinear.

---

## Why more than one linear layer?

A linear layer calculates `x @ W + b`. Stacking linear layers without an activation still gives a linear transformation.

A ReLU activation replaces negative values with zero. Hidden layers plus nonlinear activations allow a model to represent more complicated patterns.

A network with multiple learned layers is a small example of deep learning. Depth alone does not guarantee useful predictions; data, optimization, and evaluation still matter.

## The XOR problem

XOR is true when exactly one of two binary inputs is 1:

| Input | Label |
|---|---|
| 0, 0 | 0 |
| 0, 1 | 1 |
| 1, 0 | 1 |
| 1, 1 | 0 |

A single straight decision boundary cannot separate these two classes.

## Python example - Learn XOR

This script is standalone and fits all four points. It demonstrates representation and optimization, rather than generalization.

```python
import torch
from torch import nn

torch.manual_seed(7)
x = torch.tensor([
    [0.0, 0.0], [0.0, 1.0],
    [1.0, 0.0], [1.0, 1.0],
])
y = torch.tensor([[0.0], [1.0], [1.0], [0.0]])

class XorNetwork(nn.Module):
    def __init__(self):
        super().__init__()
        self.layers = nn.Sequential(
            nn.Linear(2, 16),
            nn.ReLU(),
            nn.Linear(16, 1),
        )

    def forward(self, inputs):
        return self.layers(inputs)

model = XorNetwork()
loss_fn = nn.BCEWithLogitsLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=0.03)

model.train()
for epoch in range(400):
    optimizer.zero_grad()
    logits = model(x)
    loss = loss_fn(logits, y)
    loss.backward()
    optimizer.step()
    if epoch in (0, 399):
        print("epoch", epoch, "loss", round(loss.item(), 4))

model.eval()
with torch.no_grad():
    probabilities = torch.sigmoid(model(x))
    labels = (probabilities >= 0.5).to(torch.int64)
    print("Probabilities:", probabilities.flatten().tolist())
    print("Labels:", labels.flatten().tolist())
```

**Expected behavior:** loss should fall and the learned labels should match `[0, 1, 1, 0]`. If they do not, inspect loss and training settings; exact probabilities vary.

## Match the loss to the task

| Task | Model output | Typical loss |
|---|---|---|
| Predict a number | Real-valued prediction | MSELoss |
| Binary classification | One raw logit per example | BCEWithLogitsLoss |
| One of several classes | Raw logit per class | CrossEntropyLoss |

A **logit** is a raw score. `BCEWithLogitsLoss` applies the required sigmoid-related calculation internally, so do not put a sigmoid before that loss. Convert logits to probabilities for interpretation afterward.

For binary loss here, targets are floating-point with the same shape as logits. For `CrossEntropyLoss` with class-index targets, labels are usually integer `torch.long` values shaped `(batch,)`.

## Exercises

1. Replace the hidden width 16 with 2. Compare several seeds and record failures.
2. Remove ReLU. Explain why two linear layers cannot solve XOR with a linear boundary.
3. Print the shape after each layer.
4. Count trainable parameters using `sum(p.numel() for p in model.parameters())`.

**Hints:** each linear layer has a weight matrix and a bias vector. The parameter count in this example is 65.

## Checkpoint

- [ ] I can identify parameters, activations, logits, loss, and optimizer.
- [ ] I can explain the order of the training loop.
- [ ] I know why fitting four points is not a held-out accuracy result.

Reference: [PyTorch neural-network tutorial](https://docs.pytorch.org/tutorials/beginner/basics/buildmodel_tutorial.html).

Previous: [Autograd](02-autograd.md). Next: [Data and training](04-data-and-training.md). [Track index](README.md) | [Progress](progress.md).

# Lesson 4 - Data and Training

> 60-90 minutes - Keep data preparation separate from learning.

**Goal:** split a dataset, train in batches, and monitor validation error.

**Prerequisites:** [neural networks](03-neural-networks.md) and basic indexing.

**Focus:** parameters learn from training data; validation helps choose settings; test estimates final performance after those choices.

---

## What each split is for

| Split | Purpose | Used for optimizer updates? |
|---|---|---|
| Training | Fit parameters | Yes |
| Validation | Compare settings and choose a checkpoint | No |
| Test | Evaluate the chosen final approach | No |

For independent synthetic examples, a random split is suitable. For forecasting, use the [chronological approach](../graphs-routing-gnns-traffic/05-traffic-prediction.md) instead.

A **batch** is a subset of training examples used in one optimizer update. An **epoch** is one pass through the training set.

## Python example - Batched regression

This standalone example creates its own data. It reserves test examples without evaluating them.

```python
import torch
from torch import nn
from torch.utils.data import DataLoader, TensorDataset

torch.manual_seed(7)
x = torch.linspace(-2.0, 2.0, 120).unsqueeze(1)
y = 3.0 * x + 0.5 + 0.1 * torch.randn_like(x)

indices = torch.randperm(len(x))
train_ids = indices[:80]
val_ids = indices[80:100]
test_ids = indices[100:]

# Fit normalization using training inputs only.
feature_mean = x[train_ids].mean(dim=0, keepdim=True)
feature_scale = x[train_ids].std(dim=0, keepdim=True).clamp_min(1e-6)
scaled_x = (x - feature_mean) / feature_scale

dataset = TensorDataset(scaled_x[train_ids], y[train_ids])
loader = DataLoader(dataset, batch_size=16, shuffle=True, num_workers=0)
model = nn.Linear(1, 1)
optimizer = torch.optim.SGD(model.parameters(), lr=0.05)
loss_fn = nn.MSELoss()

print("Split sizes:", len(train_ids), len(val_ids), len(test_ids))
for epoch in range(60):
    model.train()
    total_loss = 0.0
    for batch_x, batch_y in loader:
        optimizer.zero_grad()
        loss = loss_fn(model(batch_x), batch_y)
        loss.backward()
        optimizer.step()
        total_loss += loss.item() * len(batch_x)

    model.eval()
    with torch.no_grad():
        val_loss = loss_fn(model(scaled_x[val_ids]), y[val_ids]).item()

    if epoch in (0, 59):
        print(
            "epoch", epoch,
            "train MSE", round(total_loss / len(dataset), 4),
            "validation MSE", round(val_loss, 4),
        )
```

**Expected behavior:** split sizes `80 20 20`; training and validation MSE should become small. Exact losses vary. The per-epoch training number combines losses measured during updates, while validation is measured after the epoch.

`TensorDataset` keeps inputs and targets paired. `DataLoader` supplies batches and can shuffle training order without changing the split. `num_workers=0` keeps the example simple on Windows.

## Scaling without leakage

Standardization subtracts a mean and divides by a scale. Compute those values on training data only, then reuse them unchanged on validation, test, and future inputs.

The minimum scale avoids division by zero for a constant feature. Store the mean and scale with a saved model; otherwise the same raw input can produce a different prediction after reopening.

## Exercises

1. Change batch size from 16 to 1, then to 80. Count updates per epoch.
2. Disable shuffling. Does training still work for this small dataset?
3. Increase noise. Explain why even a correct linear model has nonzero prediction error.
4. Print the first training batch's input and target shapes.
5. Record two learning-rate trials using validation error. Keep test untouched.

**Hints:** with 80 examples and batch size 16 there are five updates per epoch. Use a fresh model for every trial.

## Common mistakes

- Shuffling inputs and targets separately.
- Fitting normalization on the entire dataset.
- Dividing summed batch means by the number of examples without weighting by batch size.
- Adjusting settings repeatedly after looking at test results.

## Checkpoint

- [ ] I can explain split roles, batches, epochs, and shuffling.
- [ ] I can identify exactly which examples affect gradients.
- [ ] I can reproduce the normalization used at inference.

Reference: [PyTorch datasets and DataLoaders](https://docs.pytorch.org/tutorials/beginner/basics/data_tutorial.html).

Previous: [Neural networks](03-neural-networks.md). Next: [Evaluation and checkpoints](05-evaluation-and-checkpoints.md). [Track index](README.md) | [Progress](progress.md).

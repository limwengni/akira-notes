# Mini-project - Train and Reopen a Small Classifier

> 2-4 sessions - Keep a record of the baseline and your final result.

**Goal:** train a nonlinear classifier, select weights using validation, and reproduce its predictions after reloading.

**Prerequisites:** all five lessons and a working CPU PyTorch installation.

**Deliverable:** one script, its printed results, a saved checkpoint, and a short write-up.

---

## The problem

Generate points inside a square. Class 1 means a point lies outside a circle centered at the origin; class 0 means it lies inside.

This nonlinear boundary is more interesting than a straight line, while synthetic data lets us understand exactly how labels are made.

## Milestones

1. Run the complete example and explain the input/output shapes.
2. Record the majority-class baseline and the neural network's test accuracy.
3. Verify saved/reloaded predictions.
4. Try one change using validation results, then describe what you learned.

## Complete starter example

Run this standalone script from your practice directory. It writes `circle_classifier.pt` there.

```python
import copy
import torch
from torch import nn
from torch.utils.data import DataLoader, TensorDataset

torch.manual_seed(7)
raw_x = torch.rand(600, 2) * 2.0 - 1.0
y = (raw_x.square().sum(dim=1) > 0.5).float().unsqueeze(1)
ids = torch.randperm(len(raw_x))
train_ids, val_ids, test_ids = ids[:400], ids[400:500], ids[500:]

mean = raw_x[train_ids].mean(dim=0, keepdim=True)
scale = raw_x[train_ids].std(dim=0, keepdim=True).clamp_min(1e-6)
x = (raw_x - mean) / scale
loader = DataLoader(
    TensorDataset(x[train_ids], y[train_ids]),
    batch_size=64, shuffle=True, num_workers=0,
)

def build_model():
    return nn.Sequential(
        nn.Linear(2, 16), nn.ReLU(),
        nn.Linear(16, 16), nn.ReLU(),
        nn.Linear(16, 1),
    )

model = build_model()
optimizer = torch.optim.Adam(model.parameters(), lr=0.01)
loss_fn = nn.BCEWithLogitsLoss()
best_loss, best_state = float("inf"), None

for _ in range(100):
    model.train()
    for batch_x, batch_y in loader:
        optimizer.zero_grad()
        loss = loss_fn(model(batch_x), batch_y)
        loss.backward()
        optimizer.step()

    model.eval()
    with torch.no_grad():
        val_loss = loss_fn(model(x[val_ids]), y[val_ids]).item()
    if val_loss < best_loss:
        best_loss = val_loss
        best_state = copy.deepcopy(model.state_dict())

model.load_state_dict(best_state)
model.eval()
majority_label = (y[train_ids].mean() >= 0.5).float()
with torch.no_grad():
    test_logits = model(x[test_ids])
    predicted = (torch.sigmoid(test_logits) >= 0.5).float()
    accuracy = (predicted == y[test_ids]).float().mean().item()
    baseline = (y[test_ids] == majority_label).float().mean().item()

torch.save({
    "model_state": best_state,
    "mean": mean,
    "scale": scale,
}, "circle_classifier.pt")
saved = torch.load(
    "circle_classifier.pt", map_location="cpu", weights_only=True
)
restored = build_model()
restored.load_state_dict(saved["model_state"])
restored.eval()
with torch.no_grad():
    reopened_x = (raw_x[test_ids] - saved["mean"]) / saved["scale"]
    reopened_logits = restored(reopened_x)

torch.testing.assert_close(test_logits, reopened_logits)
print("Best validation loss:", round(best_loss, 4))
print("Majority baseline accuracy:", round(baseline, 3))
print("Network test accuracy:", round(accuracy, 3))
print("Reload predictions matched.")
```

**Expected behavior:** the reload comparison passes. The network should usually beat the majority baseline on this learnable toy boundary, but record actual results rather than assuming a fixed accuracy.

The threshold 0.5 is fixed before test evaluation. The majority label comes from training targets; test targets only measure its accuracy.

## Exercises and experiments

- Replace the network with `nn.Linear(2, 1)`. Can a straight boundary represent the circle?
- Reduce the training set to 40 points. Inspect training and validation behavior.
- Add label noise to training examples and record its effect.
- Repeat with three seeds. Report variation, rather than selecting only the best test run.
- Print false positives and false negatives and inspect their coordinates.

**Hints:** plot points later if useful, but first inspect their distance from the circle boundary. Keep the same split when comparing settings and choose those settings using validation.

## Acceptance checks

- [ ] Input shape is `(batch, 2)`; logits and floating targets are `(batch, 1)`.
- [ ] Normalization uses training examples only.
- [ ] Optimizer updates never use validation or test examples.
- [ ] A copied validation-best state is selected before evaluating test.
- [ ] Baseline and model test results are both recorded.
- [ ] The checkpoint includes preprocessing, and reloaded logits match.
- [ ] I can explain a misclassified example and one limitation of synthetic data.

**Write-up:** include environment/package versions, commands, metrics, one failed experiment, and what you would test next.

Return to the [track index](README.md) or [progress tracker](progress.md). Continue to [GNNs](../graphs-routing-gnns-traffic/04-graph-neural-networks.md) if you want to apply these foundations to graph data.

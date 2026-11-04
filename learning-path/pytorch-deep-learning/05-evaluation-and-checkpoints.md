# Lesson 5 - Evaluation and Checkpoints

> 60-90 minutes - Treat reopening a model as part of the workflow.

**Goal:** evaluate without training and save enough state to reproduce predictions.

**Prerequisites:** [data and training](04-data-and-training.md).

**Focus:** model weights and input preprocessing must agree before and after a reload.

---

## Evaluation has two switches

`model.eval()` changes the behavior of layers such as dropout and batch normalization. It does not disable autograd.

`torch.no_grad()` disables gradient tracking inside its block. It does not switch dropout or batch normalization into evaluation behavior.

Use both for ordinary evaluation. The simple model below has neither dropout nor batch normalization, but the pattern remains useful.

## Python example - Train, save, and reopen

Run this standalone script in your practice directory. It creates `toy_checkpoint.pt` there. This is a tiny pipeline demonstration, not a broad generalization study.

```python
import torch
from torch import nn

torch.manual_seed(7)
raw_x = torch.tensor([[0.0], [1.0], [2.0], [3.0]])
targets = 2.0 * raw_x + 1.0
feature_mean = raw_x.mean(dim=0, keepdim=True)
feature_scale = raw_x.std(dim=0, keepdim=True).clamp_min(1e-6)
x = (raw_x - feature_mean) / feature_scale

model = nn.Linear(1, 1)
optimizer = torch.optim.SGD(model.parameters(), lr=0.05)
for _ in range(150):
    optimizer.zero_grad()
    loss = (model(x) - targets).square().mean()
    loss.backward()
    optimizer.step()

probe = torch.tensor([[1.5], [4.0]])
model.eval()
with torch.no_grad():
    before = model((probe - feature_mean) / feature_scale)

torch.save({
    "model_state": model.state_dict(),
    "feature_mean": feature_mean,
    "feature_scale": feature_scale,
}, "toy_checkpoint.pt")

checkpoint = torch.load(
    "toy_checkpoint.pt", map_location="cpu", weights_only=True
)
restored = nn.Linear(1, 1)
restored.load_state_dict(checkpoint["model_state"])
restored.eval()
with torch.no_grad():
    after = restored(
        (probe - checkpoint["feature_mean"]) / checkpoint["feature_scale"]
    )
    expected = 2.0 * probe + 1.0
    mae = (after - expected).abs().mean().item()

torch.testing.assert_close(before, after)
print("Reload matched.")
print("Predictions:", after.flatten().tolist())
print("Probe MAE:", round(mae, 4))
```

**Expected:** reload comparison passes and predictions are close to `[4.0, 9.0]`. The probe includes a value beyond the training range; success on this exact linear rule does not show reliable extrapolation for arbitrary data.

A state dictionary stores parameters and registered buffers. Recreate the same architecture before loading it. Saving optimizer state and the training step is additionally useful when resuming training, which this example does not cover.

## Choosing a checkpoint

During training, record validation loss after each epoch. Keep the weights with the best validation result and evaluate that choice on test.

Use `copy.deepcopy(model.state_dict())` for an in-memory best snapshot. Keeping a plain reference to `model.state_dict()` can allow later updates to change the supposedly saved tensors.

## Reading the metrics

For regression, MAE keeps the target's units; MSE penalizes large errors more strongly. For classification, accuracy is a starting point, but compare it with the majority-class baseline and inspect mistakes.

**Overfitting:** training performance keeps improving while validation performance worsens. More data, a smaller model, regularization, or stopping earlier may help. Choose changes using validation evidence.

## Exercises

1. Load into an architecture with two input features. Explain the shape mismatch.
2. Use the wrong feature mean after reload. Observe how predictions change.
3. Add `nn.Dropout` to a small network and compare repeated predictions in train and eval modes.
4. Explain which additional values you would save to resume optimizer updates.

**Hints:** a successful load is only one check. Compare actual predictions on the same raw inputs with the same preprocessing.

## Checkpoint

- [ ] I can explain eval mode versus gradient tracking.
- [ ] I can save weights and preprocessing, then verify reloaded predictions.
- [ ] I know the difference between choosing a checkpoint and evaluating the final model.

Reference: [PyTorch save/load tutorial](https://docs.pytorch.org/tutorials/beginner/basics/saveloadrun_tutorial.html).

Previous: [Data and training](04-data-and-training.md). Next: [Classifier project](mini-project.md). [Track index](README.md) | [Progress](progress.md).

# Lesson 1 - Tensor Foundations

> 45-75 minutes - Write down shapes before calculating.

**Goal:** represent batches of numbers and apply one calculation to every example.

**Prerequisites:** Python lists, arithmetic, and the [PyTorch setup](README.md#setup).

**Focus:** a tensor stores numbers with a shape, a data type, and a device.

---

## What is a tensor?

| Example | Shape | Interpretation |
|---|---|---|
| One number | `()` | Scalar |
| Three numbers | `(3,)` | Vector |
| Three rows and two columns | `(3, 2)` | Matrix |
| A batch of color images | `(batch, channels, height, width)` | Four-dimensional tensor |

A dimension describes an axis. The meaning of an axis comes from your data, so record it explicitly.

For a batch with three examples and two input features, use shape `(3, 2)`. A single predicted number per example has shape `(3, 1)`.

## Python example - A batch of linear predictions

This is a standalone script.

```python
import torch

# Rows are examples; columns are two input features.
x = torch.tensor([
    [1.0, 2.0],
    [3.0, 4.0],
    [5.0, 6.0],
], dtype=torch.float32)

weights = torch.tensor([[2.0], [-1.0]])
bias = torch.tensor([0.5])
predictions = x @ weights + bias
targets = torch.tensor([[0.0], [2.0], [4.0]])

assert predictions.shape == targets.shape
mse = (predictions - targets).square().mean()
print("x:", tuple(x.shape))
print("weights:", tuple(weights.shape))
print("predictions:", predictions.flatten().tolist())
print("MSE:", mse.item())

# Broadcast one offset for each feature column.
offset = torch.tensor([10.0, 100.0])
print("First shifted row:", (x + offset)[0].tolist())
```

**Expected:** shapes `(3, 2)` and `(2, 1)`; predictions `[0.5, 2.5, 4.5]`; MSE `0.25`; shifted first row `[11.0, 102.0]`.

## Matrix multiplication versus elementwise multiplication

`x @ weights` performs matrix multiplication: each row's weighted sum produces one number. The inside dimensions must agree: `(3, 2) @ (2, 1) -> (3, 1)`.

`x * x` multiplies corresponding elements. It does not combine feature columns.

**Broadcasting** lets compatible smaller shapes expand across larger ones. The bias is added to every row. Broadcasting is convenient, but a wrong target shape can quietly create an unintended calculation. Compare `(3, 1)` predictions with `(3, 1)` targets, rather than `(3,)`.

## Data types and devices

Use floating-point tensors for trainable numerical calculations. Integer tensors are useful for class indices and indexing. All tensors participating in an operation need compatible devices and data types.

These lessons stay on CPU. Moving only the model to a GPU while leaving inputs on CPU causes a device mismatch.

## Exercises

1. Add a fourth input row. Predict every shape that changes.
2. Replace the weights with `[[1.0], [1.0]]`. Calculate the predictions by hand.
3. Try `weights @ x`. Explain the dimension error.
4. Replace targets with shape `(3,)`. Inspect the shape of `predictions - targets` before calculating a loss.

**Hints:** broadcasting aligns dimensions from the right. `(3, 1)` and `(3,)` can produce a `(3, 3)` difference, which is not three paired errors.

## Checkpoint

- [ ] I can label the example and feature axes.
- [ ] I can predict matrix-multiplication output shapes.
- [ ] I can explain why target shape matters.

Reference: [PyTorch tensor tutorial](https://docs.pytorch.org/tutorials/beginner/basics/tensorqs_tutorial.html).

Next: [Autograd](02-autograd.md). [Track index](README.md) | [Progress](progress.md).

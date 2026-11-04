# Lesson 2 - Autograd

> 45-75 minutes - Follow one parameter through one update.

**Goal:** calculate gradients automatically and use them to reduce an error.

**Prerequisites:** [tensor foundations](01-tensor-foundations.md) and basic algebra.

**Focus:** a gradient describes how changing a parameter changes the loss.

---

## From prediction to learning

Suppose `prediction = w * x`. We know `x = 2` should give `y = 6`, but the initial weight is zero.

Use squared error: `loss = (w * x - y)^2`. At `w = 0`, the loss is 36. Its derivative with respect to w is `2 * (w*x - y) * x = -24`.

Gradient descent updates `w = w - learning_rate * gradient`. With learning rate 0.1, the first update changes w from 0 to 2.4, moving it toward 3.

## Python example - Learn one weight

This complete standalone script uses no optimizer class yet.

```python
import torch

w = torch.tensor(0.0, requires_grad=True)
x = torch.tensor(2.0)
target = torch.tensor(6.0)

for step in range(5):
    w.grad = None
    prediction = w * x
    loss = (prediction - target).square()
    loss.backward()

    print(
        "step", step,
        "loss", round(loss.item(), 4),
        "gradient", round(w.grad.item(), 4),
    )
    with torch.no_grad():
        w -= 0.1 * w.grad

print("Learned weight:", round(w.item(), 4))
```

**Expected:** the first loss is `36.0` and its gradient is `-24.0`. Loss decreases and the final weight is about `2.999`.

## What autograd remembers

When a tensor requires gradients, PyTorch tracks operations needed to differentiate a resulting loss. Calling `loss.backward()` computes gradients of that scalar loss.

Gradients accumulate by default. Setting `w.grad = None` clears the previous gradient before each step. In later lessons, `optimizer.zero_grad()` handles parameter gradients.

The parameter update happens inside `torch.no_grad()` because the update itself should not become part of the next differentiation graph. A new forward calculation builds the next graph.

`loss.item()` extracts a Python number for printing. Keep the tensor-valued loss for `backward()`; a Python float has no gradient history.

## Learning-rate intuition

A small learning rate can make progress slow. A large one can overshoot or diverge. This one-parameter example is easy to visualize; real networks have many parameters with interacting effects.

Reducing training loss means fitting the examples used for updates. It does not by itself show that unseen examples will be predicted well.

## Exercises

1. Change the learning rate to 0.01 and compare progress after five steps.
2. Try 0.3. Record whether the error settles down or grows.
3. Remove gradient clearing and inspect the changed behavior.
4. Change the target to 10. What weight should the model learn?

**Hints:** when `x = 2`, the correct weight is target divided by 2. Print each step before deciding what a learning-rate change did.

## Common mistakes

- Calling `backward()` on a detached value or `loss.item()`.
- Reusing old gradients unintentionally.
- Updating a leaf parameter in place while autograd is tracking the update.
- Assuming a gradient is the parameter's correct final value.

## Checkpoint

- [ ] I can explain the forward calculation, loss, backward calculation, and update.
- [ ] I know why gradients are cleared.
- [ ] I can predict the direction of the first update.

Reference: [PyTorch automatic differentiation tutorial](https://docs.pytorch.org/tutorials/beginner/basics/autogradqs_tutorial.html).

Previous: [Tensors](01-tensor-foundations.md). Next: [Neural networks](03-neural-networks.md). [Track index](README.md) | [Progress](progress.md).

# PyTorch, Neural Networks and Deep Learning - Beginner

> Five lessons plus a mini-project - Allow 1-2 sessions per lesson and 2-4 for the project.

**Goal:** Explain the training loop, choose a compatible loss, and show that reloading preserves predictions.

## Prerequisites

Python functions, lists, classes, and basic algebra. A derivative measures how much an output changes when an input changes; lesson 2 builds that intuition.

## Setup

Use the [shared Python setup](../README.md#python-setup). These examples use CPU tensors and synthetic data.

For Windows CPU learning, install PyTorch in the virtual environment:

```powershell
python -m pip install torch --index-url https://download.pytorch.org/whl/cpu
python -c "import torch; print(torch.__version__); print(torch.ones(2))"
```

If your platform or Python version needs another wheel, use the [official installation selector](https://pytorch.org/get-started/locally/). No GPU, torchvision, dataset download, or API key is required.

Use the [shared instructions for saving and running examples](../README.md#python-setup). Keep scripts imported by a lesson in the same practice directory.

---

## Lessons

| Order | Lesson | Focus |
|---|---|---|
| 1 | [Tensor foundations](01-tensor-foundations.md) | Read tensor shapes and perform batch calculations. |
| 2 | [Autograd](02-autograd.md) | Compute gradients and update parameters. |
| 3 | [Neural networks](03-neural-networks.md) | Build and train a small nonlinear model. |
| 4 | [Data and training](04-data-and-training.md) | Split data and train with batches. |
| 5 | [Evaluation and checkpoints](05-evaluation-and-checkpoints.md) | Evaluate, diagnose overfitting, and reload weights. |
| 6 | [Mini-project](mini-project.md) | A synthetic-data classifier with a baseline, validation checkpoints, held-out evaluation, and a reload check. |

## Progress and review

Use the [progress tracker](progress.md) after every session. Completion means you can run the example, explain it, and adapt it for an exercise.

[PyTorch Learn the Basics](https://docs.pytorch.org/tutorials/beginner/basics/intro.html) provides further practice.

See the [roadmap](../ROADMAP.md) for the recommended order across tracks, or return to [all learning journeys](../README.md).

# Lesson 5 - Traffic Prediction

> 60-90 minutes - Define the forecast time before choosing a model.

**Goal:** create historical input windows and measure a simple next-step forecast.

**Prerequisites:** Python lists and functions; [graph foundations](01-graph-foundations.md). The example uses only the standard library.

**Focus:** prediction requires a clear boundary between information available now and a value observed later.

---

## Define the task

Suppose a sensor records travel time every five minutes. At 08:00, predict the travel time at 08:05 using the last three observations.

- **Lookback:** three observations.
- **Horizon:** one observation ahead.
- **Input:** values already available at the prediction time.
- **Target:** the next observed travel time, in minutes.

**Persistence baseline:** predict that the next value equals the latest observed value. It is simple and often a useful reference.

**Mean absolute error (MAE):** average the absolute differences between predictions and targets. If the values are minutes, MAE is in minutes too.

## Python example - Windows and chronological splits

This is a complete standalone example.

```python
from statistics import mean

def make_windows(series, lookback):
    if lookback < 1 or len(series) <= lookback:
        raise ValueError("Need a positive lookback and at least one target.")
    return [
        (target_index, series[target_index-lookback:target_index],
         series[target_index])
        for target_index in range(lookback, len(series))
    ]

def mae(predictions, targets):
    if not predictions or len(predictions) != len(targets):
        raise ValueError("Need equally sized, nonempty sequences.")
    return mean(abs(p - y) for p, y in zip(predictions, targets))

# Invented travel times, not measurements from real roads.
travel_minutes = [10.0 + (t % 6) for t in range(30)]
windows = make_windows(travel_minutes, lookback=3)

# Split by target timestamp: train <18, validation 18-23, test 24-29.
train = [row for row in windows if row[0] < 18]
validation = [row for row in windows if 18 <= row[0] < 24]
test = [row for row in windows if row[0] >= 24]

print("Split sizes:", len(train), len(validation), len(test))
print("First window:", windows[0])
for name, split in [("validation", validation), ("test", test)]:
    predictions = [history[-1] for _, history, _ in split]
    targets = [target for _, _, target in split]
    print(name, "MAE:", round(mae(predictions, targets), 2))
```

**Expected:** split sizes `15 6 6`; the first window is `(3, [10.0, 11.0, 12.0], 13.0)`; both reported MAEs are about `1.67` minutes.

No training is needed for persistence. A trainable model uses the training split, chooses settings on validation, and evaluates the final choice on test.

## How to avoid leakage

Keep target times in chronological order. A random split can place future observations in training and make a forecasting experiment unrealistic.

An input window may reach back into the previous split because those historical measurements were available at prediction time. The target must stay in its assigned split.

This example evaluates **rolling one-step forecasts**: after each real observation arrives, it may be used for the next forecast. A forecast of several future steps made at one fixed time cannot use intermediate values that have not arrived yet.

Fit scaling parameters and any learned preprocessing on training data only. Choose a graph based on known roads or training information; a graph estimated using future traffic can also leak information.

## From a forecast to a route

A model could predict travel time directly, or predict speed and convert it:

`travel_minutes = distance_km / speed_kmh * 60`

Predicted speed must be positive. A closed road should be removed or marked unavailable. Do not turn missing measurements into a free, zero-minute road.

Run Dijkstra using a fixed set of predicted travel-time costs to obtain a route for that snapshot. A long trip where costs change as the vehicle moves needs a time-dependent routing formulation; the project keeps the snapshot assumption.

## Exercises

1. Change lookback to 5. Which split sizes change, and why?
2. Predict the training mean for every test target. Compare MAE with persistence.
3. Add a sudden traffic spike. Which forecast errors become largest?
4. Explain how you would forecast 15 minutes ahead when observations arrive every five minutes.

**Hints:** a three-step target is later than a one-step target. Every feature must still be available at the same prediction origin. Never compute the mean from test targets.

## Checkpoint

- [ ] I can identify the forecast origin, input window, horizon, and target.
- [ ] I can calculate MAE and explain its units.
- [ ] I can explain chronological splitting and rolling evaluation.

For a later research step, [DCRNN](https://arxiv.org/abs/1707.01926) combines graph-based spatial relationships with temporal forecasting.

Previous: [GNNs](04-graph-neural-networks.md). Next: [Mini-project](mini-project.md). [Track index](README.md) | [Progress](progress.md).

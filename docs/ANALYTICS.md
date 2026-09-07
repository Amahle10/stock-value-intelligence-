# Analytics methodology

This project focuses on statistical market behaviour rather than deterministic trading predictions.

## Price regime
The project computes rolling mean, median, standard deviation, z-score, and percentile rank to describe whether the current market observation is statistically expensive or cheap relative to recent history.

## Time pressure
Upward pressure is calculated when the close is above the previous close. Downward pressure is calculated when the close is below the previous close. These are then aggregated by hour and weekday.

## Historical analogue
Similar observations are matched against past conditions, then subsequent price direction is measured over a chosen horizon. This yields historical continuation/reversal probabilities, not forecasts.

## Machine Learning baseline
A logistic regression model uses price-derived features only and a chronological train/validation/test split to avoid data leakage.

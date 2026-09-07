export type PairSummary = {
  pair: string;
  latest_close: number;
  rolling_mean: number;
  rolling_median: number;
  z_score: number;
  percentile_rank: number;
  regime_score: number;
  regime_label: string;
};

export type LatestPrice = {
  pair: string;
  timestamp: string;
  price: number;
  bid?: number;
  ask?: number;
  spread?: number;
};

export type Reversal = {
  pair: string;
  horizon: string;
  similar_observations: number;
  price_higher_probability: number;
  price_lower_probability: number;
  average_future_return: number;
  median_future_return: number;
};

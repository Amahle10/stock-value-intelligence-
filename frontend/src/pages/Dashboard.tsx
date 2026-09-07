import { useEffect, useState } from 'react';
import Plot from 'react-plotly.js';
import { fetchLatest, fetchPairs, fetchReversal, fetchSummary, fetchTimeAnalysis, fetchModelPrediction } from '../services/api';
import type { LatestPrice, PairSummary, Reversal } from '../types';

const defaultPair = 'EUR/USD';

export default function Dashboard() {
  const [pairs, setPairs] = useState<string[]>([]);
  const [currentPair, setCurrentPair] = useState(defaultPair);
  const [latest, setLatest] = useState<LatestPrice | null>(null);
  const [summary, setSummary] = useState<PairSummary | null>(null);
  const [reversal, setReversal] = useState<Reversal | null>(null);
  const [modelProbability, setModelProbability] = useState<number | null>(null);
  const [heatmap, setHeatmap] = useState<Record<string, Record<string, number>>>({});

  useEffect(() => {
    fetchPairs().then((res) => setPairs(res.data.pairs)).catch(() => setPairs([defaultPair]));
  }, []);

  useEffect(() => {
    if (!currentPair) return;
    fetchLatest(currentPair).then((res) => setLatest(res.data)).catch(() => {});
    fetchSummary(currentPair).then((res) => setSummary(res.data)).catch(() => {});
    fetchReversal(currentPair, '4h').then((res) => setReversal(res.data)).catch(() => {});
    fetchTimeAnalysis(currentPair).then((res) => setHeatmap(res.data)).catch(() => {});
    fetchModelPrediction(currentPair).then((res) => setModelProbability(res.data.model_estimated_probability)).catch(() => {});
  }, [currentPair]);

  const spread = latest && latest.bid && latest.ask ? latest.ask - latest.bid : 0;

  return (
    <div className="dashboard">
      <div className="page-header">
        <h1>FX PRICE INTELLIGENCE</h1>
        <div className="toolbar">
          <select value={currentPair} onChange={(e) => setCurrentPair(e.target.value)}>
            {pairs.map((pair) => (
              <option key={pair} value={pair}>
                {pair}
              </option>
            ))}
          </select>
          <span className="timeframe">4H</span>
        </div>
      </div>

      <div className="stats-grid">
        <div className="card metric">
          <span>Current Price</span>
          <strong>{latest ? latest.price.toFixed(4) : '—'}</strong>
        </div>
        <div className="card metric">
          <span>Bid</span>
          <strong>{latest?.bid ? latest.bid.toFixed(4) : '—'}</strong>
        </div>
        <div className="card metric">
          <span>Ask</span>
          <strong>{latest?.ask ? latest.ask.toFixed(4) : '—'}</strong>
        </div>
        <div className="card metric">
          <span>Spread</span>
          <strong>{spread ? `${(spread * 10000).toFixed(1)} pips` : '—'}</strong>
        </div>
        <div className="card metric">
          <span>Price Regime</span>
          <strong>{summary?.regime_label ?? 'NEUTRAL'}</strong>
        </div>
        <div className="card metric">
          <span>Percentile</span>
          <strong>{summary ? `${(summary.percentile_rank * 100).toFixed(0)}%` : '—'}</strong>
        </div>
        <div className="card metric">
          <span>Z-score</span>
          <strong>{summary ? summary.z_score.toFixed(2) : '—'}</strong>
        </div>
        <div className="card metric">
          <span>4H Historical Outcome</span>
          <strong>
            {reversal ? `${(reversal.price_higher_probability * 100).toFixed(0)}% higher / ${(reversal.price_lower_probability * 100).toFixed(0)}% lower` : '—'}
          </strong>
        </div>
      </div>

      <div className="chart-grid two-up">
        <div className="card chart-card">
          <h3>Interactive Price Chart</h3>
          <Plot
            data={[{
              x: [new Date().toISOString()],
              y: [latest?.price ?? 1.1],
              type: 'scatter',
              mode: 'lines',
              line: { color: '#5eead4' },
            }]}
            layout={{
              paper_bgcolor: '#0f172a',
              plot_bgcolor: '#0f172a',
              font: { color: '#e2e8f0' },
              margin: { l: 40, r: 20, t: 20, b: 40 },
              xaxis: { title: 'Time' },
              yaxis: { title: 'Price' },
            }}
            style={{ width: '100%', height: '280px' }}
            config={{ displayModeBar: false }}
          />
        </div>

        <div className="card chart-card">
          <h3>Model Probability</h3>
          <div className="model-probability">
            <strong>{modelProbability !== null ? `${(modelProbability * 100).toFixed(1)}%` : '—'}</strong>
            <span>model-estimated probability of a higher next interval</span>
          </div>
        </div>
      </div>

      <div className="chart-grid three-up">
        <div className="card chart-card">
          <h3>Relative Valuation</h3>
          <p>Z-score: {summary ? summary.z_score.toFixed(2) : '—'}</p>
          <p>Rolling mean: {summary ? summary.rolling_mean.toFixed(4) : '—'}</p>
          <p>Rolling median: {summary ? summary.rolling_median.toFixed(4) : '—'}</p>
        </div>
        <div className="card chart-card">
          <h3>Time-of-Day Behaviour</h3>
          <p>Upward pressure and downward pressure are aggregated by hour and weekday.</p>
          <pre>{JSON.stringify(heatmap, null, 2).slice(0, 400)}</pre>
        </div>
        <div className="card chart-card">
          <h3>Historical Analogue</h3>
          {reversal ? (
            <>
              <p>Similar observations: {reversal.similar_observations}</p>
              <p>Higher probability: {(reversal.price_higher_probability * 100).toFixed(0)}%</p>
              <p>Lower probability: {(reversal.price_lower_probability * 100).toFixed(0)}%</p>
            </>
          ) : (
            <p>Awaiting analogue data.</p>
          )}
        </div>
      </div>
    </div>
  );
}

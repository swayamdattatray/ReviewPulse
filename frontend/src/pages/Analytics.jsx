import { useState, useEffect } from 'react';
import { api } from '../api';

export default function Analytics() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api.analytics()
      .then((res) => setData(res.data))
      .catch(() => {})
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <div className="loading">Loading analytics...</div>;
  if (!data) return <div className="loading">Failed to load analytics</div>;

  const { summary, sentiment_distribution, rating_distribution, top_products, recent_reviews } = data;

  const maxSentiment = Math.max(...Object.values(sentiment_distribution), 1);
  const maxRating = Math.max(...Object.values(rating_distribution), 1);

  return (
    <div>
      <div className="page-header">
        <h1>Analytics Dashboard</h1>
        <p>Insights across all products and reviews</p>
      </div>

      <div className="cards">
        <div className="card">
          <div className="card-icon blue">P</div>
          <div className="card-info">
            <h3>Products</h3>
            <p>{summary.total_products}</p>
          </div>
        </div>
        <div className="card">
          <div className="card-icon green">R</div>
          <div className="card-info">
            <h3>Reviews</h3>
            <p>{summary.total_reviews.toLocaleString()}</p>
          </div>
        </div>
        <div className="card">
          <div className="card-icon purple">★</div>
          <div className="card-info">
            <h3>Avg Rating</h3>
            <p>{summary.avg_rating}</p>
          </div>
        </div>
        <div className="card">
          <div className="card-icon green">✓</div>
          <div className="card-info">
            <h3>Verified</h3>
            <p>{summary.verified_pct}%</p>
          </div>
        </div>
      </div>

      <div className="analytics-grid">
        <div className="analytics-panel">
          <h3>Sentiment Distribution</h3>
          <div className="bar-chart">
            {Object.entries(sentiment_distribution).map(([label, count]) => (
              <div key={label} className="bar-row">
                <span className="bar-label">{label}</span>
                <div className="bar-track">
                  <div
                    className={`bar-fill sentiment-${label}`}
                    style={{ width: `${(count / maxSentiment) * 100}%` }}
                  />
                </div>
                <span className="bar-count">{count}</span>
              </div>
            ))}
          </div>
        </div>

        <div className="analytics-panel">
          <h3>Rating Distribution</h3>
          <div className="bar-chart">
            {[5, 4, 3, 2, 1].map((star) => (
              <div key={star} className="bar-row">
                <span className="bar-label">{star} ★</span>
                <div className="bar-track">
                  <div
                    className="bar-fill rating-bar"
                    style={{ width: `${((rating_distribution[star] || 0) / maxRating) * 100}%` }}
                  />
                </div>
                <span className="bar-count">{rating_distribution[star] || 0}</span>
              </div>
            ))}
          </div>
        </div>
      </div>

      <div className="analytics-grid">
        <div className="analytics-panel">
          <h3>Top Products</h3>
          <div className="top-list">
            {top_products.map((p, i) => (
              <div key={p.product_id} className="top-item">
                <span className="top-rank">#{i + 1}</span>
                <div className="top-info">
                  <strong>{p.name}</strong>
                  <span>{p.avg_rating.toFixed(1)} ★ &middot; {p.review_count} reviews</span>
                </div>
                <span className="top-price">${p.price.toFixed(2)}</span>
              </div>
            ))}
          </div>
        </div>

        <div className="analytics-panel">
          <h3>Recent Reviews</h3>
          <div className="top-list">
            {recent_reviews.map((r) => (
              <div key={r.review_id} className="top-item">
                <span className={`sentiment-tag ${r.sentiment}`}>{r.sentiment[0].toUpperCase()}</span>
                <div className="top-info">
                  <strong>{r.author_name} &middot; {r.product_name}</strong>
                  <span>{r.content.substring(0, 60)}...</span>
                </div>
                <span className="review-rating-sm">{'★'.repeat(r.rating)}</span>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}

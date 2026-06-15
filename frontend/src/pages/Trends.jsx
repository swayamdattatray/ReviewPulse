import { useState, useEffect } from 'react';
import { api } from '../api';

export default function Trends() {
  const [categoryTrends, setCategoryTrends] = useState([]);
  const [products, setProducts] = useState([]);
  const [selectedProduct, setSelectedProduct] = useState('');
  const [productTrends, setProductTrends] = useState(null);
  const [loading, setLoading] = useState(true);
  const [productLoading, setProductLoading] = useState(false);

  useEffect(() => {
    Promise.all([
      api.categoryTrends(),
      api.products({ per_page: 50 }),
    ])
      .then(([catRes, prodRes]) => {
        setCategoryTrends(catRes.data);
        setProducts(prodRes.data.products);
      })
      .catch(() => {})
      .finally(() => setLoading(false));
  }, []);

  useEffect(() => {
    if (!selectedProduct) { setProductTrends(null); return; }
    setProductLoading(true);
    api.productTrends(selectedProduct)
      .then((res) => setProductTrends(res.data))
      .catch(() => setProductTrends(null))
      .finally(() => setProductLoading(false));
  }, [selectedProduct]);

  if (loading) return <div className="loading">Loading trends...</div>;

  return (
    <div>
      <div className="page-header">
        <h1>Trends</h1>
        <p>Category and product-level trend analysis</p>
      </div>

      <div className="section">
        <h2>Category Performance</h2>
        <div className="trends-grid">
          {categoryTrends.map((c) => (
            <div key={c.category} className="trend-card">
              <h3>{c.category}</h3>
              <div className="trend-stats">
                <div className="trend-stat">
                  <span className="trend-stat-label">Avg Rating</span>
                  <span className="trend-stat-value">{c.avg_rating}</span>
                </div>
                <div className="trend-stat">
                  <span className="trend-stat-label">Reviews</span>
                  <span className="trend-stat-value">{c.review_count}</span>
                </div>
                <div className="trend-stat">
                  <span className="trend-stat-label">Sentiment</span>
                  <span className="trend-stat-value">{(c.avg_sentiment * 100).toFixed(0)}%</span>
                </div>
              </div>
              <div className="sentiment-bar">
                <div
                  className="sentiment-bar-fill"
                  style={{ width: `${c.avg_sentiment * 100}%` }}
                />
              </div>
            </div>
          ))}
        </div>
      </div>

      <div className="section">
        <h2>Product Trends</h2>
        <select
          value={selectedProduct}
          onChange={(e) => setSelectedProduct(e.target.value)}
          className="filter-select"
          style={{ maxWidth: 400, marginBottom: '1.5rem' }}
        >
          <option value="">Select a product...</option>
          {products.map((p) => (
            <option key={p.product_id} value={p.product_id}>{p.name}</option>
          ))}
        </select>

        {productLoading && <div className="loading">Loading product trends...</div>}

        {productTrends && !productLoading && (
          <>
            {productTrends.monthly_trends.length > 0 && (
              <div className="analytics-panel" style={{ marginBottom: '1.5rem' }}>
                <h3>Monthly Rating Trends</h3>
                <div className="monthly-chart">
                  {productTrends.monthly_trends.map((m) => (
                    <div key={m.month} className="monthly-bar-group">
                      <div className="monthly-bar-wrapper">
                        <div
                          className="monthly-bar"
                          style={{ height: `${(m.avg_rating / 5) * 100}%` }}
                        />
                      </div>
                      <span className="monthly-label">{m.month}</span>
                      <span className="monthly-count">{m.review_count}r</span>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {productTrends.sentiment_trends.length > 0 && (
              <div className="analytics-panel">
                <h3>Sentiment Over Time</h3>
                <div className="sentiment-timeline">
                  {productTrends.sentiment_trends.map((s) => {
                    const total = (s.positive || 0) + (s.neutral || 0) + (s.negative || 0);
                    return (
                      <div key={s.month} className="timeline-row">
                        <span className="timeline-month">{s.month}</span>
                        <div className="timeline-bar">
                          {total > 0 && (
                            <>
                              <div className="timeline-segment positive" style={{ width: `${((s.positive || 0) / total) * 100}%` }} />
                              <div className="timeline-segment neutral" style={{ width: `${((s.neutral || 0) / total) * 100}%` }} />
                              <div className="timeline-segment negative" style={{ width: `${((s.negative || 0) / total) * 100}%` }} />
                            </>
                          )}
                        </div>
                        <span className="timeline-count">{total}</span>
                      </div>
                    );
                  })}
                </div>
                <div className="legend">
                  <span className="legend-item"><span className="legend-dot positive" /> Positive</span>
                  <span className="legend-item"><span className="legend-dot neutral" /> Neutral</span>
                  <span className="legend-item"><span className="legend-dot negative" /> Negative</span>
                </div>
              </div>
            )}
          </>
        )}
      </div>
    </div>
  );
}

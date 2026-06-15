import { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import { api } from '../api';

export default function ProductDetail() {
  const { id } = useParams();
  const [product, setProduct] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api.product(id)
      .then((res) => setProduct(res.data))
      .catch(() => {})
      .finally(() => setLoading(false));
  }, [id]);

  if (loading) return <div className="loading">Loading...</div>;
  if (!product) return <div className="loading">Product not found</div>;

  const sentimentColor = (rating) => {
    if (rating >= 4) return 'green';
    if (rating >= 3) return 'yellow';
    return 'red';
  };

  return (
    <div>
      <Link to="/products" className="back-link">&larr; Back to Products</Link>

      <div className="product-detail">
        <div className="product-detail-header">
          <span className="product-brand">{product.brand}</span>
          <span className="product-category-tag">{product.category}</span>
        </div>
        <h1>{product.name}</h1>
        <p className="product-detail-desc">{product.description}</p>
        <div className="product-detail-stats">
          <div className="stat-box">
            <span className="stat-label">Price</span>
            <span className="stat-value">${product.price.toFixed(2)}</span>
          </div>
          <div className="stat-box">
            <span className="stat-label">Avg Rating</span>
            <span className={`stat-value ${sentimentColor(product.avg_rating)}`}>
              {product.avg_rating.toFixed(1)} / 5
            </span>
          </div>
          <div className="stat-box">
            <span className="stat-label">Reviews</span>
            <span className="stat-value">{product.review_count}</span>
          </div>
        </div>
      </div>

      <div className="section">
        <h2>Recent Reviews</h2>
        {product.reviews && product.reviews.length > 0 ? (
          <div className="reviews-list">
            {product.reviews.map((r) => (
              <div key={r.review_id} className="review-card">
                <div className="review-header">
                  <div>
                    <strong>{r.author_name}</strong>
                    {r.is_verified && <span className="verified-badge">Verified</span>}
                  </div>
                  <div className="review-meta">
                    <span className={`sentiment-tag ${r.sentiment}`}>{r.sentiment}</span>
                    <span className="review-rating">{'★'.repeat(r.rating)}{'☆'.repeat(5 - r.rating)}</span>
                  </div>
                </div>
                {r.title && <h4>{r.title}</h4>}
                <p>{r.content}</p>
                <div className="review-footer">
                  <span>{new Date(r.created_at).toLocaleDateString()}</span>
                  <span>{r.helpful_votes} helpful</span>
                </div>
              </div>
            ))}
          </div>
        ) : (
          <p className="empty-state">No reviews yet.</p>
        )}
      </div>
    </div>
  );
}

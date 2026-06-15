import { useState, useEffect } from 'react';
import { api } from '../api';

export default function Reviews() {
  const [reviews, setReviews] = useState([]);
  const [page, setPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const [total, setTotal] = useState(0);
  const [sentiment, setSentiment] = useState('');
  const [minRating, setMinRating] = useState('');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    setLoading(true);
    const params = { page, per_page: 15 };
    if (sentiment) params.sentiment = sentiment;
    if (minRating) params.min_rating = minRating;
    api.reviews(params)
      .then((res) => {
        setReviews(res.data.reviews);
        setTotalPages(res.data.pages);
        setTotal(res.data.total);
      })
      .catch(() => {})
      .finally(() => setLoading(false));
  }, [page, sentiment, minRating]);

  return (
    <div>
      <div className="page-header">
        <h1>Reviews</h1>
        <p>{total.toLocaleString()} total reviews across all products</p>
      </div>

      <div className="filters">
        <select
          value={sentiment}
          onChange={(e) => { setSentiment(e.target.value); setPage(1); }}
          className="filter-select"
        >
          <option value="">All Sentiments</option>
          <option value="positive">Positive</option>
          <option value="neutral">Neutral</option>
          <option value="negative">Negative</option>
        </select>
        <select
          value={minRating}
          onChange={(e) => { setMinRating(e.target.value); setPage(1); }}
          className="filter-select"
        >
          <option value="">All Ratings</option>
          <option value="5">5 Stars</option>
          <option value="4">4+ Stars</option>
          <option value="3">3+ Stars</option>
          <option value="2">2+ Stars</option>
          <option value="1">1+ Stars</option>
        </select>
      </div>

      {loading ? (
        <div className="loading">Loading...</div>
      ) : (
        <>
          <div className="reviews-list">
            {reviews.map((r) => (
              <div key={r.review_id} className="review-card">
                <div className="review-header">
                  <div>
                    <strong>{r.author_name}</strong>
                    {r.is_verified && <span className="verified-badge">Verified</span>}
                    <span className="review-product-link">&middot; {r.product_name}</span>
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

          {totalPages > 1 && (
            <div className="pagination">
              <button disabled={page <= 1} onClick={() => setPage(page - 1)}>Prev</button>
              <span>Page {page} of {totalPages}</span>
              <button disabled={page >= totalPages} onClick={() => setPage(page + 1)}>Next</button>
            </div>
          )}
        </>
      )}
    </div>
  );
}

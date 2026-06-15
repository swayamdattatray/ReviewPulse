import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { api } from '../api';

export default function Products() {
  const [products, setProducts] = useState([]);
  const [categories, setCategories] = useState([]);
  const [selectedCategory, setSelectedCategory] = useState('');
  const [search, setSearch] = useState('');
  const [page, setPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api.categories().then((res) => setCategories(res.data)).catch(() => {});
  }, []);

  useEffect(() => {
    setLoading(true);
    const params = { page, per_page: 12 };
    if (selectedCategory) params.category = selectedCategory;
    if (search) params.search = search;
    api.products(params)
      .then((res) => {
        setProducts(res.data.products);
        setTotalPages(res.data.pages);
      })
      .catch(() => {})
      .finally(() => setLoading(false));
  }, [page, selectedCategory, search]);

  const sentimentColor = (rating) => {
    if (rating >= 4) return 'green';
    if (rating >= 3) return 'yellow';
    return 'red';
  };

  return (
    <div>
      <div className="page-header">
        <h1>Products</h1>
        <p>Browse and analyze product reviews</p>
      </div>

      <div className="filters">
        <input
          type="text"
          placeholder="Search products..."
          value={search}
          onChange={(e) => { setSearch(e.target.value); setPage(1); }}
          className="search-input"
        />
        <select
          value={selectedCategory}
          onChange={(e) => { setSelectedCategory(e.target.value); setPage(1); }}
          className="filter-select"
        >
          <option value="">All Categories</option>
          {categories.map((c) => (
            <option key={c} value={c}>{c}</option>
          ))}
        </select>
      </div>

      {loading ? (
        <div className="loading">Loading...</div>
      ) : (
        <>
          <div className="product-grid">
            {products.map((p) => (
              <Link to={`/products/${p.product_id}`} key={p.product_id} className="product-card">
                <div className="product-card-header">
                  <span className="product-brand">{p.brand}</span>
                  <span className={`rating-badge ${sentimentColor(p.avg_rating)}`}>
                    {p.avg_rating.toFixed(1)}
                  </span>
                </div>
                <h3>{p.name}</h3>
                <p className="product-desc">{p.description}</p>
                <div className="product-card-footer">
                  <span className="product-price">${p.price.toFixed(2)}</span>
                  <span className="product-reviews">{p.review_count} reviews</span>
                </div>
              </Link>
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

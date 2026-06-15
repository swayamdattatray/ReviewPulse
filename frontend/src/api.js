const API_BASE = '/api/v1';

function getHeaders() {
  const headers = { 'Content-Type': 'application/json' };
  const token = localStorage.getItem('token');
  if (token) {
    headers['Authorization'] = `Bearer ${token}`;
  }
  return headers;
}

async function request(path, options = {}) {
  const res = await fetch(`${API_BASE}${path}`, {
    ...options,
    headers: { ...getHeaders(), ...options.headers },
  });
  const data = await res.json();
  if (!res.ok) {
    throw new Error(data.error || `Request failed with status ${res.status}`);
  }
  return data;
}

export const api = {
  health: () => request('/health'),
  root: () => request('/'),

  register: (body) =>
    request('/auth/register', { method: 'POST', body: JSON.stringify(body) }),
  login: (body) =>
    request('/auth/login', { method: 'POST', body: JSON.stringify(body) }),
  me: () => request('/auth/me'),

  products: (params = {}) => {
    const qs = new URLSearchParams(params).toString();
    return request(`/products${qs ? '?' + qs : ''}`);
  },
  product: (id) => request(`/products/${id}`),
  categories: () => request('/products/categories'),

  reviews: (params = {}) => {
    const qs = new URLSearchParams(params).toString();
    return request(`/reviews${qs ? '?' + qs : ''}`);
  },
  review: (id) => request(`/reviews/${id}`),
  createReview: (body) =>
    request('/reviews', { method: 'POST', body: JSON.stringify(body) }),

  analytics: () => request('/analytics/dashboard'),
  productTrends: (id) => request(`/trends/product/${id}`),
  categoryTrends: () => request('/trends/category'),
};

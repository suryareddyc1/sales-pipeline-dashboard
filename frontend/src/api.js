const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

async function request(path, options = {}) {
  const response = await fetch(`${API_BASE_URL}${path}`, options);
  if (!response.ok) {
    const error = await response.json().catch(() => ({}));
    throw new Error(error.detail || 'Something went wrong');
  }
  return response.json();
}

export const api = {
  loadSample: () => request('/pipeline/load-sample', { method: 'POST' }),
  uploadCsv: (file) => {
    const formData = new FormData();
    formData.append('file', file);
    return request('/pipeline/upload-csv', {
      method: 'POST',
      body: formData
    });
  },
  getSummary: () => request('/dashboard/summary'),
  getRevenueByMonth: () => request('/dashboard/revenue-by-month'),
  getRevenueByRegion: () => request('/dashboard/revenue-by-region'),
  getTopProducts: () => request('/dashboard/top-products'),
  getCategoryShare: () => request('/dashboard/category-share')
};

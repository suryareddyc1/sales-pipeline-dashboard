import { useEffect, useState } from 'react';
import { api } from './api';
import Dashboard from './components/Dashboard';
import FileUpload from './components/FileUpload';

export default function App() {
  const [dashboardData, setDashboardData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState('');
  const [error, setError] = useState('');

  async function fetchDashboard() {
    setLoading(true);
    setError('');
    try {
      const [summary, monthly, regions, products, categories] = await Promise.all([
        api.getSummary(),
        api.getRevenueByMonth(),
        api.getRevenueByRegion(),
        api.getTopProducts(),
        api.getCategoryShare()
      ]);
      setDashboardData({ summary, monthly, regions, products, categories });
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  async function loadSampleData() {
    setLoading(true);
    setError('');
    try {
      const result = await api.loadSample();
      setMessage(`${result.message}. Rows loaded: ${result.rows_loaded}`);
      await fetchDashboard();
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  async function handleCsvUpload(file) {
    setLoading(true);
    setError('');
    try {
      const result = await api.uploadCsv(file);
      setMessage(`${result.message}. Rows loaded: ${result.rows_loaded}`);
      await fetchDashboard();
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    fetchDashboard();
  }, []);

  return (
    <main className="page">
      <section className="hero">
        <div>
          <p className="eyebrow">End-to-end data engineering starter</p>
          <h1>Automated Sales Pipeline Dashboard</h1>
          <p className="subtitle">
            Upload CSV sales data, clean it with Pandas, query it using SQL,
            and visualize revenue insights with React and Plotly.
          </p>
        </div>
        <button className="primary-button" onClick={loadSampleData} disabled={loading}>
          Load Sample Data
        </button>
      </section>

      <FileUpload onUpload={handleCsvUpload} loading={loading} />

      {message && <div className="success">{message}</div>}
      {error && <div className="error">{error}</div>}
      {loading && <div className="loading">Processing pipeline...</div>}

      {dashboardData && <Dashboard data={dashboardData} />}
    </main>
  );
}

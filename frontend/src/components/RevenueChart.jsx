import { useEffect, useRef } from 'react';
import Plotly from 'plotly.js-basic-dist-min';

export default function RevenueChart({ title, data, layout = {} }) {
  const chartRef = useRef(null);
  const hasData = data?.some((series) => {
    if (Array.isArray(series.y)) return series.y.length > 0;
    if (Array.isArray(series.values)) return series.values.length > 0;
    return false;
  });

  useEffect(() => {
    if (!chartRef.current || !hasData) return;

    const finalLayout = {
      title: { text: title },
      autosize: true,
      margin: { t: 50, r: 24, b: 50, l: 60 },
      paper_bgcolor: 'rgba(0,0,0,0)',
      plot_bgcolor: 'rgba(0,0,0,0)',
      font: { family: 'Inter, system-ui, sans-serif' },
      ...layout
    };

    Plotly.react(chartRef.current, data, finalLayout, {
      responsive: true,
      displayModeBar: false
    });

    return () => {
      if (chartRef.current) Plotly.purge(chartRef.current);
    };
  }, [title, data, layout, hasData]);

  return (
    <div className="chart-card">
      {!hasData ? (
        <div className="empty-chart">
          <h3>{title}</h3>
          <p>No data yet. Click <strong>Load Sample Data</strong> or upload a CSV.</p>
        </div>
      ) : (
        <div ref={chartRef} className="plotly-chart" />
      )}
    </div>
  );
}

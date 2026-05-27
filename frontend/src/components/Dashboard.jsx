import MetricCard from './MetricCard';
import RevenueChart from './RevenueChart';

const currency = new Intl.NumberFormat('en-IN', {
  style: 'currency',
  currency: 'INR',
  maximumFractionDigits: 0
});

export default function Dashboard({ data }) {
  const { summary, monthly, regions, products, categories } = data;

  return (
    <section className="dashboard">
      <div className="metrics-grid">
        <MetricCard label="Total Revenue" value={currency.format(summary.total_revenue || 0)} />
        <MetricCard label="Total Orders" value={summary.total_orders || 0} />
        <MetricCard label="Customers" value={summary.total_customers || 0} />
        <MetricCard label="Avg Order Value" value={currency.format(summary.average_order_value || 0)} />
      </div>

      <div className="charts-grid">
        <RevenueChart
          title="Monthly Revenue"
          data={[
            {
              x: monthly.map((item) => item.month),
              y: monthly.map((item) => item.revenue),
              type: 'scatter',
              mode: 'lines+markers',
              fill: 'tozeroy',
              name: 'Revenue'
            }
          ]}
        />

        <RevenueChart
          title="Revenue by Region"
          data={[
            {
              x: regions.map((item) => item.region),
              y: regions.map((item) => item.revenue),
              type: 'bar',
              name: 'Revenue'
            }
          ]}
        />

        <RevenueChart
          title="Top Products"
          data={[
            {
              x: products.map((item) => item.revenue),
              y: products.map((item) => item.product),
              type: 'bar',
              orientation: 'h',
              name: 'Revenue'
            }
          ]}
          layout={{ yaxis: { automargin: true } }}
        />

        <RevenueChart
          title="Category Revenue Share"
          data={[
            {
              labels: categories.map((item) => item.category),
              values: categories.map((item) => item.revenue),
              type: 'pie',
              hole: 0.45
            }
          ]}
        />
      </div>
    </section>
  );
}

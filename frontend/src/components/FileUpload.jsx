import { useState } from 'react';

export default function FileUpload({ onUpload, loading }) {
  const [file, setFile] = useState(null);

  function submit(event) {
    event.preventDefault();
    if (file) onUpload(file);
  }

  return (
    <form className="upload-card" onSubmit={submit}>
      <div>
        <h2>Upload CSV</h2>
        <p>Expected columns: order_id, order_date, customer, region, product, category, quantity, unit_price, discount</p>
      </div>
      <div className="upload-actions">
        <input
          type="file"
          accept=".csv"
          onChange={(event) => setFile(event.target.files?.[0] || null)}
        />
        <button type="submit" disabled={!file || loading}>Run Pipeline</button>
      </div>
    </form>
  );
}

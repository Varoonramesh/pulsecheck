import { useEffect, useState } from "react";
import axios from "axios";
import "./App.css";

const API = "http://127.0.0.1:8000";

function App() {
  const [urls, setUrls] = useState([]);
  const [newUrl, setNewUrl] = useState("");

  const fetchUrls = async () => {
    try {
      const res = await axios.get(`${API}/api/urls`);
      setUrls(res.data);
    } catch (err) {
      console.error(err);
    }
  };

  useEffect(() => {
    fetchUrls();
    const timer = setInterval(fetchUrls, 5000);
    return () => clearInterval(timer);
  }, []);

  const addUrl = async (e) => {
    e.preventDefault();

    if (!newUrl.trim()) return;

    try {
      await axios.post(`${API}/api/urls`, {
        url: newUrl,
      });

      setNewUrl("");
      fetchUrls();
    } catch (err) {
      console.error(err);
      alert("Failed to add URL");
    }
  };

  const deleteUrl = async (id) => {
    try {
      await axios.delete(`${API}/api/urls/${id}`);
      fetchUrls();
    } catch (err) {
      console.error(err);
    }
  };

  return (
    <div className="container">
      <h1>PulseCheck</h1>

      <form onSubmit={addUrl}>
        <input
          type="text"
          placeholder="https://example.com"
          value={newUrl}
          onChange={(e) => setNewUrl(e.target.value)}
        />

        <button type="submit">
          Add URL
        </button>
      </form>

      <table>
        <thead>
          <tr>
            <th>ID</th>
            <th>URL</th>
            <th>Status</th>
            <th>Status Code</th>
            <th>Response Time</th>
            <th>Checked At</th>
            <th>Action</th>
          </tr>
        </thead>

        <tbody>          {urls.length === 0 ? (
            <tr>
              <td colSpan="7" style={{ textAlign: "center" }}>
                No URLs found
              </td>
            </tr>
          ) : (
            urls.map((item) => (
              <tr key={item.id}>
                <td>{item.id}</td>
                <td>{item.url}</td>
                <td>{item.status}</td>
                <td>{item.status_code ?? "-"}</td>
                <td>
                  {item.response_time_ms != null
                    ? `${item.response_time_ms} ms`
                    : "-"}
                </td>
                <td>
                  {item.checked_at
                    ? new Date(item.checked_at).toLocaleString()
                    : "-"}
                </td>
                <td>
                  <button
                    className="delete-btn"
                    onClick={() => deleteUrl(item.id)}
                  >
                    Delete
                  </button>
                </td>
              </tr>
            ))
          )}
        </tbody>
      </table>
    </div>
  );
}

export default App;

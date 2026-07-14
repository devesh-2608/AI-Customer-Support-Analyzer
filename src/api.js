const BASE_URL = "http://localhost:8000"

async function handle(res) {
  if (!res.ok) throw new Error(`Request failed: ${res.status}`)
  return res.json()
}

export const api = {
  getCustomers: () => fetch(`${BASE_URL}/api/customers`).then(handle),
  getHistory: (customerId) => fetch(`${BASE_URL}/api/customers/${customerId}/history`).then(handle),
  getTickets: () => fetch(`${BASE_URL}/api/tickets`).then(handle),
  getSummary: () => fetch(`${BASE_URL}/api/analytics/summary`).then(handle),
  getTrend: () => fetch(`${BASE_URL}/api/analytics/trend`).then(handle),
  uploadDoc: (file) => {
    const formData = new FormData()
    formData.append("file", file)
    return fetch(`${BASE_URL}/api/kb/upload`, { method: "POST", body: formData }).then(handle)
  },
  listDocs: () => fetch(`${BASE_URL}/api/kb/documents`).then(handle),
  askQuestion: (customerId, question) =>
    fetch(`${BASE_URL}/api/chat/query`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ customer_id: customerId, question }),
    }).then(handle),
}

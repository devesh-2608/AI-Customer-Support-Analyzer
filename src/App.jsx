import { useEffect, useState } from "react"
import { api } from "./api"
import ChatConsole from "./components/ChatConsole"
import CustomerPanel from "./components/CustomerPanel"
import Dashboard from "./pages/Dashboard"
import KnowledgeBase from "./pages/KnowledgeBase"

const TABS = [
  { key: "console", label: "Support Console" },
  { key: "dashboard", label: "Analytics" },
  { key: "kb", label: "Knowledge Base" },
]

export default function App() {
  const [tab, setTab] = useState("console")
  const [customers, setCustomers] = useState([])
  const [activeCustomer, setActiveCustomer] = useState(null)
  const [apiDown, setApiDown] = useState(false)

  useEffect(() => {
    api.getCustomers()
      .then((data) => {
        setCustomers(data)
        if (data.length > 0) setActiveCustomer(data[0])
      })
      .catch(() => setApiDown(true))
  }, [])

  return (
    <div className="h-screen flex flex-col">
      {/* Top bar */}
      <header className="border-b border-line px-5 py-3 flex items-center justify-between shrink-0">
        <div className="flex items-center gap-2">
          <div className="w-2 h-2 rounded-full bg-signal" />
          <h1 className="text-sm font-semibold text-ink">
            Support Console <span className="text-muted font-normal">/ AI Ticket Analyzer</span>
          </h1>
        </div>
        <nav className="flex gap-1">
          {TABS.map((t) => (
            <button
              key={t.key}
              onClick={() => setTab(t.key)}
              className={`px-3 py-1.5 rounded-md text-xs font-medium transition ${
                tab === t.key
                  ? "bg-signal/15 text-signal border border-signal/30"
                  : "text-muted hover:text-ink border border-transparent"
              }`}
            >
              {t.label}
            </button>
          ))}
        </nav>
      </header>

      {apiDown && (
        <div className="bg-alert/10 text-alert text-xs px-5 py-2 border-b border-alert/20 mono">
          Can't reach the backend at localhost:8000. Start it with: uvicorn app.main:app --reload
        </div>
      )}

      {/* Body */}
      <main className="flex-1 min-h-0">
        {tab === "console" && (
          <div className="grid grid-cols-[280px_1fr] h-full">
            <div className="border-r border-line min-h-0 overflow-hidden">
              <CustomerPanel
                customers={customers}
                activeCustomer={activeCustomer}
                setActiveCustomer={setActiveCustomer}
              />
            </div>
            <div className="min-h-0 overflow-hidden">
              <ChatConsole customers={customers} activeCustomer={activeCustomer} />
            </div>
          </div>
        )}

        {tab === "dashboard" && <Dashboard />}
        {tab === "kb" && <KnowledgeBase />}
      </main>
    </div>
  )
}

import { useEffect, useState } from "react"
import { api } from "../api"
import Badge from "./Badge"

export default function CustomerPanel({ customers, activeCustomer, setActiveCustomer }) {
  const [history, setHistory] = useState([])

  useEffect(() => {
    if (!activeCustomer) return
    api.getHistory(activeCustomer.id).then(setHistory).catch(() => setHistory([]))
  }, [activeCustomer])

  return (
    <div className="flex flex-col h-full">
      <div className="px-4 py-4 border-b border-line">
        <h2 className="text-sm font-semibold text-ink">Customers</h2>
      </div>

      <div className="border-b border-line max-h-52 overflow-y-auto">
        {customers.map((c) => (
          <button
            key={c.id}
            onClick={() => setActiveCustomer(c)}
            className={`w-full text-left px-4 py-2.5 border-l-2 transition ${
              activeCustomer?.id === c.id
                ? "border-signal bg-signal/5"
                : "border-transparent hover:bg-line/30"
            }`}
          >
            <div className="text-sm text-ink">{c.name}</div>
            <div className="text-xs text-muted mono">{c.plan}</div>
          </button>
        ))}
      </div>

      <div className="px-4 py-3 border-b border-line">
        <h3 className="text-xs font-semibold text-muted uppercase tracking-wide">
          History {activeCustomer ? `— ${activeCustomer.name}` : ""}
        </h3>
      </div>

      <div className="flex-1 overflow-y-auto px-4 py-3 space-y-3">
        {!activeCustomer && (
          <p className="text-xs text-muted">Select a customer to see their ticket history.</p>
        )}
        {activeCustomer && history.length === 0 && (
          <p className="text-xs text-muted">No prior tickets for this customer.</p>
        )}
        {history.map((t) => (
          <div key={t.id} className="border border-line rounded-lg p-3 space-y-1.5">
            <p className="text-xs text-ink leading-snug">{t.message}</p>
            <div className="flex flex-wrap gap-1">
              <Badge tone={t.sentiment}>{t.sentiment}</Badge>
              <Badge tone={t.status}>{t.status}</Badge>
              <Badge>{t.category}</Badge>
            </div>
            <p className="text-[10px] text-muted mono">
              {new Date(t.created_at).toLocaleDateString()}
            </p>
          </div>
        ))}
      </div>
    </div>
  )
}

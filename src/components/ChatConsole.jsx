import { useState } from "react"
import { api } from "../api"
import Badge from "./Badge"

export default function ChatConsole({ customers, activeCustomer }) {
  const [question, setQuestion] = useState("")
  const [loading, setLoading] = useState(false)
  const [thread, setThread] = useState([])
  const [error, setError] = useState(null)

  async function handleAsk(e) {
    e.preventDefault()
    if (!question.trim() || !activeCustomer) return
    setLoading(true)
    setError(null)
    const q = question
    setQuestion("")

    try {
      const result = await api.askQuestion(activeCustomer.id, q)
      setThread((prev) => [...prev, { question: q, ...result }])
    } catch (err) {
      setError("Couldn't reach the backend. Is FastAPI running on :8000?")
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="flex flex-col h-full">
      <div className="px-5 py-4 border-b border-line">
        <h2 className="text-sm font-semibold text-ink">Support Query Console</h2>
        <p className="text-xs text-muted mt-0.5">
          Answers are grounded in your uploaded knowledge base — nothing outside retrieved context.
        </p>
      </div>

      <div className="flex-1 overflow-y-auto px-5 py-4 space-y-4">
        {thread.length === 0 && (
          <div className="text-sm text-muted border border-dashed border-line rounded-lg p-6 text-center">
            Ask a customer support question below. The system will retrieve relevant
            knowledge-base passages, classify the ticket, and score sentiment/urgency.
          </div>
        )}

        {thread.map((item, i) => (
          <div key={i} className="space-y-2">
            <div className="flex justify-end">
              <div className="bg-line/60 rounded-lg px-3 py-2 max-w-[80%] text-sm text-ink">
                {item.question}
              </div>
            </div>
            <div className="bg-panel border border-line rounded-lg px-4 py-3 max-w-[85%] space-y-2.5">
              <p className="text-sm text-ink leading-relaxed">{item.answer}</p>
              <div className="flex flex-wrap gap-1.5 items-center pt-1">
                <Badge tone={item.sentiment}>{item.sentiment}</Badge>
                <Badge tone={item.urgency}>{item.urgency} urgency</Badge>
                <Badge>{item.category}</Badge>
                <Badge tone={item.confidence > 0.4 ? "positive" : "negative"}>
                  {Math.round(item.confidence * 100)}% KB confidence
                </Badge>
              </div>
              {item.sources.length > 0 && (
                <p className="text-xs text-muted mono">
                  sources: {item.sources.join(", ")}
                </p>
              )}
            </div>
          </div>
        ))}

        {loading && (
          <div className="text-xs text-muted mono animate-pulse">retrieving context, generating response…</div>
        )}
        {error && <div className="text-xs text-alert mono">{error}</div>}
      </div>

      <form onSubmit={handleAsk} className="border-t border-line p-4 flex gap-2">
        <input
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          placeholder={activeCustomer ? `Ask as ${activeCustomer.name}…` : "Select a customer first…"}
          disabled={!activeCustomer}
          className="flex-1 bg-panel border border-line rounded-lg px-3 py-2 text-sm text-ink placeholder:text-muted outline-none focus:border-signal/50"
        />
        <button
          type="submit"
          disabled={loading || !activeCustomer}
          className="bg-signal/15 text-signal border border-signal/30 rounded-lg px-4 py-2 text-sm font-medium hover:bg-signal/25 transition disabled:opacity-40"
        >
          Ask
        </button>
      </form>
    </div>
  )
}

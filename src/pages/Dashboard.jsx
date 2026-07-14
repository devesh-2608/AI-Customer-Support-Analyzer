import { useEffect, useState } from "react"
import { api } from "../api"
import {
  BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer,
  PieChart, Pie, Cell, LineChart, Line, CartesianGrid,
} from "recharts"

const PIE_COLORS = ["#4FD1A5", "#E8896B", "#7C8894"]

function StatCard({ label, value, sub }) {
  return (
    <div className="bg-panel border border-line rounded-lg p-4">
      <p className="text-xs text-muted uppercase tracking-wide">{label}</p>
      <p className="text-2xl font-semibold text-ink mono mt-1">{value}</p>
      {sub && <p className="text-xs text-muted mt-1">{sub}</p>}
    </div>
  )
}

export default function Dashboard() {
  const [summary, setSummary] = useState(null)
  const [trend, setTrend] = useState([])

  useEffect(() => {
    api.getSummary().then(setSummary).catch(() => {})
    api.getTrend().then(setTrend).catch(() => {})
  }, [])

  if (!summary) {
    return <div className="p-6 text-sm text-muted">Loading analytics…</div>
  }

  const categoryData = Object.entries(summary.category_breakdown || {}).map(([name, value]) => ({ name, value }))
  const sentimentData = Object.entries(summary.sentiment_breakdown || {}).map(([name, value]) => ({ name, value }))

  return (
    <div className="p-6 space-y-6 overflow-y-auto h-full">
      <div>
        <h2 className="text-sm font-semibold text-ink">Analytics Dashboard</h2>
        <p className="text-xs text-muted mt-0.5">Live view of ticket volume, sentiment, and knowledge-base performance.</p>
      </div>

      <div className="grid grid-cols-4 gap-4">
        <StatCard label="Total Tickets" value={summary.total_tickets} />
        <StatCard label="Resolution Rate" value={`${summary.resolution_rate}%`} />
        <StatCard label="Avg KB Confidence" value={summary.avg_kb_confidence} />
        <StatCard label="KB Gaps Found" value={summary.kb_gaps.length} sub="low-confidence questions" />
      </div>

      <div className="grid grid-cols-2 gap-4">
        <div className="bg-panel border border-line rounded-lg p-4">
          <p className="text-xs text-muted uppercase tracking-wide mb-3">Tickets by Category</p>
          <ResponsiveContainer width="100%" height={220}>
            <BarChart data={categoryData}>
              <XAxis dataKey="name" stroke="#7C8894" fontSize={11} />
              <YAxis stroke="#7C8894" fontSize={11} allowDecimals={false} />
              <Tooltip contentStyle={{ background: "#161C24", border: "1px solid #232B36", fontSize: 12 }} />
              <Bar dataKey="value" fill="#4FD1A5" radius={[4, 4, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>

        <div className="bg-panel border border-line rounded-lg p-4">
          <p className="text-xs text-muted uppercase tracking-wide mb-3">Sentiment Distribution</p>
          <ResponsiveContainer width="100%" height={220}>
            <PieChart>
              <Pie data={sentimentData} dataKey="value" nameKey="name" innerRadius={50} outerRadius={80}>
                {sentimentData.map((_, i) => (
                  <Cell key={i} fill={PIE_COLORS[i % PIE_COLORS.length]} />
                ))}
              </Pie>
              <Tooltip contentStyle={{ background: "#161C24", border: "1px solid #232B36", fontSize: 12 }} />
            </PieChart>
          </ResponsiveContainer>
        </div>
      </div>

      <div className="bg-panel border border-line rounded-lg p-4">
        <p className="text-xs text-muted uppercase tracking-wide mb-3">Ticket Volume Trend</p>
        <ResponsiveContainer width="100%" height={200}>
          <LineChart data={trend}>
            <CartesianGrid stroke="#232B36" strokeDasharray="3 3" />
            <XAxis dataKey="date" stroke="#7C8894" fontSize={11} />
            <YAxis stroke="#7C8894" fontSize={11} allowDecimals={false} />
            <Tooltip contentStyle={{ background: "#161C24", border: "1px solid #232B36", fontSize: 12 }} />
            <Line type="monotone" dataKey="count" stroke="#4FD1A5" strokeWidth={2} dot={false} />
          </LineChart>
        </ResponsiveContainer>
      </div>

      <div className="bg-panel border border-line rounded-lg p-4">
        <p className="text-xs text-muted uppercase tracking-wide mb-3">
          Knowledge Base Gaps <span className="text-muted/70 normal-case">— low-confidence questions worth documenting</span>
        </p>
        {summary.kb_gaps.length === 0 && <p className="text-xs text-muted">No gaps detected yet.</p>}
        <div className="space-y-2">
          {summary.kb_gaps.map((g, i) => (
            <div key={i} className="flex justify-between items-center text-xs border-b border-line pb-2">
              <span className="text-ink">{g.question}</span>
              <span className="text-alert mono">{Math.round(g.confidence * 100)}%</span>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}

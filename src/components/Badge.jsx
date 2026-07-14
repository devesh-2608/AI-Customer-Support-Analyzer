const TONES = {
  positive: "bg-signal/15 text-signal border-signal/30",
  negative: "bg-alert/15 text-alert border-alert/30",
  neutral: "bg-muted/15 text-muted border-muted/30",
  high: "bg-alert/15 text-alert border-alert/30",
  medium: "bg-amber-400/15 text-amber-300 border-amber-400/30",
  low: "bg-muted/15 text-muted border-muted/30",
  resolved: "bg-signal/15 text-signal border-signal/30",
  open: "bg-amber-400/15 text-amber-300 border-amber-400/30",
  default: "bg-line text-ink border-line",
}

export default function Badge({ children, tone = "default" }) {
  const cls = TONES[tone] || TONES.default
  return (
    <span className={`inline-flex items-center px-2 py-0.5 rounded text-xs font-medium border mono ${cls}`}>
      {children}
    </span>
  )
}

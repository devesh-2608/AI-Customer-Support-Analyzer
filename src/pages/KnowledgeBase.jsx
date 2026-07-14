import { useEffect, useState } from "react"
import { api } from "../api"

export default function KnowledgeBase() {
  const [docs, setDocs] = useState([])
  const [status, setStatus] = useState("")

  const refresh = () => api.listDocs().then(setDocs).catch(() => {})

  useEffect(() => { refresh() }, [])

  async function handleUpload(e) {
    const file = e.target.files[0]
    if (!file) return
    setStatus("Uploading & embedding…")
    try {
      const result = await api.uploadDoc(file)
      setStatus(`Stored ${result.chunks_stored} chunks from ${result.filename}`)
      refresh()
    } catch {
      setStatus("Upload failed — is the backend running?")
    }
  }

  return (
    <div className="p-6 space-y-5">
      <div>
        <h2 className="text-sm font-semibold text-ink">Knowledge Base</h2>
        <p className="text-xs text-muted mt-0.5">Upload company docs (PDF/TXT). They're chunked and embedded for retrieval.</p>
      </div>

      <label className="block border border-dashed border-line rounded-lg p-6 text-center cursor-pointer hover:border-signal/40 transition">
        <input type="file" accept=".pdf,.txt" onChange={handleUpload} className="hidden" />
        <p className="text-sm text-ink">Click to upload a document</p>
        <p className="text-xs text-muted mt-1">PDF or TXT</p>
      </label>

      {status && <p className="text-xs text-signal mono">{status}</p>}

      <div className="space-y-2">
        {docs.map((d, i) => (
          <div key={i} className="flex justify-between items-center border border-line rounded-lg px-3 py-2 text-sm">
            <span className="text-ink">{d.filename}</span>
            <span className="text-xs text-muted mono">{d.chunks} chunks</span>
          </div>
        ))}
        {docs.length === 0 && <p className="text-xs text-muted">No documents uploaded yet.</p>}
      </div>
    </div>
  )
}

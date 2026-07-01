import { useState } from 'react'
import { motion } from 'framer-motion'
import { Upload, Loader2, Lock } from 'lucide-react'
import SignalBar from './SignalBar'

export default function UploadCV() {
  const [file, setFile] = useState(null)
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState(null)
  const [error, setError] = useState('')
  const [setPrimary, setSetPrimary] = useState(false)
  const [password, setPassword] = useState('')

  async function handleSubmit(e) {
    e.preventDefault()
    if (!file) return
    setLoading(true)
    setError('')
    setResult(null)

    const formData = new FormData()
    formData.append('cv', file)
    formData.append('setPrimary', setPrimary)
    formData.append('password', password)

    try {
      const res = await fetch('/api/upload-cv', { method: 'POST', body: formData })
      const data = await res.json()
      if (!res.ok) throw new Error(data.error || 'Gagal memproses CV')
      setResult(data)
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="bg-panel/50 border border-line rounded-xl p-6 mb-10">
      <h2 className="font-display text-xl font-semibold text-white mb-1">Upload CV, Dapatkan Rekomendasi</h2>
      <p className="text-muted text-sm mb-5">
        Upload CV kamu (PDF) untuk melihat rekomendasi lowongan secara langsung.
      </p>

      <form onSubmit={handleSubmit} className="space-y-4">
        <input
          type="file"
          accept=".pdf"
          onChange={(e) => setFile(e.target.files[0])}
          className="block w-full text-sm text-muted file:mr-4 file:py-2 file:px-4 file:rounded-md file:border-0 file:bg-signal/10 file:text-signal file:font-mono file:text-sm hover:file:bg-signal/20"
        />

        <label className="flex items-center gap-2 text-sm text-muted">
          <input
            type="checkbox"
            checked={setPrimary}
            onChange={(e) => setSetPrimary(e.target.checked)}
            className="accent-signal"
          />
          Jadikan CV utama saya (butuh password)
        </label>

        {setPrimary && (
          <div className="relative">
            <Lock size={14} className="absolute left-3 top-1/2 -translate-y-1/2 text-muted" />
            <input
              type="password"
              placeholder="Password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="w-full bg-ink border border-line rounded-md pl-8 pr-3 py-2 text-sm focus:outline-none focus:border-signal/50"
            />
          </div>
        )}

        <button
          type="submit"
          disabled={!file || loading}
          className="inline-flex items-center gap-2 bg-signal/10 text-signal border border-signal/30 hover:bg-signal/20 transition-colors px-4 py-2 rounded-md text-sm font-medium disabled:opacity-40"
        >
          {loading ? <Loader2 size={16} className="animate-spin" /> : <Upload size={16} />}
          {loading ? 'Memproses...' : 'Analisis CV'}
        </button>
      </form>

      {error && <p className="text-alert text-sm mt-4">{error}</p>}

      {result && (
        <div className="mt-6 space-y-3">
          {result.savedAsPrimary && (
            <p className="text-signal text-sm font-mono">✓ CV tersimpan sebagai CV utama</p>
          )}
          <p className="text-white font-medium">Halo, {result.cvData.name || 'kandidat'} — berikut rekomendasi teratas:</p>
          {result.matches.slice(0, 5).map((m, i) => (
            <motion.div
              key={i}
              initial={{ opacity: 0, y: 8 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: i * 0.05 }}
              className="flex items-center justify-between bg-ink/50 border border-line rounded-md p-3"
            >
              <div>
                <p className="text-white text-sm font-medium">{m.job.title}</p>
                <p className="text-muted text-xs">{m.job.company}</p>
              </div>
              <SignalBar score={m.match.score} />
            </motion.div>
          ))}
        </div>
      )}
    </div>
  )
}
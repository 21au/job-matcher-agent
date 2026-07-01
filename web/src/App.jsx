import { useState, useEffect } from 'react'
import { motion } from 'framer-motion'
import { Search, Loader2 } from 'lucide-react'
import { supabase } from './supabaseClient'
import JobCard from './components/JobCard'
import StatsBar from './components/StatsBar'

function App() {
  const [matches, setMatches] = useState([])
  const [loading, setLoading] = useState(true)
  const [searchTerm, setSearchTerm] = useState('')
  const [sortBy, setSortBy] = useState('score')

  useEffect(() => {
    fetchMatches()
  }, [])

  async function fetchMatches() {
    setLoading(true)
    const { data, error } = await supabase
      .from('matches')
      .select(`
        id, score, matched_skills, missing_skills, summary, created_at,
        job_postings ( id, title, company, url, source )
      `)
      .order('score', { ascending: false })

    if (error) console.error('Error fetching matches:', error)
    else setMatches(data || [])
    setLoading(false)
  }

  const filteredMatches = matches
    .filter(m =>
      m.job_postings?.title?.toLowerCase().includes(searchTerm.toLowerCase()) ||
      m.job_postings?.company?.toLowerCase().includes(searchTerm.toLowerCase())
    )
    .sort((a, b) => sortBy === 'score' ? b.score - a.score : new Date(b.created_at) - new Date(a.created_at))

  const avgScore = matches.length > 0
    ? Math.round(matches.reduce((s, m) => s + m.score, 0) / matches.length)
    : 0
  const highMatches = matches.filter(m => m.score >= 70).length

  return (
    <div className="min-h-screen">
      <div className="relative overflow-hidden border-b border-line dot-grid">
        <div className="absolute top-0 left-0 h-px w-1/3 bg-gradient-to-r from-transparent via-signal to-transparent scan-line" />
        <div className="max-w-6xl mx-auto px-4 py-14">
          <motion.p
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            className="font-mono text-xs text-signal tracking-widest uppercase mb-3"
          >
            Signal scan — AI Engineer track
          </motion.p>
          <motion.h1
            initial={{ opacity: 0, y: -12 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: 0.1 }}
            className="font-display text-3xl sm:text-5xl font-semibold text-white leading-tight max-w-2xl"
          >
            Job Matcher Dashboard
          </motion.h1>
          <motion.p
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.25 }}
            className="text-muted mt-3 max-w-lg"
          >
            Agent AI memindai lowongan baru secara berkala dan mencocokkannya
            dengan profil kandidat secara otomatis.
          </motion.p>
        </div>
      </div>

      <div className="max-w-6xl mx-auto px-4 py-10">
        {!loading && <StatsBar totalJobs={matches.length} avgScore={avgScore} highMatches={highMatches} />}

        <div className="flex flex-col sm:flex-row gap-3 mb-8">
          <div className="relative flex-1">
            <Search size={16} className="absolute left-3 top-1/2 -translate-y-1/2 text-muted" />
            <input
              type="text"
              placeholder="Cari lowongan atau perusahaan..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="w-full bg-panel/50 border border-line rounded-md pl-9 pr-4 py-2.5 text-sm font-mono placeholder:text-muted focus:outline-none focus:border-signal/50 transition-colors"
            />
          </div>
          <select
            value={sortBy}
            onChange={(e) => setSortBy(e.target.value)}
            className="bg-panel/50 border border-line rounded-md px-4 py-2.5 text-sm font-mono focus:outline-none focus:border-signal/50 transition-colors"
          >
            <option value="score">Sinyal tertinggi</option>
            <option value="recent">Terbaru</option>
          </select>
        </div>

        {loading ? (
          <div className="flex justify-center items-center py-24">
            <Loader2 className="animate-spin text-signal" size={28} />
          </div>
        ) : filteredMatches.length === 0 ? (
          <div className="text-center py-24 text-muted font-mono text-sm">
            Belum ada sinyal terdeteksi.
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {filteredMatches.map((m, i) => (
              <JobCard key={m.id} job={m.job_postings} match={m} index={i} />
            ))}
          </div>
        )}
      </div>
    </div>
  )
}

export default App
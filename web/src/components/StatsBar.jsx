import { motion } from 'framer-motion'

function Readout({ label, value, delay }) {
  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{ duration: 0.4, delay }}
      className="border-l border-line pl-4"
    >
      <p className="font-mono text-2xl sm:text-3xl text-white">{value}</p>
      <p className="text-muted text-xs uppercase tracking-wider mt-1">{label}</p>
    </motion.div>
  )
}

export default function StatsBar({ totalJobs, avgScore, highMatches }) {
  return (
    <div className="flex flex-wrap gap-8 mb-10 pb-8 border-b border-line">
      <Readout label="Lowongan dipindai" value={totalJobs} delay={0} />
      <Readout label="Rata-rata sinyal" value={`${avgScore}%`} delay={0.08} />
      <Readout label="Kecocokan tinggi" value={highMatches} delay={0.16} />
    </div>
  )
}
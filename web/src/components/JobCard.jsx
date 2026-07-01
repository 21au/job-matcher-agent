import { motion } from 'framer-motion'
import { ArrowUpRight } from 'lucide-react'
import SignalBar from './SignalBar'

export default function JobCard({ job, match, index }) {
return (
    <motion.div
    initial={{ opacity: 0, y: 16 }}
    animate={{ opacity: 1, y: 0 }}
    transition={{ duration: 0.35, delay: index * 0.04 }}
    whileHover={{ y: -3 }}
    className="group bg-panel/60 backdrop-blur border border-line rounded-lg p-5 hover:border-signal/40 transition-colors"
    >
    <div className="flex justify-between items-start mb-1">
        <p className="font-mono text-xs text-muted uppercase tracking-wider">{job.source || 'manual'}</p>
        <SignalBar score={match.score} />
    </div>

    <h3 className="font-display text-lg font-medium text-white mt-2 leading-snug">
        {job.title}
    </h3>
    <p className="text-muted text-sm mb-4">{job.company}</p>

    <p className="text-slate-300 text-sm mb-4 line-clamp-2">{match.summary}</p>

    <div className="space-y-2 mb-5">
        {match.matched_skills?.length > 0 && (
        <div className="flex flex-wrap gap-1.5">
            {match.matched_skills.map((skill, i) => (
            <span key={i} className="text-xs font-mono bg-cyanx/10 text-cyanx px-2 py-0.5 rounded border border-cyanx/20">
                {skill}
            </span>
            ))}
        </div>
        )}
        {match.missing_skills?.length > 0 && (
        <div className="flex flex-wrap gap-1.5">
            {match.missing_skills.map((skill, i) => (
            <span key={i} className="text-xs font-mono bg-alert/10 text-alert px-2 py-0.5 rounded border border-alert/20">
                {skill}
            </span>
            ))}
        </div>
        )}
</div>

    
    <a href={job.url}
        target="_blank"
        rel="noopener noreferrer"
        className="inline-flex items-center gap-1 text-sm text-signal hover:text-signal2 transition-colors font-medium"
    >
        Lihat lowongan
        <ArrowUpRight size={15} className="group-hover:translate-x-0.5 group-hover:-translate-y-0.5 transition-transform" />
    </a>
    </motion.div>
)
}
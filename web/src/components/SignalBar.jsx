export default function SignalBar({ score }) {
  const segments = 10
  const filled = Math.round((score / 100) * segments)

  const colorFor = (i) => {
    if (i >= filled) return 'bg-line'
    if (score >= 80) return 'bg-signal2'
    if (score >= 60) return 'bg-signal'
    return 'bg-alert'
  }

  return (
    <div className="flex items-center gap-3">
      <div className="flex gap-[3px]">
        {Array.from({ length: segments }).map((_, i) => (
          <div
            key={i}
            className={`w-1.5 h-4 rounded-sm transition-colors ${colorFor(i)}`}
          />
        ))}
      </div>
      <span className="font-mono text-sm text-white">{score}</span>
    </div>
  )
}
const modules = [
  'CEO approvals',
  'Trend intelligence',
  'Platform-aware content',
  'Reel generation',
  'Sales outreach',
  'Operations risk control',
  'Analytics learning',
  'Make.com execution',
]

export default function Home() {
  return (
    <main className="min-h-screen bg-slate-950 text-white">
      <section className="mx-auto max-w-6xl px-6 py-20">
        <p className="text-sm uppercase tracking-[0.3em] text-cyan-300">Autonomous Company OS</p>
        <h1 className="mt-4 text-5xl font-bold tracking-tight">Operate content, sales, approvals, and analytics from one AI command center.</h1>
        <p className="mt-6 max-w-3xl text-lg text-slate-300">The frontend is intentionally an operator console: it starts approved runs, reviews queues, and monitors execution. Intelligence remains in the FastAPI/LangGraph backend.</p>
        <div className="mt-10 grid gap-4 md:grid-cols-4">
          {modules.map((module) => (
            <div key={module} className="rounded-2xl border border-white/10 bg-white/5 p-5 shadow-2xl">
              <div className="text-sm font-semibold text-cyan-200">{module}</div>
            </div>
          ))}
        </div>
      </section>
    </main>
  )
}

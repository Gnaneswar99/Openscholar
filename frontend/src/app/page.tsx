import Link from 'next/link';
import {
  Brain,
  Search,
  FileText,
  CheckCircle2,
  GitBranch,
  Zap,
} from 'lucide-react';

export default function HomePage() {
  return (
    <main className="min-h-screen">
      {/* Hero */}
      <section className="bg-gradient-to-br from-indigo-50 via-white to-purple-50 px-4 py-20">
        <div className="max-w-5xl mx-auto text-center">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-scholar/10 text-scholar text-xs font-medium mb-6">
            <Zap className="w-3.5 h-3.5" />
            Multi-Agent AI Research, Powered by Claude
          </div>
          <h1 className="text-5xl md:text-6xl font-bold tracking-tight">
            Research at <span className="text-scholar">the speed of thought.</span>
          </h1>
          <p className="mt-6 text-lg text-slate-600 max-w-2xl mx-auto">
            Ask any question — OpenScholar dispatches a team of specialized AI agents to
            search the web, read papers, and synthesize a fully-cited research report in
            minutes.
          </p>
          <div className="mt-10 flex flex-wrap justify-center gap-3">
            <Link href="/register" className="btn-primary px-6 py-3">
              Start researching free
            </Link>
            <Link href="/login" className="btn-secondary px-6 py-3">
              Sign in
            </Link>
          </div>
        </div>
      </section>

      {/* Features */}
      <section className="px-4 py-20">
        <div className="max-w-5xl mx-auto">
          <div className="grid md:grid-cols-3 gap-6">
            <FeatureCard
              icon={Brain}
              title="Multi-Agent Orchestration"
              body="A Planner decomposes your question, parallel Researchers gather evidence, a Synthesizer writes the report, and a Critic scores every claim."
            />
            <FeatureCard
              icon={Search}
              title="Cited Sources"
              body="Every claim links back to its source — web, arXiv, Semantic Scholar, or your own uploaded documents."
            />
            <FeatureCard
              icon={FileText}
              title="Publication-Ready Reports"
              body="Markdown reports with executive summary, structured sections, and exports to PDF, DOCX, or Markdown."
            />
            <FeatureCard
              icon={CheckCircle2}
              title="Confidence Scoring"
              body="Built-in RAGAS evaluation grades faithfulness and relevance. Know what to trust."
            />
            <FeatureCard
              icon={GitBranch}
              title="Reasoning Tree"
              body="See exactly how the agents reasoned — every sub-question, every search, every source."
            />
            <FeatureCard
              icon={Zap}
              title="Real-time Streaming"
              body="Watch the agents think live as the report builds. Cancel anytime."
            />
          </div>
        </div>
      </section>

      {/* Tech */}
      <section className="bg-slate-900 text-slate-300 px-4 py-16">
        <div className="max-w-5xl mx-auto text-center">
          <p className="text-xs uppercase tracking-wider text-slate-500 mb-4">
            Built on
          </p>
          <div className="flex flex-wrap justify-center gap-x-8 gap-y-2 text-sm font-medium text-slate-300">
            <span>FastAPI</span>
            <span>·</span>
            <span>Next.js 14</span>
            <span>·</span>
            <span>LangGraph</span>
            <span>·</span>
            <span>Anthropic Claude</span>
            <span>·</span>
            <span>Tavily</span>
            <span>·</span>
            <span>pgvector</span>
            <span>·</span>
            <span>Postgres</span>
            <span>·</span>
            <span>Docker</span>
          </div>
        </div>
      </section>

      <footer className="px-4 py-8 text-center text-sm text-slate-500">
        <p>
          OpenScholar · Open-source ·{' '}
          <a
            href="https://github.com/Gnaneswar99/openscholar"
            className="text-scholar hover:underline"
          >
            View on GitHub
          </a>
        </p>
      </footer>
    </main>
  );
}

function FeatureCard({
  icon: Icon,
  title,
  body,
}: {
  icon: typeof Brain;
  title: string;
  body: string;
}) {
  return (
    <div className="card p-6">
      <div className="w-10 h-10 rounded-lg bg-scholar/10 flex items-center justify-center mb-4">
        <Icon className="w-5 h-5 text-scholar" />
      </div>
      <h3 className="font-semibold">{title}</h3>
      <p className="text-sm text-slate-600 mt-2">{body}</p>
    </div>
  );
}

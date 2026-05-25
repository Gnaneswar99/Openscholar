'use client';

import { useState, type FormEvent } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import {
  Brain,
  Loader2,
  Search,
  LogOut,
  FileText,
  Clock,
  CheckCircle2,
  XCircle,
} from 'lucide-react';
import { researchApi } from '@/lib/research-api';
import { useAuthStore } from '@/hooks/useAuthStore';
import { formatRelative, cn } from '@/lib/utils';
import type { ResearchJobStatus } from '@/types';

const statusConfig: Record<
  ResearchJobStatus,
  { label: string; color: string; icon: typeof Clock }
> = {
  pending: { label: 'Queued', color: 'bg-slate-100 text-slate-600', icon: Clock },
  planning: { label: 'Planning', color: 'bg-blue-100 text-blue-700', icon: Brain },
  researching: { label: 'Researching', color: 'bg-amber-100 text-amber-700', icon: Search },
  synthesizing: { label: 'Synthesizing', color: 'bg-purple-100 text-purple-700', icon: FileText },
  critiquing: { label: 'Critiquing', color: 'bg-pink-100 text-pink-700', icon: CheckCircle2 },
  completed: { label: 'Completed', color: 'bg-emerald-100 text-emerald-700', icon: CheckCircle2 },
  failed: { label: 'Failed', color: 'bg-red-100 text-red-700', icon: XCircle },
};

export default function ResearchPage() {
  const router = useRouter();
  const qc = useQueryClient();
  const { user, logout, isAuthenticated } = useAuthStore();
  const [query, setQuery] = useState('');

  // Client-side auth redirect
  if (typeof window !== 'undefined' && !isAuthenticated()) {
    router.push('/login');
  }

  const jobs = useQuery({
    queryKey: ['research-jobs'],
    queryFn: () => researchApi.list(50, 0),
    refetchInterval: 5_000,
  });

  const createJob = useMutation({
    mutationFn: (q: string) => researchApi.create(q),
    onSuccess: () => {
      setQuery('');
      qc.invalidateQueries({ queryKey: ['research-jobs'] });
    },
  });

  const handleSubmit = (e: FormEvent) => {
    e.preventDefault();
    if (query.trim().length >= 10) createJob.mutate(query.trim());
  };

  const handleLogout = () => {
    logout();
    router.push('/');
  };

  return (
    <div className="min-h-screen bg-slate-50">
      {/* Header */}
      <header className="bg-white border-b border-slate-200">
        <div className="max-w-6xl mx-auto px-4 py-3 flex items-center justify-between">
          <Link href="/research" className="flex items-center gap-2.5">
            <div className="w-8 h-8 rounded-lg bg-scholar flex items-center justify-center">
              <Brain className="w-4 h-4 text-white" />
            </div>
            <span className="font-semibold">OpenScholar</span>
          </Link>
          <div className="flex items-center gap-3">
            <span className="text-sm text-slate-500 hidden sm:inline">
              {user?.full_name ?? user?.email}
            </span>
            <button onClick={handleLogout} className="btn-secondary text-xs">
              <LogOut className="w-3.5 h-3.5" />
              Sign out
            </button>
          </div>
        </div>
      </header>

      <main className="max-w-4xl mx-auto px-4 py-10">
        {/* Search bar */}
        <div className="text-center mb-8">
          <h1 className="text-3xl font-bold tracking-tight">
            What would you like to research?
          </h1>
          <p className="text-slate-500 mt-2 text-sm">
            Ask anything — the agents will gather evidence and write you a report.
          </p>
        </div>

        <form onSubmit={handleSubmit} className="mb-10">
          <div className="card p-2 flex gap-2 shadow-md">
            <input
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="e.g. What are the latest breakthroughs in fusion energy in 2026?"
              className="flex-1 px-3 py-2.5 text-sm focus:outline-none rounded-md"
              minLength={10}
            />
            <button
              type="submit"
              disabled={query.trim().length < 10 || createJob.isPending}
              className="btn-primary"
            >
              {createJob.isPending ? (
                <Loader2 className="w-4 h-4 animate-spin" />
              ) : (
                <Search className="w-4 h-4" />
              )}
              Research
            </button>
          </div>
          <p className="text-xs text-slate-400 mt-2 text-center">
            Min 10 characters. Agent pipeline runs in Phase 2 — Phase 1 stores the query.
          </p>
        </form>

        {/* Jobs list */}
        <section>
          <h2 className="text-sm font-semibold text-slate-700 uppercase tracking-wider mb-3">
            Your research
          </h2>

          {jobs.isLoading && (
            <div className="flex justify-center py-10">
              <Loader2 className="w-5 h-5 animate-spin text-slate-400" />
            </div>
          )}

          {jobs.data && jobs.data.items.length === 0 && (
            <div className="card p-10 text-center">
              <FileText className="w-10 h-10 text-slate-300 mx-auto mb-3" />
              <p className="text-sm text-slate-500">No research jobs yet.</p>
              <p className="text-xs text-slate-400 mt-1">
                Ask your first question above to get started.
              </p>
            </div>
          )}

          <div className="space-y-2">
            {jobs.data?.items.map((job) => {
              const cfg = statusConfig[job.status];
              const StatusIcon = cfg.icon;
              return (
                <div key={job.id} className="card p-4 hover:shadow-md transition-shadow">
                  <div className="flex items-start justify-between gap-3">
                    <div className="flex-1 min-w-0">
                      <p className="font-medium text-sm">
                        {job.title ?? job.query}
                      </p>
                      <p className="text-xs text-slate-500 mt-1">
                        {formatRelative(job.created_at)}
                      </p>
                    </div>
                    <span
                      className={cn(
                        'inline-flex items-center gap-1 px-2 py-1 rounded-full text-xs font-medium shrink-0',
                        cfg.color,
                      )}
                    >
                      <StatusIcon className="w-3 h-3" />
                      {cfg.label}
                    </span>
                  </div>
                </div>
              );
            })}
          </div>
        </section>
      </main>
    </div>
  );
}

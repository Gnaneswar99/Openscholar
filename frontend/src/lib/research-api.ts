'use client';

import { api } from './api';
import type { ResearchJob, ResearchJobDetail, ResearchJobList } from '@/types';

export const researchApi = {
  create: (query: string) =>
    api.post<ResearchJob>('/research', { query }).then((r) => r.data),
  list: (limit = 50, offset = 0) =>
    api
      .get<ResearchJobList>('/research', { params: { limit, offset } })
      .then((r) => r.data),
  get: (id: string) => api.get<ResearchJobDetail>(`/research/${id}`).then((r) => r.data),
  remove: (id: string) => api.delete(`/research/${id}`).then(() => undefined as void),
};

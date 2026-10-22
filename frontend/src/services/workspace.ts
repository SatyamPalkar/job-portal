export interface SavedJob {
  id: string; title: string; company: string; location: string;
  description: string; url: string; keywords: string;
}
export interface SavedResume { id: string; title: string; content: string }
export const statuses = ['Saved', 'Applied', 'Interviewing', 'Offer', 'Rejected'] as const;
export interface SavedApplication {
  id: string; jobId: string; resumeId: string; status: typeof statuses[number]; notes: string;
}
export interface Workspace { version: 1; jobs: SavedJob[]; resumes: SavedResume[]; applications: SavedApplication[] }
export const STORAGE_KEY = 'satyam-job-portal-workspace-v1';
export const emptyWorkspace = (): Workspace => ({ version: 1, jobs: [], resumes: [], applications: [] });

export function safeJobUrl(value: string) {
  if (!value.trim()) return '';
  const url = new URL(value);
  if (!['https:', 'http:'].includes(url.protocol) || url.username || url.password) {
    throw new Error('Use a public HTTP or HTTPS job link without credentials.');
  }
  return url.href;
}

const knownSkills = ['python', 'sql', 'excel', 'power bi', 'tableau', 'pandas', 'numpy',
  'scikit-learn', 'tensorflow', 'pytorch', 'machine learning', 'data analysis', 'statistics',
  'r', 'spark', 'airflow', 'dbt', 'postgresql', 'mongodb', 'aws', 'azure', 'gcp',
  'docker', 'kubernetes', 'git', 'javascript', 'typescript', 'react', 'node.js', 'java',
  'c++', 'c#', 'communication', 'leadership', 'agile'];
function contains(text: string, phrase: string) {
  const escaped = phrase.trim().replace(/[.*+?^${}()|[\]\\]/g, '\\$&').replace(/\s+/g, '\\s+');
  return new RegExp(`(^|[^\\p{L}\\p{N}_])${escaped}(?=$|[^\\p{L}\\p{N}_])`, 'iu').test(text);
}
export function compareResume(job: SavedJob, resume: SavedResume) {
  const skills = job.keywords.trim()
    ? [...new Set(job.keywords.split(',').map(s => s.trim().toLowerCase()).filter(Boolean))]
    : knownSkills.filter(skill => contains(job.description, skill));
  const matched = skills.filter(skill => contains(resume.content, skill));
  return { skills, matched, missing: skills.filter(skill => !matched.includes(skill)),
    score: skills.length ? Math.round(matched.length / skills.length * 100) : null };
}

export function validateWorkspace(value: unknown): Workspace {
  const fail = () => { throw new Error('This backup is not a valid Job Portal workspace. Your current data has not been changed.'); };
  if (!value || typeof value !== 'object') return fail();
  const w = value as Workspace;
  if (w.version !== 1 || !Array.isArray(w.jobs) || !Array.isArray(w.resumes) || !Array.isArray(w.applications)
      || w.jobs.length > 200 || w.resumes.length > 50 || w.applications.length > 200) return fail();
  const fields = (row: unknown, keys: string[]) => !!row && typeof row === 'object'
    && keys.every(k => typeof (row as Record<string, unknown>)[k] === 'string'
      && ((row as Record<string, string>)[k]).length <= 30000);
  if (!w.jobs.every(j => fields(j, ['id', 'title', 'company', 'location', 'description', 'url', 'keywords']))
    || !w.resumes.every(r => fields(r, ['id', 'title', 'content']))
    || !w.applications.every(a => fields(a, ['id', 'jobId', 'resumeId', 'status', 'notes']) && statuses.includes(a.status))) return fail();
  for (const rows of [w.jobs, w.resumes, w.applications]) {
    if (new Set(rows.map(r => r.id)).size !== rows.length || rows.some(r => !r.id)) return fail();
  }
  for (const job of w.jobs) { try { safeJobUrl(job.url); } catch { return fail(); } }
  if (w.applications.some(a => !w.jobs.some(j => j.id === a.jobId) || !w.resumes.some(r => r.id === a.resumeId))) return fail();
  return w;
}

export function downloadText(name: string, content: string, type = 'text/plain;charset=utf-8') {
  const url = URL.createObjectURL(new Blob([content], { type }));
  const anchor = document.createElement('a');
  anchor.href = url; anchor.download = name.replace(/[^a-z0-9._-]/gi, '_');
  anchor.click();
  setTimeout(() => URL.revokeObjectURL(url), 1000);
}

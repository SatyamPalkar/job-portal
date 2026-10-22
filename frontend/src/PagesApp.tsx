import React, { useEffect, useState } from 'react';
import { Briefcase, FileText, ClipboardList, Home, Download, ArrowUpRight, Plus, Trash2 } from 'lucide-react';
import Button from './components/Button';
import Card from './components/Card';
import { STORAGE_KEY, emptyWorkspace, validateWorkspace, compareResume, safeJobUrl, downloadText, statuses } from './services/workspace';
import type { Workspace, SavedJob, SavedResume } from './services/workspace';

const tabs = [
  { id: 'dashboard', label: 'Dashboard', icon: Home }, { id: 'jobs', label: 'Saved jobs', icon: Briefcase },
  { id: 'resumes', label: 'Resumes', icon: FileText }, { id: 'applications', label: 'Applications', icon: ClipboardList },
];
const field = 'w-full rounded-lg border border-gray-300 bg-white px-3 py-2.5 text-base focus:outline-none focus:ring-2 focus:ring-primary-500';
const blankJob = { title: '', company: '', location: '', description: '', url: '', keywords: '' };
const readTab = () => tabs.some(t => t.id === location.hash.slice(1)) ? location.hash.slice(1) : 'dashboard';

export default function PagesApp() {
  const [tab, setTab] = useState(readTab);
  const [data, setData] = useState<Workspace>(emptyWorkspace);
  const [error, setError] = useState('');
  const [notice, setNotice] = useState('');
  const [jobDraft, setJobDraft] = useState(blankJob);
  const [resumeDraft, setResumeDraft] = useState({ title: '', content: '' });
  const [search, setSearch] = useState('');
  const [selectedResume, setSelectedResume] = useState('');
  const [comparison, setComparison] = useState<{ jobId: string; resumeId: string } | null>(null);
  const [viewResume, setViewResume] = useState<SavedResume | null>(null);
  useEffect(() => {
    const listener = () => setTab(readTab());
    window.addEventListener('hashchange', listener);
    try { const saved = localStorage.getItem(STORAGE_KEY); if (saved) setData(validateWorkspace(JSON.parse(saved))); }
    catch { setError('Saved data could not be opened. Import a valid backup or use another browser. The stored copy has not been overwritten.'); }
    return () => window.removeEventListener('hashchange', listener);
  }, []);
  function save(next: Workspace) {
    try {
      validateWorkspace(next);
      localStorage.setItem(STORAGE_KEY, JSON.stringify(next));
      setData(next); setError(''); setNotice('Saved in this browser.'); return true;
    } catch { setError('Could not save. Storage may be full or blocked, or the workspace limit was reached (200 jobs/applications, 50 resumes). Export a backup before clearing browser data.'); return false; }
  }
  function addJob(e: React.FormEvent) {
    e.preventDefault();
    try {
      const job: SavedJob = { ...jobDraft, title: jobDraft.title.trim(), company: jobDraft.company.trim(),
        description: jobDraft.description.trim(), url: safeJobUrl(jobDraft.url), id: crypto.randomUUID() };
      if (!job.title || !job.company || !job.description) throw new Error('Enter the job title, company and description.');
      if (save({ ...data, jobs: [job, ...data.jobs] })) setJobDraft(blankJob);
    } catch (e) { setError((e as Error).message); }
  }
  function addResume(e: React.FormEvent) {
    e.preventDefault();
    if (!resumeDraft.title.trim() || !resumeDraft.content.trim()) { setError('Enter a resume title and text.'); return; }
    if (save({ ...data, resumes: [{ ...resumeDraft, id: crypto.randomUUID() }, ...data.resumes] })) setResumeDraft({ title: '', content: '' });
  }
  async function uploadResume(file?: File) {
    if (!file) return;
    try {
      if (!file.name.toLowerCase().endsWith('.txt') || file.size > 100000) throw new Error('Choose a TXT file up to 100 KB, or paste the text from your PDF or DOCX.');
      const content = await file.text();
      if (!content.trim() || content.length > 30000) throw new Error('Use a non-empty resume with at most 30,000 characters.');
      setResumeDraft({ title: file.name.replace(/\.txt$/i, ''), content }); setError('');
    } catch (e) { setError((e as Error).message); }
  }
  async function importBackup(file?: File) {
    if (!file) return;
    try {
      if (file.size > 2000000) throw new Error('Backups must be under 2 MB.');
      const next = validateWorkspace(JSON.parse(await file.text()));
      if (!confirm('Replace this browser workspace with the imported backup?')) return;
      if (save(next)) { setComparison(null); setSelectedResume(''); setViewResume(null); }
    } catch (e) { setError((e as Error).message); }
  }
  function track(job: SavedJob) {
    const resumeId = comparison?.jobId === job.id ? comparison.resumeId : selectedResume || data.resumes[0]?.id;
    if (!resumeId || !data.resumes.some(r => r.id === resumeId)) { setError('Save a resume and select it before tracking an application.'); return; }
    if (data.applications.some(a => a.jobId === job.id)) { location.hash = 'applications'; return; }
    if (save({ ...data, applications: [{ id: crypto.randomUUID(), jobId: job.id, resumeId, status: 'Saved', notes: '' }, ...data.applications] })) location.hash = 'applications';
  }
  function deleteItem(kind: 'jobs' | 'resumes', id: string) {
    if (!confirm('Delete this item and its linked application records?')) return;
    const next = { ...data, applications: data.applications.filter(a => kind === 'jobs' ? a.jobId !== id : a.resumeId !== id) };
    if (kind === 'jobs') next.jobs = next.jobs.filter(item => item.id !== id);
    else next.resumes = next.resumes.filter(item => item.id !== id);
    if (save(next)) { setComparison(null); setViewResume(null); }
  }
  const comparedJob = data.jobs.find(j => j.id === comparison?.jobId);
  const comparedResume = data.resumes.find(r => r.id === comparison?.resumeId);
  const match = comparedJob && comparedResume ? compareResume(comparedJob, comparedResume) : null;

  return <div className="min-h-screen bg-gray-50 text-gray-900">
    <header className="border-b border-gray-200 bg-white"><div className="max-w-7xl mx-auto px-4 sm:px-6 py-5 flex flex-wrap gap-4 items-center justify-between">
      <a href="#dashboard" className="flex items-center gap-3"><FileText className="h-8 w-8 text-primary-600"/><span className="text-xl font-bold">Job Portal<span className="block text-xs font-medium tracking-wide text-gray-500">YOUR NEXT CHAPTER, ORGANIZED</span></span></a>
      <nav aria-label="Main navigation" className="flex gap-1 flex-wrap">{tabs.map(({ id, label, icon: Icon }) => <a key={id} href={`#${id}`} aria-current={tab === id ? 'page' : undefined} className={`flex items-center gap-2 rounded-lg px-3 py-2 text-sm font-medium ${tab === id ? 'bg-primary-50 text-primary-700' : 'text-gray-600 hover:bg-gray-50'}`}><Icon className="h-4 w-4"/>{label}</a>)}</nav>
    </div></header>
    <main className="max-w-7xl mx-auto px-4 sm:px-6 py-8 space-y-6">
      <div className="flex flex-wrap items-center justify-between gap-3 rounded-xl bg-primary-50 border border-primary-100 px-5 py-4">
        <p className="text-sm text-primary-900"><strong>Browser workspace</strong> · Your saved jobs, resumes and applications stay in this browser. Export a backup to keep a copy.</p>
        <div className="flex flex-wrap gap-3"><Button size="sm" variant="outline" onClick={() => downloadText('job-portal-backup.json', JSON.stringify(data, null, 2), 'application/json')}><Download className="h-4 w-4 mr-2"/>Export backup</Button><label className="cursor-pointer text-sm underline py-2">Import backup<input aria-label="Import backup" type="file" accept=".json" className="sr-only" onChange={e => { void importBackup(e.target.files?.[0]); e.target.value = ''; }}/></label></div>
      </div>
      {error && <div role="alert" className="rounded-lg border border-red-200 bg-red-50 p-4 text-red-800">{error}</div>}
      <p role="status" className="text-sm text-gray-500">{notice}</p>
      {tab === 'dashboard' && <>
        <div><p className="text-sm font-semibold text-primary-700 mb-2">ONE WORKSPACE. YOUR NEXT OPPORTUNITY.</p><h1 className="text-3xl sm:text-4xl font-bold tracking-tight">Make your next move.</h1><p className="text-gray-600 mt-3 max-w-2xl text-lg">Keep promising roles in reach. Compare your resume with each role, then follow every application from saved to offer.</p></div>
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">{[{ label: 'Saved jobs', count: data.jobs.length, to: 'jobs', Icon: Briefcase }, { label: 'Resumes', count: data.resumes.length, to: 'resumes', Icon: FileText }, { label: 'Applications', count: data.applications.length, to: 'applications', Icon: ClipboardList }].map(({ label, count, to, Icon }) => <a href={`#${to}`} key={to} className="rounded-xl border border-gray-200 bg-white p-6 hover:shadow-md transition-shadow"><Icon className="h-7 w-7 text-primary-600 mb-5"/><p className="text-3xl font-semibold">{count}</p><p className="text-gray-500 mt-1">{label}</p></a>)}</div>
        <Card title="Start with a role you want"><ol className="list-decimal list-inside space-y-3 text-gray-600"><li><a href="#jobs" className="text-primary-700 underline">Save a job</a> by pasting its description and link.</li><li><a href="#resumes" className="text-primary-700 underline">Add your resume</a> as text or a TXT file.</li><li>Compare keywords, then track your application and next steps.</li></ol></Card>
        <p className="text-sm text-gray-500">Keyword coverage is a transparent text comparison, not an ATS score or a hiring prediction. The server edition in the source repository includes separate authentication and AI integrations.</p>
      </>}
      {tab === 'jobs' && <>
        <div><h1 className="text-3xl font-bold">Saved jobs</h1><p className="mt-2 text-gray-600">Bring roles from any job board into one place.</p></div>
        <Card title="Save a role"><form onSubmit={addJob} className="space-y-4">
          <div className="grid sm:grid-cols-2 gap-4">{(['title', 'company', 'location', 'url'] as const).map(key => <label key={key} className="text-sm font-medium block">{{ title: 'Job title', company: 'Company', location: 'Location', url: 'Original job URL (optional)' }[key]}<input id={`job-${key}`} required={key === 'title' || key === 'company'} type={key === 'url' ? 'url' : 'text'} maxLength={300} className={`${field} mt-1`} value={jobDraft[key]} onChange={e => setJobDraft({ ...jobDraft, [key]: e.target.value })}/></label>)}</div>
          <label className="text-sm font-medium block">Job description<textarea id="job-description" required maxLength={30000} rows={5} className={`${field} mt-1`} value={jobDraft.description} onChange={e => setJobDraft({ ...jobDraft, description: e.target.value })}/></label>
          <label className="text-sm font-medium block">Skills to compare (optional, comma-separated)<input id="job-keywords" maxLength={1000} className={`${field} mt-1`} placeholder="Python, SQL, Power BI — leave blank to detect common technical skills" value={jobDraft.keywords} onChange={e => setJobDraft({ ...jobDraft, keywords: e.target.value })}/></label>
          <Button type="submit"><Plus className="h-4 w-4 mr-2"/>Save job</Button>
        </form></Card>
        <div className="grid sm:grid-cols-2 gap-4"><label className="text-sm font-medium">Filter saved jobs<input id="job-search" className={`${field} mt-1`} placeholder="Job title, company or location" value={search} onChange={e => setSearch(e.target.value)}/></label><label className="text-sm font-medium">Resume to compare<select id="compare-resume" className={`${field} mt-1`} value={selectedResume || data.resumes[0]?.id || ''} onChange={e => setSelectedResume(e.target.value)}>{!data.resumes.length && <option value="">Add a resume first</option>}{data.resumes.map(r => <option key={r.id} value={r.id}>{r.title}</option>)}</select></label></div>
        {!data.jobs.length && <Card><p className="text-gray-600">Your saved roles will appear here. Paste a job description above to get started.</p></Card>}
        {data.jobs.filter(j => `${j.title} ${j.company} ${j.location}`.toLowerCase().includes(search.toLowerCase())).map(job => <Card key={job.id}><div className="space-y-4"><div className="flex justify-between gap-3"><div className="min-w-0"><h2 className="text-xl font-semibold break-words">{job.title}</h2><p className="text-gray-600">{job.company} · {job.location || 'Location not set'}</p></div><button aria-label={`Delete ${job.title}`} onClick={() => deleteItem('jobs', job.id)} className="text-gray-500 hover:text-red-600"><Trash2 className="h-5 w-5"/></button></div><p className="text-gray-600 whitespace-pre-wrap line-clamp-3 break-words">{job.description}</p><div className="flex gap-3 flex-wrap"><Button variant="outline" disabled={!data.resumes.length} onClick={() => setComparison({ jobId: job.id, resumeId: selectedResume || data.resumes[0].id })}>Compare resume</Button><Button disabled={!data.resumes.length} onClick={() => track(job)}>Track application</Button>{job.url && <a href={job.url} target="_blank" rel="noopener noreferrer" className="inline-flex items-center gap-1 text-primary-700 text-sm">Original listing<ArrowUpRight className="h-4 w-4"/></a>}</div>
          {comparison?.jobId === job.id && match && <div className="bg-primary-50 border border-primary-100 rounded-lg p-4 space-y-3"><h3 className="font-semibold">{match.score === null ? 'No recognized skills to compare' : `${match.score}% keyword coverage`} · {comparedResume?.title}</h3><p className="text-sm text-gray-600">{match.matched.length} of {match.skills.length} selected keywords appear in your resume. This is a text comparison, not an ATS or AI score.</p><p className="text-sm"><strong>Found:</strong> {match.matched.join(', ') || 'None'}</p><p className="text-sm"><strong>Not found:</strong> {match.missing.join(', ') || 'None'}</p><p className="text-sm text-gray-600">{!match.skills.length ? 'Add comma-separated skills in the job form for a custom comparison.' : 'Mention missing skills only when you have that experience. Your resume has not been rewritten.'}</p></div>}
        </div></Card>)}
      </>}
      {tab === 'resumes' && <>
        <div><h1 className="text-3xl font-bold">Your resumes</h1><p className="mt-2 text-gray-600">Save a text version for comparison and download it whenever you need it.</p></div>
        <Card title="Add a resume"><form onSubmit={addResume} className="space-y-4"><label className="block text-sm font-medium">Resume title<input id="resume-title" required maxLength={300} className={`${field} mt-1`} value={resumeDraft.title} onChange={e => setResumeDraft({ ...resumeDraft, title: e.target.value })}/></label>
          <label className="block text-sm font-medium">Import a TXT file<input aria-label="Import resume TXT" type="file" accept=".txt,text/plain" className="mt-2 block w-full text-sm" onChange={e => { void uploadResume(e.target.files?.[0]); e.target.value = ''; }}/></label>
          <label className="block text-sm font-medium">Resume text<textarea id="resume-content" required rows={9} maxLength={30000} className={`${field} mt-1`} placeholder="Paste text from your PDF or DOCX, or import a TXT file above." value={resumeDraft.content} onChange={e => setResumeDraft({ ...resumeDraft, content: e.target.value })}/></label>
          <Button type="submit"><Plus className="h-4 w-4 mr-2"/>Save resume</Button></form></Card>
        <div className="grid md:grid-cols-2 gap-4">{data.resumes.map(resume => <Card key={resume.id}><h2 className="text-lg font-semibold break-words">{resume.title}</h2><p className="text-sm text-gray-500 my-3">{resume.content.length.toLocaleString()} characters</p><div className="flex flex-wrap gap-2"><Button variant="outline" onClick={() => setViewResume(viewResume?.id === resume.id ? null : resume)}>View text</Button><Button variant="outline" onClick={() => downloadText(`${resume.title}.txt`, resume.content)}>Download TXT</Button><Button variant="danger" onClick={() => deleteItem('resumes', resume.id)}>Delete</Button></div>{viewResume?.id === resume.id && <pre className="mt-4 whitespace-pre-wrap break-words text-sm text-gray-600 font-sans">{resume.content}</pre>}</Card>)}</div>
      </>}
      {tab === 'applications' && <>
        <div><h1 className="text-3xl font-bold">Applications</h1><p className="mt-2 text-gray-600">Keep your progress and next steps in view. Tracking a role saves a record; submit applications on the original job site.</p></div>
        {!data.applications.length && <Card><p className="text-gray-600 mb-4">Choose a saved job and resume, then select Track application.</p><a href="#jobs" className="text-primary-700 underline">Go to saved jobs →</a></Card>}
        {data.applications.map(application => { const job = data.jobs.find(j => j.id === application.jobId)!; const resume = data.resumes.find(r => r.id === application.resumeId)!; return <Card key={application.id}><div className="space-y-4"><div><h2 className="text-xl font-semibold break-words">{job.title}</h2><p className="text-gray-600">{job.company} · Resume: {resume.title}</p></div><label className="block text-sm font-medium">Status<select aria-label={`Status for ${job.title}`} className={`${field} mt-1 sm:max-w-xs`} value={application.status} onChange={e => save({ ...data, applications: data.applications.map(a => a.id === application.id ? { ...a, status: e.target.value as typeof application.status } : a) })}>{statuses.map(status => <option key={status}>{status}</option>)}</select></label><label className="block text-sm font-medium">Notes and next steps<textarea aria-label={`Notes for ${job.title}`} maxLength={10000} rows={3} className={`${field} mt-1`} value={application.notes} onChange={e => save({ ...data, applications: data.applications.map(a => a.id === application.id ? { ...a, notes: e.target.value } : a) })}/></label><div className="flex gap-3 flex-wrap"><Button variant="outline" onClick={() => downloadText(`${resume.title}.txt`, resume.content)}>Download resume TXT</Button>{job.url && <a className="inline-flex items-center text-primary-700 text-sm gap-1" href={job.url} target="_blank" rel="noopener noreferrer">Open job site<ArrowUpRight className="h-4 w-4"/></a>}<Button variant="danger" onClick={() => { if (confirm('Delete this application record?')) save({ ...data, applications: data.applications.filter(a => a.id !== application.id) }); }}>Delete record</Button></div></div></Card>; })}
      </>}
    </main>
    <footer className="border-t border-gray-200 bg-white mt-12"><div className="max-w-7xl mx-auto px-4 sm:px-6 py-6 flex flex-wrap justify-between gap-3 text-sm text-gray-500"><span>Free browser edition · Local storage · Rule-based keyword comparison</span><a className="text-primary-700" href="https://github.com/SatyamPalkar/job-portal" target="_blank" rel="noopener noreferrer">Built by Satyam Palkar · View source ↗</a></div></footer>
  </div>;
}

import test from 'node:test';
import assert from 'node:assert/strict';
import ts from 'typescript';
import { readFile, mkdtemp, writeFile, rm } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { pathToFileURL } from 'node:url';

const directory = await mkdtemp(join(tmpdir(), 'job-workspace-test-'));
const code = ts.transpileModule(await readFile(new URL('../src/services/workspace.ts', import.meta.url), 'utf8'), {
  compilerOptions: { target: ts.ScriptTarget.ES2022, module: ts.ModuleKind.ES2022 },
}).outputText;
await writeFile(join(directory, 'workspace.mjs'), code);
const { compareResume, safeJobUrl, validateWorkspace, emptyWorkspace } = await import(pathToFileURL(join(directory, 'workspace.mjs')));
test.after(() => rm(directory, { recursive: true, force: true }));
const job = { id: 'j1', title: 'Analyst', company: 'Company', location: 'Sydney', url: '', description: 'Python SQL Power BI R C++', keywords: '' };
const resume = { id: 'r1', title: 'Resume', content: 'Python, SQL and Power BI. Worked in C++.' };

test('keyword coverage uses whole skills, including punctuation, and never fabricates resume content', () => {
  const match = compareResume(job, resume);
  assert.equal(match.score, 80);
  assert.deepEqual(match.missing, ['r']);
  assert.equal(compareResume({ ...job, description: 'R Java' }, { ...resume, content: 'React JavaScript' }).score, 0);
  assert.equal(resume.content, 'Python, SQL and Power BI. Worked in C++.');
});
test('custom skills support whitespace, de-duplication and regex characters', () => {
  const match = compareResume({ ...job, keywords: 'Power BI, C++, C++, a.b' }, { ...resume, content: 'Power\nBI, C++ and aXb' });
  assert.equal(match.skills.length, 3);
  assert.deepEqual(match.matched, ['power bi', 'c++']);
});
test('no recognized skills is unscored rather than a misleading zero', () => {
  assert.equal(compareResume({ ...job, description: 'A role with different duties' }, resume).score, null);
});
test('only credential-free web URLs can be stored or imported', () => {
  assert.equal(safeJobUrl('https://example.com/jobs/1'), 'https://example.com/jobs/1');
  assert.equal(safeJobUrl(''), '');
  for (const link of ['javascript:alert(1)', 'data:text/html,test', 'https://name:secret@example.com', 'not a url']) {
    assert.throws(() => safeJobUrl(link));
    assert.throws(() => validateWorkspace({ ...emptyWorkspace(), jobs: [{ ...job, url: link }] }));
  }
});
test('backups must have unique IDs, valid references, bounded fields and known statuses', () => {
  const workspace = { version: 1, jobs: [job], resumes: [resume], applications: [{ id: 'a1', jobId: 'j1', resumeId: 'r1', status: 'Saved', notes: '' }] };
  assert.deepEqual(validateWorkspace(workspace), workspace);
  assert.throws(() => validateWorkspace({ ...workspace, resumes: [] }));
  assert.throws(() => validateWorkspace({ ...workspace, jobs: [job, job] }));
  assert.throws(() => validateWorkspace({ ...workspace, resumes: [{ ...resume, content: 'x'.repeat(30001) }] }));
  assert.throws(() => validateWorkspace({ ...workspace, applications: [{ ...workspace.applications[0], status: 'invented' }] }));
  assert.throws(() => validateWorkspace({ version: 1, jobs: [null], resumes: [], applications: [] }));
});

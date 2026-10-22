# Free GitHub Pages edition

GitHub Pages serves the checked-in `docs/` directory on `main`. It contains only
the browser application and public assets. No Python packages, credentials,
uploaded files or the example personal resume are included in that directory.

## What works without a server

- Save real jobs by pasting a title, company, description and optional listing URL.
- Save resume text by pasting it or importing a TXT file (up to 100 KB and 30,000
  characters). For PDF/DOCX, paste the extracted text into the resume form.
- Compare the resume with known skills detected in a job, or explicitly entered
  comma-separated keywords. Matching uses whole phrases, ignores case, and handles
  punctuation such as C++. Scores are the percentage of selected keywords found.
  No recognized skills produces an unscored result. This is rule-based keyword
  coverage, not an AI assessment, ATS score or a hiring prediction.
- Track an application with a selected resume, a status and notes. A saved record
  does not submit an application. Use the original job link to apply.
- Download the unchanged resume as TXT; export/import a JSON workspace backup.
- Refresh or revisit the same browser to retrieve its local workspace.

The empty initial workspace contains no invented jobs or application results.
Nothing adds unsupported skills or rewrites employment history. The browser
edition does not ask for a login or simulate account authentication.

Data is stored in localStorage under the project-specific key
`satyam-job-portal-workspace-v1`. Clearing browser data removes the workspace;
export a backup first. It is not synchronized across devices or browsers. Browser
storage is not an encrypted account vault, and other scripts on the same origin
can access it. Limits are 200 jobs, 50 resumes and 200 application records.
Backups are validated before replacement, and an explicit confirmation is needed.
Storage errors are shown without claiming a successful save.

## Build and update

From the repository root:

```sh
cd frontend
npm ci
npm run test:workspace
npm run build:pages
```

Commit `docs/` together with source edits and push `main`. The generated
`.nojekyll` file disables Jekyll. Vite's base path is `/job-portal/`; navigation
uses URL fragments so direct links and refreshes work without server rewrites.
The Pages configuration is in `frontend/vite.pages.config.ts`.

The standard `npm run build` continues to produce the original server-backed
frontend in `frontend/dist/`. The browser-only flag is compiled in only by the
Pages configuration. Server authentication, live job APIs, AI optimization,
PDF/DOCX processing, scheduling and automation still require the original backend
and any associated credentials. GitHub Pages does not host those features.

## Verification

Five focused tests cover whole-skill matching, custom skill lists, unscored input,
safe job links and backup validation. Both frontend production builds passed.
Chrome verified job/resume creation, actual keyword scores, application status and
notes persisting after refresh, JSON backup export, TXT download and rejection of
invalid backup data. Layouts were checked at 320, 390, 768 and 1440 pixels.
The browser edition made no backend API requests during these checks.

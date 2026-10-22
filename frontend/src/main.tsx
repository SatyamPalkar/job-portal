import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';

const App = import.meta.env.VITE_BROWSER_WORKSPACE === 'true'
  ? React.lazy(() => import('./PagesApp')) : React.lazy(() => import('./App'));

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <React.Suspense fallback={<p className="p-8">Loading workspace…</p>}><App /></React.Suspense>
  </React.StrictMode>,
);



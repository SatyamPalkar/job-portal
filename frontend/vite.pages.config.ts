import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import path from 'path';

export default defineConfig({
  plugins: [react()],
  base: '/job-portal/',
  define: { 'import.meta.env.VITE_BROWSER_WORKSPACE': JSON.stringify('true') },
  resolve: { alias: { '@': path.resolve(__dirname, './src') } },
  build: { outDir: '../docs', emptyOutDir: true },
});

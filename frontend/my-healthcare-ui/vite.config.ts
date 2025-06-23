// frontend/my-healthcare-ui/vite.config.ts

import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import path from 'path'

export default defineConfig({
  // Treat this folder—where vite.config.ts and index.html live—as the project root
  root: './',
  plugins: [react()],
  resolve: {
    // Allow imports like `import X from '@/components/X'` → frontend/src/components/X
    alias: { '@': path.resolve(__dirname, 'src') },
  },
  css: {
    postcss: './postcss.config.cjs',
  },
  server: {
    port: 5173,
    proxy: {
      '/api': {
        // Proxy all /api/* calls to Django on port 8000
        target: 'http://127.0.0.1:8000',
        changeOrigin: true,
        secure: false,
      },
      '/api-auth': {
        // If you ever need Django's session‐login or CSRF endpoints
        target: 'http://127.0.0.1:8000',
        changeOrigin: true,
        secure: false,
      },
    },
  },
})

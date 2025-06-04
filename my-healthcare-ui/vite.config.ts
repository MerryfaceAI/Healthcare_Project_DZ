import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// tell Vite to forward API calls to port 8000
export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      // whenever your React app does fetch('/patients/api/...'),
      // Vite will forward it to localhost:8000
      '/patients/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
        secure: false,
      },
      // same for the auth endpoints
      '/api-auth': {
        target: 'http://localhost:8000',
        changeOrigin: true,
        secure: false,
      },
    }
  }
})

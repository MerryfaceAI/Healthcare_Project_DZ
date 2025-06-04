import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      // forward any request starting /patients/api to Django
      '/patients/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
      },
      // for session-auth login/logout
      '/api-auth': {
        target: 'http://localhost:8000',
        changeOrigin: true,
      },
    },
  },
});

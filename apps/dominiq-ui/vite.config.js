import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      '/chat_with_agent': {
        target: 'https://chatapp-rfodgphkaq-uc.a.run.app',
        changeOrigin: true,
        secure: false,
      },
      '/generate_diagram_from_chat': {
        target: 'https://chatapp-rfodgphkaq-uc.a.run.app',
        changeOrigin: true,
        secure: true,
      },
      '/api/chat/completions': {
        target: 'https://api.saia.ai', // Cambia esto a la URL de tu API
        changeOrigin: true,
        secure: true,
        rewrite: (path) => path.replace(/^\/api/, ''), // Reescribe la ruta para que coincida con la API
      },
      '/api': {
        target: 'https://api.saia.ai', // Cambia esto a la URL de tu API
        changeOrigin: true,
        secure: true,
        rewrite: (path) => path.replace(/^\/api/, ''), // Reescribe la ruta para que coincida con la API
      },
    }
  }
});
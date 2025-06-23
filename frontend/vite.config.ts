import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

// https://vitejs.dev/config/
export default defineConfig({
    base: '/',
    plugins: [react()],
    define: {
    'process.env': {}
    },
  server: {
    port: 3000,
    open: true,
    host: true,
  },
  preview: {
    port: 3000,
    open: true,
    host: true,
  },
  build: {
    outDir: 'dist',
    assetsDir: 'assets',
    emptyOutDir: true,
    sourcemap: true,
    minify: 'esbuild',
    rollupOptions: {
      output: {
        manualChunks: {
          react: ['react', 'react-dom', 'react-router-dom'],
          vendor: ['axios', 'date-fns'],
        },
      },
    },
  }
});

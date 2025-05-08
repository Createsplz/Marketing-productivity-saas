import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import rollupNodePolyFill from 'rollup-plugin-polyfill-node'

export default defineConfig({
  plugins: [react(), rollupNodePolyFill()],
  resolve: {
    alias: {
      crypto: 'crypto-browserify',
      stream: 'stream-browserify',
      process: 'process/browser'
    }
  },
  define: {
    'process.env': {}
  },
  server: {
    port: 3000
  },
  build: {
    target: 'esnext'
  }
})

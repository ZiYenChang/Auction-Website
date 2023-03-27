import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// https://vitejs.dev/config/
export default defineConfig(({ command,mode}) => {
  return{
    plugins: [vue()],
    build:{
      emptyOutDir:true,
      outDir:'../../auction/static/auction/vue'
    },
    base: (mode == 'development') ? 'http://localhost:5173/' : '/static/auction/vue',
  }
})

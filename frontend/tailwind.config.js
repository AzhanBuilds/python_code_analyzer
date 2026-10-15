/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        dark: {
          950: '#070b0e',
          900: '#0b1116',
          850: '#0f171f',
          800: '#141e28',
          700: '#1e2c3a',
          600: '#2a3b4c',
        },
        forest: {
          950: '#03140c',
          900: '#062316',
          800: '#0c3b26',
          700: '#105034',
          600: '#166542',
          500: '#10b981',
          400: '#34d399',
          300: '#6ee7b7',
        }
      },
      fontFamily: {
        mono: ['"JetBrains Mono"', 'Fira Code', 'Consolas', 'monospace'],
        sans: ['Inter', 'system-ui', '-apple-system', 'sans-serif'],
      }
    },
  },
  plugins: [],
}

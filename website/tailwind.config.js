/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}",
    "./docs/**/*.{md,mdx}",
  ],
  darkMode: ['class', '[data-theme="dark"]'],
  theme: {
    extend: {
      colors: {
        primary: "#00FFCC", // Cyan
        secondary: "#DAFF00", // Vibrant Lime-Green
        "background-dark": "#05070a", 
        "surface-dark": "#0e1116",
      },
      fontFamily: {
        display: ["Orbitron", "sans-serif"],
        mono: ["JetBrains Mono", "monospace"],
      },
      animation: {
          'rain': 'rain 20s linear infinite',
          'rain-fast': 'rain 12s linear infinite',
          'scan-vertical': 'scan-vertical 6s ease-in-out infinite',
          'scan-vertical-slow': 'scan-vertical 12s ease-in-out infinite',
          'float-slow': 'float 8s ease-in-out infinite',
          'float-delayed': 'float 8s ease-in-out infinite 4s',
          'pulse-glow': 'pulse-glow 4s ease-in-out infinite',
          'node-pulse': 'node-pulse 3s ease-in-out infinite',
          'spin-slow': 'spin 12s linear infinite',
          'spin-reverse-slow': 'spin-reverse 8s linear infinite',
      },
      keyframes: {
          rain: {
              '0%': { transform: 'translateY(0%)' },
              '100%': { transform: 'translateY(-50%)' },
          },
          'scan-vertical': {
              '0%': { top: '0%', opacity: '0.4' },
              '50%': { top: '95%', opacity: '1' },
              '100%': { top: '0%', opacity: '0.4' },
          },
          float: {
              '0%, 100%': { transform: 'translateY(0px)' },
              '50%': { transform: 'translateY(-15px)' },
          },
          'pulse-glow': {
              '0%, 100%': { opacity: '0.3' },
              '50%': { opacity: '0.6' },
          },
          'node-pulse': {
              '0%, 100%': { r: '3', opacity: '0.6' },
              '50%': { r: '4', opacity: '1' },
          },
          spin: {
              from: { transform: 'rotate(0deg)' },
              to: { transform: 'rotate(360deg)' },
          },
          'spin-reverse': {
              from: { transform: 'rotate(360deg)' },
              to: { transform: 'rotate(0deg)' },
          }
      }
    },
  },
  plugins: [],
  corePlugins: {
    preflight: false,
  },
}

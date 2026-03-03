/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './pages/**/*.{js,ts,jsx,tsx,mdx}',
    './components/**/*.{js,ts,jsx,tsx,mdx}',
    './app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        'health-green': '#22c55e',
        'health-yellow': '#f59e0b',
        'health-red': '#ef4444',
      },
    },
  },
  plugins: [],
}

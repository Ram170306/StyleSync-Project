/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './src/pages/**/*.{js,ts,jsx,tsx,mdx}',
    './src/components/**/*.{js,ts,jsx,tsx,mdx}',
    './src/app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        primary: '#FF6B6B',
        'primary-dark': '#FF5252',
        secondary: '#4ECDC4',
        'secondary-dark': '#45B7AF',
        accent: '#FFE66D',
        'accent-dark': '#FFD93D',
        background: '#F7F7F7',
        foreground: '#2D3436',
        card: '#FFFFFF',
        'card-foreground': '#2D3436',
        border: '#E2E8F0',
        input: '#E2E8F0',
        ring: '#FF6B6B',
      },
      borderRadius: {
        DEFAULT: '0.5rem',
      },
    },
  },
  plugins: [],
} 
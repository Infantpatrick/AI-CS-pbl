/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        background: {
          DEFAULT: 'var(--bg-default)',
          alt: 'var(--bg-alt)',
          deep: 'var(--bg-deep)'
        },
        surface: {
          DEFAULT: 'var(--surface-default)',
          hover: 'var(--surface-hover)',
          active: 'var(--surface-active)'
        },
        primary: {
          DEFAULT: 'var(--primary-default)',
          strong: 'var(--primary-strong)'
        },
        purple: {
          light: '#818CF8',
          DEFAULT: '#6366F1',
          strong: '#A855F7'
        },
        success: '#34D399',
        warning: '#FBBF24',
        danger: '#F87171',
        text: {
          primary: 'var(--text-primary)',
          secondary: 'var(--text-secondary)',
          muted: 'var(--text-muted)'
        },
        border: {
          subtle: 'var(--border-subtle)',
          strong: 'var(--border-strong)'
        }
      },
      fontFamily: {
        sans: ['Inter Variable', 'sans-serif'],
        mono: ['JetBrains Mono Variable', 'monospace'],
      },
    },
  },
  plugins: [],
}

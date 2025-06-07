// tailwind.config.cjs
/** @type {import('tailwindcss').Config} */
const { join } = require('path');

module.exports = {
  content: [
    join(__dirname, 'index.html'),
    join(__dirname, 'src/**/*.{js,jsx,ts,tsx}')
  ],
  theme: {
    extend: {
      colors: {
        sidebar: {
          DEFAULT: '#2d6a6d',
          hover:   '#26585f',
          active:  '#1e4e54',
        },
        appbg:   '#f5f7fa',
        cardbg:  '#ffffff',
        btn:     '#007acc',
      },
      spacing: {
        sidebarCollapsed: '64px',
        sidebarExpanded:  '240px',
        topbarHeight:     '64px',
      }
    }
  },
  plugins: [],
};

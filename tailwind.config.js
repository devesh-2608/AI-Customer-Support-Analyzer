/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,jsx}"],
  theme: {
    extend: {
      colors: {
        base: "#0F1419",       // near-black console background
        panel: "#161C24",      // slightly lifted panel
        line: "#232B36",       // hairline borders
        signal: "#4FD1A5",     // resolved / positive — muted signal green
        alert: "#E8896B",      // urgent / negative — warm clay, used sparingly
        muted: "#7C8894",      // secondary text
        ink: "#EAEDF0",        // primary text
      },
      fontFamily: {
        mono: ["'JetBrains Mono'", "ui-monospace", "monospace"],
        sans: ["'Inter'", "system-ui", "sans-serif"],
      },
    },
  },
  plugins: [],
}

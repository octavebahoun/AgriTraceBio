/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,ts,jsx,tsx}"],
  theme: {
    extend: {
      colors: {
        brand: {
          50:  "#f2faf0",
          100: "#e0f2dc",
          200: "#c1e5b8",
          300: "#94d187",
          400: "#5eb64d",
          500: "#3d9d2b",
          600: "#2b7d1e",
          700: "#22631a",
          800: "#1e4f18",
          900: "#194117",
        },
        gold: {
          400: "#f2b135",
          500: "#e69517",
        },
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
      },
      boxShadow: {
        card: "0 1px 2px rgba(15,23,42,0.04), 0 1px 3px rgba(15,23,42,0.06)",
      },
    },
  },
  plugins: [],
}

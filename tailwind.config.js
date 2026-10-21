/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./app/**/*.{js,ts,jsx,tsx}", "./components/**/*.{js,ts,jsx,tsx}"],
  theme: {
    extend: {
      colors: {
        brand: { blue: "#0A84FF", blue2: "#0066FF", dark: "#000000", dark2: "#0A0A0A" }
      }
    }
  },
  plugins: []
}

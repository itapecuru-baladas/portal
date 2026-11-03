/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./app/**/*.{js,ts,jsx,tsx,mdx}", "./components/**/*.{js,ts,jsx,tsx,mdx}"],
  theme: {
    extend: {
      colors: {
        ib: {
          black: "#000000",
          white: "#FFFFFF",
          blueDark: "#0047BB",
          blueMid: "#0077FF",
          blueLight: "#00A6FF",
        }
      },
      fontFamily: {
        futur: ["Orbitron", "Rajdhani", "sans-serif"],
        baladas: ["Montserrat", "sans-serif"],
        slogan: ["Inter", "sans-serif"]
      },
      backgroundImage: {
        "ib-gradient": "linear-gradient(90deg, #0047BB 0%, #0077FF 50%, #00A6FF 100%)",
        "ib-gradient-vertical": "linear-gradient(180deg, #00A6FF 0%, #0047BB 100%)",
        "ib-equalizer": "linear-gradient(180deg, #00A6FF 0%, #0047BB 100%)"
      }
    },
  },
  plugins: [],
}

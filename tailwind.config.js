/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./templates/**/*.html",
    "./**/templates/**/*.html",
    "./static/js/**/*.js"
  ],
  darkMode: "class",
  theme: {
    extend: {
      colors: {
        primary: "#D4AF37",
        "gold-light": "#F9F295",
        "gold-dark": "#B38728",
        "background-light": "#FDFCFB",
        "background-dark": "#0A0A0A",
        "card-dark": "#161616",
        "surface-dark": "#1A1A1A",
      },
      fontFamily: {
        display: ["Playfair Display", "Montserrat", "serif"],
        sans: ["Montserrat", "Inter", "sans-serif"],
        body: ["Inter", "sans-serif"],
      },
      borderRadius: {
        DEFAULT: "0.75rem",
        "xl": "1rem",
        "2xl": "1.5rem",
        "3xl": "2rem",
      },
    },
  },
  plugins: [
    require('@tailwindcss/typography'),
    require('@tailwindcss/forms'),
  ],
}
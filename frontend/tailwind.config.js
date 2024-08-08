/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./src/**/*.{html,js,svelte,ts}",
    "./node_modules/flowbite-svelte/**/*.{html,js,svelte,ts}",
    "./node_modules/flowbite-svelte-icons/**/*.{html,js,svelte,ts}",
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          50: "#ebf8ff",
          100: "#bee3f8",
          200: "#90cdf4",
          300: "#63b3ed",
          400: "#4299e1",
          500: "#3182ce",
          600: "#2b6cb0",
          700: "#2c5282",
          800: "#2a4365",
          900: "#1A365D",
        },
      },
      screens: {
        xs: "480px",
        sm: "640px",
        md: "768px",
        lg: "1024px",
        xl: "1280px",
        "2xl": "1536px",
        "3xl": "1600px",
        "4xl": "1920px",
        "5xl": "2560px",
        "6xl": "3840px",
        "7xl": "5120px",
      },
      keyframes: {
        rotate: {
          '30%': { transform: 'rotate(220deg)' },
          '40%': { transform: 'rotate(450deg)' },
          '75%': { transform: 'rotate(720deg)', opacity: '1' },
          '76%': { opacity: '0' },
          '100%': { transform: 'rotate(0deg)', opacity: '0' },
        },
      },
      animation: {
        rotate: 'rotate 3.5s linear infinite',
      },
    },
  },
  plugins: [require("flowbite/plugin")],
  darkMode: "class",
};

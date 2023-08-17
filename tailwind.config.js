/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,ts,jsx,tsx}"],
  theme: {
    extend: {
      colors: {
        primary: "#1b59f8",
        "bg-primary": "rgba(27, 89, 248, 0.1)",
        success: "#059669",
        "bg-success": "rgba(5, 150, 105, 0.2)",
        error: "#b91c1c",
        "bg-error": "rgba(185, 28, 28, 0.2)",
        warning: "#eab308",
        "bg-warning": "rgba(234, 179, 8, 0.2)",
        text: "rgba(0, 0, 0, 0.7)",
        background: "#f8fafc",
        border: "#e5e5e5",
        "bg-text": "rgba(0, 0, 0, 0.1)",
        "secondary-text": "#949494",
      },
    },
  },
  plugins: [],
};

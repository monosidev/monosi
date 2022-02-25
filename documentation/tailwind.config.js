const round = (num) =>
  num
    .toFixed(7)
    .replace(/(\.[0-9]+?)0+$/, "$1")
    .replace(/\.0$/, "");
// const rem = (px) => `${round(px / 16)}rem`
const em = (px, base) => `${round(px / base)}em`;

module.exports = {
  mode: "jit",
  content: [
    "./src/components/**/*.{js,ts,jsx,tsx}",
    "./src/pages/**/*.{js,ts,jsx,tsx}",
    "./src/theme/**/*.{js,ts,jsx,tsx}",
  ],
  // corePlugins: {
  //   // preflight: false, // to use Docusaurus base styles
  //   // container: false, // use container style from docusaurus
  // },
  // // important: "#tailwind", // incrementally adopt Tailwind by wrapping pages with <div id="tailwind"> </div>
  theme: {
    extend: {
      typography: {
        DEFAULT: {
          css: {
            color: "var(--ifm-color)",
            h1: {
              color: "var(--ifm-color)",
            },
            h2: {
              color: "var(--ifm-color)",
            },
            h3: {
              color: "var(--ifm-color)",
            },
            h4: {
              color: "var(--ifm-color)",
            },
            li: {
              color: "var(--ifm-color)",
            },
            strong: {
              color: "var(--ifm-color)",
            },
            table: {
              thead: {
                color: "var(--ifm-color)",
              },
              "thead th:first-child": {
                paddingLeft: em(8, 14),
              },
              "tbody td:first-child": {
                paddingLeft: em(8, 14),
              },
              "tbody td:last-child": {
                paddingRight: em(8, 14),
              },
            },
            blockquote: {
              // border: "none",
              color: "var(--ifm-color)",
              // backgroundColor: "transparent",
              fontSize: "inherit",
              fontStyle: "inherit",
              fontWeight: "medium",
            },
            "blockquote p:first-of-type::before": {
              content: "",
            },
            "blockquote p:last-of-type::after": {
              content: "",
            },
            img: {
              borderRadius: "0.5rem",
              display: "inline",
            },
            "code::before": false,
            "code::after": false,
            code: {
              color: "var(--ifm-color)",
              "border-radius": "0.25rem",
              padding: "0.15rem 0.3rem",
            },
            pre: {
              borderWidth: "2px",
            },
            a: {
              color: "#3182ce",
              "&:hover": {
                color: "#2c5282",
              },
            },
          },
        },
      },
      transitionDelay: {
        3000: "3000ms",
      },
      fontFamily: {
        light: ["Aeonik-Light"],
        bold: ["Aeonik-Bold"],
      },
      keyframes: {
        "fade-in-down": {
          "0%": {
            opacity: "0",
            transform: "translateY(-10px)",
          },
          "100%": {
            opacity: "1",
            transform: "translateY(0)",
          },
        },
      },
      animation: {
        "fade-in-down": "fade-in-down 0.5s ease-out",
      },
      colors: {
        offwhite: "#F2F2F2",
        spaceblack: "#141414",
        green1: "#9EE587",
        green2: "#32D67B",
        orange1: "#FFA280",
        orange2: "#FF7065",
        gray5: "#E0E0E0",
        lightgray: "rgba(242,242,242,0.5)",
        lightteal: "#C7EDEF",
      },
      gridTemplateColumns: {
        usecases: "200px minmax(0, 1fr)",
      },
      maxWidth: {
        700: "700px",
      },
      width: {
        200: "200px",
        300: "300px",
        700: "700px",
        800: "800px",
        "3/1": "300%",
      },
      height: {
        60: "60px",
        200: "200px",
        300: "300px",
        400: "400px",
        700: "700px",
        800: "800px",
        "3/1": "300%",
      },
      fontSize: {
        60: "60px",
        144: "144px",
      },
      lineHeight: {
        36: "36px",
        48: "48px",
        60: "60px",
        72: "72px",
        144: "144px",
      },
      zIndex: {
        "-1": "-1",
      },
    },
  },
  plugins: [require("@tailwindcss/typography")],
};

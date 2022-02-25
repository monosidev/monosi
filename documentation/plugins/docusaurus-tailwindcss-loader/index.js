module.exports = function (context, options) {
  return {
    name: "postcss-tailwindcss-loader",
    configurePostCss(postcssOptions) {
      // Appends new PostCSS plugin.
      postcssOptions.plugins.push(
        require("postcss-import"),
        require("tailwindcss"),
        require("postcss-preset-env")({
          autoprefixer: {
            flexbox: "no-2009",
          },
          stage: 4,
        })
      );
      return postcssOptions;
    },
  };
};

//@ts-check
const path = require("path");
const visit = require("unist-util-visit");
const FontPreloadPlugin = require("webpack-font-preload-plugin");

/** @type {import('@docusaurus/types').DocusaurusConfig} */
module.exports = {
  title: "Monosi Documentation",
  tagline: "Open Source Data Observability",
  url: "https://docs.monosi.dev",
  baseUrl: "/",
  onBrokenLinks: "warn",
  onBrokenMarkdownLinks: "warn",
  favicon: "img/favicon.png",
  organizationName: "monosidev",
  projectName: "monosi",
  plugins: [
    function preloadFontPlugin() {
      return {
        name: "preload-font-plugin",
        configureWebpack() {
          return {
            plugins: [new FontPreloadPlugin()],
          };
        },
      };
    },
    "docusaurus-tailwindcss-loader",
  ],
  themeConfig: {
    colorMode: {
      defaultMode: "light",
      disableSwitch: false,
      switchConfig: {
        darkIcon: "🌙",
        darkIconStyle: {
          content: `url(/img/moon.svg)`,
          transform: "scale(2)",
          margin: "0 0.2rem",
        },
        lightIcon: "\u{1F602}",
        lightIconStyle: {
          content: `url(/img/sun.svg)`,
          transform: "scale(2)",
        },
      },
    },
    prism: {
      theme: require("prism-react-renderer/themes/nightOwlLight"),
      darkTheme: require("prism-react-renderer/themes/dracula"),
      additionalLanguages: ["java", "ruby", "php"],
    },
    // hideableSidebar: true,
    navbar: {
      hideOnScroll: true,
      title: "Monosi",
      items: [
        {
          activeBasePath: "/docs",
          label: "Docs",
          items: [
            {
              to: "/docs/user-guide/introduction",
              activeBasePath: "/docs/user-guide/",
              label: "User Guide - Start Here",
            },
            // {
            //   to: "/docs/msi/",
            //   activeBasePath: "/docs/msi/",
            //   label: "msi (CLI)",
            // },
            {
              to: "/integrations",
              activeBasePath: "/integrations",
              label: "Integrations",
            },
            {
              to: "/docs/guides/quick-install",
              activeBasePath: "/docs/guides/",
              label: "Guides",
            },
            {
              to: "/docs/contributing/contributing-overview",
              activeBasePath: "/docs/contributing/contributing-overview",
              label: "Contributing",
            },
          ],
        },
        {
          to: "https://demo.monosi.dev",
          label: "Live Demo",
        },
        {
          to: "/changelog",
          activeBasePath: "/changelog",
          label: "Changelog",
        },
      ],
    },
    footer: {
      copyright: `
      <div className="footer__icons">
        <a href="https://github.com/monosidev/monosi" aria-label="GitHub"><svg class="footer__svg" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"><path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z"/></svg></a>
        <a href="https://twitter.com/monosidev" aria-label="Twitter"><svg class="footer__svg" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"><path d="M24 4.557c-.883.392-1.832.656-2.828.775 1.017-.609 1.798-1.574 2.165-2.724-.951.564-2.005.974-3.127 1.195-.897-.957-2.178-1.555-3.594-1.555-3.179 0-5.515 2.966-4.797 6.045-4.091-.205-7.719-2.165-10.148-5.144-1.29 2.213-.669 5.108 1.523 6.574-.806-.026-1.566-.247-2.229-.616-.054 2.281 1.581 4.415 3.949 4.89-.693.188-1.452.232-2.224.084.626 1.956 2.444 3.379 4.6 3.419-2.07 1.623-4.678 2.348-7.29 2.04 2.179 1.397 4.768 2.212 7.548 2.212 9.142 0 14.307-7.721 13.995-14.646.962-.695 1.797-1.562 2.457-2.549z"/></svg></a>
        <a href="https://www.linkedin.com/company/monosi/" aria-label="LinkedIn"><svg class="footer__svg" width="24" height="25" viewBox="0 0 24 25" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M0 1.73012C0 0.775103 0.794422 0 1.77383 0H22.2262C23.2059 0 24 0.775103 24 1.73012V22.4222C24 23.3776 23.2059 24.152 22.2262 24.152H1.77383C0.794422 24.152 0 23.3776 0 22.4226V1.72981V1.73012Z" fill="#270D5B"/><path d="M7.27432 20.2178V9.31189H3.64936V20.2178H7.27463H7.27432ZM5.46247 7.82314C6.72633 7.82314 7.51315 6.98563 7.51315 5.93907C7.4894 4.86875 6.72633 4.05469 5.48654 4.05469C4.24581 4.05469 3.43555 4.86875 3.43555 5.93907C3.43555 6.98563 4.22205 7.82314 5.43871 7.82314H5.46215H5.46247ZM9.28065 20.2178H12.9053V14.1282C12.9053 13.8026 12.9291 13.4763 13.0247 13.2438C13.2867 12.5922 13.8831 11.9179 14.8847 11.9179C16.1961 11.9179 16.7209 12.9179 16.7209 14.3841V20.2178H20.3456V13.9647C20.3456 10.615 18.5575 9.05627 16.1726 9.05627C14.2173 9.05627 13.3586 10.1491 12.8815 10.8935H12.9056V9.31221H9.28097C9.32817 10.3353 9.28065 20.2181 9.28065 20.2181V20.2178Z" fill="white"/></svg></a>
      </div>
      <div class="footer__copyright"><span class="footer__block">Copyright © ${new Date().getFullYear()}</span> Vocable Inc. dba Monosi</div>
      `,
    },
    gtag: {
      trackingID: "G-M6MW4MGZS8",
    },
    algolia: {
      apiKey: "53bfbe8a5227e168e89437292698846f",
      appId: "GNDLCIWQCJ",
      indexName: "monosi",
    },
  },
  presets: [
    [
      "@docusaurus/preset-classic",
      {
        // Will be passed to @docusaurus/plugin-content-docs
        docs: {
          sidebarPath: require.resolve("./sidebars.js"),
          routeBasePath: "docs",
          exclude: ["**/shared/**"], // do not render "shared" content
          editUrl:
            "https://github.com/monosidev/monosi/tree/master/documentation",
          /**
           * Whether to display the author who last updated the doc.
           */
          showLastUpdateAuthor: false,
          /**
           * Whether to display the last date the doc was updated.
           */
          showLastUpdateTime: false,
          /**
           * Skip the next release docs when versioning is enabled.
           * This will not generate HTML files in the production build for documents
           * in `/docs/next` directory, only versioned docs.
           */
          // excludeNextVersionDocs: false,
          includeCurrentVersion: true, // excludeNextVersionDocs is now deprecated
          remarkPlugins: [
            [
              () =>
                function addTSNoCheck(tree) {
                  // Disable TS type checking for any TypeScript code blocks.
                  // This is because imports are messy with snipsync: we don't
                  // have a way to pull in a separate config for every example
                  // snipsync pulls from.
                  function visitor(node) {
                    if (!/^ts$/.test(node.lang)) {
                      return;
                    }
                    node.value = "// @ts-nocheck\n" + node.value.trim();
                  }

                  visit(tree, "code", visitor);
                },
              {},
            ],
            [
              require("remark-typescript-tools").transpileCodeblocks,
              {
                compilerSettings: {
                  tsconfig: path.join(
                    __dirname,
                    "docs",
                    "typescript",
                    "tsconfig.json"
                  ),
                  externalResolutions: {},
                },
                fileExtensions: [".md", ".mdx"],
                // remark-typescript-tools automatically running prettier with a custom config that doesn't
                // line up with ours. This disables any post processing, including the default prettier step.
                postProcessTs: (files) => files,
                postProcessTranspiledJs: (files) => files,
              },
            ],
            [
              () =>
                function removeTSNoCheck(tree) {
                  function visitor(node) {
                    if (!/^ts$/.test(node.lang) && !/^js$/.test(node.lang)) {
                      return;
                    }
                    if (node.value.startsWith("// @ts-nocheck\n")) {
                      node.value = node.value.slice("// @ts-nocheck\n".length);
                    }
                    // If TS compiled output is empty, replace it with a more helpful comment
                    if (
                      node.lang === "js" &&
                      node.value.trim() === "export {};"
                    ) {
                      node.value = "// Not required in JavaScript";
                    } else if (node.lang === "js") {
                      node.value = convertIndent4ToIndent2(node.value).trim();
                    }
                  }
                  visit(tree, "code", visitor);
                },
              {},
            ],
          ],
        },
        // INSERT CHANGES HERE
        // Will be passed to @docusaurus/plugin-content-blog
        // options: https://docusaurus.io/docs/api/plugins/@docusaurus/plugin-content-blog
        blog: {
          routeBasePath: "changelog",
          path: "changelog",
          postsPerPage: 10,
          editUrl:
            "https://github.com/monosidev/monosi/tree/master/documentation",
          blogTitle: "Monosi Changelog",
          showReadingTime: true, // Show estimated reading time for the blog post.
          feedOptions: {
            type: "all",
            copyright: `Copyright © ${new Date().getFullYear()} Vocable Inc. dba Monosi`,
          },
        },
        // Will be passed to @docusaurus/theme-classic.
        theme: {
          customCss: require.resolve("./src/css/custom.css"),
        },
        // Will be passed to @docusaurus/plugin-content-sitemap
        sitemap: {
          // Per v2.0.0-alpha.72 cacheTime is now deprecated
          //cacheTime: 600 * 1000, // 600 sec - cache purge period
          changefreq: "weekly",
          priority: 0.5,
        },
      },
    ],
  ],
  scripts: [
    {
      src: "/scripts/feedback.js",
      async: true,
      defer: true,
    },
    {
      src: "/scripts/fullstory.js",
      async: true,
      defer: true,
    },
  ],
};

function convertIndent4ToIndent2(code) {
  // TypeScript always outputs 4 space indent. This is a workaround.
  // See https://github.com/microsoft/TypeScript/issues/4042
  return code.replace(/^( {4})+/gm, (match) => {
    return "  ".repeat(match.length / 4);
  });
}

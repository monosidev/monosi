module.exports = {
  sidebarUserGuide: [
    {
      type: "category",
      label: "User Guide",
      collapsible: false,
      collapsed: false,
      items: [
        {
          type: "category",
          label: "Introduction",
          collapsible: false,
          collapsed: false,
          items: [
            "user-guide/introduction",
            "user-guide/getting-started",
          ]
        },
        {
          type: "category",
          label: "Data Monitors",
          collapsible: false,
          collapsed: false,
          items: [
            "user-guide/table-health",
            // "user-guide/schema-changes",
            // "user-guide/freshness",
            // "user-guide/distribution",
            // "user-guide/custom-sql",
          ]
        },
        {
          type: "category",
          label: "Deployment",
          collapsed: true,
          items: [
            "user-guide/local-deployment",
            "user-guide/terraform-deployment",
            "user-guide/aws-ec2",
            "user-guide/kubernetes",
            "user-guide/hybrid-deployment",
          ]
        },
        {
          type: "category",
          label: "Data Warehouses",
          collapsed: true,
          items: [
            "integrations/snowflake",
            "integrations/postgresql",
            "integrations/redshift",
          ]
        },
        {
          type: "category",
          label: "Alert Destinations",
          collapsed: true,
          items: [
            "integrations/slack",
            "integrations/webhooks",
            "integrations/email",
          ]
        },
        {
          type: "category",
          label: "Guides",
          collapsed: true,
          items: [
            "guides/quick-install"
          ]
        },
        {
          type: "category",
          label: "Contributing",
          collapsed: true,
          items: [
            "contributing/contributing-overview",
            "contributing/local-development",
          ]
        },
        {
          type: "category",
          label: "Project Overview",
          collapsed: true,
          items: [
          ]
        },
        {
          type: "category",
          label: "Support & FAQ",
          collapsed: true,
          items: [
            "supportfaq/usage-data-preferences"
          ]
        },
      ],
    },
  ],
  sidebarmsi: [
    {
      type: "category",
      label: "msi",
      collapsible: false,
      collapsed: false,
      link: {
        type: "doc",
        id: "msi/index",
      },
      items: [
        "msi/how-to-install-msi",
        "msi/how-to-use-msi",
        "msi/configuration",
        "msi/environment-variables",
        {
          type: "category",
          label: "Project",
          items: [
            "msi/msiprojectyml",
            "msi/inputsyml",
            "msi/collectorsyml",
            "msi/routesyml",
            "msi/outputsyml",
          ],
        },
        {
          type: "category",
          label: "Pipeline",
          items: [
            "msi/sources",
            "msi/normalization",
            "msi/functions",
            "msi/destinations",
          ],
        },
        "msi/state",
        {
          type: "category",
          label: "msi commands",
          collapsible: true,
          collapsed: true,
          link: {
            type: "doc",
            id: "msi/index",
          },
          items: [
            "msi/init/index",
            "msi/bootstrap/index",
            "msi/test-connection/index",
            "msi/run/index",
          ],
        },
      ],
    },
  ],
};

import React from "react";
import useBaseUrl from "@docusaurus/useBaseUrl";
import Link from "@docusaurus/Link";

export const Integrations = () => {
  return (
    <section className="my-20">
      <h2 className="mb-2 text-3xl md:text-4xl">Integrations</h2>
      <p className="mb-8">
        Integrate with and monitor your data stack.
      </p>
      <div className="grid grid-cols-1 gap-6  md:grid-cols-3 lg:gap-8">
        <Link to={useBaseUrl("/docs/integrations/snowflake")}>
          <div className=" scale flex flex-col items-center justify-center space-y-3 rounded-lg bg-[color:var(--ifm-card-background-color)] p-6 text-center shadow-lg">
            <img
              className="h-16 w-16"
              src="/img/snowflake.svg"
              alt="Snowflake logo"
            />
            <p className="text-lg">Snowflake</p>
          </div>
        </Link>
        <Link
          className=" scale flex flex-col items-center justify-center space-y-3 rounded-lg bg-[color:var(--ifm-card-background-color)] p-6 text-center shadow-lg"
          to={useBaseUrl("/docs/integrations/postgresql")}
        >
          <img
            className="h-16 w-16"
            src="/img/postgresql.svg"
            alt="PostgreSQL logo"
          />
          <p className="text-lg">PostgreSQL</p>
        </Link>
        <Link
          to={useBaseUrl("/docs/integrations/redshift")}
          className=" scale flex flex-col items-center justify-center space-y-3 rounded-lg bg-[color:var(--ifm-card-background-color)] p-6 text-center shadow-lg"
        >
          <img className="h-16 w-16" src="/img/redshift.svg" alt="Redshift logo" />
          <p className="text-lg">Redshift</p>
        </Link>
        <Link
          to={useBaseUrl("/docs/integrations/slack")}
          className=" scale flex flex-col items-center justify-center space-y-3 rounded-lg bg-[color:var(--ifm-card-background-color)] p-6 text-center shadow-lg"
        >
          <img className="h-16 w-16" src="http://assets.stickpng.com/images/5cb480cd5f1b6d3fbadece79.png" alt="Slack logo" />
          <p className="text-lg">Slack</p>
        </Link>
        <Link
          to={useBaseUrl("/docs/integrations/webhooks")}
          className=" scale flex flex-col items-center justify-center space-y-3 rounded-lg bg-[color:var(--ifm-card-background-color)] p-6 text-center shadow-lg"
        >
          <p className="text-lg">Webhooks</p>
        </Link>
        <Link
          to={useBaseUrl("/docs/integrations/email")}
          className=" scale flex flex-col items-center justify-center space-y-3 rounded-lg bg-[color:var(--ifm-card-background-color)] p-6 text-center shadow-lg"
        >
          <p className="text-lg">Email</p>
        </Link>
        <Link
          className=" scale flex flex-col items-center justify-center space-y-3 rounded-lg bg-[color:var(--ifm-card-background-color)] p-6 text-center shadow-lg"
          disabled
          >
          <img className="h-16 w-16" src="https://cdn.worldvectorlogo.com/logos/google-bigquery-logo-1.svg" alt="BigQuery logo" />
          <p className="text-lg">Google BigQuery</p>
        </Link>
        <Link
          disabled
          className=" scale flex flex-col items-center justify-center space-y-3 rounded-lg bg-[color:var(--ifm-card-background-color)] p-6 text-center shadow-lg"
        >
          <img className="h-16 w-16" src="https://asset.brandfetch.io/idofJOT4bu/id3jbLcFnO.png" alt="dbt Logo" />
          <p className="text-lg">dbt</p>
        </Link>
        <Link
          disabled
          className=" scale flex flex-col items-center justify-center space-y-3 rounded-lg bg-[color:var(--ifm-card-background-color)] p-6 text-center shadow-lg"
        >
          <img className="h-16" src="https://seeklogo.com/images/G/google-looker-logo-B27BD25E4E-seeklogo.com.png" alt="Looker logo" />
          <p className="text-lg">Looker</p>
        </Link>
        <Link
          disabled
          className=" scale flex flex-col items-center justify-center space-y-3 rounded-lg bg-[color:var(--ifm-card-background-color)] p-6 text-center shadow-lg"
        >
          <img className="h-16 w-16" src="https://iconape.com/wp-content/files/cw/345108/svg/345108.svg" alt="Mode logo" />
          <p className="text-lg">Mode</p>
        </Link>
        <Link
          disabled
          className=" scale flex flex-col items-center justify-center space-y-3 rounded-lg bg-[color:var(--ifm-card-background-color)] p-6 text-center shadow-lg"
        >
          <img className="h-16 w-16" src="http://assets.stickpng.com/images/58480fc5cef1014c0b5e4941.png" alt="Metabase logo" />
          <p className="text-lg">Metabase</p>
        </Link>
        <Link
          disabled
          className=" scale flex flex-col items-center justify-center space-y-3 rounded-lg bg-[color:var(--ifm-card-background-color)] p-6 text-center shadow-lg"
        >
          <img className="h-16" src="https://financeandbusiness.ucdavis.edu/sites/g/files/dgvnsk4871/files/styles/sf_landscape_16x9/public/images/article/tableau_logo.png?h=c673cd1c&itok=5J3wvhE8" alt="Tableau logo" />
          <p className="text-lg">Tableau</p>
        </Link>
        <Link
          disabled
          className=" scale flex flex-col items-center justify-center space-y-3 rounded-lg bg-[color:var(--ifm-card-background-color)] p-6 text-center shadow-lg"
        >
          <img className="h-16 w-16" src="http://assets.stickpng.com/images/5848104fcef1014c0b5e4950.png" alt="MySQL logo" />
          <p className="text-lg">MySQL</p>
        </Link>
        <Link
          disabled
          className=" scale flex flex-col items-center justify-center space-y-3 rounded-lg bg-[color:var(--ifm-card-background-color)] p-6 text-center shadow-lg"
        >
          <img className="h-16 w-16" src="https://avatars.githubusercontent.com/u/33643075?s=280&v=4" alt="Airflow logo" />
          <p className="text-lg">Airflow</p>
        </Link>
        <Link
          disabled
          className=" scale flex flex-col items-center justify-center space-y-3 rounded-lg bg-[color:var(--ifm-card-background-color)] p-6 text-center shadow-lg"
        >
          <img className="h-16 w-16" src="https://symbols.getvecta.com/stencil_91/7_pagerduty-icon.32302d0739.png" alt="PagerDuty logo" />
          <p className="text-lg">PagerDuty</p>
        </Link>
        <Link
          disabled
          className=" scale flex flex-col items-center justify-center space-y-3 rounded-lg bg-[color:var(--ifm-card-background-color)] p-6 text-center shadow-lg"
        >
          <img className="h-16 w-16" src="https://cdn.iconscout.com/icon/free/png-256/power-bi-3244521-2701891.png" alt="Power BI logo" />
          <p className="text-lg">Power BI</p>
        </Link>
      </div>
    </section>
  );
};

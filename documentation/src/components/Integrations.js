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
          <img className="h-16 w-16" src="/img/Slack_Mark.svg" alt="Slack logo" />
          <p className="text-lg">Slack</p>
        </Link>
        <Link
          to={useBaseUrl("/docs/integrations/webhooks")}
          className=" scale flex flex-col items-center justify-center space-y-3 rounded-lg bg-[color:var(--ifm-card-background-color)] p-6 text-center shadow-lg"
        >
          <img className="h-16 w-16" src="/img/webhooks.svg" alt="Webhook logo" />
          <p className="text-lg">Webhooks</p>
        </Link>
        <Link
          to={useBaseUrl("/docs/integrations/email")}
          className=" scale flex flex-col items-center justify-center space-y-3 rounded-lg bg-[color:var(--ifm-card-background-color)] p-6 text-center shadow-lg"
        >
          <img className="h-16 w-16" src="/img/email.png" alt="Email logo" />
          <p className="text-lg">Email</p>
        </Link>
        <Link
          className=" scale flex flex-col items-center justify-center space-y-3 rounded-lg bg-[color:var(--ifm-card-background-color)] p-6 text-center shadow-lg"
          disabled
          >
          <img className="h-16 w-16" src="/img/bigquery.svg" alt="BigQuery logo" />
          <p className="text-lg">Google BigQuery</p>
        </Link>
        <Link
          disabled
          className=" scale flex flex-col items-center justify-center space-y-3 rounded-lg bg-[color:var(--ifm-card-background-color)] p-6 text-center shadow-lg"
        >
          <img className="h-16 w-16" src="/img/dbt.png" alt="dbt Logo" />
          <p className="text-lg">dbt</p>
        </Link>
        <Link
          disabled
          className=" scale flex flex-col items-center justify-center space-y-3 rounded-lg bg-[color:var(--ifm-card-background-color)] p-6 text-center shadow-lg"
        >
          <img className="h-16" src="/img/looker.png" alt="Looker logo" />
          <p className="text-lg">Looker</p>
        </Link>
        <Link
          disabled
          className=" scale flex flex-col items-center justify-center space-y-3 rounded-lg bg-[color:var(--ifm-card-background-color)] p-6 text-center shadow-lg"
        >
          <img className="h-16 w-16" src="/img/mode.svg" alt="Mode logo" />
          <p className="text-lg">Mode</p>
        </Link>
        <Link
          disabled
          className=" scale flex flex-col items-center justify-center space-y-3 rounded-lg bg-[color:var(--ifm-card-background-color)] p-6 text-center shadow-lg"
        >
          <img className="h-16 w-16" src="/img/metabase.svg" alt="Metabase logo" />
          <p className="text-lg">Metabase</p>
        </Link>
        <Link
          disabled
          className=" scale flex flex-col items-center justify-center space-y-3 rounded-lg bg-[color:var(--ifm-card-background-color)] p-6 text-center shadow-lg"
        >
          <img className="h-16" src="/img/tableau.png" alt="Tableau logo" />
          <p className="text-lg">Tableau</p>
        </Link>
        <Link
          disabled
          className=" scale flex flex-col items-center justify-center space-y-3 rounded-lg bg-[color:var(--ifm-card-background-color)] p-6 text-center shadow-lg"
        >
          <img className="h-16 w-16" src="/img/mysql.png" alt="MySQL logo" />
          <p className="text-lg">MySQL</p>
        </Link>
        <Link
          disabled
          className=" scale flex flex-col items-center justify-center space-y-3 rounded-lg bg-[color:var(--ifm-card-background-color)] p-6 text-center shadow-lg"
        >
          <img className="h-16 w-16" src="/img/mssql.png" alt="MS SQL logo" />
          <p className="text-lg">MS SQL</p>
        </Link>        
        <Link
          disabled
          className=" scale flex flex-col items-center justify-center space-y-3 rounded-lg bg-[color:var(--ifm-card-background-color)] p-6 text-center shadow-lg"
        >
          <img className="h-16 w-16" src="/img/airflow.png" alt="Airflow logo" />
          <p className="text-lg">Airflow</p>
        </Link>
        <Link
          disabled
          className=" scale flex flex-col items-center justify-center space-y-3 rounded-lg bg-[color:var(--ifm-card-background-color)] p-6 text-center shadow-lg"
        >
          <img className="h-16 w-16" src="/img/pagerduty.png" alt="PagerDuty logo" />
          <p className="text-lg">PagerDuty</p>
        </Link>
        <Link
          disabled
          className=" scale flex flex-col items-center justify-center space-y-3 rounded-lg bg-[color:var(--ifm-card-background-color)] p-6 text-center shadow-lg"
        >
          <img className="h-16 w-16" src="/img/powerbi.png" alt="Power BI logo" />
          <p className="text-lg">Power BI</p>
        </Link>
      </div>
    </section>
  );
};

import React from "react";
import Link from "@docusaurus/Link";
import useBaseUrl from "@docusaurus/useBaseUrl";

function SDKs() {
  return (
    <div className="rounded-lg bg-[color:var(--ifm-card-background-color)] p-5 shadow">
      <div className="flex items-center space-x-4">
        <svg
          width="13"
          className="mb-4 h-10 w-10 rounded-lg bg-[color:var(--ifm-color-highlight)] p-2 text-[color:var(--ifm-background-color)]"
          height="14"
          viewBox="0 0 13 14"
          fill="none"
          xmlns="http://www.w3.org/2000/svg"
        >
          <path
            d="M11.7538 3.95126C11.9211 3.87442 12.0617 3.75645 12.16 3.61054C12.2583 3.46463 12.3103 3.29653 12.3103 3.12505C12.3103 2.95357 12.2583 2.78547 12.16 2.63956C12.0617 2.49365 11.9211 2.37567 11.7538 2.29884L6.95069 0.0974684C6.81075 0.0333693 6.65646 0 6.50002 0C6.34358 0 6.18929 0.0333693 6.04935 0.0974684L1.2462 2.29884C1.07895 2.37567 0.938326 2.49365 0.840051 2.63956C0.741776 2.78547 0.689727 2.95357 0.689727 3.12505C0.689727 3.29653 0.741776 3.46463 0.840051 3.61054C0.938326 3.75645 1.07895 3.87442 1.2462 3.95126L6.04935 6.15263C6.18929 6.21673 6.34358 6.2501 6.50002 6.2501C6.65646 6.2501 6.81075 6.21673 6.95069 6.15263L11.7538 3.95126Z"
            fill="currentColor"
          />
          <path
            d="M7.07848 13.3891C6.99477 13.2516 6.95078 13.0968 6.95069 12.9393V7.6124C6.95079 7.44081 7.003 7.27264 7.10147 7.12672C7.19994 6.9808 7.34079 6.86289 7.50824 6.78619L11.5411 4.93785C11.6948 4.86746 11.8655 4.83423 12.0371 4.84132C12.2088 4.8484 12.3756 4.89557 12.5217 4.97833C12.6679 5.0611 12.7885 5.17673 12.8722 5.31424C12.9559 5.45175 12.9999 5.60659 13 5.76406V11.091C12.9999 11.2626 12.9477 11.4307 12.8492 11.5766C12.7507 11.7226 12.6099 11.8405 12.4425 11.9172L8.40958 13.7655C8.25591 13.8359 8.08516 13.8691 7.91355 13.862C7.74193 13.855 7.57513 13.8078 7.42898 13.725C7.28284 13.6423 7.16218 13.5266 7.07848 13.3891Z"
            fill="currentColor"
          />
          <path
            d="M0.96287 4.97833C1.13449 4.97125 1.30523 5.00448 1.45891 5.07487L5.49178 6.9232C5.65922 6.9999 5.80007 7.11781 5.89854 7.26374C5.99701 7.40966 6.04922 7.57783 6.04932 7.74941V13.0763C6.04923 13.2338 6.00524 13.3886 5.92154 13.5261C5.83783 13.6637 5.71718 13.7793 5.57103 13.862C5.42488 13.9448 5.25809 13.992 5.08647 13.9991C4.91485 14.0061 4.7441 13.9729 4.59043 13.9025L0.55756 12.0542C0.390115 11.9775 0.249269 11.8596 0.150797 11.7137C0.0523254 11.5677 0.000115828 11.3996 1.58649e-05 11.228V5.90107C0.000107582 5.7436 0.044094 5.58876 0.127801 5.45125C0.211509 5.31374 0.332161 5.19812 0.478309 5.11535C0.624457 5.03258 0.791253 4.98542 0.96287 4.97833Z"
            fill="currentColor"
          />
        </svg>
        <h2 className="mb-4 text-xl font-semibold">Integrations</h2>
      </div>
      <p className="mb-4 flex-grow">
          Integrate Monosi with your entire data stack with these integrations, and more.
      </p>
      <ul className="flex flex-col space-y-2">
        {/* <ul className="grid grid-cols-2 gap-6 xl:gap-8"> */}
        <li className="">
          <Link
            className="flex items-center space-x-3 hover:underline"
            to={useBaseUrl("/docs/integrations/snowflake")}
          >
            <img
              className="h-8 w-8 transition hover:scale-110"
              src="/img/snowflake.svg"
              alt="Snowflake logo"
            />
            <p className="font-semibold">Snowflake</p>
          </Link>
        </li>
        <li className="">
          <Link
            className="flex items-center space-x-3 hover:underline"
            to={useBaseUrl("/docs/integrations/bigquery")}
          >
            <img
              className="h-8 w-8 transition hover:scale-110"
              src="/img/bigquery.svg"
              alt="BigQuery logo"
            />
            <p className="font-semibold">BigQuery</p>
          </Link>
        </li>

        <li className="">
          <Link
            className="flex items-center space-x-5"
            to={useBaseUrl("/docs/integrations/redshift")}
          >
            <div className="flex items-center space-x-3 hover:underline">
              <img
                className="h-8 w-8 transition hover:scale-110"
                src="/img/redshift.svg"
                alt="Redshift logo"
              />
              <p className="font-semibold">Redshift</p>{" "}
            </div>
          </Link>
        </li>
        <li className="">
          <Link to={useBaseUrl("/integrations")}>
            <div className="flex space-x-3 hover:underline" style={{justifyContent: 'right'}}>
              <p className="font-semibold">View all</p>
            </div>
          </Link>
        </li>
      </ul>
    </div>
  );
}

function Server() {
  return (
    <div className="flex flex-col rounded-lg bg-[color:var(--ifm-card-background-color)] p-5 shadow">
      <div className="flex items-center space-x-4">
        <svg
          className="mb-4 h-10 w-10 rounded-lg bg-[color:var(--ifm-color-highlight)] p-2 text-[color:var(--ifm-background-color)]"
          width="16"
          height="13"
          viewBox="0 0 16 13"
          fill="none"
          xmlns="http://www.w3.org/2000/svg"
        >
          <path
            fillRule="evenodd"
            clipRule="evenodd"
            d="M0 2C0 1.46957 0.210714 0.960859 0.585786 0.585786C0.960859 0.210714 1.46957 0 2 0H14C14.5304 0 15.0391 0.210714 15.4142 0.585786C15.7893 0.960859 16 1.46957 16 2V4C16 4.53043 15.7893 5.03914 15.4142 5.41421C15.0391 5.78929 14.5304 6 14 6H2C1.46957 6 0.960859 5.78929 0.585786 5.41421C0.210714 5.03914 0 4.53043 0 4V2ZM14 3C14 3.26522 13.8946 3.51957 13.7071 3.70711C13.5196 3.89464 13.2652 4 13 4C12.7348 4 12.4804 3.89464 12.2929 3.70711C12.1054 3.51957 12 3.26522 12 3C12 2.73478 12.1054 2.48043 12.2929 2.29289C12.4804 2.10536 12.7348 2 13 2C13.2652 2 13.5196 2.10536 13.7071 2.29289C13.8946 2.48043 14 2.73478 14 3ZM0 9C0 8.46957 0.210714 7.96086 0.585786 7.58579C0.960859 7.21071 1.46957 7 2 7H14C14.5304 7 15.0391 7.21071 15.4142 7.58579C15.7893 7.96086 16 8.46957 16 9V11C16 11.5304 15.7893 12.0391 15.4142 12.4142C15.0391 12.7893 14.5304 13 14 13H2C1.46957 13 0.960859 12.7893 0.585786 12.4142C0.210714 12.0391 0 11.5304 0 11V9ZM14 10C14 10.2652 13.8946 10.5196 13.7071 10.7071C13.5196 10.8946 13.2652 11 13 11C12.7348 11 12.4804 10.8946 12.2929 10.7071C12.1054 10.5196 12 10.2652 12 10C12 9.73478 12.1054 9.48043 12.2929 9.29289C12.4804 9.10536 12.7348 9 13 9C13.2652 9 13.5196 9.10536 13.7071 9.29289C13.8946 9.48043 14 9.73478 14 10Z"
            fill="currentColor"
          />
        </svg>
        <h2 className="mb-4 text-xl font-semibold">Guides</h2>
      </div>
      <p className="mb-4 flex-grow">
        Learn about how Monosi works and how to deploy and begin monitoring your data stack.
      </p>

      <ul className="flex list-disc flex-col space-y-2 pl-4">
        <li className="list-disc">
          <Link
            to={useBaseUrl("/docs/user-guide/getting-started")}
            className="hover:underline"
          >
            <p className="font-semibold">Getting Started</p>
          </Link>
        </li>
        <li className="list-disc">
          <Link
            to={useBaseUrl("/docs/user-guide/table-health")}
            className="hover:underline"
          >
            <p className="font-semibold">Ensuring Table Health</p>
          </Link>
        </li>
        <li className="list-disc">
          <Link
            to={useBaseUrl("/docs/contributing/contributing-overview")}
            className="hover:underline"
          >
            <p className="font-semibold">Contributing to Monosi</p>
          </Link>
        </li>
        {/* <li className="list-disc">
          <Link to={"#"} className="hover:underline">
            <p className="font-semibold">
              Monosi Cloud Waitlist
              <svg
                className="w-4 h-4 inline"
                fill="currentColor"
                viewBox="0 0 20 20"
                xmlns="http://www.w3.org/2000/svg"
              >
                <path d="M11 3a1 1 0 100 2h2.586l-6.293 6.293a1 1 0 101.414 1.414L15 6.414V9a1 1 0 102 0V4a1 1 0 00-1-1h-5z" />
                <path d="M5 5a2 2 0 00-2 2v8a2 2 0 002 2h8a2 2 0 002-2v-3a1 1 0 10-2 0v3H5V7h3a1 1 0 000-2H5z" />
              </svg>
            </p>
          </Link>
        </li> */}
      </ul>
      <Link
        to={useBaseUrl("/docs/user-guide/local-deployment")}
        className="mt-2 -ml-2 hover:underline"
      >
        <p className="font-semibold">
          <span className="mr-1">⭐</span> Quick Install (with Docker)
        </p>
      </Link>
    </div>
  );
}

function Tools() {
  return (
    <div className="flex flex-col rounded-lg bg-[color:var(--ifm-card-background-color)] p-5 shadow">
      <div className="flex items-center space-x-4">
        <svg
          className="mb-4 h-10 w-10 rounded-lg bg-[color:var(--ifm-color-highlight)] p-2 text-[color:var(--ifm-background-color)]"
          viewBox="0 0 15 15"
          fill="currentColor"
          xmlns="http://www.w3.org/2000/svg"
        >
          <path
            d="M9.70951 4.76529C9.35941 4.41517 9.35941 3.8475 9.70951 3.49739L11.8346 1.37235C11.3366 1.13367 10.7788 1 10.1897 1C8.08533 1 6.37939 2.70594 6.37939 4.81031C6.37939 5.39939 6.51306 5.95726 6.75172 6.4552L1.37136 11.8355C0.876212 12.3307 0.876212 13.1336 1.37136 13.6286C1.86651 14.1238 2.6693 14.1238 3.16445 13.6286L8.54481 8.24829C9.04275 8.48695 9.60066 8.62062 10.1897 8.62062C12.2941 8.62062 14 6.91468 14 4.81031C14 4.2287 13.8697 3.67752 13.6367 3.18438L11.5166 5.30445C11.1665 5.65458 10.5988 5.65458 10.2487 5.30446L9.70951 4.76529Z"
            fill="currentColor"
            stroke="currentColor"
            strokeWidth="0.75"
            strokeLinecap="round"
            strokeLinejoin="round"
          />
          <path
            fillRule="evenodd"
            clipRule="evenodd"
            d="M11.5223 8.36487L6.75835 3.08342C7.97767 2.68073 9.53838 3.15399 10.6381 4.37315C11.7378 5.5923 12.0482 7.19339 11.5223 8.36487ZM6.15533 8.43785L6.13426 8.4145C6.13776 8.4184 6.14126 8.4223 6.14478 8.42619C6.14829 8.43009 6.15181 8.43397 6.15533 8.43785Z"
            fill="currentColor"
          />
        </svg>

        <h2 className="mb-4 text-xl font-semibold">Get Started</h2>
      </div>
      <p className="mb-4 flex-grow">
          Monosi deploys as a full, standalone data observability solution that provides functionality to monitor your data pipelines for anomalies.
      </p>
      <div className="flex flex-col space-y-2">
        <Link
          to={useBaseUrl("/docs/user-guide/introduction")}
          className="flex space-x-3 font-semibold hover:underline"
        >
          <svg
            className="h-6 w-6 transition hover:scale-110"
            fill="currentColor"
            viewBox="0 0 20 20"
            xmlns="http://www.w3.org/2000/svg"
          >
            <path
              fillRule="evenodd"
              d="M3 5a2 2 0 012-2h10a2 2 0 012 2v8a2 2 0 01-2 2h-2.22l.123.489.804.804A1 1 0 0113 18H7a1 1 0 01-.707-1.707l.804-.804L7.22 15H5a2 2 0 01-2-2V5zm5.771 7H5V5h10v7H8.771z"
              clipRule="evenodd"
            />
          </svg>
          <div className="">Web UI</div>
        </Link>
        <Link
          to={useBaseUrl("/docs/user-guide/table-health")}
          className="flex space-x-3 font-semibold hover:underline"
        >
          <svg
            className="h-6 w-6 transition hover:scale-110"
            fill="currentColor"
            viewBox="0 0 20 20"
            xmlns="http://www.w3.org/2000/svg"
          >
            <path
              fillRule="evenodd"
              d="M3 5a2 2 0 012-2h10a2 2 0 012 2v8a2 2 0 01-2 2h-2.22l.123.489.804.804A1 1 0 0113 18H7a1 1 0 01-.707-1.707l.804-.804L7.22 15H5a2 2 0 01-2-2V5zm5.771 7H5V5h10v7H8.771z"
              clipRule="evenodd"
            />
          </svg>
          <div className="">Table Health Monitoring</div>
        </Link>
          {/* <Link
          to={useBaseUrl("/docs/msi")}
          className="flex space-x-3 font-semibold hover:underline"
        >
          <svg
            className="h-6 w-6 transition hover:scale-110"
            fill="currentColor"
            viewBox="0 0 20 20"
            xmlns="http://www.w3.org/2000/svg"
          >
            <path
              fillRule="evenodd"
              d="M2 5a2 2 0 012-2h12a2 2 0 012 2v10a2 2 0 01-2 2H4a2 2 0 01-2-2V5zm3.293 1.293a1 1 0 011.414 0l3 3a1 1 0 010 1.414l-3 3a1 1 0 01-1.414-1.414L7.586 10 5.293 7.707a1 1 0 010-1.414zM11 12a1 1 0 100 2h3a1 1 0 100-2h-3z"
              clipRule="evenodd"
            />
          </svg>
          <div>msi (CLI)</div>
        </Link> */ }
      </div>
    </div>
  );
}

export const Intro = () => {
  return (
    <section className="mt-1 mb-14">
      <h1 className="mb-4 text-4xl font-semibold tracking-wide md:text-5xl">
        Monosi Documentation
      </h1>
      <p className="max-w-2xl text-xl">
        Learn about Monosi, the open source platform for data observability and quality.
      </p>

      <div className="my-10 grid grid-cols-1 gap-6 md:grid-cols-2 lg:grid-cols-3 lg:gap-8">
        <Tools />
        <Server />
        <SDKs />
      </div>
    </section>
  );
};

import React from "react";
import Layout from "@theme/Layout";
import useDocusaurusContext from "@docusaurus/useDocusaurusContext";
import {Integrations} from "../components/Integrations";

export default function MonosiIntegrations() {
  const context = useDocusaurusContext();
  const {siteConfig = {}} = context;
  return (
    <Layout
      title="Monosi Integrations"
      permalink="/integrations"
    >
      <div className="mx-auto mb-12 max-w-screen-lg p-6 md:p-10">
        <Integrations />
      </div>
    </Layout>
  );
}

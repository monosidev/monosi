import React from "react";

export const MonosiCloud = () => {
  return (
    <section
      id="cloud"
      className="mt-24 mb-12 flex max-w-7xl items-center space-x-5 rounded-lg bg-[color:var(--ifm-card-background-color)] p-5"
    >
      <img
        className="h-12 flex-none "
        src="https://www.monosi.dev/images/monosi_logo.png"
      />
      <p className="my-3 block">
        Monosi Cloud is a fully managed cloud offering of the open-source
        suite of tools. We are currently accepting private Design Partners.{" "}
        <a
          href="https://monosi.dev/cloud.html"
          className="text-blue-400 underline hover:text-blue-200"
        >
          Apply here!
        </a>
      </p>
    </section>
  );
};

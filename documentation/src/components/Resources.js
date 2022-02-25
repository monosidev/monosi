import React from "react";
import useBaseUrl from "@docusaurus/useBaseUrl";
import Link from "@docusaurus/Link";

const links = [
  {
    type: "article",
    title: "Why Monosi?",
    length: "3-20 min reads",
    url: "#",
  },
  {
    type: "article",
    title: "Monosi Core Concepts",
    length: "20 min read",
    url: "#",
  },
  // {
  //   type: "video",
  //   title: "Monosi architecture deep dive",
  //   length: "20 min read/watch",
  //   url: "#",
  // },
];

export const Resources = () => {
  return (
    <section className="my-12">
      <h2 className="text-3xl md:text-4xl">Resources and guides</h2>
      <ul className="mt-5 flex flex-col space-y-3 text-lg">
        {links.map((link, i) => (
          <li key={i} className="flex items-center space-x-3 hover:underline">
            {link.type === "article" ? (
              <svg
                className="h-7 w-7"
                fill="currentColor"
                viewBox="0 0 20 20"
                xmlns="http://www.w3.org/2000/svg"
              >
                <path
                  fillRule="evenodd"
                  d="M4 4a2 2 0 012-2h4.586A2 2 0 0112 2.586L15.414 6A2 2 0 0116 7.414V16a2 2 0 01-2 2H6a2 2 0 01-2-2V4zm2 6a1 1 0 011-1h6a1 1 0 110 2H7a1 1 0 01-1-1zm1 3a1 1 0 100 2h6a1 1 0 100-2H7z"
                  clipRule="evenodd"
                />
              </svg>
            ) : (
              <svg
                className="h-7 w-7"
                fill="currentColor"
                viewBox="0 0 20 20"
                xmlns="http://www.w3.org/2000/svg"
              >
                <path
                  fillRule="evenodd"
                  d="M10 18a8 8 0 100-16 8 8 0 000 16zM9.555 7.168A1 1 0 008 8v4a1 1 0 001.555.832l3-2a1 1 0 000-1.664l-3-2z"
                  clipRule="evenodd"
                />
              </svg>
            )}

            <Link className="flex-1" to={useBaseUrl(link.url)}>
              {link.title}{" "}
              <span className="text-xs uppercase opacity-80">
                {link.length}
              </span>
            </Link>
          </li>
        ))}
      </ul>
    </section>
  );
};

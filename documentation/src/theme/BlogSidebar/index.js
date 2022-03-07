import React from "react";
import Link from "@docusaurus/Link";
export default function BlogSidebar({sidebar, row}) {

  const tags = []
  // const tags = [
  //   {
  //     title: "community",
  //     url: "/blog/tags/community",
  //   },
  //   {
  //     title: "announcement",
  //     url: "/blog/tags/announcement",
  //   },
  //   {
  //     title: "releases",
  //     url: "/blog/tags/release",
  //   },
  // ];

  if (sidebar.items.length === 0 || tags.length === 0) {
    return null;
  }

  return (
    <div>
      <div className={row && "col col--4"}>
        <h3 className="mb-2 text-xl font-semibold">Tags</h3>
        <ul>
          {
            <span className="mb-5 flex flex-wrap">
              {tags.map(({title, url}) => (
                <Link
                  key={url}
                  className="my-2 mr-2 inline-flex items-center rounded-full bg-[color:var(--ifm-badge-background-color)] px-3 py-0.5 text-sm font-medium text-[color:var(--ifm-color)] no-underline hover:opacity-80"
                  to={url}
                >
                  {title}
                </Link>
              ))}
            </span>
          }
        </ul>
      </div>
    </div>
  );
}

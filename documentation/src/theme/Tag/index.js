/**
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
import React from "react";
import Link from "@docusaurus/Link";

function Tag(props) {
  const {permalink, name, count} = props;
  return (
    <Link
      href={permalink}
      className={`my-2 mr-2 inline-flex items-center rounded-full bg-[color:var(--ifm-badge-background-color)] px-3 py-1 text-sm font-medium text-[color:var(--ifm-color)] no-underline hover:opacity-80 ${
        count ? "" : ""
      }`}
    >
      {name}
      {count && (
        <span className="ml-2 inline-flex items-center justify-center rounded-full bg-[color:var(--ifm-color)] px-2 py-1 text-xs font-bold leading-none text-[color:var(--ifm-badge-background-color)]">
          {count}
        </span>
      )}
    </Link>
  );
}

export default Tag;

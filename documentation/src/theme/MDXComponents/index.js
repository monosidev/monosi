/**
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
import React, {isValidElement} from "react";
import Link from "@docusaurus/Link";
import CodeBlock from "@theme/CodeBlock";
import Heading from "@theme/Heading";
import Details from "@theme/Details";

const MDXComponents = {
  code: (props) => {
    const {children} = props; // For retrocompatibility purposes (pretty rare use case)
    // See https://github.com/facebook/docusaurus/pull/1584

    if (isValidElement(children)) {
      return children;
    }

    return !children.includes("\n") ? (
      <code {...props} />
    ) : (
      <CodeBlock {...props} />
    );
  },
  a: (props) => <Link {...props} />,
  pre: (props) => {
    const {children} = props; // See comment for `code` above

    if (isValidElement(children?.props?.children)) {
      return children?.props.children;
    }

    return (
      <div className="md:text-md w-80 text-sm sm:w-full sm:max-w-lg md:max-w-5xl">
        <CodeBlock
          {...(isValidElement(children) ? children?.props : {...props})}
        />
      </div>
    );
  },
  details: (props) => {
    const items = React.Children.toArray(props.children); // Split summary item from the rest to pass it as a separate prop to the Detais theme component

    const summary = items.find((item) => item?.props?.mdxType === "summary");
    const children = <>{items.filter((item) => item !== summary)}</>;
    return (
      <Details {...props} summary={summary}>
        {children}
      </Details>
    );
  },
  h1: Heading("h1"),
  h2: Heading("h2"),
  h3: Heading("h3"),
  h4: Heading("h4"),
  h5: Heading("h5"),
  h6: Heading("h6"),
  preview: Preview,
};
export default MDXComponents;

export function Preview({
  page: {
    frontMatter,
    metadata,
    // contentTitle // doesnt seem to work yet
  },
  children,
}) {
  const [show, setShow] = React.useState(false);
  return (
    <span
      onMouseEnter={() => setShow(true)}
      onMouseLeave={() => setShow(false)}
      style={{position: "relative", display: "inline-block"}}
    >
      <a href={metadata.permalink}>
        {children}
        <InfoIcon />
      </a>
      {show && (
        <div
          style={{
            position: "absolute",
            zIndex: 1,
            width: "max-content",
            maxWidth: "350px",
            display: "flex",
            flexDirection: "column",
            borderRadius: "8px",
            backgroundColor: "#f2f2f2",
            color: "#020202",
            padding: "8px",
          }}
        >
          <div
            style={{fontSize: "1rem", fontWeight: "bold", textAlign: "center"}}
          >
            {frontMatter.title}
          </div>
          <div
            style={{
              backgroundColor: "#f2f2f2",
              padding: 10,
              fontSize: "0.8rem",
            }}
          >
            <span style={{}}>{metadata.description}</span>
            <span
              style={{marginTop: "1rem", display: "block", fontSize: "0.75rem"}}
            >
              <a style={{color: "blue"}} href={metadata.permalink}>
                see full article >>
              </a>
            </span>
          </div>
        </div>
      )}
    </span>
  );
}

function InfoIcon() {
  return (
    <span
      style={{
        display: "inline-flex",
        flexDirection: "column",
        alignItems: "center",
      }}
    >
      <svg
        xmlns="http://www.w3.org/2000/svg"
        height="0.75rem"
        width="0.75rem"
        viewBox="0 0 20 20"
        fill="currentColor"
      >
        <path
          fillRule="evenodd"
          d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z"
          clipRule="evenodd"
        />
      </svg>
    </span>
  );
}

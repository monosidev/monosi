import React from "react";
import clsx from "clsx";
import Link from "@docusaurus/Link";
import {v4 as uuidv4} from "uuid";

export function RelatedReadContainer({children}) {
  let rl = [];
  if (React.Children.count(children) > 1) {
    React.Children.forEach(children, function (child) {
      let id = uuidv4();
      rl.push({id: id, child: child});
    });
  }
  return (
    <div className={"related-read-div"}>
      <span className={"related-read-label"}>Related 📚 </span>
      {rl.length > 1 ? (
        <ul className="related-read-list">
          {rl.map(({id, child}) => (
            <li key={id}>{child}</li>
          ))}
        </ul>
      ) : (
        children
      )}
    </div>
  );
}

export function RelatedReadItem({page, children}) {
  const {
    frontMatter,
    metadata,
    // contentTitle // doesnt seem to work yet
  } = page;
  // console.log({ frontMatter, metadata })
  // identify tags
  let tagClass, tag;
  for (const t of frontMatter.tags) {
    if (
      [
        "developer-guide",
        "operation-guide",
        "tutorial",
        "explanation",
        "reference",
      ].includes(t)
    ) {
      tag = t;
      tagClass = "archetype-tag-" + t;
    }
  }
  return (
    <>
      <Preview className={"related-read-link"} page={page}>
        {children || frontMatter.title}
      </Preview>
      <span className={clsx("related-read-archetype-tag", tagClass)}>
        {tag}
      </span>
    </>
  );
}

export function Preview({
  className,
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
      className={className}
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

// TODO - delete everything below this line once we deprecate

export default function RelatedReadList({readlist}) {
  let readingList = [];
  for (const item of readlist) {
    const tagStuff = tagInfo(item[2]);
    if (tagStuff instanceof Error) throw tagStuff;
    // form data structure
    readingList.push({
      id: uuidv4(),
      text: item[0],
      goTo: item[1],
      tag: tagStuff.tag,
      tagClass: tagStuff.tagClass,
    });
  }
  if (readingList.length == 1) {
    return (
      <div className={"related-read-div"}>
        <span className={"related-read-label"}>Related 📚 </span>
        {readingList.map(({id, text, goTo, tag, tagClass}) => (
          <span key={id}>
            <Link className={"related-read-link"} to={goTo}>
              {text}
            </Link>
            <span className={clsx("related-read-archetype-tag", tagClass)}>
              {tag}
            </span>
          </span>
        ))}
      </div>
    );
  } else {
    return (
      <div className={"related-read-div"}>
        <span className={"related-read-label"}>Related 📚 </span>
        <ul className="related-read-list">
          {readingList.map(({id, text, goTo, tag, tagClass}) => (
            <li key={id}>
              <Link className={"related-read-link"} to={goTo}>
                {text}
              </Link>
              <span className={clsx("related-read-archetype-tag", tagClass)}>
                {tag}
              </span>
            </li>
          ))}
        </ul>
      </div>
    );
  }
}

function tagInfo(tag) {
  var tagClass;
  switch (tag) {
    case "developer guide":
      tagClass = "archetype-tag-developer-guide";
      break;
    case "operation guide":
      tagClass = "archetype-tag-operation-guide";
      break;
    case "tutorial":
      tagClass = "archetype-tag-tutorial";
      break;
    case "explanation":
      tagClass = "archetype-tag-explanation";
      break;
    case "reference":
      tagClass = "archetype-tag-reference";
      break;
    default:
      return new Error("unrecognized tag: " + tag);
  }
  return {tag: tag, tagClass: tagClass};
}

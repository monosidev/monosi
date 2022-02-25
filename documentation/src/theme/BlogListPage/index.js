import React from "react";
import useDocusaurusContext from "@docusaurus/useDocusaurusContext";
import BlogLayout from "@theme/BlogLayout";
import BlogPostItem from "@theme/BlogPostItem";
import BlogListPaginator from "@theme/BlogListPaginator";
import Link from "@docusaurus/Link";

import {translate} from "@docusaurus/Translate";
import {usePluralForm} from "@docusaurus/theme-common"; // Very simple pluralization: probably good enough for now

function useReadingTimePlural() {
  const {selectMessage} = usePluralForm();
  return (readingTimeFloat) => {
    const readingTime = Math.ceil(readingTimeFloat);
    return selectMessage(
      readingTime,
      translate(
        {
          id: "theme.blog.post.readingTime.plurals",
          description:
            'Pluralized label for "{readingTime} min read". Use as much plural forms (separated by "|") as your language support (see https://www.unicode.org/cldr/cldr-aux/charts/34/supplemental/language_plural_rules.html)',
          message: "One min read|{readingTime} min read",
        },
        {
          readingTime,
        }
      )
    );
  };
}

function BlogListPage(props) {
  const {metadata, items, sidebar} = props;
  const {
    siteConfig: {title: siteTitle},
  } = useDocusaurusContext();
  const {blogDescription, blogTitle, permalink} = metadata;
  const isBlogOnlyMode = permalink === "/";
  const title = isBlogOnlyMode ? siteTitle : blogTitle;

  return (
    <BlogLayout
      title={title}
      description={blogDescription}
      wrapperClassName="max-w-screen-lg mx-auto px-10 my-16"
      pageClassName=""
      searchMetadatas={{
        // assign unique search tag to exclude this page from search results!
        tag: "blog_posts_list",
      }}
      sidebar={sidebar}
    >
      <ul className="space-y-8">
        {items.map(({content: BlogPostContent}) => (
          <BlogListPageItem
            key={BlogPostContent.metadata.permalink}
            frontMatter={BlogPostContent.frontMatter}
            assets={BlogPostContent.assets}
            metadata={BlogPostContent.metadata}
            truncated={BlogPostContent.metadata.truncated}
          >
            <BlogPostContent />
          </BlogListPageItem>
        ))}
      </ul>
      <BlogListPaginator metadata={metadata} />
    </BlogLayout>
  );
}

export default BlogListPage;

// we fork the original BlogPostItem because it is not the look we want for the blog list
function BlogListPageItem(props) {
  const readingTimePlural = useReadingTimePlural();
  const {
    // children,
    frontMatter,
    metadata,
    truncated,
  } = props;
  const {date, formattedDate, permalink, tags, readingTime} = metadata;
  const {
    // author,
    title,
  } = frontMatter;
  return (
    <li>
      <h3 className="text-xl font-bold leading-relaxed">
        <Link className="text-[color:var(--color)]" to={permalink}>
          {title}
        </Link>
      </h3>
      <p className="py-1 text-sm">
        <time dateTime={date} className="text-sm">
          {formattedDate}
          {readingTime && (
            <>
              {" · "}
              {readingTimePlural(readingTime)}
            </>
          )}
        </time>
      </p>

      {(tags.length > 0 || truncated) && tags.length > 0 && (
        <span className="mb-5 flex flex-wrap">
          {tags.map(({label, permalink: tagPermalink}) => (
            <Link
              key={tagPermalink}
              className="inline-flex items-center rounded-full bg-[color:var(--ifm-badge-background-color)] px-3 py-0.5 text-sm font-medium text-[color:var(--ifm-color)] no-underline hover:opacity-80"
              to={tagPermalink}
            >
              {label}
            </Link>
          ))}
        </span>
      )}
      {props.children}
    </li>
  );
}

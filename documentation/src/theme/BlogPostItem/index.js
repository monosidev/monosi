import React from "react";
import {MDXProvider} from "@mdx-js/react";
import {translate} from "@docusaurus/Translate";
import Link from "@docusaurus/Link";
import MDXComponents from "@theme/MDXComponents";
import Seo from "@theme/Seo";
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

function BlogPostItem(props) {
  const readingTimePlural = useReadingTimePlural();
  const {
    children,
    frontMatter,
    metadata,
    truncated,
    isBlogPostPage = false,
  } = props;
  const {date, formattedDate, permalink, tags, readingTime} = metadata;
  const {
    author,
    title,
  } = frontMatter;

  const authorURL = frontMatter.author_url || frontMatter.authorURL;
  // const authorTitle = frontMatter.author_title || frontMatter.authorTitle;
  const authorImageURL =
    frontMatter.author_image_url || frontMatter.authorImageURL;

  const renderPostHeader = () => {
    const TitleHeading = isBlogPostPage ? "h1" : "h2";
    return (
      <header
        className={`my-12 flex flex-col ${
          isBlogPostPage ? "items-center justify-center" : ""
        }`}
      >
        <TitleHeading
          className={`mb-4 text-3xl font-semibold leading-relaxed  ${
            isBlogPostPage ? "max-w-lg text-center" : ""
          }`}
        >
          {isBlogPostPage ? (
            title
          ) : (
            <Link className="text-[color:var(--color)]" to={permalink}>
              {title}
            </Link>
          )}
        </TitleHeading>
        <div className="mb-4 flex items-center space-x-2 py-2">
          {authorImageURL && (
            <Link href={authorURL}>
              <img
                className="h-10 w-10 rounded-full shadow-md"
                src={authorImageURL}
                alt={author}
              />
            </Link>
          )}
          {author && (
            <p className="py-1 font-medium">
              {authorURL ? (
                <Link href={authorURL}>{author}</Link>
              ) : (
                <span>{author}</span>
              )}
            </p>
          )}
        </div>
        <time dateTime={date} className="mb-4 block text-sm">
          {formattedDate}
          {readingTime && (
            <>
              {" · "}
              {readingTimePlural(readingTime)}
            </>
          )}
        </time>

        {(tags.length > 0 || truncated) && tags.length > 0 && (
          <span className="mb-5 flex flex-wrap">
            {tags.map(({label, permalink: tagPermalink}) => (
              <Link
                key={tagPermalink}
                className="my-2 mr-2 inline-flex items-center rounded-full bg-[color:var(--ifm-badge-background-color)] px-3 py-0.5 text-sm font-medium text-[color:var(--ifm-color)] no-underline hover:opacity-80"
                to={tagPermalink}
              >
                {label}
              </Link>
            ))}
          </span>
        )}
      </header>
    );
  };

  return (
    <>
      <Seo
        {...{
          title,
          description: metadata.description,
          keywords: tags.map((x) => x.label).join(", "),
        }}
      />

      <article
        className={!isBlogPostPage ? "mb-8 max-w-screen-lg lg:mb-0" : undefined}
      >
        {renderPostHeader()}
        <article className="md:prose-md prose mx-auto sm:prose lg:prose-lg">
          <MDXProvider components={MDXComponents}>{children}</MDXProvider>
        </article>
      </article>
    </>
  );
}

export default BlogPostItem;

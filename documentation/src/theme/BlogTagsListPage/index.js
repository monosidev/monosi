/**
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
import React from "react";
import BlogLayout from "@theme/BlogLayout";
import TagsListByLetter from "@theme/TagsListByLetter";
import {
  ThemeClassNames,
  translateTagsPageTitle,
} from "@docusaurus/theme-common";

function BlogTagsListPage(props) {
  const {tags, sidebar} = props;
  const title = translateTagsPageTitle();
  return (
    <BlogLayout
      title={title}
      wrapperClassName="max-w-screen-lg mx-auto px-10 my-16"
      pageClassName={ThemeClassNames.page.blogTagsListPage}
      searchMetadatas={{
        // assign unique search tag to exclude this page from search results!
        tag: "blog_tags_list",
      }}
      sidebar={sidebar}
    >
      <h1 className="mb-5 text-3xl font-semibold">{title}</h1>
      <TagsListByLetter tags={Object.values(tags)} />
    </BlogLayout>
  );
}

export default BlogTagsListPage;

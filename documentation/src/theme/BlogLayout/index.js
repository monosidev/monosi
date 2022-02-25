import React from "react";
import Layout from "@theme/Layout";
import BlogSidebar from "@theme/BlogSidebar";

function BlogLayout(props) {
  const {sidebar, children, ...layoutProps} = props;
  const hasSidebar = sidebar && sidebar.items.length > 0;

  return (
    <Layout {...layoutProps} className="relative">
      <div className="flex space-x-20 ">
        <main itemScope itemType="http://schema.org/Blog">
          {children}
        </main>
        {hasSidebar && (
          <aside className="sticky top-24 mt-12 hidden h-full md:inline">
            <BlogSidebar sidebar={sidebar} />
          </aside>
        )}
      </div>
    </Layout>
  );
}

export default BlogLayout;

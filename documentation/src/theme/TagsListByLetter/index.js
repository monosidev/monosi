/**
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
import React from "react";
import Tag from "@theme/Tag";
import {listTagsByLetters} from "@docusaurus/theme-common";

function TagLetterEntryItem({letterEntry}) {
  return (
    <article>
      <h2 className="text-xl font-semibold">{letterEntry.letter}</h2>
      <ul className="mb-5">
        {letterEntry.tags.map((tag) => (
          <li key={tag.permalink} className="mx-2 my-1 inline-block">
            <Tag {...tag} />
          </li>
        ))}
      </ul>
      <hr />
    </article>
  );
}

function TagsListByLetter({tags}) {
  const letterList = listTagsByLetters(tags);
  return (
    <section className="flex flex-col space-y-10">
      {letterList.map((letterEntry) => (
        <TagLetterEntryItem
          key={letterEntry.letter}
          letterEntry={letterEntry}
        />
      ))}
    </section>
  );
}

export default TagsListByLetter;

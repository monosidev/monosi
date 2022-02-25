import React from "react";

export default function RowOfImages({imagePath1, imagePath2}) {
  return (
    <div className={"docs-centered-image-wrapper"}>
      <div className="row">
        <div className="col col--6">
          <img className="docs-centered-image-size-100" src={imagePath1} />
        </div>
        <div className="col col--6">
          <img className="docs-centered-image-size-100" src={imagePath2} />
        </div>
      </div>
    </div>
  );
}

import React from "react";
import {v4 as uuidv4} from "uuid";

export default function CenteredImage({imagePath, imageSize, title, legend}) {
  const legendList = [];
  if (legend != undefined) {
    for (const item of legend) {
      legendList.push({
        id: uuidv4(),
        symbol: item[0],
        description: item[1],
      });
    }
  }
  let imageClass = "";
  switch (imageSize) {
    case "25":
      imageClass = "docs-centered-image-size-25";
      break;
    case "50":
      imageClass = "docs-centered-image-size-50";
      break;
    case "75":
      imageClass = "docs-centered-image-size-75";
      break;
    default:
      imageClass = "docs-centered-image-size-100";
  }
  return (
    <div className={"docs-image-wrapper"}>
      <div className={"docs-image-title-wrapper"}>
        <p className={"docs-image-title"}>{title}</p>
      </div>
      <div className={"docs-centered-image-wrapper"}>
        <img className={imageClass} src={imagePath} alt={title} />
      </div>
      {legendList.length > 0 && (
        <div className={"docs-image-legend-wrapper"}>
          <ul className={"docs-image-legend-list"}>
            {legendList.map(({id, symbol, description}) => (
              <li key={id}>
                <span className={"docs-image-legend-symbol"}>{symbol}</span> ={" "}
                {description}
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}

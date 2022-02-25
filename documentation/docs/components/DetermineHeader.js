import React from "react";
import clsx from "clsx";
import Link from "@docusaurus/Link";

export default function DetermineHeader({hLevel, hText}) {
  switch (hLevel) {
    case "##":
      return <h2>{hText}</h2>;
      break;
    case "###":
      return <h3>{hText}</h3>;
      break;
    case "####":
      return <h4>{hText}</h4>;
      break;
    case "#####":
      return <h4>{hText}</h4>;
      break;
    default:
      return null;
  }
}

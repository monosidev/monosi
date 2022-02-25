import React from "react";

export default function CustomWarning({
  children,
  title = "experimental",
  color = "var(--ifm-color-warning)", // you can customize with any color you wish
}) {
  const [isOpen, setOpen] = React.useState(false);
  if (!isOpen) {
    return (
      <button
        onClick={() => setOpen(!isOpen)}
        style={{
          border: 0,
          borderRadius: "20px",
          padding: "0.5rem",
          marginBottom: "1rem",
          backgroundColor: color,
          borderColor: color,
          cursor: "pointer",
        }}
      >
        <h5 style={{textTransform: "uppercase", color: "black", margin: 0}}>
          <span
            style={{
              display: "inline-block",
              verticalAlign: "middle",
              marginRight: "0.2em",
            }}
          >
            <svg
              xmlns="http://www.w3.org/2000/svg"
              width="16"
              height="16"
              viewBox="0 0 16 16"
              style={{fill: "black"}}
            >
              <path
                fillRule="evenodd"
                d="M8.893 1.5c-.183-.31-.52-.5-.887-.5s-.703.19-.886.5L.138 13.499a.98.98 0 0 0 0 1.001c.193.31.53.501.886.501h13.964c.367 0 .704-.19.877-.5a1.03 1.03 0 0 0 .01-1.002L8.893 1.5zm.133 11.497H6.987v-2.003h2.039v2.003zm0-3.004H6.987V5.987h2.039v4.006z"
              ></path>
            </svg>
          </span>
          {title}
        </h5>
      </button>
    );
  }

  return (
    <div
      style={{
        backgroundColor: color,
        borderColor: color,
        borderRadius: "var(--ifm-alert-border-radius)",
        borderStyle: "solid",
        borderWidth: "var(--ifm-alert-border-width)",
        padding:
          "var(--ifm-alert-padding-vertical) var(--ifm-alert-padding-horizontal)",
        marginBottom: "1em",
      }}
    >
      <h5 style={{textTransform: "uppercase", color: "black"}}>
        <span
          style={{
            display: "inline-block",
            verticalAlign: "middle",
            marginRight: "0.2em",
          }}
        >
          <svg
            xmlns="http://www.w3.org/2000/svg"
            width="16"
            height="16"
            viewBox="0 0 16 16"
            style={{fill: "black"}}
          >
            <path
              fillRule="evenodd"
              d="M8.893 1.5c-.183-.31-.52-.5-.887-.5s-.703.19-.886.5L.138 13.499a.98.98 0 0 0 0 1.001c.193.31.53.501.886.501h13.964c.367 0 .704-.19.877-.5a1.03 1.03 0 0 0 .01-1.002L8.893 1.5zm.133 11.497H6.987v-2.003h2.039v2.003zm0-3.004H6.987V5.987h2.039v4.006z"
            ></path>
          </svg>
        </span>
        {title}
      </h5>
      <div
        style={{
          color: "black",
          marginBottom: "-1.5rem",
          "--ifm-link-color": "darkblue",
          "--ifm-link-decoration": "underline",
        }}
      >
        {children}
      </div>
    </div>
  );
}

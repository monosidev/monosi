import * as React from 'react';

const logoClickhouse = ({ height = 400, width = 400, ...props }) => (
    <svg
      xmlns="http://www.w3.org/2000/svg"
      width="1em"
      height="1em"
      viewBox="0 0 9 8"
      {...props}
    >
      <style>{".o{fill:#fc0}"}</style>
      <path
        d="M0 7h1v1H0z"
        style={{
          fill: "red",
        }}
      />
      <path
        d="M0 0h1v7H0zM2 0h1v8H2zM4 0h1v8H4zM6 0h1v8H6zM8 3.25h1v1.5H8z"
        className="o"
      />
    </svg>
);

export default logoClickhouse;

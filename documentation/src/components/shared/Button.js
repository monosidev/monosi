import React from "react";

export const Button = ({children, type, name, className}) => {
  return (
    <button
      type={type}
      name={name}
      className={`flex items-center justify-center rounded-md border border-transparent bg-[color:var(--ifm-color)] px-5 py-3 text-base font-medium  text-[color:var(--ifm-background-color)]
      hover:opacity-90 focus:outline-none focus:ring-2 focus:ring-[color:var(--ifm-color)] focus:ring-offset-2 ${className}`}
    >
      {children}
    </button>
  );
};

import React from "react";
import {Button} from "../components";

// TODO: INSERT UPDATED MAILCHIMP LINK
export const Newsletter = () => {
  return (
    <section className="my-12 max-w-7xl rounded-lg bg-[color:var(--ifm-card-background-color)] p-10 py-12 shadow-lg">
      <h2 className="text-3xl font-extrabold tracking-wide sm:text-4xl">
        <span className="block">Sign up for the Monosi newsletter</span>
      </h2>
      <p className="my-3 block">
        Sign up to receive updates about Monosi and get notified whenever we
        post new content or updates!
        <br />
      </p>
      <form
        action="https://dev.us1.list-manage.com/subscribe/post?u=e18eb60531cb2e284ca11ae4e&id=edd6302f06"
        method="get"
        id="wf-form-Newsletter-Form-1"
        name="wf-form-Newsletter-Form-1"
        className="mt-8 sm:flex"
        data-name="Newsletter Form 1"
        aria-label="Newsletter Form 1"
      >
        <label htmlFor="mce-EMAIL" className="sr-only">
          Email address
        </label>
        <input
          type="email"
          name="EMAIL"
          id="mce-EMAIL"
          required
          autoComplete="email"
          className="w-full rounded-md border-gray-300 px-5 py-3 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50 sm:max-w-xs"
          placeholder="Enter your email"
          data-name="Email"
        />
        <span className="cta_text" style={{display: "none"}}>
          You are on the waitlist!
        </span>
        <div className="mt-3 rounded-md sm:mt-0 sm:ml-3 sm:flex-shrink-0">
          <Button className="w-full" type="submit" name="waitlist">
            Subscribe
          </Button>
        </div>
      </form>
    </section>
  );
};

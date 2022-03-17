import React, {useState, useRef} from "react";
import {Button} from "../components";

export const Newsletter = () => {
  const [submissionSuccessful, setSubmissionSuccessful] = useState(false);
  const [submissionFailed, setSubmissionFailed] = useState(false);
  const [emailInput, setEmailInput] = useState("");
  const form = useRef(null);

  const submitEmail = async (e) => {
    e.preventDefault();
    setSubmissionSuccessful(false);
    setSubmissionFailed(false);

    const action = form.current.getAttribute("action");
    const method = form.current.getAttribute("method");

    const body = {
      submittedAt: Date.now(),
      fields: [
        {
          objectTypeId: "0-1",
          name: "email",
          value: emailInput,
        },
        {
          objectTypeId: "0-1",
          name: "subscribed_to_newsletter",
          value: "true",
        },
      ],
    };

    try {
      var res = await fetch(action, {
        method,
        headers: {
          Accept: "application/json",
          "Content-Type": "application/json",
        },
        body: JSON.stringify(body),
      });

      if (res.ok) setSubmissionSuccessful(true);
      else setSubmissionFailed(true);
    } catch (error) {
      console.error(error);
      setSubmissionFailed(true);
    }
  };

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
        action="https://api.hsforms.com/submissions/v3/integration/submit/21571271/c8b48f0f-0186-4dcf-8899-df23fbc170fa"
        method="POST"
        id="wf-form-Newsletter-Form-1"
        name="wf-form-Newsletter-Form-1"
        className="mt-8 sm:flex"
        data-name="Newsletter Form 1"
        aria-label="Newsletter Form 1"
        onSubmit={submitEmail}
        ref={form}
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
          value={emailInput}
          onChange={(e) => setEmailInput(e.target.value)}
        />
        <input type="hidden" name="u" value="e18eb60531cb2e284ca11ae4e" />
        <input type="hidden" name="id" value="edd6302f06" />
        <input type="hidden" name="c" value="?" />
        <div className="mt-3 rounded-md sm:mt-0 sm:ml-3 sm:flex-shrink-0">
          <Button className="w-full" type="submit" name="waitlist">
            Subscribe
          </Button>
        </div>
      </form>
      <span
        className="cta_text"
        style={submissionSuccessful ? {} : {display: "none"}}
      >
        Thank you for subscribing!
      </span>
      <span
        className="cta_text"
        style={submissionFailed ? {} : {display: "none"}}
      >
        Something went wrong, please try again.
      </span>
    </section>
  );
};

---
tags:
  - releases
posted_on_: 2022-04-01T00:00:00Z
slug: latest-release
title: "v0.1.0-alpha Release"
author: Kevin Unkrich
author_title: Co-Founder
author_image_url: https://avatars.githubusercontent.com/u/15347345?v=4
release_version: V0.1.0-alpha
---

Monosi Alpha Release

<!--truncate-->

---

Monosi's v0.1.0-alpha release brings a new UI, ease of use & deployment, and much more.

### Overhauled Web Interface

The release brings a new design to the UI with an updated information heirarchy. You can quickly get started with data monitoring by following the directions displayed on the home page of the new UI.

Furthermore, monitor details have been expanded upon to provide details about each run and anomaly analysis.

<img alt="Monosi Release" class="case-study-header" src='/img/example.gif' />

### Updated Deployment

Deploying has been simplified with Docker and Docker Compose. All the necessary dependencies for Monosi to run are managed through Docker Compose, making it easy to start with just 3 commands:

```
git clone https://github.com/monosidev/monosi.git
cd monosi
make compose
```

### Updated Documentation

As you can see by the new location of the changelog, we have enhanced our documentation from a content, UI, and information hierarchy perspective (powered by [Docusaurus](https://docusaurus.io/)). Deployed through Github Pages and versioned in the Monosi monorepo.

It should be easier to understand and get started using Monosi. If there any issues that appear in the docs, please open an [issue on Github](https://github.com/monosidev/monosi/issues).


### Testing & Bug fixes

More tests have been added to ensure the reliability of the code. Furthermore, bug fixes and code changes have been made to make Monosi increasingly more stable.
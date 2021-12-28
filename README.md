<p align="center">
  <a href="https://github.com/monosidev/monosi-oss/">
    <img width="150px" height="150px" src="https://avatars.githubusercontent.com/u/93743778?s=200&v=4"/>
  </a>
</p>
<h1 align="center">Open Source Data Observability & Monitoring Framework</h1>

Welcome to the monosi repository! Monosi is an extensible data observability platform that ensures teams achieve data reliability. It gives data teams the missing tools for ensuring data quality, similarly to what NewRelic or DataDog provide for SWE's. In turn, less time is spent fighting fires in the data. Monosi offers an alternative to proprietary data quality and observability systems to further build an open, and modular data stack.

## Features

💯 Data quality testing & monitoring

💻 CLI

📊 Field Health Monitors

❄️ Snowflake Connection

📚 Own your stack - Avoid integration pitfalls with fragmented, legacy tools by using open source & prevent vendor lock-in by decoupling metric definitions from visualization.

## Trying it out

This repository is intended to house the core monosi components for monitoring. Monosi provides a pip image via pypi that can be used on any system that supports Python 3. To use it, simply run:

```
pip install monosi
```

For instructions on getting started, check out our [documentation](https://docs.monosi.dev/introduction/getting-started).

## Why we're building it

Data reliability and data quality are massively error prone in present day pipelines. Much of the data that companies are ingesting, storing, and querying is still inaccurate, incomplete, or corrupted. 

Unreliable data and poor data quality leads to **incorrect reports** and **broken dashboards**, resulting in

- Bad business decisions
- Lost clients & deals
- A lot of time lost in debugging data problems

Data engineers are tasked to solve these issues on an ad-hoc basis on top of their already expanding responsibilities in data pipeline and reliable data management. The process for one-off fixes has become too time consuming. Software engineers have tools like New Relic, DataDog, PagerDuty, etc. to help them quickly resolve issues. Unfortunately, data engineers have limited tooling in this aspect. 

Some concrete examples that identify if your organization faces these problems:

- Several dashboards are broken or are occasionally showing false data but no one knows why. The C-Suite has noticed that the numbers are incorrect and a level of data distrust has started forming.
- Consumers of the data are complaining about data being wrong and charts need to be fixed
- Data-driven decisions are becoming a struggle
- Data and analytics teams are spending all of their time fixing data issues rather than making progress on valuable assets for customers.




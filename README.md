<p align="center">
  <a href="https://github.com/monosidev/monosi-oss/">
    <img width="150px" height="150px" src="https://avatars.githubusercontent.com/u/93743778?s=200&v=4"/>
  </a>
</p>

<h1 align="center">Open Source Data Observability Platform</h1>

<p align="center">
  <a href="https://monosi.dev/slack">Join the community</a>
  |
  <a href="https://www.monosi.dev/community.html">Newsletter</a>
  |
  <a href="https://docs.monosi.dev">Docs</a>
  |  
  <a href="https://www.monosi.dev">Website</a>
  |
  <a href="mailto:support@monosi.dev">Contact us</a>
</p>


Monosi is an extensible data observability platform that ensures teams achieve data reliability. It provides:

- Data monitoring setup in [less than 10 minutes](https://docs.monosi.dev/introduction/getting-started)

- OSS alternative to proprietary data quality and observability systems 


## Installation
*Compatible with Python 3.6+*

```
pip install monosi
```
### OR

```
docker run -d -p 3000:3000 monosi/monosi
```

For instructions on getting started, check out our [documentation](https://docs.monosi.dev/introduction/getting-started).

## Community

* [Join us on Slack](https://monosi.dev/slack)
* [Newsletter](https://www.monosi.dev/community.html)
* [Contact the development team](mailto:support@monosi.dev)

## Features

### CLI & Web Interface

Choose between using a CLI or a web interface to interact with Monosi.

![web interface](https://www.monosi.dev/images/ui_interface_v003.gif)

### Monitors as code

Define monitors on your data stores as code. Use provided table health metrics monitors or create custom table monitors. 

![monitors as code](https://www.monosi.dev/images/custom_monitor.gif)
### Profiler
Monosi automatically profiles your database to suggest and create new monitors for you to run from scratch.

![monosi profiler](https://www.monosi.dev/images/profile.gif)
### Schedule monitors

Schedule monitors to run in the background on an interval basis. 

### Alerting

Get alerts in slack when Monosi detects anomalies in defined monitors.

![monosi slack alerts](https://www.monosi.dev/images/Monosi_Slack_Alert.svg)

### Own your stack
Avoid integration pitfalls with fragmented, legacy tools by using open source & prevent vendor lock-in by decoupling metric definitions from visualization.

## Contributing

To start contributing, check out our [Contributing Guide](CONTRIBUTING.md)




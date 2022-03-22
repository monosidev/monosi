---
id: quick-install
title: Quick Install
sidebar_label: Quick Install
---


## Overview

There are three ways to quickly install and run the Monosi application:

- [Docker](#docker): Using `docker-compose` makes it easy to develop Workflows locally.
- (Coming Soon) [Helm Charts](#helm-charts): Deploying the Server to [Kubernetes](https://kubernetes.io/) is an easy way to test the system and develop Workflows.

_Note: These methods are not ready for deployment in a full production environment._

## Docker

### Prerequisites

1. [Install Docker](https://docs.docker.com/engine/install)
2. [Install docker-compose](https://docs.docker.com/compose/install)

### Run Monosi

The following steps will run a local instance of Monosi using the default configuration:

1. Clone the [monosidev/monosi](https://github.com/monosidev/monosi) repository.
2. Change directory into the root of the project.
3. Run the `make compose` command.

```bash
git clone https://github.com/monosidev/monosi.git
cd  monosi
make compose
```

After the Monosi application has started you can view the Monosi Web interface in your browser: [localhost:3000](http://localhost:3000/)

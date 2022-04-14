---
id: local-development
title: Local Development Setup
sidebar_label: Local Development
---

The directions below outline the process for setting up Monosi for local development. To get started:

1. Create a fork of the Monosi repository to your personal GitHub account
2. Clone the fork URL that you have created to your local machine (`git clone <fork-url>`)

Monosi can be installed either through docker or through a local dependency setup.
## Running with Docker

1. Ensure that you have installed docker and it is running on your machine
2. In a terminal, navigate to the cloned repository
3. Run `make compose-build` from the base of the directory to build a local instance of Monosi
4. Run `make compose-up` from the base of the directory to run the local build
5. Navigate to `http://localhost:3000` and you will see the Monosi UI

For any changes you make to the code locally, you can test them by re-running steps 3 & 4.
## Running without Docker

1. Ensure that you have Python3, Node, and Yarn on your machine
2. In a terminal, navigate to the cloned repository

For the server: 
1. Create a Python virtualenv by running `virtualenv .venv`

2. Activte the virtualenv by running `source .venv/bin/activate`
3. Install the Monosi dependencies by running `python3 setup.py install`
4. Navigate to the server directory `cd src/server`
5. Run `flask run`
6. You should see the server startup and become accessible at `http://localhost:5000`

For the client:
1. Navigate to the ui directory `cd src/ui`
2. Run `yarn && yarn start`
3. The React application should start on `localhost:3000`


If there's any problems with the setup, please send us a message in the [Slack](https://monosi.dev/slack) or over [email](mailto:support@monosi.dev). 

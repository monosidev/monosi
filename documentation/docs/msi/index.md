---
id: index
title: What is msi?
description: msi is a command-line tool that you can use to pipe, manipulate, and analyze metadata
tags:
  - operation-guide
  - msi
---

The Monosi CLI (msi) is a command-line tool that you can use to pipe, manipulate, and analyze metadata.
It allows users to define the metadata they would like to monitor as code, create a git-based project for data quality checks, and load that data into your chosen data source for any purpose - analysis, lineage, observability, and more.

- [How to install msi](/docs/msi/how-to-install-msi)
- [Your first msi project](/docs/msi/project)
- [How to use msi](/docs/msi/how-to-use-msi)

## msi commands

- [`msi init`](/docs/msi/init)
- [`msi bootstrap`](/docs/msi/bootstrap)
- [`msi test-connection`](/docs/msi/test-connection)
- [`msi run`](/docs/msi/run)


## Global modifiers

You can supply the values for many of these modifiers by setting [environment variables](/docs/msi/environment-variables) instead of including the modifiers in a msi command.

### `--project-path`

Specify the path to the project file and the monitors defined as code.

### `--workspace-path`

Specify the path to the `workspaces.yml` file.

### `--source-name`

Specify the name of the source for the workspace used.

### `--workspace-name`

Specify the name of the workspace for the file in the workspace path.

### `--help`

Display help for msi in the CLI.

### `--version`

Display the version of msi in the CLI.

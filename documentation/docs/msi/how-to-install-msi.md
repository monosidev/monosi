---
id: how-to-install-msi
title: How to install msi
sidebar_label: Install
description: You can install msi in four ways, described in this topic.
tags:
  - msi
---

You can install [msi](/docs/msi) in three ways.

- Install locally by using [Homebrew](https://brew.sh/): `brew install msi`
- Install locally by using [Python's Package Manager (pip)](https://pypi.org/): `pip install msi`
- Build it locally:
  1. Clone the [Monosi repo](https://github.com/monosidev/monosi).
  1. Run `make msi`.
  1. Copy the `msi` executable to any directory that appears in the `PATH` environment variable; for example, `/usr/bin/`.

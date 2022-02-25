---
id: custom-sql
title: Custom SQL Monitor
sidebar_label: Custom SQL
---

The Custom SQL monitor allows the user to write a custom SQL query which evaluates to one column and define custom thresholds on which to alert. It’s primary purpose is to cover long-tail use cases that the built-in metrics and monitors do not already cover.

| Name                  | Description                                                      | Identifier |
|-----------------------|------------------------------------------------------------------|------------|
| Equals                | Is equal in value                                                | eq         |
| Not Equals            | Is not equal in value                                            | ne         |
| Greater Than          | Is greater than in value                                         | gt         |
| Greater Than or Equal | Is greater than or equal in value                                | ge         |
| Less Than             | Is greater than or equal in value                                | lt         |
| Less Than or Equal    | Is less than or equal in value                                   | le         |
| Absolute Increase     | Has increased from the beginning to end by a certain percentage  | abs_inc    |
| Absolute Decrease     | Has increased from the beginning to end by a certain percentage  | abs_dec    |
| Relative Increase     | Has increased from one value to the next by a certain percentage | rel_inc    |
| Relative Decrease     | Has decreased from one value to the next by a certain percentage | rel_dec    |

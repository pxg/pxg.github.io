---
layout: post
description: Online tool for exporting Github issues
title:  "Github Issues Excel Export"
date:   2015-05-13 17:25:43
categories: Python Excel Github
---

**UPDATE: The Github issues export tool is no longer live but the code is still available on Github if you'd like to run your own service.**

This article was originally written when I was running [Lost Property](http://lostpropertyhq.com/) with [Rachid Belaid](http://rachbelaid.com) and [Rob Berry](http://robb.re/).

At Lost Property we use Github issues to manage our projects. We need to keep our clients updated on progress, our less technical clients don't have Github accounts and are familiar with Excel. So we created the [github-issues.lostpropertyhq.com](http://github-issues.lostpropertyhq.com) to export our project issues as Excel files.

When we researched Github issues export tools we could only find command line scripts, or sites like [http://www.gitbugs.com](http://www.gitbugs.com) which is great but just for public repositories.

## Open Source Online Service
[github-issues.lostpropertyhq.com](http://github-issues.lostpropertyhq.com) is an online service where anyone with a Github account can login and export their issues. The code is open source and available on [Github](https://github.com/LostProperty/Github-Issues). If you spot any bugs or would like to suggest a new feature let us know using [Github Issues](https://github.com/LostProperty/Github-Issues/issues).

## Origins
The project started out as a command line script to export issues. We knew people had the same need so created this website which requires no installation.

The project was originally part of a much more sophisticated tool called Feedback. The aim of the Feedback project was to let clients create issues and track progress without overwhelming them with too much technical information.

One of our major clients started to use JIRA so the need for the Feedback tool was negated, we could achieve what we needed by copying issues from JIRA to Github. We created a [JIRA to Github](https://github.com/LostProperty/jira_to_github) command-line tool to automate this task.

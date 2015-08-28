# Using the Github API in Python
## Intro
Pete Graham
Lost Property
@petexgraham

## Github API
 - Very good, complete API
 - Allows you to automate workflows
 - Let you build your own tools to integrate with Github

## Github Issues for Project Managment
 - Developers like Github (Pull Request, refernce issue in comments, close in comments)
 - A lot of people don't like JIRA, trac, Pivotal tracker
 - Succesful open source projects use it
 - Very simple (missing features: priorities, story sizing, burn-down)

## Client Feedback Paradox
 - Client send feedback as Powerpoints, Excel, Emails
 - We want all issues in one place
 - But clients can't right good bug reports

## Feedback Tool
 - Client issues go into Github issues
 - But with a label so you can triage them
 - Client doesn't have access to all isssues or source code
 - Open Source, written in Django, on Githu https://github.com/LostProperty/Feedback

## Python Github libraries
 - Search Github on Pypi
 - Use v3 of the API

githubpy
https://github.com/michaelliao/githubpy/
https://pypi.python.org/pypi/githubpy/1.1.0
29 stars

PyGithub
https://github.com/dustin/py-github
https://pypi.python.org/pypi/PyGithub/1.24.0
135 stars

A bunch of others.

## PyGithub

from github import Github
g = Github("user", "password")

for repo in g.get_user().get_repos():
    print repo.name

## Get Github Issues

from github import Github
g = Github("user", "password")

github_repo = github.get_repo('LostProperty/Feedback_demo')
filter_label = get_label(github_repo, 'Feedback')
issues = github_repo.get_issues(labels=[filter_label])
for issue in issues:
    print(issue.title)

## Other Github Issues tools
 - ghi command line interface for Issues
 - hub create pull requests from issues


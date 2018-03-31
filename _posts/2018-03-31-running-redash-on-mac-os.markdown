---
layout: post
title:  Getting Redash running on macOS
description: Getting a local version of Redash running on a Mac
date:   2018-03-31 11:30:00
categories: Redash Reporting Docker Mac
---

I wanted to try out the open source reporting software [Redash](https://redash.io) so got a local copy running on my MacBook. These are the instructions.

Installing Redash locally
-------------------------
Clone the Github repo:
```
git clone git@github.com:getredash/redash.git
```

The simplest way to run Redash is using Docker:
```
docker-compose -f docker-compose.production.yml run --rm server create_db
docker-compose -f docker-compose.production.yml up
```

Your local Redash instance will be running on <http://127.0.0.1:5000/> the first time you visit you'll be prompted to set-up your admin user.

Links:
 - Docker for Mac <https://www.docker.com/docker-mac>
 - Official documentation <https://redash.io/help/open-source/setup>

Setting up a Data Source
------------------------
You'll need some data to have a play about with Redash, I dumped a local Postgres databases for this:
```
pg_dump -h localhost my_db > my_dump.sql
```

Next copy the database dump to the Redash Postgres Docker container:
```
docker cp my_dump.sql redash_postgres_1:/
```

Create your new database and read in the dump:
```
docker-compose exec postgres psql -U postgres
CREATE DATABASE pete_test;
\c pete_test
\i my_dump.sql
```

Add a new datasource <http://127.0.0.1:5000/queries/new> in the Redash UI:
- Database IP is `postgres`
- Database username is `postgres`
- Full connection string `postgresql://postgres@postgres/pete_test`

![Screenshot of Redash UI](/assets/images/posts/redash_ui.png)

You can test the connection from the UI to make sure it works ok.

Creating a Report
-----------------
Now go to <http://127.0.0.1:5000/queries/new> and create a report by writing an SQL query. You can create visualisations of queries and create dashboards of multiple queries and visualisations.

First Impressions
-----------------
First impressions are good! Next steps are to get Redash set-up on an AWS server and try it out on some real data sources with real users.

I like the fact it can integrate with G Suite for login. Redash has an export feature to CSV and Excel, but doesn't currently has an export to Google Sheets feature, this is something I'd be interested to develop if I become a regular Redash user.

Redash v3, the current version, doesn't have fine levels of access control for data sources, but it appears you can work round this by adding the same database as multiple data sources and restricting access to different queries this way.
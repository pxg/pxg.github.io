---
layout: til
title: "Today I learnt about the Postgres VACUUM FULL 👨‍💻"
date: 2021-08-12
---

We currently have an issue with our EC2 server running [Redash](https://redash.io/) where it's eating the world by taking up more and more disk space.

[Carlos](https://www.linkedin.com/in/carlos-espino-timon/) spotted that the Postgres data directory is taking up majority of the space but strangely our DB didn't contain that much data 🤔.

It seems that Postgres is not always freeing up space even after it deletes data but running the `VACUUM FULL` command can free this space up.

[The Postgres docs](https://www.postgresql.org/docs/9.1/sql-vacuum.html) state `VACUUM FULL` takes a long time and exclusively locks the table, it also requires extra disk space, since it writes a new copy of the table and doesn't release the old copy until the operation is complete. So if you're trying to free up space you'll need to increase your HD size first.

![Scary vaccum clearn](/assets/images/til/vacuum.gif)
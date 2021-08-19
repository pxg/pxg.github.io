---
layout: til
title: "Today I learnt about Postgres user 🐘"
date: 2021-08-19
---

Today I learnt about the Postgres `user` function. While working on my side project Focust I saw some strange behaviour trying to to select all users from my user table:
```
select * from user;
    user
------------
 petegraham
(1 row)
```

It turns our that `user` is a keyword in Postgres which gets the current user so to select from the table I need to run `select * from "user";`. [Here's a more in-dept explanation](https://dba.stackexchange.com/questions/75551/returning-rows-in-postgresql-with-a-table-called-user).
---
layout: til
title: "Today I learnt about SQL Alchemy relationship filters ⚗️"
date: 2021-08-26
---

I was working on an SQLAlchemy project where I wanted to select all the tasks on a list which hadn't been completed, it turns out this custom relationship filter can be done with the use of `primaryjoin` parameter. The values provided are Python code rather than raw SQL.
```
tasks = relationship(
    "Task",
    order_by="Task.priority",
    primaryjoin="and_(Task.list_id==List.id, Task.completed==None)",
    back_populates="task_list",
)
``` 
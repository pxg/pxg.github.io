---
layout: til
title: "Today I learnt about HTTPie 🥧"
date: 2021-08-09
---

Today I learnt about [HTTPie](https://httpie.io/) "a user-friendly command-line HTTP client for the API era".

I installed it with `pip install httpie` it can be installed in a [multitude of different ways](https://httpie.io/docs#installation). I really like how simple it is to use, for an example to make a post call to `httpbin.org/post` with a json payload:
```
https post httpbin.org/post hello=world
```
Using `cURL` now makes me feel like a caveman!

![Mind Blown](/assets/images/til/caveman.gif)
---
layout: til
title: "Today I learnt rendering liquid code examples in Jekyll"
date: 2021-08-05
draft: true
---

In order to write my TIL on [how to order Jekyll collections]() I had to figure out how to render code examples of liquid templates, which is the templating language Jekyll uses.

This is trickier than it sounds as Jekyll see's the liquid template tags in the code example and tries to render them.

This can be avoided by using the `highlight liquid` tag followed by the `raw` tag after an example can be seen [here]() in the source code for this site.

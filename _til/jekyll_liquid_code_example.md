---
layout: til
title: "Today I learnt rendering liquid code examples in Jekyll"
date: 2021-08-05
---

In order to write my TIL on [ordering Jekyll collections](/TIL/jekyll_order_collection/) I had to figure out how to render code examples of liquid templates, which is the templating language Jekyll uses.

This is trickier than it sounds as Jekyll see's the liquid template tags in the code example and tries to render them. This can be avoided by using the `highlight liquid` tag followed by the `raw` tag after, an example can be seen [in the source code](https://raw.githubusercontent.com/pxg/pxg.github.io/main/_til/jekyll_order_collection.md) for this site.

As Jeykll uses markdown files Github will also try and render them, [see example](https://github.com/pxg/pxg.github.io/blob/main/_til/jekyll_order_collection.md), which is why I've linked to the raw file.
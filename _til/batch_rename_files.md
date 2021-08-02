---
layout: til
title: "Today I learnt how to batch rename file extensions"
date: 2021-08-04
---

I found myself needed to change all the extensions of files in a folder, in this case the files were using `.markdown` and I wanted to change them all to `.md`.

They are a number of ways to achieve this but the simplest I found was using the `rename` command line program.

This isn't pre-installed on MacOS so I need to install it with `brew install rename`. I was then able to achieve what I wanted by running the following command:

{% highlight bash %}
rename 's/.markdown$/.md/' *.markdown
{% endhighlight %}
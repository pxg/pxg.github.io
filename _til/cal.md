---
layout: til
title: "Today I learnt about the command line program cal 📅"
date: 2021-07-29
---

Cal is a great little command line program that will render a calendar of the current month in the terminal, great for checking dates very quickly.

{% highlight plain %}
$ cal

      July 2021
 Mo Tu We Th Fr Sa Su
           1  2  3  4
  5  6  7  8  9 10 11
 12 13 14 15 16 17 18
 19 20 21 22 23 24 25
 26 27 28 29 30 31
{% endhighlight %}

It come pre-installed on MacOS, however an annoyance for me is it renders Sunday as the first day of the week. To render Monday as the first day of the week I ended up installing gcal with `brew install gcal`. I added the following alias to my `~/.zshrc` file:
{% highlight plain %}
alias cal='gcal --starting-day=1'
{% endhighlight %}

You can view other months and years, the following command will show July 1983:
{% highlight plain %}
cal -m 7 1983
{% endhighlight %}

Really useful for reminding myself I was born on a Wednesday!
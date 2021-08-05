---
layout: til
title: "Today I learnt ordering Jekyll collections"
date: 2021-08-03
---

This site in built using the Jekyll static site builder, I wanted to order the [Today I Learnt](/TIL) page so the newest are first. `til` is one of my Jekyll collections, this is the code I have in `_includes/til-list.html` to sort by date in reverse order:

{% highlight liquid %}
{% raw %}
<ul id="post-list">
    {% assign sorted = site.til | sort: 'date' | reverse %}
    {% for post in sorted %}
    <li>
        <a href='{{ post.url }}'><aside class="dates">{{ post.date | date:"%b %d %Y" }}</aside></a>
        <a href='{{ post.url }}'>{{ post.title }} <h2>{{ post.description }}</h2></a>
    </li>
    {% endfor %}
</ul>
{% endraw %}
{% endhighlight %}

Whilst aspiring to be an outspoken buffoon I'm no [DHH](https://twitter.com/dhh), I only know a little Ruby and didn't invent this technique, I originally found it on [this gist](https://gist.github.com/Phlow/1f27dfafdf2bbcc5c48e).
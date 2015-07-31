---
layout: post
description: Providing the latest version of my CV from this site
title:  "Google docs PDF download from Jekyll"
date:   2015-07-31 17:25:43
categories: Google Jekyll
---

For years I'd kept my CV as HTML. When I wanted to update my CV I'd edit the HTML. Editing HTML isn't difficult, but you need to check the page in the browser after, to make sure you've not made a mistake, like missing a closing tag.

The issue I had is recruiters and big companies always wanted a PDF or Word version of my CV. I'm not entirely sure why this is, I guess they must use software to process CVs which expects PDF or Word as input.

So I'd end up opening my CV in the browser, going to print it and choosing the "print to PDF" option. A little bit tedious but not a big problem.

I find it's useful to keep a copy of my CV on-line, so it's easy to give people the link.

Somewhat ironically I'd keep the PDF not HTML version online for all these people who are obsessed with getting PDF or Word CVs (maybe it's some sort of Pokemon style collection game?). My CV update process looked like this.

1. Edit HTML
2. Check HTML page in browser for errors
3. Print to PDF
4. Deploy PDF to petegraham.co.uk

Surely there's a better way than this. Surely we can automate this.

#Google Docs PDF Download URL

I decide to move my CV to Google docs for two reasons:

1. I didn't have to manually check the document in my browser after editing.
2. It can automatically provide a PDF download link

Every Google doc with link sharing on has a URL like this `https://docs.google.com/document/d/FILE_ID/edit?usp=sharing`

Here's the one for my CV Google doc `https://docs.google.com/document/d/1eHTHX6pSbG7_FrNAVtmc_7GzR6WPU8VAYmpVzHsLmCQ/edit?usp=sharing`

Once you have the `FILE_ID` you can use can create the PDF download link like this `https://docs.google.com/document/d/FILE_ID/export?format=pdf`

This gives me the following URL for my CV PDF download [
https://docs.google.com/document/d/1eHTHX6pSbG7_FrNAVtmc_7GzR6WPU8VAYmpVzHsLmCQ/export?format=pdf](https://docs.google.com/document/d/1eHTHX6pSbG7_FrNAVtmc_7GzR6WPU8VAYmpVzHsLmCQ/export?format=pdf)

This is great. I can update my CV and easily have a link where people can get the newest version as a PDF. The problem is the link is difficult to remember unless you're Derren Brown.

#Jekyll Redirects

This site is built with Jekyll and hosted by Github pages. As Github pages is static there isn't a way to provide rewrites like you would with Nginx or Apache.

Jekyll provides a redirect mechanism, using jekyll-redirect-from. To install it
{% highlight bash %}
gem install jekyll-redirect-from
{% endhighlight %}

Next add the following to your `_config.yml` file
{% highlight bash %}
gems:
    - jekyll-redirect-from
{% endhighlight %}

I want the url [petegraham.co.uk/cv/](petegraham.co.uk/cv/) to be a link to my CV so I create a file called cv.md with the following contents:
{% highlight python %}
---
title: Pete Graham CV
permalink: cv/
redirect_to:
  - https://docs.google.com/document/d/1eHTHX6pSbG7_FrNAVtmc_7GzR6WPU8VAYmpVzHsLmCQ/export?format=pdf
---
{% endhighlight %}

My only issue with this technique is the require is done client side. However I don't think this is a huge deal. Maybe they'll be an updated version of Github pages in the future which will support simple redirect rules.

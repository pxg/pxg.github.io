---
layout: post
description: Some DNS techniques I tend to forget.
title:  "AWS and Chrome DNS tricks"
date:   2015-08-02 17:25:43
categories: Chrome DNS
---
Back in the noughties I used to like blogging, in fact I liked blogging so much I had two WordPress blogs [blog.petegraham.co.uk](http://blog.petegraham.co.uk) and [tech.petegraham.co.uk](http://tech.petegraham.co.uk).

Neither blog has been running for a while, however there are still some links to them. I wanted to redirect all traffic to either of these sub-domains to petegraham.co.uk with a permanently moved 301 header.

The DNS for petegraham.co.uk is handled by Route 53, I didn't want to have to set-up a server with Nginx just to handle redirects for a couple of sub-domains.

## AWS Domain Redirects

Currently you can't have domain redirects using just Route 53 however Adrian Holovaty has written a good article on how to set this up with a combination of Route 53 and S3's "redirect all requests" feature [http://www.holovaty.com/writing/aws-domain-redirection/](http://www.holovaty.com/writing/aws-domain-redirection/).

##Clear the DNS Cache in Chrome
Clearing the Chrome DNS cache is always useful when fiddling about with DNS settings. However I'm always forgetting how to do it. I've put this here mainly as a reminder to myself. Put the following in your browser's address bar:

`chrome://net-internals/#dns`

Then hit the "Clear host cache" button. Annoyingly if I make it into a hyper link it doesn't work. I assume for security reasons.

##Curl headers

Another thing I forget is how to just get the headers with curl.

{% highlight bash %}
curl -I blog.petegraham.co.uk
{% endhighlight %}

Running this shows going to [blog.petegraham.co.uk](http://blog.petegraham.co.uk) now gives us HTTP header `301 Moved Permanently` to [petegraham.co.uk](http://petegraham.co.uk).

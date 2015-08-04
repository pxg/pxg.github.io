---
layout: post
description: Challenges with new language version adoption
title:  "The Python 3 Problem and how Swift side steps it"
date:   2015-08-02 17:25:43
categories: Python Swift PHP
draft: true
---
A frequently discussed problem in the Python community is the slow adoption of Python 3. This problem isn't unique to Python, a similar situation happened with the switch from PHP 4 to PHP 5. The new version of the language brought many improvements but introduced backwards incompatible changes. For some the benefits introduced by upgrading didn't outweigh the effort of porting.

When PHP 5 was released many people were using shared hosting. Today, with the popularity of cloud hosting providers, being locked into an old version of a language by your hosting provider is rare. The tipping point for PHP 5 happened when majority of the big packages, WordPress, Drupal etc, provided PHP 5 versions. At this point the shared hosting providers could upgrade their servers without fear of breaking millions of WordPress blogs.

The influence of a large package switching to a new version of the language shouldn't be under estimated. [WordPress runs more than 22% of the entire web](http://fourhourworkweek.com/2015/02/09/matt-mullenweg/), a very impressive feat. PHP 4 was discontinued on 31st December 2007 and everyone in PHP land lived happily ever after. Well apart from people [ripping on the language](http://eev.ee/blog/2012/04/09/php-a-fractal-of-bad-design/) all the time.

There's been a lot of effort to encourage people to move to Python 3. One is the [Python 3 Wall of Superpowers]( https://python3wos.appspot.com/) promoting people to port the most popular packages. The majority of the most popular and widely used package have now been ported. I dug into why packages I use, such as [Supervisor](http://supervisord.org/), [Ansible](http://www.ansible.com/) and [Fabric](http://www.fabfile.org/), haven't been ported yet. I was pleased to find out the next major versions of them are in development and will support Python 3. [SciPy](http://www.scipy.org/) and [NumPy](http://www.numpy.org/), the big Python numerical and scientific packages, support Python 3 along with [scikit-learn](http://scikit-learn.org/) which is the most popular machine learning package.

If most open source packages have been upgraded to Python 3 then what's holding us back? Guido Van Rossum, the inventor of Python, talked about this at both [Pycon in Montreal](https://www.youtube.com/watch?v=G-uKNd5TSBw) and [Pycon Europe](https://lwn.net/Articles/651967/) this year. His very pragmatic reasoning is "It's a lot of hard work that could be spent on other things", such as new features or services. Surprisingly he mentioned that Dropbox, his employer, still uses Python 2.7. Presumably Dropbox has a large codebase which would be a lot of work to switch to Python 3.

In many ways Python 2 has become a victim of its own success, companies have built large mission critical systems in the language and are now reluctant to port them. If companies build systems with a compartmentalised microservice approach, then it'd be easier to migrate services one at a time. However there are [trade-offs with choosing to use micro-services](http://martinfowler.com/articles/microservice-trade-offs.html) and I don't believe it's realistic, or appropriate, for everything to be built in this way.

Apple has a clever approach at avoiding this language upgrade problem. Recently I updated my iPhone to iOS 8.4, when I went to use XCode the next day it wouldn't let me run the app I was developing on my iPhone until I upgraded to XCode 6.4. New versions of XCode often come bundled with a new version of Swift, XCode 6.4 for example came bundled with Swift 1.2. Even thought Swift 1.2 was not a major new version of the language, Swift 1.1 code did needed to be ported to run on 1.2. To clarify Swift 1.1 code wouldn't run "out of the box" in XCode 6.4 without making the effort to update the code.

One advantage Apple has over the [Python Software Foundation](https://www.python.org/psf/) is that it's running a closed ecosystem it can control. With the announcement that Swift will be open source, it will be interesting to see if this impacts, how rapidly people adopt new versions. Currently Swift 2 and XCode 7 are in beta. They will be released with iOS 9 later this year, I predict the adoption of Swift 2 will be incredibly fast, especially in comparison to Python 3.

Another advantage Swift has over Python, in terms of language upgrades, is many of the libraries used by Swift developers will be the those provided by Apple. While [Cocapods](https://cocoapods.org/) provides third party libraries for Swift and Objective-C, I wouldn't find myself using it for a typical iOS project to the same extend that I'd use [Pypi](https://pypi.python.org/) for a Python project.

In general I've been surprised and impressed with the pace of how quickly Swift has gathered momentum replacing Objective-C. One speculation I'd make is that the appeal and excitement of switching to a completely new language is greater than porting code to a newer version of an existing language.

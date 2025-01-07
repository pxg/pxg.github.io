---
layout: post
title: Kindle Faff
description: How to fix connecting a new Kindle to a Mac with USB-c
date: 2025-01-07 09:43:00
categories: Kindle
---
TLDR: new Kindles don't show up as external drives on MacOS when connected by USB-c, you need a program like OpenMTP to transfer files to them

I'm a big fan of reading on the Kindle mainly for portability reasons, I also enjoy the backlight for reading in lower-light environments.

I've been using one since 2011, and I last upgraded in 2014 when I left my first Kindle on an Airplane by mistake.

In my opinion, Kindle devices are very nicely designed and, in general, need upgrading much less frequently than a mobile phone. However, my trusty 2014 Paperwhite Kindle was getting a bit long in the tooth; whilst still having a good reading experience, it was painfully slow for browsing the Kindle store and transferring books. So I decided to treat myself to a new Kindle on Black Friday. The colour Kindle looked interesting but had mixed reviews, so I went for the new Paperwhite model.
## Kindle Design
When the new Kindle arrived, I was pleased to see they'd increased the screen size slightly to 6.8 inches and reduced the Bezel; they'd also added a warmth setting to the backlight and embraced the future by switching to a USB-C port!
## Connecting as an External Drive didn't work on MacOS
I waited until the Christmas Holidays to switch over my devices, everything was going well until I tried to transfer some books via USB cable as I'd always done previously, I got the following screen, but the Kindle wouldn't show on my Mac as an external drive.

// insert photo

Thankfully ChatGPT gave me some troubleshooting steps; upgrade Kindle, upgrade MacOS, factory reset the Kindle, switch it off and on again, blah blah blah. 

None of these worked, including installing the official Amazon MacApp Send to Kindle, so I decided to transfer the files using the [Email to Kindle Service](https://www.amazon.com/sendtokindle/email) for now.

// insert Kinde Y U No show as External Drive meme

My hunch based on ChatGPT's advice and transfer issues on my previous Kindles was that I wasn't using the official Kindle USB cable. However, I confirmed this wasn't the case.
## Amazon Customer Support == Turd (get emoji)
As the new Kindle appeared to be working perfectly, I decided to contact Amazon Customer Support to request a new cable rather than return the whole device.

Amazon, who claim to be the most customer centric company on the planet, did a terrible job. I was transferred by chat through six different departments, and the whole process took over an hour.

To Amazon's credit, I appeared to be talking to real people who were absolutely useless rather than AI. When I finally got to talk to the "Kindle Specialist", he was the most useless of them all. He told me that the Kindle-supplied cable didn't support data transfer and tried to get me to buy a new cable from Amazon. 

I had to point out that the cable he wanted me to buy was micro-USB and therefore not compatible with my new Kindle, I then suggested he send me a replacement cable for free to which he acquiesced, probably to get rid of me.
## The Failure of AI!
The new cable arrived, and still no joy. Back to my ChatGPT troubleshooting, I tried all the steps, but still no luck!

At wit's end, I decided to search on Google, like a man from the past, this led to [a result to Reddit](https://www.reddit.com/r/kindle/comments/1gb23jq/new_kindle_ereaders_no_longer_appear_on_computers/#:~:text=iFuckingHateKiwis,%E2%80%A2%202mo%20ago%20%E2%80%A2) where Reddit user "iFuckingHateKiwis" helpfully explains that newer Kindles (Scribe, 2024 release 11th gen Kindle, 12th gen Paperwhite) now use MTP (Media Transfer Protocol) instead of appearing as a USB mass storage device on your computer. Apple does not ship a native MTP driver with MacOS, which means you have to rely on a third-party program like OpenMTP.

ChatGPT had lied to me! Not only that, I'd been saved by a Reddit user with a questionably racist user handle!

// add ChatGPT screenshot here

To be fair to our AI overlords, this appears to be a source of confusion on the internet (and at Amazon Customer Support), so ChatGPT isn't the only place this is wrong.
## Files transfers and formats
With [OpenMTP](https://openmtp.ganeshrvel.com/) installed, I can now happily transfer files to my Kindle as I've always done. I use [Calibre](https://calibre-ebook.com/) for e-book management and to convert formats, mainly because it does a good job, but also for the amazing logo.

A bit of research reveals that .mobi has been superseded by the .azw3 and .kfx formats, so it's probably best to convert to one of these.

It turns out that [Email to Kindle](https://www.amazon.com/sendtokindle/email) now supports `.epub`; however, I don't think this works if you transfer by USB; Amazon are converting the book for you with Email to Kindle.

I would add that the Kindle USB File Manager App, which comes with the Send to Kindle Mac app, appears to function as well as OpenMTP, to open search "USB File Manager" in Spotlight.
## Conclusion
That was some time of my life I'll not get back! I still like books. I still like Kindles. I now believe what ChatGPT tells me less. I believe what Amazon Customer Support tell me even less! Finally, I am thankful for the help of Reddit users, even if they have questionable opinions about Kiwis.

Amazon could do a much better job explaining how to transfer books to Kindles via USB. Understandably, they are focused on people buying e-books from them in the Kindle Store and have little motivation to provide a good experience for USB transfer. However, they have chosen to continue to offer this functionality and could do a better job supporting it.

P.S. I now have a 2014 Kindle Paperwhite looking for a good home. Let me know if you either want it or know a charity I could donate it to by either emailing writing@petegraham.co.uk or contacting me on BlueSky https://bsky.app/profile/petexgraham.bsky.social
---
layout: post
title:  Anonymising email addresses for GDPR & safe development
description: Technique for anonymising emails in Postgres using SQL
date: 2018-04-23 09:23:00
categories: Postgres Development SQL
---

A lot of software has the ability to email users. When developing software it's often useful to be able to test systems end to end by actually sending emails. This has the pitfall that emails can be accidentally sent to a user, or even worst an entire user base, from a development or staging environment.

In order to avoid this embarrassment many people disable email sending in all environments except production. The compromise here is the system is only ever fully testable in production.

GDPR states that we shouldn't have Personally Identifiable Information in development environments. Anonymising email addresses not only keeps the GDPR Police happy but avoids the danger of emailing users by mistake. The following SQL anonymises user email addresses in a database table:
```
UPDATE user SET email = id || '@petegraham.co.uk';
```

It changes the table `user` from this:

ID | email
--- | ---
1 | jeff@amazon.com
2 | shingy@aol.com
3 | jony@apple.com

To this:

ID | email
--- | ---
1 | 1@petegraham.co.uk
2 | 2@petegraham.co.uk
3 | 3@petegraham.co.uk

The provided SQL is known to work with Postgres but the technique should work on other SQL databases.

Catch-all email addresses
-------------------------
A catch-all email address is a special email addresses for a domain, it "catches" any emails sent to addresses at the domain which aren't real email addresses.

Having a catch-all email address can be incredibly useful for testing systems where users need to have unique emails addresses, especially when testing registrations forms.

Without this people end up having to exhaust their Hotmail or Yahoo email addresses from the 90s to be able to test. I use [G Suite](https://gsuite.google.com) for the petegraham.co.uk email, however other email providers have catch-all functionality.

Development back-ups
--------------------
If you're backing up your database to an S3 bucket it's a good idea to using two buckets:
1. The real back-ups with limited access
2. Annoymised back-ups which the entire development team can access

It's possible to use the same technique I wrote about in [S3 Automatic Image Compression](/s3-automatic-image-compression/) to take a newly uploaded production back-up, annoymise it, then upload this to the other bucket.
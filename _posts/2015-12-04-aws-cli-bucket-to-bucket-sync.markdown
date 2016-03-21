---
layout: post
title:  AWS CLI bucket to bucket sync
description: Fast syncing from one s3 bucket to another
date:   2015-12-04 17:36:00
categories: AWS
---
I often need to sync files in one s3 bucket to another, for example if a project uses s3 for assets then you'll frequently want to copy your production assets to the stage bucket.

In the past I've either used [boto](http://docs.pythonboto.org/en/latest/) or [s3cmd](http://s3tools.org/s3cmd) to sync the source bucket files locally then sync these up to the destination bucket. This technique works but can be slow if you have a lot of files in your bucket.

Amazon now has an official [AWS CLI](https://aws.amazon.com/cli/) tool which provides bucket to bucket copies. Once you've installed the tool you'll need to find the region of your bucket, this can be done with the following command:

{% highlight bash %}
aws s3api get-bucket-location --bucket BUCKET_NAME
{% endhighlight %}

The `BUCKET_NAME` is only the name so shouldn't include `s3://`. Your region will be something like `eu-west-1`. You can now run the sync command:

{% highlight bash %}
aws s3 sync s3://SOURCE_BUCKET s3://DEST_BUCKET --region REGION.
{% endhighlight %}

If you want the files in the destination bucket to be publicly accessible you'll need to modify the command:

{% highlight bash %}
aws s3 sync s3://SOURCE_BUCKET s3://DEST_BUCKET --region eu-west-1 --acl public-read
{% endhighlight %}

It's worth nothing that later versions of s3cmd also provide bucket to bucket syncing, but it's best to use the official Amazon tool to keep Jeff Bezos happy.

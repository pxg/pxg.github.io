---
layout: post
description: Case study of getting a Django site running on Python 3
title:  "Upgrading a Django 1.8 site to Python 3"
date:   2015-08-18 12:09:00
categories: Python Django
draft: true
---
In my last article I covered the steps of upgrading a Django 1.5 site to 1.8. For my next trick I will port the site to Python 3.

But why should we use Python 3 I hear you ask. Python 2.7 is good enough.
For me they are two main reasons:

1. Python 3 is a better language. In particular it is easier for new comers to learn.
2. Continuing to use Python 2 causes technical dept. Package maintainers need to support both versions of the language, this time and effort could be better spend on new features.

For a more discussion on Python 3 check out [this from python import podcast](http://frompythonimportpodcast.com/2014/03/31/episode-017-the-one-about-python-3/) episode.

Here's an overview of my approach for upgrading the site.

1. Upgrade Django version from 1.5 to 1.8. Done.
2. Upgrade other libraries to latest Python 2.7 versions. Done.
3. Run 2 to 3 migrations tools
4. Run site on Python 3

##Can I use Python 3?

Install the caniusepython3 package then run it to check your requirements file.

{% highlight bash %}
pip install caniusepython3
caniusepython3 -r requirements.txt

...

You need 4 projects to transition to Python 3.
Of those 4 projects, 4 have no direct dependencies blocking their transition:

  django-admin-sortable
  fabric
  pywurfl
  xhtml2pdf
{% endhighlight %}

Quel désastre! Four packages aren't supported. Let's look into if we can still port.

Fabric isn't an issue as it's run on the laptop deploying not the server and I'll have Python 2 and 3 installed on my laptop. Alternatively you could try [this](https://gist.github.com/mok0/99b51e95ceeb4f3fd28b).

According to the README on the [django-admin-sortable Github](https://github.com/iambrandontaylor/django-admin-sortable) "django-admin-sortable 1.7.1 and higher are compatible with Python 3.". Strange that caniusepython3 doesn't think it is. I aint got time to bleed, let's move on.

I can see on the [pywurfl Pypi page](https://pypi.python.org/pypi/pywurfl/) "[pywurfl][1] is a [Python][3]" not sure what the use of the angular brackets is all about. Last package.

A quick google for xhtml2pdf python 3 shows [some discussion](https://github.com/chrisglass/xhtml2pdf/issues/190) on Github which says even though Python 3 isn't supported it might work.

Lessons learnt:

* Don't believe everything caniusepython3 says.
* Just man-up and install Python 3 and see what breaks.

##Installing Python 3 Virtual Environments

If you're running a Mac then the easiest way to install Python 3 is to go to [https://www.python.org/downloads/](https://www.python.org/downloads/) and download and run the installer. This will install Python 3 but leave the system Python 2.7 as the default. At the time of writing the latest stable version of Python is 3.4.3. Optional step listen to [Jean Michel Jarre](https://open.spotify.com/album/2fUrnjG4BPBH52aEAv1XyA) to add to the futuristic feeling.

Next create a virtual environment with Python 3. In the example I'm using [virtualenvwrapper](https://virtualenvwrapper.readthedocs.org/en/latest/).

{% highlight bash %}
mkvirtualenv --python=/usr/local/bin/python3 graduates-python-3
{% endhighlight %}

Now comes the scary step. Let's try and install our requirements.

{% highlight bash %}
pip install -r requirements.txt

...
blah blah pip is installing packages
...

Collecting wsgiref==0.1.2 (from -r requirements.txt (line 10))
  Downloading wsgiref-0.1.2.zip
    Complete output from command python setup.py egg_info:
    Traceback (most recent call last):
      File "<string>", line 20, in <module>
      File "/private/var/folders/ny/0wbl966d11v2j9brxg1vtqy00000gn/T/pip-build-vaxm8il7/wsgiref/setup.py", line 5, in <module>
        import ez_setup
      File "/private/var/folders/ny/0wbl966d11v2j9brxg1vtqy00000gn/T/pip-build-vaxm8il7/wsgiref/ez_setup/__init__.py", line 170
        print "Setuptools version",version,"or greater has been installed."
                                 ^
    SyntaxError: Missing parentheses in call to 'print'

    ----------------------------------------
Command "python setup.py egg_info" failed with error code 1 in /private/var/folders/ny/0wbl966d11v2j9brxg1vtqy00000gn/T/pip-build-vaxm8il7/wsgiref
{% endhighlight %}

Noooo! There's an error with [wsgiref](https://docs.python.org/2/library/wsgiref.html) and what's worst it to do with the bloody print statement needing brackets.

It's been a couple of years since I worked on this site, and to be honest I don't remember what wsgiref is used for. I search in the project and can't find a reference to it (apart from the requirements). So I remove it from the requirements, I'm sure we'll find out if we need it later, if not we're dropped a redundant requirement.

(stand alone version if I need it https://pypi.python.org/pypi/wsgiref)

##Python 3 code changes

Now is the time when they advise you to run the https://docs.python.org/2/library/2to3.html. My [maverick approach](/django-upgrade-maverick-style/) with upgrading Django worked so I opt for the "run the site and see what breaks" method instead.

{% highlight python %}
django-admin runserver

...

  File "/Users/pxg/Projects/graduates/graduates/applicant/admin.py", line 6, in <module>
    from graduates.applicant.download_as_csv import download_as_csv
  File "/Users/pxg/Projects/graduates/graduates/applicant/download_as_csv.py", line 103, in <module>
    @download_as_csv.register(basestring)
NameError: name 'basestring' is not defined
{% endhighlight %}

I can see this code is related to downloading CSV files, when I dig into this I find out that the project used to support downloading CSVs for the client. It turned out the client preferred PDFs, so this is in fact obsolete code. I delete it. I am the eradicator of technical debt.

I run the site again and hit a syntax error. It appears to be coming from the xhtml2pdf package.

From reseaching this further is appears that the xhtml2pdf code on Github supports Python 3 but the version of Pypi doesn't.

{% highlight bash %}
pip uninstall xhtml2pdf
{% endhighlight %}

I update my requirements to install from Github with this magical syntax.
{% highlight bash %}
-e git://github.com/chrisglass/xhtml2pdf.git#egg=xhtml2pdf
{% endhighlight %}

Great success! The homepage of the site has loaded. Now let's check the rest of it. When my submit one of my forms and it saves I now have a new error.

{% highlight bash %}
TypeError at /apply
Unicode-objects must be encoded before hashing
{% endhighlight %}

The culprit appears to be this line.
{% highlight python %}
instance.hash = hashlib.sha1(string).hexdigest()
{% endhighlight %}

The fix is straight forward, we just need to specify the string encoding.
{% highlight python %}
instance.hash = hashlib.sha1(string.encode('utf-8')).hexdigest()
{% endhighlight %}

I hit another error later in the multi-step form.
{% highlight python %}
name 'basestring' is not defined
{% endhighlight %}

This error can be tracked to this line in `widgets.py`
{% highlight python %}
if isinstance(value, basestring):
{% endhighlight %}

Looking on Stack Overflow the top rated answer is to change the code to this.

{% highlight python %}
from six import string_types
if isinstance(value, string_types):
{% endhighlight %}

I try submitting my form again. A new error!

{% highlight python %}
'dict_items' object has no attribute 'append'
{% endhighlight %}

Looking into the code further I realise it originates from here https://djangosnippets.org/snippets/1688/. The perils of copy and pasting code!

No-one on the internet has solved this problem so I'm going to have to roll up my sleaves and solve it myself. The fix is to change

{% highlight python %}
month_choices = MONTHS.items()
{% endhighlight %}

to

{% highlight python %}
month_choices = list(MONTHS.items())
{% endhighlight %}

The error occurred because MONTHS.items() is a list in Python 2, but a [view](https://docs.python.org/3.3/library/stdtypes.html#dict-views) in Python 3.

On the final step of the form I notice my form drop-down for University are all displaying as "University Object".

TODO: add picture

This is fixed by changing

{% highlight python %}
def __unicode__(self):
    return self.name
{% endhighlight %}

On my University model to

{% highlight python %}
def __str__(self):
    return self.name
{% endhighlight %}

The Django docs explain this best: "On Python 3, as all strings are natively considered Unicode, only use the __str__() method (the __unicode__() method is obsolete). If you’d like compatibility with Python 2, you can decorate your model class with python_2_unicode_compatible()." - [https://docs.djangoproject.com/en/1.8/ref/models/instances/](https://docs.djangoproject.com/en/1.8/ref/models/instances/)

Looking in the Django docs I also find thier [Porting to Python 3](https://docs.djangoproject.com/en/1.8/topics/python3/) which I should have probably read before I started. But who likes to read the instructions hey?

##One more thing...

I think I'm finished but then I go to test the download applicants as PDF functionality and see.

{% highlight python %}
'str' does not support the buffer interface
{% endhighlight %}

This was fixed with:

from io import StringIO
# try:
#     from cStringIO import StringIO
# except ImportError:
#     from io import BytesIO as StringIO

next error: iter.next()
not supported easy fix

next error:

In memory zip file technique from http://stackoverflow.com/questions/2463770/python-in-memory-zip-library doesn't work for Pyton3
```
string argument expected, got 'bytes'
```

#Conclusion

I've been quite rough with my upgrade approach. I'd only recommend upgrading in this way if the site is going to go through a through QA review, or if you are working on a pet project and don't mind potentially breaking it.

I've been lucky with this site that I've not had to manually port any Python 3 packages. Also a number of the hurdles I hit were caused by redundant requirements or functionality so could be removed rather than fixed.

Porting older codebasese to Python 3 can be a bit of a ball ache. However for new projects there's no reason to not use Python 3. Due to the ease of running two versions of Python, you can always start with Python 3, then drop back to Python 2.7 if you find a particular package doesn't support Python 3 yet.

The most troublesome code to fix was code I hadn't written myself, especially when this was copy and pasted code which had abstracted a problem. If simpler code you can write yourself can do the job then I recommend this over copy and pasting complex abstract solutions.

I would add have a decent search on Google, Slack overflow and Github, they are often already Python 3 fixes out there especially for popular packages.

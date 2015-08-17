---
layout: post
description: Upgrading Django sites to work with Python 3
title:  "Django and Python 3"
date:   2015-08-17 12:09:00
categories: Python Django
---
TODO: add why to upgrade to python 3. Link to other article
Approach:

TODO: overview of site and complexity. Basic functionality. Multi-step form. Email. CMS. PDF extrac

1. Upgrade Django version from 1.5 to 1.8????
2. Upgrade other libraries to latest Python 2.7 versions
3. Run 2 to 3 migrations tools
4. Run site on Python 3

## Django upgrade maverick style

The site I'm upgrading is a Django 1.5 site as it was originally made in 2013, and has only had minor edits made on it in the last two years.

Django 1.5 was the first version of Django to support Python 3. So I could try and port the code to Python 3 straight away. However Django 1.5 support finished on September 2nd 2014 so I definitely want to upgrade the Django version.

I could upgrade to 1.7 and have support until December 2015, however the newest supported version of Django at the time of writing is 1.8.3. Django 1.8 is an LTS (Long Term Support) version, this will give me support to at least April 2018.

We start with the following dependencies
{% highlight bash %}
Django==1.5.10
Fabric==1.7.0
Pillow==2.5.3
South==0.8.2
django-admin-sortable==1.5.4
ipython==1.1.0
paramiko==1.11.0
psycopg2==2.5.1
pycrypto==2.6
python-Levenshtein==0.10.2
wsgiref==0.1.2
pywurfl==6.3.1b
singledispatch==3.4.0.2
django-user-agents==0.3.0
xhtml2pdf==0.0.6
{% endhighlight %}

It's a good idea to upgrade Django versions one at a time. As I'm a maverick who doesn't play by the rules, but gets results, so I upgrade straight to 1.8.

{% highlight bash %}
$pip install Django==1.8.3
{% endhighlight %}

I need to remove `south` from `INSTALLED_APPS` to get the site to run. `south` isn't supported as [Django migrations](https://docs.djangoproject.com/en/1.8/topics/migrations/) were introduced in 1.7.

I also need to delete my `migrations` folder from my apps to get the site to run without error. This flattens my migrations, I'm fine with this as production is up to date. I go to run my dev site.



{% highlight bash %}
$python manage.py runserver

...

You have unapplied migrations; your app may not work properly until they are applied.
Run 'python manage.py migrate' to apply them.
{% endhighlight %}

Django is complaining, I try and shut it up
{% highlight bash %}
$python manage.py migrate`

...

blah blah loads of Django errors
...
 return self.cursor.execute(sql)
django.db.utils.ProgrammingError: relation "django_content_type" already exists
{% endhighlight %}

Argh! A big big ugly stack trace. I'm starting to question my cavalier approach. I try again but with the `--fake-initial` flag.

{% highlight bash %}
$python manage.py runserver --fake-initial

...

Operations to perform:
  Synchronize unmigrated apps: staticfiles, adminsortable, applicant, messages, django_user_agents
  Apply all migrations: admin, contenttypes, auth, sessions
Synchronizing apps without migrations:
  Creating tables...
    Running deferred SQL...
  Installing custom SQL...
Running migrations:
  Rendering model states... DONE
  Applying contenttypes.0001_initial... FAKED
  Applying auth.0001_initial... FAKED
  Applying admin.0001_initial... FAKED
  Applying contenttypes.0002_remove_content_type_name... OK
  Applying auth.0002_alter_permission_name_max_length... OK
  Applying auth.0003_alter_user_email_max_length... OK
  Applying auth.0004_alter_user_username_opts... OK
  Applying auth.0005_alter_user_last_login_null... OK
  Applying auth.0006_require_contenttypes_0002... OK
  Applying sessions.0001_initial... FAKED
{% endhighlight %}

Ok that seams to have worked. Still go it. Let's run the site and check.

{% highlight bash %}
ImproperlyConfigured at /
Creating a ModelForm without either the 'fields' attribute or the 'exclude' attribute is prohibited; form ApplicationAnswerForm needs updating.
{% endhighlight %}

Another stack trace, but this time in the browser for some variety. Let try and fix it by editing `forms.py`, I add `exclude = {}`.
{% highlight python %}
class ApplicationAnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        exclude = {}
{% endhighlight %}

I run the site agin, the anticipation is killing me as I refresh the browser, it works! That was easy. Not so fast some quick testing on the admin reveals another error.
{% highlight bash %}
AttributeError at /admin/applicant/faq/
'FaqAdmin' object has no attribute 'queryset'
{% endhighlight %}

The root of the error appears to be the `adminsortable` package so I upgrade this from 1.5.4.
{% highlight bash %}
pip install django-admin-sortable --upgrade
{% endhighlight %}
We're on version 1.8.4 now, and feeling much more futuristic. I test again. Success!

The next error found is on our export applicants as PDF functionality. The root of this error is the following line.
{% highlight python %}
response = HttpResponse(zipped_applicants, mimetype='application/zip')
{% endhighlight %}

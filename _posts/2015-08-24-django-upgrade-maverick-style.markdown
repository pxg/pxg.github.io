---
layout: post
description: My experience upgrading from Django 1.5 to 1.8
title:  "Django Upgrade Maverick Style"
date:   2015-08-24 12:09:00
categories: Python Django
---
I'm upgrading a website, the site was originally made in 2013, it's only had minor edits in the last two years, it's stuck on Django 1.5.

The site is for job applications and has a relatively small code base. It let's applicants sign-up with a multistep form, they get emailed when they complete the form. The site uses Django Admin for content management and the admin can export all applicant data as a PDF. It's a relatively small codebase so I decide I'm going to upgrade the site to Python 3, because I'm that kind of guy. Let the [yak shaving](http://sethgodin.typepad.com/seths_blog/2005/03/dont_shave_that.html) commence!


Django 1.5 was the first version of Django to support Python 3. I could try and port the code to Python 3 straight away. However Django 1.5 support finished on September 2nd 2014 so I definitely want to upgrade.

I could upgrade to 1.7 and have support until December 2015, but I don't want to upgrade to 1.7 because Django 1.7 is for losers. The newest supported version of Django at the time of writing is 1.8.3. Django 1.8 is an LTS (Long Term Support) version, this will give me support to at least April 2018.

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

It's a good idea to upgrade Django versions one at a time. I'm a maverick who doesn't play by the rules, but gets results, so I upgrade straight to 1.8.

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

Django is complaining, I try and shut it up!
{% highlight bash %}
$python manage.py migrate

...

blah blah loads of Django errors
...
 return self.cursor.execute(sql)
django.db.utils.ProgrammingError: relation "django_content_type" already exists
{% endhighlight %}

Argh! A big ugly stack trace. I'm starting to question my cavalier approach. But then I try again but with the `--fake-initial` flag.

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

Ok that seams to have worked. Still got it. Let's run the site and check.

{% highlight bash %}
ImproperlyConfigured at /
Creating a ModelForm without either the 'fields' attribute or the 'exclude' attribute is prohibited; form ApplicationAnswerForm needs updating.
{% endhighlight %}

Another stack trace, but this time in the browser. Let try and fix it by editing `forms.py` and adding the `exclude = {}` line.
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

A quick search revealed that passing mimetype to `HttpResponse` was removed in Django 1.7. That Django 1.7 has a lot to answer for. I change the code.
{% highlight python %}
response = HttpResponse(zipped_applicants, content_type='application/zip')
{% endhighlight %}

I can now download my applications as a zip file containing PDFs. Nice.

Next task is to test the multi-step application form is working correctly. The first thing I notice is the email fields on displaying strangely. On further inspection it turns out the HTML for the emails fields has changed from:

{% highlight html %}
<input id="id_email" maxlength="254" name="email" type="email">
{% endhighlight %}
To:
{% highlight html %}
<input id="id_email" maxlength="254" name="email" type="text">
{% endhighlight %}
A quick CSS edit later and we're looking good. I fill out the first step of the form and submit.

{% highlight html %}
IntegrityError at /apply
null value in column "require_uk_work_permit_or_visa" violates not-null constraint
DETAIL:  Failing row contains (123, mr_fake@gmail.com, , Mr, fakey, fako, null, null, null, null, 2015-08-17 15:33:17.064549+00, 2015-08-17 15:33:17.064571+00, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, f, null).
{% endhighlight %}

Argh!

The multi-step form works by saving to the DB on the first step then updating the database at each step.
I can see that the problem column is `require_uk_work_permit_or_visa`. From running a manual test on the stage server (which is still running Django 1.5) I can see this field is being set to false after the first step saves. Time to check the models.

The issue is `require_uk_work_permit_or_visa` is a non-null boolean field and it doesn't have a default. I give it a default,  explicit is better than implicit after all.

{% highlight python %}
require_uk_work_permit_or_visa = models.BooleanField(default=False)
{% endhighlight %}

All steps of our form now work. Next task is to see what other packages need updating. Pip has a handy option to do this.

{% highlight bash %}
pip list --outdated

Fabric (Current: 1.7.0 Latest: 1.10.2 [wheel])
ipython (Current: 1.1.0 Latest: 4.0.0 [wheel])
paramiko (Current: 1.11.0 Latest: 1.15.2 [wheel])
Pillow (Current: 2.5.3 Latest: 2.9.0 [wheel])
psycopg2 (Current: 2.5.1 Latest: 2.6.1 [sdist])
pycrypto (Current: 2.6 Latest: 2.6.1 [sdist])
python-Levenshtein (Current: 0.10.2 Latest: 0.12.0 [sdist])
pywurfl (Current: 6.3.1b0 Latest: 7.2.1 [sdist])
setuptools (Current: 18.0.1 Latest: 18.1 [wheel])
singledispatch (Current: 3.4.0.2 Latest: 3.4.0.3 [wheel])
South (Current: 0.8.2 Latest: 1.0.2 [sdist])
{% endhighlight %}

This prints a list of outdating requirements in a human readable format. You can then decide which you want to update, by editing the version numbers in requirement.txt. Here's what the updated file looks like.

{% highlight bash %}
Django==1.8.3
Fabric==1.10.2
Pillow==2.9.0
django-admin-sortable==1.8.4
ipython==4.0.0
paramiko==1.15.2
psycopg2==2.6.1
pycrypto==2.6.1
python-Levenshtein==0.12.0
wsgiref==0.1.2
pywurfl==7.2.1
singledispatch==3.4.0.3
django-user-agents==0.3.0
xhtml2pdf==0.0.6
{% endhighlight %}

Time to test the new site now we've upgraded packages. Yes more manual testing! I really missed my calling as a QA.

Ok so now we've upgraded Django and our other requirements. Is the fun over? Hell no it's just started, we'll be upgrading to Python 3 in the [next part](/django-and-python-3/).

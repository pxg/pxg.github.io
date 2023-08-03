---
layout: til
title: "Today I learnt why pdb can't access an exception 🐍"
date: 2023-08-03
---

I like to use `pdb` for debugging in Python, I'd noticed when using it to debug exceptions I can't always access the exception. Take the following code:
{% highlight python %}
import pdb
try:
    1/0
except Exception as err:
    pdb.set_trace()
{% endhighlight %}

If you run it and try and inspect the value of `err` you'll see `*** NameError: name 'err' is not defined`. Why is this? 🤔

The exception is only within scope in the `try` `except` block, if the call to `pdb.set_trace()` is the last line then the block has been closed when we enter the debugger.

A simple way to get round this is to add a `pass` after the `pdb` call.
{% highlight python %}
import pdb
try:
    1/0
except Exception as err:
    pdb.set_trace()
    pass
{% endhighlight %}

Thanks to Stack Overflow for teaching me this!
[https://stackoverflow.com/questions/38672560/why-cant-pdb-access-a-variable-containing-an-exception](https://stackoverflow.com/questions/38672560/why-cant-pdb-access-a-variable-containing-an-exception)
<br/>
[https://stackoverflow.com/questions/62796591/breakpoint-in-except-clause-doesnt-have-access-to-the-bound-exception](https://stackoverflow.com/questions/62796591/breakpoint-in-except-clause-doesnt-have-access-to-the-bound-exception)


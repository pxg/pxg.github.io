---
layout: til
title:  "Today I learnt about Python type hints"
date:   2021-08-02
---

Up until today I knew type hints existed in Python and had read code which used them but hadn't written any. I wanted to decide if this is a useful technique for me. Let's say I have the following function:

{% highlight python %}
def product(x, y):
    return x * y
{% endhighlight %}

I like the idea that I could automatically detect if someone calls it with parameters which aren't numbers. I wrote a few different calls to test how the function behaves.

{% highlight python %}
product(2, 4)
# Returns 8

product(2, -4)
# Returns -8

product(2.1, 4)
# Returns 8.4

product(2, True)
# Returns 2 a bit odd

product('a', 2)
# Returns aa which is unexpected

product('a', '2')
# Throws TypeError: can't multiply sequence by non-int of type 'str'

product('a', 'b')
# Throws TypeError: can't multiply sequence by non-int of type 'str'
{% endhighlight %}

Here's a type hint version of the same code:

{% highlight python %}
def product(x: int, y: int) -> int:
    return x * y
{% endhighlight %}

I was hoping the Python interpreter would throw an exception if I call:

{% highlight python %}
product('a', 2)
{% endhighlight %}

It doesn't, so whilst type hints are useful for documenting what type of parameters should be used, and the return type, on their own type hints won't help catch errors.

Mypy
----
To get the behaviour I wanted I needed to install Mypy:

{% highlight python %}
pip install MyPy
{% endhighlight %}

Then by running:

{% highlight python %}
mypy my_python_file.py
{% endhighlight %}

I got the following output:

{% highlight plain %}
types_experiments.py:7: error: Argument 1 to "product" has incompatible type "float"; expected "int"
types_experiments.py:9: error: Argument 1 to "product" has incompatible type "str"; expected "int"
Found 2 errors in 1 file (checked 1 source file)
{% endhighlight %}

Very good! However interestingly Mypy is ok with:

{% highlight python %}
product(2, True)
{% endhighlight %}

So it's happy with treating `True` as `1` which surprised me.

Python Number Type
------------------
My function calculates the product of two numbers, so I'd expect the following to be a valid call:

{% highlight python %}
product(2.1, 4)
{% endhighlight %}

However I specified the parameter types to be `int` so this isn't valid and Mypy tells me off! There's no "number type" in Python but [PEP 484](https://www.python.org/dev/peps/pep-0484/#the-numeric-tower) states if we set the type to be `float` then an argument of type `int` is acceptable. So our function now looks like:

{% highlight python %}
def product(x: float, y: float) -> float:
    return x * y
{% endhighlight %}


Conclusion
----------
On the one hand I like Python type hints as they are adding extra detail to the code conveying how it should be used. It also feels similar to typing in Swift which I'm a fan of. On the other hand the fact the Python interpreter ignores the type hints and you're required to run checks separately with MyPy makes this feel a bit more of a faff, also I found Mypy a bit slow to run so maybe this would work best as a CI step.
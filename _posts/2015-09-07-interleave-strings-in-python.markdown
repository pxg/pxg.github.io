---
layout: post
title:  Interleave two strings in Python
description: Interview question for combining two strings
date:   2015-09-07 12:09:00
categories: Python
---
One programming interview question I've seen is: "Write a function to interleave two strings. You should takes two strings as input and returns one string as output. For example if the input strings are `pete` and `paul` then the output should be `ppeatuel`".

I think it's a good question as it's a little bit tricker than it initially seams. The candidate needs to dig into the problem a further by checking what happens when the strings are of different length. Sensible behavior would be to add the extra characters to the end of the return string, if our input strings are `pete graham` and `paul` then the output should be `ppeatuel graham`.

When I first saw this question my initial solution was to find the length of the larger of the strings. Then loop from the start to the end of the largest string constructing the return string:

{% highlight python %}
def interleave_strings(string1, string2):
    max_length = max(len(string1), len(string2))
    return_string = ''
    for count in range(0, max_length):
        char1 = get_char(string1, count)
        char2 = get_char(string2, count)
        return_string += '{0}{1}'.format(char1, char2)
    return return_string
{% endhighlight %}

A function `get_char` is needed to return an empty string if the index is out of bounds:

{% highlight python %}
def get_char(string, count):
    try:
        char = string[count]
    except IndexError:
        char = ''
    return char
{% endhighlight %}

This solution is easy to follow but fairly verbose. [Rob Berry](http://robb.re/) pointed this can be done much more succinctly in Python using `zip`:

{% highlight python %}
def interleave_strings(string1, string2):
    return list(zip(string1, string1))
{% endhighlight %}

We need to cast the return value to a list in Python 3 or we'll be returning a `zip object`. Calling the function with the inputs `pete` and `paul` gives us a list of tuples:

{% highlight python %}
[('p', 'p'), ('e', 'a'), ('t', 'u'), ('e', 'l')]
{% endhighlight %}

The data structure just needs to be flattened to get our desired result. However there is a flaw in this solution, to work correctly the strings must be the same length. Using `pete graham` and `paul` as the input our output is:
{% highlight python %}
[('p', 'p'), ('e', 'a'), ('t', 'u'), ('e', 'l')]
{% endhighlight %}

Not good! Our longer string has been truncated.

This can be solved by replacing `zip` with `zip_longest` from the `itertools` module and providing a fill value of an empty string. Note: `zip_longest` was called `izip_longest` in Python 2.

{% highlight python %}
from itertools import zip_longest

def interleave_strings(string1, string2):
    return list(zip_longest(string1, string2, fillvalue=''))
{% endhighlight %}

We have to cast our return value to a list otherwise an `itertools.zip_longest object` will be returned. Using the input values `pete graham` and `paul` we now get the following result:

{% highlight python %}
[('p', 'p'), ('e', 'a'), ('t', 'u'), ('e', 'l'), (' ', ''), ('g', ''), ('r', ''), ('a', ''), ('h', ''), ('a', ''), ('m', '')]
{% endhighlight %}

Now we need to flatten the data structure. One solution is to force unpacking with `*` and then use `chain` from `itertools` to combine the iterators:

{% highlight python %}
from itertools import chain, zip_longest

def interleave_strings(string1, string2):
    return list(chain(*zip_longest(string1, string2, fillvalue='')))
{% endhighlight %}

Using our inputs `pete graham` and `paul` this gives us a list as output:

{% highlight python %}
['p', 'p', 'e', 'a', 't', 'u', 'e', 'l', ' ', '', 'g', '', 'r', '', 'a', '', 'h', '', 'a', '', 'm', '']
{% endhighlight %}

The final piece of the puzzle is to join the list items to return a string:

{% highlight python %}
from itertools import chain, zip_longest

def interleave_strings(string1, string2):
    return ''.join(chain(*zip_longest(string1, string2, fillvalue='')))
{% endhighlight %}

This returns the string `ppeatuel graham`. [Wooh!](https://www.youtube.com/watch?v=2sSofokAIiw)

The above code gives us our desired output, however it can be argued it looks cryptic. An alternative solution is to replace the use of `chain` with a longer hand solution that uses list comprehension:

{% highlight python %}
from itertools import zip_longest

def interleave_strings(string1, string2):
    tuples = zip_longest(string1, string2, fillvalue='')
    string_list = [''.join(item) for item in tuples]
    return ''.join(string_list)
{% endhighlight %}

I've covered three ways to solve the problem, they are many more which can be found on [Stack Overflow](http://stackoverflow.com/questions/3083829/how-do-i-interleave-strings-in-python). The fact the question can be answered in a number of different ways is part of what I think makes it a good one.

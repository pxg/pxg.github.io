---
layout: post
title:  Integrating Python and C code
description: Calling C code from Python using c_types
date:   2016-03-07 15:39:00
categories: Python
draft: True
---
For years I've heard people talking about interfacing Python code with C. Reasons you'd want to do this are:

1. For performance critical parts of a system
2. To use a specific C library or other existing C code

Now while a lot of developers talk about doing this, no-one appears to be doing it. Until recently I though this was myth Python developers told to each other, maybe to stop getting upset when people say Python is slow.

Late last year I've begun working on a TV streaming and scheduling software project, we need to interface the [LIVE555](http://www.live555.com/) C library with Python code. We were going to need to interface Python with C!

I was concerned getting this to work was going to be a pain, it turns out Python and C integration is surpringly seamless. This is probably becuase some of the Python internals are written in C. I hit a couple of pitfalls and found it tricky to find information on a couple of things so these are my notes.

#Hello c_types

Let's start with a very simple example. I have the following C code in a file called `get_details.c` all the code examples are on [Github]().
{% highlight c %}
#include <stdio.h>

int get_age(){
    return 32;
}

int main(int argc, char *argv[]){
    printf("Pete is %d years old \n", get_age());
    return 0;
}
{% endhighlight %}
I can compile the code with `gcc get_details.c` and run the code with `./a.out`.

I want to be able to call the C `get_age` function in Python. This is achieved by using [c_types](https://docs.python.org/3.5/library/ctypes.html) library which is built-in to the language.

{% highlight python %}
from ctypes import *

dll = cdll.LoadLibrary('./a.out')
print('Pete is {} years old'.format(dll.get_age()))
{% endhighlight %}

[Whoomp! There it is.](https://www.youtube.com/watch?v=fdKsgBNEHUU)

#Hello Pete

Let's look at a seconds example. This time I want to call the `get_name` C function:
{% highlight c %}
const char * get_name(){
    return "Pete";
}
{% endhighlight %}

As C doesn't have an inbuilt string type this function returns a char pointer instead. This means we have to do a bit more work to call the function in Python:
{% highlight python %}
from ctypes import *

dll = cdll.LoadLibrary('./a.out')
get_name = dll.get_name
get_name.restype = c_char_p
name = get_name()
name_string = name.decode('utf-8')

print('Hello {}'.format(name_string))
{% endhighlight %}

The first extra thing we've done is tell Python about the return type of the function, this lets Python map C data type, this is done with `get_name.restype = c_char_p`. A list of all the possible types are [here](https://docs.python.org/3.5/library/ctypes.html#fundamental-data-types).

The other extra step is to decode the `name` variable as it contains bytes and we want to work with a string.

#Hello bananas

Next let's look at how to call C functions which require parameters. I have the following function which calculates how much my bananas are worth:
{% highlight c %}
int calc_banana_cost(int number){
    int banana_cost = 30;
    return banana_cost * number;
}
{% endhighlight %}

None, integers, bytes objects and (unicode) strings are the only native Python objects that can directly be used as parameters in function calls. Other types of paramater need to be set with `argtypes`.

# String buffer

# Arrays

#Testing

xdist utils

#Conclusion

This is a brief introduction to

If you refer to the ctypes documentation you can see more advanced techniques such as:
 - Passing python functions to C to be used as callbacks
 - Dealing with arrays and pointers

In a follow-up article I'll be writing about how we used [PyObject](https://docs.python.org/3.5/c-api/structures.html) to simply passing data from C to Python.

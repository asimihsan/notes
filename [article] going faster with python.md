# Going Faster with Python

<a rel="license" href="http://creativecommons.org/licenses/by-sa/3.0/deed.en_US"><img alt="Creative Commons License" style="border-width:0" src="http://i.creativecommons.org/l/by-sa/3.0/88x31.png" /></a><br /><span xmlns:dct="http://purl.org/dc/terms/" href="http://purl.org/dc/dcmitype/Text" property="dct:title" rel="dct:type">Going Faster With Python</span> by <a xmlns:cc="http://creativecommons.org/ns#" href="http://www.asimihsan.com" property="cc:attributionName" rel="cc:attributionURL">Asim Ihsan</a> is licensed under a <a rel="license" href="http://creativecommons.org/licenses/by-sa/3.0/deed.en_US">Creative Commons Attribution-ShareAlike 3.0 Unported License</a>.

## Revision History

-   **2013-02-24** - first draft.

## Introduction

This article is about optimisation in Python. **Optimisation**
is seeking to minimise the usage of some resource during the 
execution of a software system. Although commonly synonymous
with minimising execution time I'll also be covering 
minimising memory occupancy.

-   In a break from many articles in this vein, part 1
will ask what role optimisation plays in the software
 development process and under what conditions optimisation
is even an appropriate action.
-   Part 2 will cover techniques for measuring both the
 execution time and memory occupancy of 
Python programmes. 
-   Part 3 details, and may serve as a reference for, a
myriad of methods for optimisation in Python. All of them are
illustrated with toy examples.
-   Parts 4 and 5 are another break from most articles in
that, rather than relegate ourselves to toy micro-benchmarks,
 I'll be covering two real-world Python applications and
their profiling and optimisation.

This article's target audience is intermediate-level Python
and beginner-level C developers; you've written non-trival code 
in Python before and can compile and run a "Hello World!"
 example in C.

Although the article's primary focus is optimising to reduce
the execution time of Python programmes it will restrict itself
to single-process optimisations; parallelising tasks both on
a multicore system using e.g. multiprocessing
[@multiprocessing] and onto many systems using e.g.
 celery [@celery] or ParallelPython [@parallelpython] is a topic worthy of its own article.

## Part 1 - When Do I Optimise?

> Programmers waste enormous amounts of time thinking about, or
 worrying about, the speed of noncritical parts of their
 programs, and these attempts at efficiency actually have a
 strong negative impact when debugging and maintenance are
 considered. **We should forget about small efficiencies**, say
 about 97% of the time: premature optimization is the root of
 all evil. **Yet we should not pass up our opportunities in that
 critical 3%**. --Donald Knuth [@Knuth74structuredprogramming]

...


It is not only a standard heuristic but a repeatedly verified
 observation that software systems tend to spend most of their
 execution time in a minority of their code.

-   Knuth, in a survey of FORTRAN programmes, discovered
that not only are maintainability and readability more
 desireable properties for programmes than performance but most
FORTRAN programmes spent the majority of their time in a small
number of code locations [@knuth1971empirical].
-   Patterson and Hennsey note that software
programmes, as a rule of thumb, spend 90% of their time in 10%
 of their code, and also exhibit **temporal locality**, where
 recently accessed memory and code tend to be accessed soon
 again, [@patterson2009computer, chapter 2].

...

## Part 2 - How Do I Know Where To Optimise?

## Part 3 - How Do I Optimise?

### Introduction

### CPython and Bytecode Analysis

```python
import this
for i in xrange(5):
    print i
```

### Cython

### numpy

### Cython with numpy

### PyPy

## Part 4 - Case Study 1 - A Log Parser

### Introduction

### Use Cases

### Initial Code

### Initial Profiling

## Part 5 - Case Study 2 - N-gram Language Models

### Introduction

### Use Cases

### Initial Code

### Initial Profiling

## References


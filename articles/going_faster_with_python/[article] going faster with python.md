# Going Faster with Python

<a rel="license" href="http://creativecommons.org/licenses/by-sa/3.0/deed.en_US"><img alt="Creative Commons License" style="border-width:0" src="http://i.creativecommons.org/l/by-sa/3.0/88x31.png" /></a><br /><span xmlns:dct="http://purl.org/dc/terms/" href="http://purl.org/dc/dcmitype/Text" property="dct:title" rel="dct:type">Going Faster With Python</span> by <a xmlns:cc="http://creativecommons.org/ns#" href="http://www.asimihsan.com" property="cc:attributionName" rel="cc:attributionURL">Asim Ihsan</a> is licensed under a <a rel="license" href="http://creativecommons.org/licenses/by-sa/3.0/deed.en_US">Creative Commons Attribution-ShareAlike 3.0 Unported License</a>.

<iframe src="http://tools.flattr.net/widgets/thing.html?thing=1150097" width="292" height="420"></iframe>

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

> "Programmers waste enormous amounts of time thinking about, or
 worrying about, the speed of noncritical parts of their
 programs, and these attempts at efficiency actually have a
 strong negative impact when debugging and maintenance are
 considered. **We should forget about small efficiencies**, say
 about 97% of the time: premature optimization is the root of
 all evil. **Yet we should not pass up our opportunities in that
 critical 3%**." --Donald Knuth [@Knuth74structuredprogramming]

If we know software needs to be fast then why can't we code
 with this perspective front-and-centre at all times?

There are many problems with statement, the first being: how
 fast? The best way to achieve performance requirements is to
 associate it with precise, quantifiable, and measureable
 metrics [@williams2002five, page 2]. In this case examples would be:

-   "the time to first byte (TTFB) for the software service will be 200ms for 95% of all requests", or
-   "CPU usage will never exceed 65%"

In some environments, such as hard real-time operating system
components or mission-critical command-and-control servers,
these are reasonable requirements. In others, such as a 
personal blog, they would be patently ridiculous. Context
matters.

Another problem with the "omnipresent" approach is that there
is no free lunch. There are many characteristics of a good
 software implementation, of which performance is only one [@tsui2010essentials, chapter 9 'Implementation'], [@fowler1999refactoring, chapter 2 'Principles in Refactoring']. In no particular order some are:

-   **Readability**: can be easily read and understood.
-   **Maintainability**: can be easily modified, extended, and
maintained.
-   **Performance**: minimises any one, or all of, execution
time, memory usage, and power consumption.
-   **Correctness**: does what it is specified to do.
-   **Completeness**: all the requirements are met.

As you prioritise some of the above properties you must 
sacrifice attention to others. An absolute focus on 
performance must necessarily come at the cost of, for
 example, readability and maintainability.

Even if your software system places a premium on performance it
is a fallacy to suggest that this may only be addressed at the
code tuning level. You have many options, at many stages
 [@mcconnell2009code, chapter 25 'Code-Tuning Strategies']:

-   **Program requirements**:
    -   Do your users actually require this level of
 performance? What do they need?
    -   Users typically don't directly care about latency
and throughput and instead care about time elapsed to execute
use cases. Have you considered your user interface, user
experience, and information architecture?
-   **Program design**
    -   Set resource objectives for individual sub-components
and interfaces, and track them proactively.
    -   Set goals that may achieve performance objectives
indirectly in the future. If you aim for highly modular and
modifiable code then, as your system enters end-to-end use, 
you can easily swap out slow components for better
implementations.
-   **Class and routine design**
    -   Choose appropriate algorithms and data structures
[@sedgewick2011algorithms] at the beginning.
-   **Hardware**
    -   Is buying more or faster hardware more cost-effective
than the employee time required to tune the code?

There is a third, and perhaps the most counter-intuitive,
 problem with constant optimization throughout coding. It is 
not only a standard heuristic but a repeatedly verified 
observation that software systems tend to spend **most of 
their execution time in a minority of their code**.

-   Knuth, in a survey of FORTRAN programmes, discovered
that not only are maintainability and readability more
 desireable properties for programmes than performance but most
FORTRAN programmes spent the majority of their time in a small
number of code locations [@knuth1971empirical].
-   Patterson and Hennsey note that software
programmes, as a rule of thumb, spend 90% of their time in 10%
 of their code, and also exhibit **temporal locality**, where
 recently accessed memory and code tend to be accessed soon
 again, [@patterson2009computer, chapter 1 'Fundamentals of 
Computer Design'].

Given that programs spend the majority of their time in a
minority of their code, constantly optimizing everything, in
the best case, is mostly wasted! This "execution locality",
and how it impacts optimisation, is expressed in **Amdahl's
Law** [@patterson2009computer, chapter 1 'Fundamentals of 
Computer Design'], which describes how the total speedup of a
 software system after speeding up a constituent subcomponent
depends on what fraction of the total time the subcomponent
takes up:

$$
\begin{align}
    &\begin{aligned}
        \textrm{Execution time}_{\textrm{old}} & = \textrm{Execution time}_{\textrm{new}} \times \left( \left( 1 - \textrm{Fraction}_{\textrm{enhanced}} \right) + \frac{ \textrm{Fraction}_{\textrm{enhanced}}}{\textrm{Speedup}_{\textrm{enhanced}}} \right) \\
        \textrm{Speedup}_{\textrm{overall}} & = \frac{\textrm{Execution time}_{\textrm{old}}}{\textrm{Execution time}_{\textrm{new}}} \\
        & = \frac{1}{ \left( 1 - \textrm{Fraction}_{\textrm{enhanced}} \right) + \frac{ \textrm{Fraction}_{\textrm{enhanced}}}{\textrm{Speedup}_{\textrm{enhanced}}}}
    \end{aligned}
\end{align}
$$

Here's an example. Suppose we have a web server and there is a
 routine we could optimise such that it becomes 10 times faster.
 Assuming that the web server process is busy with with this
 routine 40% of the time what is the overall speedup after the
 optimisation?

$$
\begin{align}
    &\begin{aligned}
        \textrm{Fraction}_{\textrm{enhanced}} & = 0.4 \\
        \textrm{Speedup}_{\textrm{enhanced}} & = 10 \\
        \textrm{Speedup}_{\textrm{overall}} & = \frac{1}{(1-0.4) + \frac{0.4}{10}} \\
        & = \frac{1}{0.64} \\
        & = \textrm{1.56 (3dp)}
    \end{aligned}
\end{align}
$$ 

Indeed, by Amdahl's Law, the maximum possible speedup of the
software system is $\frac{1}{0.6} = \textrm{1.67 (3dp)}$.

In short: software optimisation is often best achieved during
the requirements analysis and component design stages, but
the time will come when you can't shy away from a performance
problem. At this point the next step is determining what is
slow, and not just jumping into coding; this is part 2.

In parting I'll leave you with this:

> "If there's a moral to this story, it is this: do not let
 performance considerations stop you from doing what is right.
 You can always make the code faster with a little cleverness.
 You can rarely recover so easily from a bad design...**Design
 the program you want in the way it should be designed. Then,
 and only then, should you worry about performance**. More often
 than not, you'll discover the program is fast enough on your
 first pass." --Elliotte Rusty Harold [@oram2007beautiful, chapter 5 'Correct, Beautiful, Fast']

## Part 2 - How Do I Know Where To Optimise?

If Part 1 is "how fast?", part 2, in an extraordinary leap of 
atrocious grammar, is "where slow?". Your software architecture
is modular with well-defined interfaces, you've defined precise,
quantifiable, and measureable performance metrics, and lo and 
behold you're not meeting them after implementing a significant
portion of tested functionality. Now what?

### Basic timing

Particularly if you're looking at system command-line utilities
or scientific computing simply knowing "how much time did this
take to finish?" or "how much RAM did it use at its peak?" is
a good first step.

Typical approaches to doing this use `top` and `time`, and
are very simple effective. Often however people forget that
measurements must be repeated in order to gain confidence as
to their accuracy. Hence to help you get started I've created a
noddy little script for this article, `src/utilities/measureproc.py`
[@going_faster_with_python:measureproc.py].

Let's assume we using this little toy script:

~~~~ {.python .numberLines}
#!/usr/bin/env python

import time

if __name__ == "__main__":
    a = range(2 ** 24)
    print a[-1]
    time.sleep(1)
~~~~

In order to make repeated measurements as to its CPU and memory
usage:

```bash
(going_faster_with_python)Mill:going_faster_with_python ai$ pwd
/Users/ai/Programming/going_faster_with_python

(going_faster_with_python)Mill:going_faster_with_python ai$ python src/utilities/measureproc.py
python src/utilities/longscript.py
Summary of 5 runs
metric  | min    | Q1     | median | Q2     | max   
--------+--------+--------+--------+--------+-------
clock   | 1.96   | 1.97   | 1.98   | 1.97   | 2.08  
user    | 0.68   | 0.68   | 0.68   | 0.68   | 0.76  
system  | 0.22   | 0.22   | 0.22   | 0.22   | 0.25  
rss_max | 525.39 | 525.39 | 525.39 | 525.39 | 525.39
```

The script outputs four important metrics:

-   **clock** (s): how much time elapsed between the start and
end of the program. You'll note that the median clock time
is approximately two seconds.
-   **user** (s): how much time spent by the CPU in the **user
space**, i.e. in your script's code.
-   **system** (s): how much time spent by the CPU in the
**kernel space**, i.e. executing code within the lower levels
of the operating system.
-   **rss_max** (MB): the peak amount of memory allocated for
the program's **Resident Set Size** (RSS), i.e. the memory
allocated within physical memory, as opposed to the **Virtual
Memory Size** (VMS).

The script summarises the measurements of these metrics over
N runs using:

-   **min**: the minimum value.
-   **Q1**: the 25% percentile, i.e. 25% of values are equal
or less than this value.
-   **median**: the 50% percentile.
-   **Q2**: the 75% percentile.
-   **max**: the maximum value.

We note the following observations:

-   $(Q2 - Q1)$ for all metrics is very small. The measurements
are consistent over time and the results are readily
reproducible.
-   The median clock time is 2 seconds. The user's perception
of the programme is that it took two seconds to execute.
-   The sum of the user and system times is approximately 0.9
seconds. This means that $2 - 0.9 = 1.1$ seconds was spent
waiting for I/O operations. This script spent half its time
using the CPU and half its time waiting.
-   The sum of the above two observations is that perhaps
one second was spent allocating memory for the array and
one second was spent sleeping.
-   The RSS max is approximately 525MB. This is rather large!

### Logging

The humblest yet most important of approaches, **logging** is an
old friend to most of us. In fact some of you may be thinking
"Why am I even bothering with this article? Everyone knows
that configurable tracing is critical in any production system.".
 Although logging isn't the focus of this article I wanted to
cover some quick points regarding it.

-   Use **discipline** when applying logging calls to you code.
As a rule of thumb:
    -   All *function entries and exits* should be traced by a log
of the lowest severity type. Function entries also within reason
trace their *arguments*.
    -   All *branches*, for example following an if statement,
an else statement, a try statement, a finally statement, etc.,
should be traced by a log of at least the lowest severity type.
    -   All *exceptions* are logged either with e.g.
`logging.exception` [@pydocs:logging:exception] to log the stack of 
the failure, or using a package like `sentry` [@sentry].
    -   All potentially *long-running tasks* are wrapped in
logging statements immediately preceding and following them. This
 is especially true for tasks involving external interfaces or
tasks with tightly defined performance requirements (you have
 those, right?).
-   Logs are far more valuable when they're **collected**, 
**parsed**, and **analysed**. 
    -   With end-to-end solutions like `logstash` [@logstash]
becoming more common there's little excuse leaving your poor logs
sitting alone in the corner.

With such discipline, in time forming habit, you can react quite
effectively to a wide variety of inquiries, such as:

-   "Well, most of the time this page is fine, but when a new
user searches for "foo bar's excellent bizz" from their empty
profile page everything grinds to a halt!"
-   "When I search for '2013/01/43 19:00' as a start datetime
the server reaches 100% CPU usage, runs out of memory, then
kernel panics." (This happened to me in a legacy system I
inherited, true story).

For Django fans `django-debug-toolbar` [@django-debug-toolbar] 
helps tie together the behaviour of Django components throughout
the request cycle, including SQL queries and time taken to
execute them.

#### PyCounter

TODO

Decorator that records frequency and time spent for individual
functions.

To install: `pip install pycounters`.

To use:

-   `from pycounters.shortcuts import frequency, time`
-   Set up a log reporter:

~~~~ {.python .numberLines}
import pycounters
import logging

reporter=pycounters.reporters.LogReporter(logging.getLogger("counters"))
pycounters.register_reporter(reporter)
pycounters.start_auto_reporting(seconds=300)
~~~~

-   Decorate functions with `@frequency()` and `@time()`.

For more information see [@pycounter].

### CPU profiling

Detailed logging, and coming up with efficient and useful
toolchains for analysing them, can be a chore sometimes.
Fortunately, particularly if you're dealing with smaller 
command-line-based tools or scientific computing, **CPU
profiling** is another option.

In CPU profiling you gather information about function call
chains (who calls whom) and how long functions take to return.
There are two types of CPU profiling methods:

1.  **Deterministic profiling**. Your measurements are 
comprehensive, in that you record every single function call at
the greatest possible precision. If the effort of such measurement
*does not impede the actual functionality* of the softare system
 this method is fine, but this is a big assumption.
2.  **Statistical profiling**. Your measurements are sporadic but
 regular, with a configurable interval. By being sporadic the
 hope is that you have less, and hopefully negligible, impact on
 the actual functionality of the software system, at the cost of
 less precise measurements.

Let's run through a variety of CPU profilers with a toy example.

#### Our toy example

Let's assume there is a BZIP2 compressed log file that we want
to parse, and that each line is a measurement of a metric in the
format `epoch, metric name, metric value`, e.g.:

```
1362330056,cpu_usage,112
1362330057,cpu_usage,21
...
```

Our objective is to determine the arithmetic mean of the `cpu_usage`
values throughout the whole file.

I've created a script `src/utilities/generate_log.py`
[@going_faster_with_python:generate_log.py] that will generate
a log in this format into the path `src/utilities/example.log.bz2`.
Please run this script before continuing.

In order to parse this script we're using
`src/cpu_profiling/parse_log.py`
[@going_faster_with_python:parse_log.py]. It has shown poor
performance and we want to see what parts are slow (I've deliberately
made this script very non-idiomatic and obtuse in places. This is
*not* an example of good code! Unsurprising considering the context):

~~~~ {.python .numberLines}
#!/usr/bin/env python

from __future__ import division

import os
import sys
import bz2
import contextlib
import re

# -------------------------------------------------------------------
#   Constants.
# -------------------------------------------------------------------
current_dir = os.path.abspath(os.path.join(__file__, os.pardir))
parent_dir = os.path.join(current_dir, os.pardir)
log_filepath = os.path.join(parent_dir, "utilities", "example.log.bz2")

re_log_line = re.compile("(.*?),(.*?),(.*)\n")
# -------------------------------------------------------------------

def main():
    cpu_usages = []
    with contextlib.closing(bz2.BZ2File(log_filepath)) as f_in:
        for line in f_in:
            process_line(line, cpu_usages)
    summarise(cpu_usages)

def summarise(cpu_usages):
    print "avg: %s" % (sum(cpu_usages) / len(cpu_usages), )

def process_line(line, cpu_usages):
    re_obj = re_log_line.search(line)
    try:
        elems = re_obj.groups()
    except:
        pass
    else:
        if elems[1] == "cpu_usage":
            cpu_usages.append(int(elems[2]))

if __name__ == "__main__":
    main()
~~~~

Looking at this script there are many possible reasons for
performance problems:

-   Looping over a compressed file must be slow! Surely we can
afford larger hard drives, keep logs decompressed, and the script
will become much faster?
-   The regular expression looks quite inefficient! It needs tuning.
-   Process calls in Python have a very large overhead. We should
be avoiding function calls within inner loops.
-   What is going on with the regular expression matching?! Exception
handling?!
-   Maybe computing the average would be faster if we maintained a
running sum rather than storing all the values in a giant array.
We'd save memory too!

These are all valid points. However, put aside the toy script for a
moment and consider the bigger picture. You may instead be faced with
a convulted, complex, and poorly documented system, where such
points are not obvious. Hence, instead of jumping in and "optimising"
the code, your response to anyone who suggests such "optimisations",
in simple or complex scenarios, is always:

> "Before we waste time on **opinions** I'd like to proceed on the
basis of **empirical measurements**.

#### cProfile

`cProfile` [@pymotw:cprofile] is a deterministic profiler that's
part of the Python standard library. It's easy to use, efficient
enough that it has neglible impact on many programmes, and with
a little trickery can be used with a decorator to profile 
individual functions.

To use it on our toy example:

```
python -m cProfile -o profile.stats parse_log.py
```

This will output a file `profile.stats` to the current working
directory. It contains low-level details that may be parsed out
and summarised. One command I like using sorts the statistics by
total time spent in particular functions, as follows:

```
(going_faster_with_python)Mill:src ai$ python -c "import pstats; p = pstats.Stats('profile.stats');
p.sort_stats('time').print_stats(5)"
Sun Mar  3 17:49:04 2013    profile.stats

         20000398 function calls (20000376 primitive calls) in 31.770 seconds

   Ordered by: internal time
   List reduced from 67 to 5 due to restriction <5>

   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
  5000000   12.930    0.000   23.044    0.000 cpu_profiling/parse_log.py:31(process_line)
        1    8.666    8.666   31.756   31.756 cpu_profiling/parse_log.py:21(main)
  5000000    7.917    0.000    7.917    0.000 {method 'search' of '_sre.SRE_Pattern' objects}
  5000000    1.621    0.000    1.621    0.000 {method 'groups' of '_sre.SRE_Match' objects}
  5000065    0.575    0.000    0.575    0.000 {method 'append' of 'list' objects}
```

Interpreting the results:

-   The script took approximately 31.8 seconds to execute.
-   The **tottime** column specifies the total time spent in a
function and *excludes* time spent in calls to sub functions.
-   The **cumtime** column specifies the total time spent in a
function and *includes* time spent in calls to sub functions.
-   12.9 seconds, or 40.7% of the total time, was spent in 
`process_line()`, and this *excludes* time spent in calls to the
regular expression module. It was called five million times.
-   8.67 seconds, or 27.2% of the total time, was spent in
`process_log()`, and this *excludes* time spent in the five
millions calls to `process_line()`.
-   7.92 seconds, or 25% of the total time, was spent calling
`re.search()`, i.e. using our regular expression.
-   The top three functions account for $\frac{12.9 + 8.67 + 7.92}{31.8} \times 100 = 92.7\textrm{%}$ of the total execution time.

What can we conclude from the results? These conclusions are
**ordered** from most to least important:

-   There is something terribly wrong with `process_line()` that is
**independent** of the regular expression used and the list append
operation.
    -   Looking at the function this suggests that the
non-idiomatic usage of exception handling is causing us pain.
(Why? Stay tuned for the "CPython and Bytecode Analysis" section
to learn more).
    -   Instead of doing a string comparison on the results of the
regular expression why couldn't we get the regular expression
to do this comparison for us, by putting `cpu_usage` into the
regular expression itself?
-   There is something about the `main()` function, **independent**
of calls to sub functions, that is slow. Looking at the function
this must largely be the decompression of the bzip2-compressed log
 file. Your options depend on your requirements. Could you get away
 with gzip compression instead, which consumes less CPU resources at
the cost of a lower compression ratio? Could you get away with no
 compression?
-   What's wrong with our regular expression? It seems a bit slow!
Could we re-write it to make it faster? (Hint: yes).
-   `summarise()` isn't even in the top five. Although this is not
the most efficient manner in which to calculate an arithmetic mean
it is most certainly **completely irrelevant at this stage of our
investigation**.

You can also use the cProfiler output to trace which functions are
calling whom. Rather than cover that in detail here I'm going to
cover the same functionality in a better user interface in the 
"callgrind" section below. However, here is how you'd get such
information from the command-line for who is *calling* the hot
functions:

```
(going_faster_with_python)Mill:src ai$ python -c "import pstats;
p = pstats.Stats('profile.stats');
p.sort_stats('cumulative').print_callers(5)"

   Ordered by: cumulative time
   List reduced from 67 to 5 due to restriction <5>

Function                                         was called by...
                                                     ncalls  tottime  cumtime
cpu_profiling/parse_log.py:3(<module>)           <-
cpu_profiling/parse_log.py:21(main)              <-       1    7.869   27.992  cpu_profiling/parse_log.py:3(<module>)
cpu_profiling/parse_log.py:31(process_line)      <- 5000000   11.267   20.078  cpu_profiling/parse_log.py:21(main)
{method 'search' of '_sre.SRE_Pattern' objects}  <- 5000000    6.946    6.946  cpu_profiling/parse_log.py:31(process_line)
{method 'groups' of '_sre.SRE_Match' objects}    <- 5000000    1.360    1.360  cpu_profiling/parse_log.py:31(process_line)
```

and for who *the hot functions are calling*:

```
(going_faster_with_python)Mill:src ai$ python -c "import pstats;
p = pstats.Stats('profile.stats');
p.sort_stats('cumulative').print_callees(5)"

   Ordered by: cumulative time
   List reduced from 67 to 5 due to restriction <5>

Function                                         called...
                                                     ncalls  tottime  cumtime
cpu_profiling/parse_log.py:3(<module>)           ->       3    0.000    0.000  /Users/ai/Programming/.envs/going_faster_with_python/lib/python2.7/posixpath.py:60(join)
                                                          1    0.000    0.000  /Users/ai/Programming/.envs/going_faster_with_python/lib/python2.7/posixpath.py:341(abspath)
                                                          1    0.000    0.000  /Users/ai/Programming/.envs/going_faster_with_python/lib/python2.7/re.py:188(compile)
                                                          1    0.000    0.000  /usr/local/Cellar/python/2.7.3/lib/python2.7/__future__.py:48(<module>)
                                                          1    0.000    0.000  /usr/local/Cellar/python/2.7.3/lib/python2.7/contextlib.py:1(<module>)
                                                          1    7.869   27.992  cpu_profiling/parse_log.py:21(main)
cpu_profiling/parse_log.py:21(main)              ->       1    0.000    0.000  /usr/local/Cellar/python/2.7.3/lib/python2.7/contextlib.py:149(__init__)
                                                          1    0.000    0.000  /usr/local/Cellar/python/2.7.3/lib/python2.7/contextlib.py:151(__enter__)
                                                          1    0.000    0.001  /usr/local/Cellar/python/2.7.3/lib/python2.7/contextlib.py:153(__exit__)
                                                          1    0.000    0.045  cpu_profiling/parse_log.py:28(summarise)
                                                    5000000   11.267   20.078  cpu_profiling/parse_log.py:31(process_line)
cpu_profiling/parse_log.py:31(process_line)      -> 5000000    0.505    0.505  {method 'append' of 'list' objects}
                                                    5000000    1.360    1.360  {method 'groups' of '_sre.SRE_Match' objects}
                                                    5000000    6.946    6.946  {method 'search' of '_sre.SRE_Pattern' objects}
{method 'search' of '_sre.SRE_Pattern' objects}  ->
{method 'groups' of '_sre.SRE_Match' objects}    ->
```

A final trick with `cProfile` is that you can craft a decorator to
only trigger it for particular functions. This is useful when the
overhead of `cProfile` over *all* the code is too high, but you
need a profile of a function and called subfunctions [@stackoverflow:cprofile_decorator]:

~~~~ {.python .numberLines}
import cProfile

def profileit(name):
    def inner(func):
        def wrapper(*args, **kwargs):
            prof = cProfile.Profile()
            retval = prof.runcall(func, *args, **kwargs)
            # Note use of name from outer scope
            prof.dump_stats(name)
            return retval
        return wrapper
    return inner

@profileit("profile_for_func1_001")
def func1(...)
    ...
~~~~

#### line_profiler

`cProfiler` is rather coarse because it only traces function calls,
and so is only precise at the function call level. Using a module
called `line_profiler` we can measure CPU occupancy at the line-level.

After a `pip install line_profiler` you just need to decorate the
functions you're interested in with `@profile`. Note that this will
render the script unexecutable because we do not use any imported
modules to profile our script. I've already done the decorating in
 `src/cpu_profiling/parse_log_line_profiler.py`. Afterward
execute `kernprof.py`:

```
(going_faster_with_python)Mill:src ai$ kernprof.py -l -v cpu_profiling/parse_log_line_profiler.py

avg: 49.9978002
Wrote profile results to parse_log_line_profiler.py.lprof
Timer unit: 1e-06 s

File: cpu_profiling/parse_log_line_profiler.py
Function: main at line 21
Total time: 105.217 s

Line #      Hits         Time  Per Hit   % Time  Line Contents
==============================================================
    21                                           @profile
    22                                           def main():
    23         1            2      2.0      0.0      cpu_usages = []
    24         1           34     34.0      0.0      with contextlib.closing(bz2.BZ2File(log_filepath)) as f_in:
    25   5000001     11602598      2.3     11.0          for line in f_in:
    26   5000000     93565103     18.7     88.9              process_line(line, cpu_usages)
    27         1        49088  49088.0      0.0      summarise(cpu_usages)

File: cpu_profiling/parse_log_line_profiler.py
Function: process_line at line 32
Total time: 44.2081 s

Line #      Hits         Time  Per Hit   % Time  Line Contents
==============================================================
    32                                           @profile
    33                                           def process_line(line, cpu_usages):
    34   5000000     14758591      3.0     33.4      re_obj = re_log_line.search(line)
    35   5000000      4406648      0.9     10.0      try:
    36   5000000      6765236      1.4     15.3          elems = re_obj.groups()
    37                                               except:
    38                                                   pass
    39                                               else:
    40   5000000      5814440      1.2     13.2          if elems[1] == "cpu_usage":
    41   5000000     12463137      2.5     28.2              cpu_usages.append(int(elems[2]))
```

The output is quite intuitive and you'll note it confirms many of
our intuitions from the "cProfiler" section. We already knew that 
`process_line()` was quite slow. However, `line_profiler` indicates 
that appending to a list in order to track CPU usage takes up 30% of 
the execution time of the function. Is it, however, the `append` 
itself, the `int`, or the array access that takes up this time? You'd 
need to do a bit of **refactoring** and spread the code over several 
lines to aid `line_profiler`.

However, the "total time" values seem a bit off. Why did `cProfiler`
run the script in 30-odd seconds and this one is spending eons just
in the individual functions? Recall that both `cProfiler` and
`line_profiler` are instances of **deterministic profilers**; in fact
the actual execution of our script is faster without such profiling
(although cProfiler doesn't add *that* much overhead):

```
(going_faster_with_python)Mill:src ai$ python utilities/measureproc.py python cpu_profiling/parse_log.py

Summary of 5 runs
metric  | min   | Q1    | median | Q2    | max  
--------+-------+-------+--------+-------+------
clock   | 24.15 | 24.23 | 24.67  | 26.02 | 31.76
user    | 24.00 | 24.12 | 24.48  | 25.86 | 30.46
system  | 0.07  | 0.09  | 0.09   | 0.11  | 0.15 
rss_max | 46.02 | 46.04 | 46.04  | 46.04 | 46.05
```

#### callgrind

TODO

This is far superior to RunSnakeRun, and to boot is actually
usable.

Installation on Mac OS X:

-   You'll need XCode Developer Tools.
-   `brew install qt graphview`
-   Download the KCachegrind source [@callgrind:source].
-   `cd kcachegrind/qcachegrind`
-   `qmake; make`
-   You'll have a `qcachegrind.app`, move it to Applications.
-   callgrind wants the Graphviz executable `dot` to be
accessible without a `~/.bash_profile`, so you need to
`sudo ln -s /usr/local/bin/dot /usr/bin/dot`
-   `pip install pyprof2calltree`

To use this:

-   Generate a regular `cProfile` profile file (see earlier).
-   `pyprof2calltree -i cprofile.out -o callgrind.output`
-   Open `callgrind.output` in QCachegrind.
-   Pretty pictures!

For more information see [@callgrind], [@callgrind:install].

#### profilestats

TODO

Decorator for profiling individual functions then converting
the profiling data to kcachegrind format. Of course you
could just use the `cProfile` decorator trick explained above
and then call `pyprof2calltree`, but to each their own.

To install this: `pip install profilestats`.

Usage:

-   `from profilestats import profile`
-   `@profile` on function.

For more information see [@profilestats].

#### statprof

TODO

Statistical profiler. Intended to have lighter impact than 
`cProfiler`. It regularly gathers the stack on a timer, rather
than deterministically tracing all calls.

To install: `pip install statprof`.

To use:

~~~~ {.python .numberLines}
import statprof

statprof.start()
    try:
        my_questionable_function()
    finally:
        statprof.stop()
        statprof.display()
~~~~

For more information see [@statprof].

#### plop

TODO

Statistical profiler, low CPU overhead.

To install: `pip install plop tornado`

To use:

-   `python -m plop.collectory myscript.py`
-   Writes output to `/tmp/plop.out`
-   `python -m python.viewer --datadir=/tmp`
-   This launches a Tornado web server.
-   Browse to [http://localhost:8888](http://localhost:8888)
-   Pretty pictures!
    -   D3 force-layout directed call graph.
    -   Radius of node is percentage of total time it takes.

For more information see [@plop], [@plop:blog]

### Memory profiling

TODO

#### pympler

TODO

#### maliae

TODO

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


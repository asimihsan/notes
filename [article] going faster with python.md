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
`logging.exception` [@pydocs:logging:exception] to log the stack of the failure, or using a package like `sentry` [@sentry].
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

Let's run through a variety of CPU profilers with toy examples.

#### cProfile

`cProfile` [@pymotw:cprofile] is a deterministic profiler that's
part of the Python standard library. It's easy to use, efficient
enough that it has neglible impact on many programmes, and with
a little trickery can be used with a decorator to profile 
individual functions.

Let's suppose we have the following code:


#### callgrind

TODO

#### line_profiler

TODO

#### profilestats

TODO

#### statprof

TODO

#### plop

TODO

### Memory profiling

TODO

#### muppy

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


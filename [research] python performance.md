# Python Performance

Research for the "Going Faster with Python" article and presentation.

## How to render this document

```
watchmedo shell-command --patterns "*.md;*.bib*" --recursive
--wait --command "pandoc \[research\]\ python\ performance.md
-o html/python_performance.html --standalone 
--table-of-contents --smart --css _pandoc.css
--highlight-style pygments --mathjax
--bibliography=bibliography/bibliography.bib
--csl=bibliography/chicago_fullnote.csl" .
```

## Python data model -> __slots__

-   [http://docs.python.org/2/reference/datamodel.html#slots](http://docs.python.org/2/reference/datamodel.html#slots)
-   Each class instance gets a dictionary of size eight. If you instantiate many class instances this is a waste.
-   By overriding `__slots__` with a string, iterable, or sequence of strings, you can reserve enough space to hold that iterable of strings as variable names.
-   By doing so you can't have new variables.
-   Allocate many objects, microbenchmark, CPython and PyPy.

## Python is only slow if you use it wrong

-   Presentation slides: [http://apenwarr.ca/diary/2011-10-pycodeconf-apenwarr.pdf](http://apenwarr.ca/diary/2011-10-pycodeconf-apenwarr.pdf)
-   Audio: [http://codeconf.s3.amazonaws.com/2011/pycodeconf/talks/PyCodeConf2011%20-%20Avery%20Pennarun.m4a](http://codeconf.s3.amazonaws.com/2011/pycodeconf/talks/PyCodeConf2011%20-%20Avery%20Pennarun.m4a)

-   [bup](http://github.com/apenwarr/bup): 80 MB/sec throughput for backup software without PyPy.
-   [sshuttle](http://github.com/apenwarr/sshuttle): VPN software that easily handles 802.11g/n speed in pure Python.
-   So: Python can easily do performance.

### The Easiest Way to Use Python Wrong

-   In compiled langauges, to do parsing we read a string into memory and then parse it character by chracter:

```python
s = open('file').read()
for char in s:
    ...
```

-   **Don't**! Do not proces character-by-character in an interpreted language if you care about performance.
    -   Avoid **tight inner loops**.
-   In Python a line of code os **80-100x** slower than a line of C code.

### The Easiest Way to use Python Right

-   Use higher-level built-ins and C-modules.
    -   `re`
-   No such thing as 100% Python; why're you limiting yourself?
-   Java's 100% pure approach is very foreign to Python's pragmatic approach.
-   C is simple. Python is simple. PyPy can be hard (to understand).
    -   And why're you using SWIG? Stop.
-   `bup`'s inner byte-by-byte processing is in C.
    -   It just loops and parses, just 50 lines of C.
-   Python has the easiest native C-API.
-   And if you just port tight inner loop processing to C it'll be cross-platform, because not using system calls.

### The Other Way to Use Python Wrong

-   CPU-bound threads are useless because of the GIL.
    -   Recall, each Python is 80-100x slower than C.
    -   And every line in Python is wrapped in a GIL lock!
    -   So multithreading, particularly for CPU-bound Python programs, doesn't exist.
-   I/O bound threads are OK, because we're waiting, not doing processing.
    -   And Python will release the GIL lock during this period.
-   `fork()` is pretty good too (`multiprocessing` does this for you).
-   You can acquire and release the GIL in C code. Process is:
    -   Grab all the data you need, might take a while.
    -   Release the GIL.
    -   *Now* start your (short-lived) threads.
    -   Do your processing.
    -   Finish processing, spin down your threads.
    -   Acquire the GIL.
    -   Return the result. 
    -   (Learned this trick from Linus Torvald's `git` code).
-   Can use `CFFI` as a type of "inline JIT" for C code. Write it once, use it many times.
    -   `SciPy` and `NumPy` can do this too.

### Garbage collection, refcounting and threads

-   Garbage collection is not refcounting.
-   And Python uses both!
-   Refcounting
    -   Every time I use a variable, I increase its reference count by one.
    -   Every time I stop using a variable, I decrease its reference count by one.
    -   If the refcount is zero then release.
-   Garbage collection
    -   No reference counting is necessarily, we just keep track of who is using what.
    -   In the background a garbage person comes along to clean up unused stuff.
-   Python is mostly refcounting, a little bit of GC.
-   The world is moving towards GC.
    -   refcounting is terrible for multithreaded performance.
    -   variables shared between threads need to have a synchronized refcount for that variable.
    -   Python "solves" this by having a GIL for everything, everywhere.
-   Python can do refcounting very fast because it totally sucks at threads, this is the tradeoff.
-   Java and C# and Ruby don't make this tradeoff, and do true GC.

-   Think of it this way: do you want fast Python with no threads or slow Python with real threading?
    -   No-one wants slow Python with real threading, so the GIL is here to stay.
    -   This is because we know how to use C to get fast threads, so why make this terrible tradeoff?

### Comparing languages

-   Sleep 1 second, then allocate 10KB in a tight loop 1 million times.

```python
for i in xrange(1000000):
    a = '\0' * 10000
```

-   PyPy JITs, so it's memory usage doubles during startup, but then allocates memory extremely fast.
-   CPython's memory usage is 1/3 of PyPy, takes longer.
    -   But key is that: memory usage **isn't climbing**.
    -   CPython is carefully noting down the refcounts, and as it always drops to 0 is always frees `a`.
-   Java is atrocious; more memory and more time than CPython.
-   C is fast and efficient.
-   Go is the slowest and efficient.
-   The next slide shows just how atrocious Java is, pretty bad.
-   Just remember, and measure, that JIT causes slow startup.
    -   So can print "Hello world", run 20 times, and measure total exec time.
    -   CPython will beat PyPy.
    -   Latency vs. throughput, long-running vs. short-running processes.

### Python is sometimes a GC language

```python
for i in xrange(1000000):
    a = ['\0' * 10000, None]
    b = ['\0' * 10000, a]
    a[1] = b

    # without this the CPython GC is clever enough to clean
    # up a and b.
    aa[i % 1000] = a
```

-   Due to circular references if CPython just relied on refcounts it'd never free anything.
-   In these cases CPython's garbage person will eventually come along and clean up.
-   The CPython GC is a backup for the primary refcounts method.
-   CPython, in this pathological case, has the same stupid behaviour as Java: allocate up to a maximum then desperately start GC'ing.

### Getting the most out of Python's GC

-   **Just avoid it at all costs**
-   Break circular references by hand when you're done.
-   Better still: use the `weakref` module.
-   Common example of accidentally requiring GC is trees.
    -   Parents have `list[]` children, child has a pointer back to parent.
    -   Great for traversal, disaster for refcounting.
    -   Either:
        -   use `weakref` to make pointers without refcounts. Just keep in mind that objects might suddenly disappear.
        -   deliberately dismantle the tree when you're done by setting `parent = None` on all children.

### Deterministic destructors

-   Does this program work on win32?

```python
open('file', 'w').write('hello')
open('file', 'w').write('world')
```

-   Reason through it.
    -   `open` creates an object with a refcount of 1.
    -   calling `write` on the object increases its refcount to 2.
    -   when `write` finishes its refcount is 1.
    -   when we advance to the next line nothing else is referring to the file object so its refcount drops to 0.
    -   at this point CPython frees the file object.
-   Double-trick question.
    -   On win32 you can't open the same file twice for writing unless you've enabled special sharing options.
    -   So the second command could fail randomly if the first file pointer hasn't been GC'd.
    -   Except we now know Python is refcount'd, with GC as a backup.
    -   So this program doesn't "randomly fail", - it always works in CPython, because the refcount of the first file pointer drops to zero.
    -   Ironically enough this program *does* fail randomly on IronPython.

-   If you had "real" GC, which CPython does not have, you would have to manually manage resources:
    -   files
    -   database handles
    -   sockets
    -   locks
-   In a way this is super-awesome; CPython just works. This would be non-deterministic in C#, Java, Ruby.
-   Context managers, the `with` statement, is more complicated and deterministic destructors are cool as-is.

### Hello World Benchmark

-   `git log` is twice as slow as CPython printing "hello world".
-   C is awesome for command-line tools.
-   CPython compiles down to PYC, and reloads fast, unlike Ruby.
-   Command-line tools in PyPy are 7 times slower than CPython.

-   The presenter is largely focused on systems-level command-line tools.
    -   Doesn't want to rely on JIT, want C code.

## Guido van Rossum on fast Python patterns

[https://plus.google.com/u/0/115212051037621986145/posts/HajXHPGN752](https://plus.google.com/u/0/115212051037621986145/posts/HajXHPGN752)

- Avoid overengineering datastructures. Tuples are better than objects (try namedtuple too though). Prefer simple fields over getter/setter functions.
- Built-in datatypes are your friends. Use more numbers, strings, tuples, lists, sets, dicts. Also check out the collections library, esp. deque.
- Be suspicious of function/method calls; creating a stack frame is expensive.
- Don't write Java (or C++, or Javascript, ...) in Python.
- Are you sure it's too slow? Profile before optimizing!
- The universal speed-up is rewriting small bits of code in C. Do this only when all else fails.

## High Performance Python (EuroPython 2011 workshop)

[http://ianozsvald.com/HighPerformancePythonfromTrainingatEuroPython2011_v0.2.pdf](http://ianozsvald.com/HighPerformancePythonfromTrainingatEuroPython2011_v0.2.pdf)

### Goal

-   Making parallelizable, CPU-bound tasks in Python faster.
-   Tutorial uses Mandelbrot fractal generation.

### Code

-   p19: code that we're using.
    -   Mandlebrot set generation, tight numerical calculation.
    -   Uses lists, then generates an image.
    -   Takes a while, generates a pretty picture.

```
python pure_python.py 1000 1000
```

-   There's one function, `calc_z_serial_purepython`, called once and takes up the most time.
-   Also notice the massive number of calls to `abs` and `range`, which `percall` are cheap but `cumtime` is expensive.


### Profiling with cProfile and line_profiler

-   So, why is this running slow?

```
python -m cProfile -o rep.profile pure_python.py 1000 1000
python -c "import pstats; p = pstats.Stats('rep.profile');
p.sort_stats('cumulative').print_stats(10)"

# can also figure out who is calling these hot functions
p.sort_stats('cumulative').print_callers(10)

# or who these hot functions call
p.sort_stats('cumulative').print_callees(10)
```

-   p21: cProfile output, sorted by cumulative.
-   can also use `runsnake` command for a pretty GUI.
    -   need `pip install SquareMap RunSnakeRun`, and `wxpython`.
    -   `wxpython` difficult to install in a virtualenv, skipping.

-   p22: which lines are causing the slowdown?
    -   `pip install line_profiler`
    -   decorate the functions you're interested in with `@profile`
    -   run: `kernprof.py -l -v pure_python.py 300 100`
-   With the line profile we can see which particular loop is causing the slowdown.
-   Remember to remove the `@profile` decorator when you're done, as only `kernprof.py` understands it.
-   As the line-based profile, just like `cProfile`, measures time, this is good for debugging I/O bound functions as well.
    -   !!AI Could show off a line-profile of an HTTP server, maybe

### Bytecode Analysis

-   We've just profiled our code to determine what parts are slow.
-   In order to make the code faster it's helpful to have an understanding of what Python is trying to do.

```python
import pure_python
import dis
dis.dis(pure_python.calculate_z_serial_purepython)
```

-   For this code:

```python
for iteration in range(maxiter):
    z[i] = z[i]*z[i] + q[i]
    if abs(z[i]) > 2.0:
        output[i] = iteration
        break
```

-   Notice how `z[i]` gets loaded as `load z` then `load z[i]` over and over again, even though this could be optimized out.
-   Notice how `abs` is loaded from the global namespace, even though it's never changed.

### Slighty faster CPython implementation

-   Knowing CPython is doing this unnecessary loading, we can do this:

```python
for iteration in range(maxiter):
    zi = z[i]
    qi = q[i]
    _abs = abs
    zi = zi*zi + qi
    if _abs(zi) > 2.0:
        output[i] = iteration
        break
```

### PyPy

-   Can speed up pure-Python code.
-   So far no `numpy` support.

### Psyco

-   It exists, but doesn't support CPython 2.7 or 64-bit systems.
-   Depreciated in favour or PyPy.

### Cython

-   Move out the hot function to it's own file, with extension PY.
-   Don't change any of the pure-Python code (yet).
-   Check it runs fine with CPython
-   Now rename your hot-function file to have an extension PYX.
-   We'll need a `setup.py` file to build this:

```python
from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext

setup(
    cmdclass = {'build_ext': build_ext},
    ext_modules = [Extension("calculate_z", ["calculate_z.pyx"])],
)
```

-   Now build it:

```
python setup.py build_ext --inplace
```

-   At this stage there is an improvement in performance, but quite minor!
-   This is because we haven't given Cython any hints about what are code looks like.
-   We can actually ask Cython what its guesses have been so far:

```
cython -a calculate_z.pyx
```

-   This produces an HTML file in the same directory, which tells you what each line of Python got converted to in C.
-   The more yellow the line the more calls a given line involves, and hence the more "Python-like" the code is; you want the lines to be white, implying Cython is happily converting it to fewer lines and hence it's more C-like.
-   !!AI Compare the HTML output after adding a few annotations to emphasise this.
-   Now on rebuild it's much faster!

-   p33: Cython supports [compiler directives](http://wiki.cython.org/enhancements/compilerdirectives) in the `setup.py` file to apply globally, or in a given PYX file. 
    -   Disable bounds checking, or negative list indexing, etc.
    -   Can use `profile` to add hooks that allow `cProfiler` to profile the compiled C code.
    -   Set on the top of a PYX file like this:

```python
#cython: boundscheck=False
```

-   Can also apply compiler directives to local blocks after `cimport cython` with a decorator:

```python
@cython.boundscheck(False)
def f():
    ...
    with cython.boundscheck(True):
        ...
```

-   Can also compile Cython at run-time or inline.
    -   Reference: [http://docs.cython.org/src/reference/compilation.html](http://docs.cython.org/src/reference/compilation.html)

-   You can follow these instructions with PyPy but note that it may be very slow because of having to use `cpyext` for all interations; PyPy can't hand-off to Cython.

### Cython with numpy arrays

-   p35: Cython with numpy arrays
-   !!AI haven't tried this.

### Shedskin

-   p36: Shedskin.
-   !!AI exists, but haven't tried it.

### Numpy vectors

-   p38: numpy vectors
-   Rather than use for loops use matrix operations.
-   !!AI haven't tried it.

### numexpr on numpy vectors

-   p42
-   Takes any numpy code and turns them into chunked vector operations, spreads them across math units in the CPU.
-   Often will just make numpy code magically faster.

```python
In [1]: import numpy

In [2]: import numexpr

In [3]: expr = numexpr.NumExpr('a > 5.0')

In [4]: numexpr.disassemble(expr)
Out[4]: [('gt_bdd', 'r0', 'r1[a]', 'c2[5.0]')]

In [5]: expr.run(4)
Out[5]: array(False, dtype=bool)

In [6]: expr.run(6)
Out[6]: array(True, dtype=bool)
```

-   Pre-compile expressions in a tight loop to avoid the overhead of re-compiling expressions.

### pyCUDA

-   p44
-   !!AI haven't tried it.

### ParalellPython

-   p51.
-   Like `multiprocessing` but across remote machines as well.
-   Doesn't send the full environment, so you need to build on all machines.

## When do I optimise?

### Computer Organization and Design, 3rd edition, Chapter 4 - Understanding and Assessing Performance

[@patterson2009computer]

-   Amdahl's law

$$
\begin{align}
    &\begin{aligned}
        & \textrm{Execution time after improvement} \\
        & = \left( \frac{\textrm{Execution time affected by improvement}}{\textrm{Amount of improvement}} + \textrm{Execution time unaffected} \right)
    \end{aligned}
\end{align}
$$

-   Amdahl's law reminds us to **make the common case fast**. But it also teaches us about decreasing returns.
-   For example, suppose I have a program that takes 100 seconds to run. I've identified a subroutine that takes 80 seconds of this time. If I half the cost of the subroutine to 40 seconds, how much faster is my program?

$$
\begin{align}
    &\begin{aligned}
        &\textrm{Execution time after improvement} \\
        & = \left( \frac{\textrm{80}}{2} + (100 - 80) \right) \\
        & = \textrm{60 seconds}
    \end{aligned}
\end{align}
$$

-   and if I quarter the cost to 20 seconds?

$$
\begin{align}
    &\begin{aligned}
        &\textrm{Execution time after improvement} \\
        & = \left( \frac{\textrm{80}}{4} + (100 - 80) \right) \\
        & = \textrm{40 seconds}
    \end{aligned}
\end{align}
$$

-   So reducing the routine's cost by 50% gives 40% returns overall, and reducing it by 75% gives 60% returns overall.
-   Even the best case, where we focus on a routine that occupies most of the execution time, shows noticeable decreasing returns. Imagine if we didn't profile and focused on a random routine!

### Make it Work, Make it Right, Make it Fast

[@c2:2013:makeitworkrightfast]
[@c2:2013:premature]

-   References:
    -   [http://c2.com/cgi/wiki?MakeItWorkMakeItRightMakeItFast](http://c2.com/cgi/wiki?MakeItWorkMakeItRightMakeItFast)
    -   [http://c2.com/cgi/wiki?PrematureOptimization](http://c2.com/cgi/wiki?PrematureOptimization)

-   Get at least some use cases working and tested so you are getting feedback.
-   Get all the use cases working and tested.
-   Use the system end-to-end, find performance bottlenecks.
-   Use the system under a profiler to identify the bottlenecks.
-   Make it fast (mercilessly; everything is tested, right?)

### The oft-misquoted Donald Knuth

[@Knuth74structuredprogramming]

-   Knuth, Donald (December 1974). "Structured Programming with go to Statements". ACM Journal Computing Surveys 6 (4): 268. [CiteSeerX](http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.103.6084)

> Programmers waste enormous amounts of time thinking about, or worrying about, the speed of noncritical parts of their programs, and these attempts at efficiency actually have a strong negative impact when debugging and maintenance are considered. *We should forget about small efficiencies, say about 97% of the time: premature optimization is the root of all evil*. **Yet we should not pass up our opportunities in that critical 3%**.

### Essentials of Software Engineering (2009), Chapter 9 - Implementation

[@tsui2010essentials]

-   Characteristics of a good implementation, in no particular order
    -   **Readability**: can be easily read and understood.
    -   **Maintainability**: can be easily modified, extended, and maintained.
    -   **Performance**: minimises any one, or all of, execution time, memory usage, and power consumption.
    -   **Correctness**: do what it is specified to do.
    -   **Completeness**: all requirements are met.

-   There is no such thing as a free lunch; what would you put these attributes in, knowing that the lower in the list the attribute the less attention it'll receive?
-   For me, performance ends up on the bottom.
-   Yet these attributes aren't independent; certainly readability and maintainability go hand in hand. And what if performance is a non-functional requirement, and hence part of completeness?
-   If so then this isn't a license to ignore the empirical fact that programs are slow in a small part of themselves, and one should likewise use empirical measurements to first determine these before making assumptions.

### Beautiful Code (2007), Chapter 5 - Correct, Beautiful, Fast (In That Order)

[@oram2007beautiful]

> If there's a moral to this story, it is this: do not let performance considerations stop you from doing what is right. You can always make the code faster with a little cleverness. You can rarely recover so easily from a bad design...Design the program you want in the way it should be designed. Then, and only then, should you worry about performance. More often than not, you'll discover the program is fast enough on your first pass.

### Computer Architecture, 4th edition, Chapter 1 - Fundamentals of Computer Design

[@hennessy2011computer]

> Important fundamental observations have come from properties
> of programs. That most important program property that we
> regularly exploit is the **principle of locality**.
> Programs tends to reuse data and instructions they have
> used recently. A widely held rule of thumb is that a program
> spends 90% of its execution time in only 10% of the code...
> Two different types of locality have been observed.
> **Temporal locality** states that recently accessed items are
> likely to be accessed in the near future. **Spatial locality**
> says that items whose addresses are near one another tend to
> be referenced close together in time.

Also, Amdahl's Law in a different form:

$$
\begin{align}
    &\begin{aligned}
        \textrm{Execution time}_{\textrm{old}} & = \textrm{Execution time}_{\textrm{new}} \times \left( \left( 1 - \textrm{Fraction}_{\textrm{enhanced}} \right) + \frac{ \textrm{Fraction}_{\textrm{enhanced}}}{\textrm{Speedup}_{\textrm{enhanced}}} \right) \\
        \textrm{Speedup}_{\textrm{overall}} & = \frac{\textrm{Execution time}_{\textrm{old}}}{\textrm{Execution time}_{\textrm{new}}} \\
        & = \frac{1}{ \left( 1 - \textrm{Fraction}_{\textrm{enhanced}} \right) + \frac{ \textrm{Fraction}_{\textrm{enhanced}}}{\textrm{Speedup}_{\textrm{enhanced}}}}
    \end{aligned}
\end{align}
$$

Here's an example. Suppose we have a web server and there is a routine we could optimise such that it is 10 times faster. Assuming that the web server process is busy with with this routine 40% of the time what is the overall speedup after the optimisation?

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

### Code Complete 2nd edition (2004), Chapter 25 - Code-Tuning Strategies

[@mcconnell2009code, chapter 25]

-   Optimization has a controversial history.
-   Was vital in the 70s, became less-so in the 80's and 90's, and in the 2000s with the advent of embedded software ha sbecome important again.
-   Users care about program throughput and latency.
-   But they implicitly care more about getting software delivered on time, a clean UI, and avoiding downtime.
-   Performance, from a user's perspective, is time taken to execute use cases.
-   How related is this to code throughput and latency, as opposed to a sane user interface, user experience, and information architecture?
-   There is no free lunch; as you focus on some attributes, you will necessarily spend less time on others.
-   Even after deciding efficiency, of speed or size, is important, you have options.
    -   Program requirements.
        -   Do your users actual require this level of performance?
    -   Program design.
        -   Are the methods you've used to achieve your requirements necessary?
        -   e.g. for high-performance simulations can you sacrifice precision for speed?
        -   If you know that size and speed are important, design the architecture to accomodate this.
            -   Set resource goals for subsystems, features, and classes.
            -   Set your objectvies explicitly, so programmers know to work on them.
            -   Set goals that may achieve efficiency indirectly in the future. With very modular and modifiable code, for example with a plugin architecture, you can identify hot components later and re-write them. Great examples of this are Apache Thrift and Audacity's plugin architecture.
    -   Class and routine design   
        -   Choosing appropriate algorithms and data structures early on is often better than optimising later, but requires a sound and thorough knowledge of them.
    -   Hardware
        -   Can you just purchase faster or bigger machines? Time is money!
-   Changing requirements, proper architecture and class design, and appropriate data structures and algorithms are more effective ways of improving performance than code-level optimization.
-   Buying new hardware is easier and could be cheaper.
-   Code optimization comes at the cost of maintainability and readability.
-   You can't identify performance bottlenecks before a program is working.
-   Focusing on optimization prevents you from achiveing other software objectives.
-   Summary of approach to code tuning
    -   Develop well-designed software that's easy to understand and modify.
    -   Measure performance.
    -   If performance is poor:
        -   Save a working version of the software.
        -   Profile the system.
        -   Determine the reason for the poor performance.
        -   Tune.
        -   Measure each improvment one at a time.
    -   Repeat.

### Five Steps to Solving Software Performance Problems

[@williams2002five]

1.   Figure out where you need to be.
    -   Define precise, quantitative, and measureable performance objectives, in terms of either or both of throughput and latency.
    -   e.g. The time to first byte (TTFB) for the software system will be 50ms for 95% of all requests at all times.
    -   e.g. CPU usage will never exceed 65%.
2.  Determine where you are now
    -   What use cases are causing problems?
    -   What is the context of these use cases?
    -   If not already done, take a look at the software architecture from a performance perspective. Given the architecture, is software tuning even a cost-effective option?
    -   Profile the system.   
3.  Can you achieve your performance objectives?
    -   Use Amdahl's Law.
    -   Is the required throughput or response time, given the hardware and architecture context, even feasible?
4.  Develop a plan.
    -   Prototypes with measurements.

Tuning software code will rarely achieve the same results as a system designed with performance in mind from the beginning. With performance in mind from the beginning, by definition, one would need to add low-level measurements and instrumentation, with a proactive mindset, to identify problems as they arise. 

###   Refactoring - Improving the Design of Existing Code (2002), Chapter 2 - Principles in Refactoring

[@fowler1999refactoring, chapter 2]

> The secret to fast software, in all but hard real-time contexts, is to write tunable software first and then tune it for sufficient speed.

One approach is to always pay attention to performance in every line of code you write. This approach has intuitive attraction; how can code be slow if you're always writing it to be fast? However, changes that improve performance *usually* make the program less maintainable and readable, which slows development and maintenance. This would be an acceptable cost if the benefit was that the program was indeed faster, but often it isn't. This is
mainly because the naive effort of optimising everything as you write code is too narrow in perspective and ignore empirical evidence of how software actually behaves.

Decades of experience and observation, both in the software and computer engineering spheres, have shown programs waste most their time in a small fraction of their code, around 10%. If you optimise everything equally by definition around 90% of your effort is wasted, because much of the code isn't run that often. Worse, you've wasted time that could have been focused on the real problem areas, and to boot have made your entire program less maintainable in the long run.

!!AI this is not to say a thorough knowledge of algorithms and data structures is useless; having these in hand at the design stage will not only provide the most meaningful optimizations but in a way that often is more readable and maintainable.

The correct way of optimizing code is, at first, to not; conduct excellent requirements analysis, then design and build your code in a well factored manner (!!AI that is informed by a thorough knowledge of algorithms and data structures). In time your non-functional requirements with respect to performance may get violated. Once they are you profile your code, find the (by definition) small part of your code that is taking up the most time. As your code is well designed and
factored you can make small, cautious, incremental fixes, constantly re-profiling after each fix, improving performance.

### Consistency

[@emerson1993self]
[@hofstadter2000godel]

-   Ralph Waldo Emerson, Self Reliance (1841)

> A foolish consistency is the hobgoblin of little minds, adored by little statesman and philosophers and divines. With consistency a great soul has simply nothing to do. He may as well concern himself with his shadow on the wall. Speak what you think now in hard words, and to-morrow speak what to-morrow thinks in hard words again, though it contradict every thing you said to-day.

-   Miguel de Unamuno, quoted by Douglas R. Hofstadter in Godel, Escher, Bach (1979)

> If a person never contradicts himself, it must be that he says nothing.

## Debugging memory usage in Python

-   References:
    -   [http://neverfear.org/blog/view/155/Investigating_memory_leaks_in_Python](http://neverfear.org/blog/view/155/Investigating_memory_leaks_in_Python)

-   `pip install Cython ipython ipdb objgraph pympler`
-   `pip install` for `meliae` doesn't work, so just install from source here: `https://launchpad.net/meliae`
-   In your application trap a signal to drop to `ipdb`:

```python
def start_ipdb(signal, trace):
    import ipdb
    ipdb.set_trace()
import signal
signal.signal(signal.SIGQUIT, start_ipdb)
```

### Maliae

-   Whilst running press `CTRL-\`, then run:

```python
from meliae import scanner
scanner.dump_all_objects('meliae.json')
```

-   Then analyze it

```python
from meliae import loader
om = loader.load('dump.meliae')
s = om.summarize();
s
```

### objgraph

-   Whilst running press `CTRL-\`, then run:

```python
import objgraph

# Show most frequent objects.
objgraph.show_most_common_types()

# Count a particular type of object.
objgraph.count("dict")

# Draw a pretty reference graph for all instances of an object.
objgraph.show_backrefs(objgraph.by_type("dict")[0:50])
```

### muppy

-   Reference: [http://pythonhosted.org/Pympler/muppy.html](http://pythonhosted.org/Pympler/muppy.html)
-   Whilst running press `CTRL-\`, then run:

```python
from pympler import muppy

# get all objects
all_objects = muppy.get_objects()
len(all_objects)

# summarize all objects
from pympler import summary
summ1 = summary.summarize(all_objects)
summary.print_(summ1)

# we can compare two different summaries to compare
# changes over time
summ2 = summary.summarize(muppy.get_objects())
diff = summary.get_diff(summ1, summ2)
summary.print_(diff)

# to do the above automatically, use tracker
from pympler import tracker
tr = tracker.SummaryTracker()
tr.print_diff()

# time passes
tr.print_diff()

# use the refbrowser module to see tree of object
# references.
```

## Profiling in Python

### !!AI ideas

-   Run CPU and I/O bound scripts with all profiling types, give hand-waving estimates of occupancy, show what deterministic vs. statistical profiling means. 

### cProfile

-   How to proflie an individual function using an undocumented feature in `cProfile`: [http://stackoverflow.com/questions/5375624/a-decorator-that-profiles-a-method-call-and-logs-the-profiling-result](http://stackoverflow.com/questions/5375624/a-decorator-that-profiles-a-method-call-and-logs-the-profiling-result)

```python
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
```

### statprof

-   References:
    -   [https://github.com/bos/statprof.py](https://github.com/bos/statprof.py)
-   `statprof` is a statistical profiler.
-   It is intended to have a lighter impact than `cProfiler`.
-   It also regularly gathers a stack, and so is able to identify hot-spots within functions.

```python
import statprof

statprof.start()
    try:
        my_questionable_function()
    finally:
        statprof.stop()
        statprof.display()
```

### line_profiler

-   References
    -   The EuroPython 2011 High Performance Computing tutorial, detailed above.
    -   [http://pythonhosted.org/line_profiler/](http://pythonhosted.org/line_profiler/)
-   `pip install line_profiler`
-   See the EuroPython talk notes.

### callgrind

-   References:
    -   [http://langui.sh/2011/06/16/how-to-install-qcachegrind-kcachegrind-on-mac-osx-snow-leopard/](http://langui.sh/2011/06/16/how-to-install-qcachegrind-kcachegrind-on-mac-osx-snow-leopard/)

-   Installation
    -   You'll need XCode Developer Tools.
    -   `brew install qt graphviz`
    -   Download the [KCachegrind source](http://kcachegrind.sourceforge.net/html/Download.html).
    -   `cd kcachegrind/qcachegrind`
    -   `qmake; make`
    -   You'll have a `qcachegrind.app`, move it to Applications.
    -   It wants the Graphviz executable `dot` to be accessible without a `~/.bash_profile`, so you need `sudo ln -s /usr/local/bin/dot /usr/bin/dot`
    -   `pip install pyprof2calltree`
-   This is far superior to RunSnakeRun
-   To use:
    -   Generate a regular `cProfile` profile file.
    -   `pyprof2calltree -i cprofile.output -o callgrind.output`
    -   Open it in QCachegrind.
    -   Pretty pictures!

### profilestats

-   References:
    -   [https://pypi.python.org/pypi/profilestats](https://pypi.python.org/pypi/profilestats)
-   Decorator for profiling individual functions and then converting the profiling data to kcachegrind format.
-   Installation
    -   `pip install profilestats`
-   Usage
    -   `from profilestats import profile`
    -   `@profile` on function

### PyCounter

-   References:
    -   [http://pycounters.readthedocs.org/en/latest/](http://pycounters.readthedocs.org/en/latest/)
-   Installation
    -   `pip install pycounters`
-   Usage
    -   `from pycounters.shortcuts import frequency, time`
    -   Set up a log reporter:

```python
import pycounters
import logging

reporter=pycounters.reporters.LogReporter(logging.getLogger("counters"))
pycounters.register_reporter(reporter)
pycounters.start_auto_reporting(seconds=300)
```

    -   Decorate functions with `@frequency()` and `@time()`.

### plop

-   References:
    -   [https://github.com/bdarnell/plop](https://github.com/bdarnell/plop)
    -   [https://tech.dropbox.com/2012/07/plop-low-overhead-profiling-for-python/](https://tech.dropbox.com/2012/07/plop-low-overhead-profiling-for-python/)
-   Statistical profiler, low CPU overhead.
-   Installation:
    -   `pip install plop tornado`
-   Usage:
    -   `python -m plop.collector myscript.py`
    -   Writes output to `/tmp/plop.out`
    -   `python -m plop.viewer --datadir=/tmp`
    -   Browse to [http://localhost:8888](http://localhost:8888)
-   Pretty pictures!
    -   D3 force-directed call graph.
    -   Radius of node is percentage time it takes.

    
## Cython

-   References:
    -   [http://docs.cython.org/](http://docs.cython.org/)

-   I wanted to use GCC 4.7 from [http://hpc.sourceforge.net](http://hpc.sourceforge.net), but a lot of Python packages use `-Qunused-arguments`.
    -   Rather than use pip, download the module, decompress.
    -   Run: `CFLAGS="" python setup.py install`.

-   Follow PyPy instructions later to install `easy_install`, `pip`, then `Cython`.


## CFFI

!!AI Placeholder for diving into CFFI here. Want to write an article and give a presentation, so make detailed notes.

-   References:
    -   Main docs: [http://cffi.readthedocs.org/en/release-0.5/](http://cffi.readthedocs.org/en/release-0.5/)
    -   A fast CSV reader demo: [https://bitbucket.org/cffi/cffi/src/default/demo/fastcsv.py?at=default](https://bitbucket.org/cffi/cffi/src/default/demo/fastcsv.py?at=default)

-   I wanted to use GCC 4.7 from [http://hpc.sourceforge.net](http://hpc.sourceforge.net), but a lot of Python packages use `-Qunused-arguments`.
    -   Rather than use pip, download the module, decompress.
    -   Run: `CFLAGS="" python setup.py install`.

-   This project is **not** intended for embedding C code, but rather to re-use existing C code.
    -   !!AI however it does seem rather easy to in-line C code...

## SciPy Weave

-   References:
    -   [http://www.scipy.org/Weave](http://www.scipy.org/Weave)
-   Intended for in-lining C code in Python.

## PyPy

-   Download from here: [http://pypy.org/download.html](http://pypy.org/download.html)
-   (Or on Mac use homebrew).

```
curl http://python-distribute.org/distribute_setup.py | pypy
curl https://raw.github.com/pypa/pip/master/contrib/get-pip.py | pypy
```

-   PyPy is garbage collected, CPython is reference counting with a backup garbage collector. References:
    -   [http://pypy.readthedocs.org/en/latest/cpython_differences.html#differences-related-to-garbage-collection-strategies](http://pypy.readthedocs.org/en/latest/cpython_differences.html#differences-related-to-garbage-collection-strategies)
    -   [http://docs.python.org/2/reference/datamodel.html](http://docs.python.org/2/reference/datamodel.html)
-   In CPython:

```
In [1]: class A(object):
   ...:     def __del__(self):
   ...:         print "A signing off!"
   ...:         

In [2]: def f():
   ...:     a = A()
   ...:     

In [3]: f()
A signing off!

In [4]: f()
A signing off!

In [5]: f()
A signing off!
```

-   In PyPy:

```
>>>> class A(object):
....     def __del__(self):
....         print 'A signing off!'
.... 
>>>> def f():
....     a = A()
.... 
>>>> f()
>>>> f()
>>>> f()
```

## Profile official docs

[http://docs.python.org/2/library/profile.html](http://docs.python.org/2/library/profile.html)

-   `cProfile` is an example of **deterministic profiling**.
    -   Every single function call, return, and exception event is monitored.
    -   CPython offers an optional callback into each event.
    -   So the overhead is not that severe and yet provides extensive statistics.
-   This is in contrast to **statistical profiling**, where you dip in and out.

## Official Python Performance Tips

[http://wiki.python.org/moin/PythonSpeed/PerformanceTips](http://wiki.python.org/moin/PythonSpeed/PerformanceTips)

!!AI TOREAD

## How to get the most out of your PyPy

[http://pyvideo.org/video/612/how-to-get-the-most-out-of-your-pypy](http://pyvideo.org/video/612/how-to-get-the-most-out-of-your-pypy)

!!AI TOWATCH

## Faster Python Programs through Optimization

[http://pyvideo.org/video/607/faster-python-programs-through-optimization](http://pyvideo.org/video/607/faster-python-programs-through-optimization)

!!AI TOWATCH

## Details of Python performance

[http://lanyrd.com/2012/pycon-za/syyft/](http://lanyrd.com/2012/pycon-za/syyft/)

!!AI TOWATCH

## References


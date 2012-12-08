# Software Testing (CS258)

via Udacity

## Lecture notes

### 1. What is Testing?

#### 1.1: Introduction

-	Don't be daunted by the large problem of "get rid of all bugs".
-	Split into smaller problems, apply patterns.

#### 1.2: What is Testing

-	Test input -> Software under test -> Test outputs.
-	Outputs OK? Yes, else debug.

#### 1.3: What Happens When We Test Software

-	Test output, what do we do when we check "OK?"
-	Running an experiment, but when it is OK we don't learn that much.
-	If not OK, and it's a bug in SUT.
-	Might be bug in acceptability test.
-	Might be bug in specification.
-	Might be bug in OS, compiler, libraries, hardware.
-	Else...don't know!
-	All these answers help us create software in the future.

#### 1.4: Mars Climate Orbiter

-	Orbiter crashed.
-	Miscommunication between Lockheed Martin and NASA.
-	NASA expected metric, m/s, but Lockheed Martin programmed in english, ft/s.
-	Not a bug in SUT.
	-	Software did what it was specified to do.
-	Not a bug in acceptability test.
	-	If we argue this then all bugs are acceptability test bugs because now we're saying acceptability tests must catch all bugs.
	-	Rather want to argue the bug isn't here; the software was acceptable as per specifications.
-	Bug in specification.
	-	Miscommunication between engineers.
-	Not a bug in OS, compiler, libraries, hardware.
	-	No evidence for this.

#### 1.5: Fixed Sized Queue

-	FIFO order.
-	Statically sized and allocated.
-	Operations.
	-	enqueue.
		-	Return True if it fits, False if not.
	-	dequeue.
		-	Return value if present, None if not.
-	Python implementation
	-	For performance use `array.array`, statically typed, 10 times faster than list.
	-	`array.array('i'), range(size_max))`
	-	Tracks `head`, `tail`, `size`.
	-	Never actually delete. On dequeue just increment head pointer.
	-	On enqueue increment tail pointer.

#### 1.6: Filling the Queue

``
q = Queue(2)
r1 = enqueue(6)
r2 = enqueue(7)
r3 = enqueue(8)
r4 = dequeue()
r5 = dequeue()
r6 = dequeue()

(r1, r2, r3, r4, r5, r6) = (True, True, False, 6, 7, None)
``

#### 1.7: What We Learn

-	How useful is any given test case?
-	How to make useful test cases?

``
enqueue(7)
x = dequeue()
if x == 7:
	print "success!"
else:
	print "error!"
``

-	If this test case passes:
	-	Our code passes this test case.
	-	Our code doesn't necessarily pass any test case where we replace 7 with a different integer.
		-	e.g. a massive integer that can't fit in memory.
		-	e.g. storing shorts, but try to put 2^32 - 1.
	-	Our code does pass many test cases where we replace 7 with a different integer.
		-	Replace 7 with any reasonably sized integer.
-	How do we write tests that represent a large space of inputs?

#### 1.8: Equivalent Tests

-	Want to argue that a single test case is representative of a whole class of executions types for the software under test.
-	Mapping single point in the input space to single point in output space.
-	Want an intuition that we've mapped many inputs to many outputs.
-	Clearly large integers different from smaller ones.
	-	Maybe Python garbage collector bug such that large integer gets garbage collected, to sleeping before dequeuing it would fail.
	-	Maybe Python runtime has bug with truncating large integers, so it wouldn't be the same when we dequeue it.
-	But note the above arguments are about the surrounding system and not the software under test.
-	Hence we can make arguments that increase test coverage but must be very careful about assumptions we make.

#### 1.9: Testing the queue

-	Test basic assumptions in every test, duplicate tests.
-	Be introspective, test internal pointers.
-	Test1: basic enqueue and dequeue.
-	Test2
	-	Queue size 2, enqueue 3 times and check `q.tail != 0`.
-	Test3
	-	Queue size 1
	-	dequeue when empty
	-	enqueue then dequeue.
	-	Check value correct and q.head != 0.

#### 1.10: Creating Testable Software

-    Write clean code.
-    Refactor code whenever necessary.
-    For any module, be able to
    -    clearly describe what it does.
    -    clearly describe how it interacts with other code.
-    No extra threads.
-    No swamp of global variables.
    -    Implicit inputs to all functions.
-    No pointer soup.
-    Modules should have unit tests.
-    When applicable, add fault injection.
    -    Inject bad inputs.
    -    Deliberately malform your code.
    -    Check your assertions trigger.
-    Assertions, assertions, assertions.

#### 1.11: Assertions

-    **Assertion**: executable check for a property that must be true.

        def sqrt(arg):
            … compute …
            assert result >= 0
            return result
            
-    We know that by definition result must be 0 or bigger.
-    Rules
    1.    *Assertions are not for error handling*.
        -    e.g. want an exception to check arg >= 0, not an assertion.
        -    Asserting our sanity, not behaviour of others.
    2.    *No side effects*.
        -    e.g. assert calls a function that modifies a global variable.
    3.    *No silly assertions*.
        -    e.g. assert (1+1) = 2
        -    check non-trivial properties that imply a fault with our logic.
        
#### 1.12: Checkrep

-    For data structures often write a *checkRep*. Validate invariants that must be true.
-    There could be deeply buried problems in our own code.
-    When they occur they affect others, infecting them.
-    Want to fail fast, and checkRep as tight as possible and catch bugs before they affect others.
-    Want to assert `self.head`, `self.tail`, and `self.size` are consistent.

        def checkRep(self):
            assert self.size >= 0 and self.size <= self.max
            if self.tail > self.head:
                assert (self.tail - self.head) == self.size
            if self.tail < self.head:
                assert (self.head - self.tail) == (self.max - self.size)
            if self.tail == self.head:
                assert (self.size == 0) or (self.size == self.max)
                
#### 1.13: Why assertions                

1.    Make code self-checking, leading to more effective testing.
2.    Make code fail early, closer to bug.
3.    Assign blame.
4.    Document and actively check:
    -    Assumptions.
    -    Preconditions.
    -    Postconditions.
    -    Invariants.

-    Assertions are used in GCC and LLVM.
-    Do you use them in production?
    -    Advantages of disabling.
        -    Code runs faster.
        -    Code keeps going. (Always good?)
    -    Disadvantages of disabling.
        -    Code relies on side-effects of assertions (whoops!)
        -    Even in production, may be better to fail early.
    -    Generally worth even the run-time cost of leaving assertions enabled in production.
    -    At NASA, left assertions on except when lander was landing - only have one shot!
    
#### 1.17: Specifications

-    SUT provides some service over some API.
-    Want to test API. e.g. sqrt.
-    Just writing and test cases help refine specifications.

#### 1.19: Domains and Ranges

-    **Domain**: set of inputs.
-    **Range**: set of outputs.
-    e.g. sqrt in Python
    -    Domain: all floating point number (F)
    -    Range: positive floating point, unioned with exception.
    -    Ideally only want domain to be positive floating point, but we accept all and throw exceptions.
-    Want to test over full domain, even if it results in exception.
-    Often domain specification is implicit; too many exceptions make code unwieldy.

#### 1.21: Crashme

-    For operating systems especially want to test over the full domain.
    -    Must be strong against any kind of bad input.
-    **crashme**. Generate garbage, then jump into the middle and ask the kernel to execute it.
-    If kernel dies then that's a bug.
-    *Interfaces that span trust boundaries are special* and must be tested on the full range of representable values.

#### 1.23: Trust Relationships

-    Browsers offer APIs (e.g. GUI), but use a lot of APIs (network, cookies onto disk).
-    If e.g. disk out of space and we try to store a cookie don't want to crash the browser.
-    But how to test this? Difficult to mimic OS API conditions, e.g. out of disk space.
-    Think of e.g. UNIX call to `read()`.
    -    Read can be asked to read 0 bytes.
    -    read() can return -1, for at least nine different reasons.
-    There is no easy or magical answer.

#### 1.24: Fault Injection

-    Use API that are predictable and return easy to understand error codes and behaviour.
    -    C `read()` vs. Python `read()`.
-    So call a stub function.

        file = open("/tmp/foo", 'w')
        
        # to
        
        file = my_open("/tmp/foo", 'w')
        
-    **Fault injection**: alter abstract function calls to other API.
-    Faults injected into a SUT should be faults that we want our code to be robust to.
    -    Don't need to be all possible faults, not feasible.
    
#### 1.25: Timing Dependency Problems

-    Read/request cycle of API isn't the only problem.
-    What is SUT cares about timing of API usage?
-    e.g. double click vs. single click.
-    Too fast vs. too slow is simple to think about.

#### 1.26: Therac 25

-    **Race condition**: different rates of execution of different parts of program cause problem.
    -    Typing slowly, Therac 25 is fine. Typical for beginners.
    -    Typing too fast, trigger race conditions. Typical for experts.
-    Do we need to care about timing?
    -    For browsers and OS kernels, yes.
    -    For sqrt, hopefully not!
-    Care about timing:
    -    Hardware interfaces.
    -    Network interfaces.
    -    Multi-threaded.

#### 1.29: Nonfunctional inputs

-    Not testing APIs the SUT provides.
-    Not testing APIs the SUT uses.
-    Examples.
    -    Context switches. How multiple threads execute in what order. Timing is under the control of the OS.
    -    Testing very reliable network switches.
        -    Open up a switch and run a key over electrical contacts.
        -    Testing a previously inaccessible part of domain.
        
#### 1.30: Testing Survey

-    **White box**: tester uses detailed knowledge about internals.
-    **Black box**: Don't use internal knowledge, just behavioural knowledge.
-    **Unit testing**: test small units of code.
    -    Typically by developer.
    -    Can be white or black box.
    -    No hypothesis about behaviour, so test over full range of domain.
    -    **Mock objects**: pretend to be other modules.
-   **Integration testing**: testing already-tested modules in combination.
    -    Very hard, even with tight specification.
-    **System testing**: does the system, as a whole, meet specifications?
    -    Internal knowledge may not be helpful.
    -    Don't really care about internals, just checking if it meets goals.
    -    May not care about all possible use cases, just important use cases.
-    **Differential testing**
    -    Deliver same input to two different versions of SUT.
-    **Stress testing**
    -    Push limits of domain, its timing, its sizes, number of API calls, etc.
    -    Testing reliability.
-    **Random testing**
    -    Exploring full domain space.    
    -    e.g. crashme.
    
#### 1.38: Being Great At Testing

-    Testing and development are different.
    -    Developer: "I want this code to succeed."
    -    Tester: "I want this code to fail."
    -    Double think!
-    Learn to test creatively.
-    Don't ignore weird stuff.
-    Fun! Profit!

#### Problem Set 1: Blackbox testing buggy Queues

-    Lessons learned.
    1.    Test maximums and minimums of interfaces.
        -    If can have a Queue of size x, what about x = 2 ** 16?
        -    If can hold any integer, what about holding 2 ** 32?
    2.    Methods that should be idempotent might not be.
        -    queue.empty() actually dequeues!
        -    Write tests that check that query methods are idempotent.
    3.    Test interfaces strictly.
        -    What do they promise to return when?
        -    False != None.
    4.    Test asssumptions.
        -    If a queue claims to have a size, how do you know? Fill it up then dequeue everything!




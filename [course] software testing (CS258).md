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
	-	Our code doesn't pass any test case where we replace 7 with a different integer.
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

!!TOWATCH
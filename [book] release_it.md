Stability Anti-Patterns
=======================

Integration points
------------------

-   **Beware this necessary evil**. All integration points fail.
-   **Prepare for the many forms of failure**. Never nice, always odd, slow, hangs, etc.
-   **Know when to open up abstractions**. Debugging may mean diving in.
-   **Failures propagate quickly**.
-   **Apply patterns to avert Integration Points problems**. Circuit Breaker, Timeout, Decoupling Middleware, Handshaking.

Chain reactions
---------------

-   **One server down jeopardizes the rest**. Increased load.
-   **Hunt for resource leaks**. Traffic -> memory leaks.
-   **Hunt for obscure timing bugs**. Race conditions.
-   **Defend with Bulkheads**. Partitioning on server side, Circuit Breaker on calling side.

Cascading failures
------------------

-   **Stop cracks from jumping the gap**. Stay up when they go down.
-   **Scrutinize resource pools**. Safe resource pools always timeout threads.
-   **Defend with Timeouts and Circuit Breaker**. Former ensures you come back, latter ensures you avoid hammering a troubled Integration Point.

Users
-----

-   **Users consume memory**. Minimize occupany per user, only use sessions for caching so purging is an option.
-   **Users do weird, random things**. Need crazy testing.
-   **Malicious users are out there**. Patch, stay frosty.
-   **Users will gang up on you**. Do stress testing on all points.

Blocked Threads
---------------

-   **The Blocked Threads antipattern is the proximate cause of most failures**. Leads to Chain Reactions and Cascading Failurs.
-   **Scrutinize resource pools**. e.g. deadlocks cause connections to be lost, incorrect exception handling.
-   **Use proven primitives**. e.g. queues.
-   **Defend with Timeouts**.
-   **Beware the code you cannot see**. i.e. third party code.

Attacks of Self-Denial
----------------------

-   **Keep the lines of communication open**. Static landing zones for destintions to special offers. No embedded session IDs.
-   **Protect shared resources**. Fight Club bugs where front-end load -> exponential back-end load.
-   **Expect rapid redistribution of any cool or valuable offer**.

Scaling effects
---------------

-   **Examine production versus QA environments to spot Scaling Effects**. Respective sizes need comparing.
-   **Watch out for point-to-point communication**. Full mesh -> O(n^2) connections.
-   **Watch out for shared resources**. Bottleneck, constraint. Stress test them, test clients' behaviour to slowness to hangs.

Unbalanced capacities
---------------------

-   **Examine server and thread counts**. Check ratio of front-end to back-end servers, compare threads.
-   **Observe near scaling effects and users**. Watch of changes in patterns of load.
-   **Stress both sides of the interface**. Flood back-end with x10 maximum load. Mimic slow or dead back end, see what happens to front-end.

Slow Responses
--------------

-   **Slow Responses triggers Cascading Failures**.
-   **For websites, Slow Responses causes more traffic**. Hit reload.
-   **Consider Fail Fast**. Track your own responsiveness, consider sending immediate failure when average response time too high.
-   **Hunt for memory leaks or resource contention**.

SLA Inversion
-------------

-   **Don't make empty promises**. Your SLA is the lowest SLA of your dependencies.
-   **Examine every dependency**. DNS? SMTP? Enterprise SAN? Message queues? Brokers?
-   **Decouple your SLAs**. Maintain service in the face of failure.

Unbounded Result Sets
---------------------

-   **Use realistic data volumes**. Test production sizes.
-   **Don't rely on the data producers**. Only sizes you care about are "zero", "one", or "lots".
-   **Put limits onto other application-level protocols**. RMI, DCOM, XML-RPC, all can return massive sets.

Stability Patterns
==================

Use Timeouts
------------

-   **Apply to Integration Points, Blocked Threads, and Slow Responses**. Prevents Blocked Threads, averts Cascading Failures.
-   **Apply to recover from unexpected failures**.
-   **Consider delayed retries**. Most problems will always exists immediately after.

Circuit Breakers
----------------

-   "Closed" -> fine. X problems in Y time -> "Open". When "Open" all calls fail. After Z time becomes "Half-Open"; even one failure makes it open again. Else "Closed".
-   **Don't do it if it hurts**. If an Integration Point hits many problems, stop calling it!
-   **Use together with Timeouts**. Timeouts offer the indication of a problem.
-   **Escape, track, and report state changes**. Popping a Circuit Breaker is always a serious problem.

Bulkheads
---------

-   **Save part of the ship**. Partition for partial functionality.
-   **Decide whether to accept less efficient use of resources**. Means keeping resource in reserve.
-   **Pick a useful granularity**. Thread pools, CPUs, or servers in a cluster.
-   **Very important with shared services models**.

Steady State
------------

-   **Avoid fiddling**. Eliminate need for recurring human intervention.
-   **Purge data with application logic**.
-   **Limit caching**. Bound memory usage.
-   **Roll the logs**. Cap their size.

Fail Fast
---------

-   **Avoid Slow Responses and Fail Fast**. If can't meet SLA, tell callers fast.
-   **Reserve resources, verify Integration Points early**. e.g. if Circuit Breaker popped on a required call, don't waste time by starting.
-   **Use for input validation**. Prevents wasting resources for duff requests.

Handshaking
-----------

-   **Create cooperative demand control**. Both client and server must be built to perform Handshaking.
-   **Consider health checks**. Application-level workaround for lack of Handshaking.
-   **Build Handshaking into your own low-level protocols**. Endpoints inform the other when they are not ready to accept work.

Test Harness
------------

-   **Emulate out-of-spec failures**.
-   **Stress the caller**. Slow responses, no responses, garbage responses.
-   **Leverage shared harnesses for common failures**.
-   **Supplement, don't replace, other test methods**. Not substitute for unit tests, acceptance tests, etc, for functional behaviour. This is for "non-functional" behaviour.

Decoupling Middleware
---------------------

-   **Decide at the last responsible moment**. Massive decision, make it early.
-   **Avoid many failure modes through total decoupling**. More adaptable too.
-   **Learn many architectures, and choose among them**.

Capacity Anti-Patterns
======================

Resource Pool Contention
------------------------

-   **Eliminate contention under normal loads**.
-   **If possible, size resource pools to the request thread pool**. Watch out for failover scenarios.
-   **Prevent vicious cycles**. Resource contention -> slow responses -> resource contention.
-   **Watch for the Blocked Threads pattern**.

AJAX Overkill
-------------

-   **Avoid needles requests**. Don't poll for autocompletion. If you need it, send requests on updates.
-   **Respect your session architecture**. Use session IDs on AJAX.
-   **Minimize the size of replies**. Use JSON, not HTML.
-   **Increase the size of your web tier**.

Overstaying Sessions
--------------------

-   **Curtail session retention**. Short as possible.
-   **Remember that users don't understand sessions**. Users get auto logout for security. Use it as a cache, not the only store of user data.
-   **Keep keys, not whole objects**.

The Reload Button
-----------------

-   **Make the Reload button irrelevant**. Serve pages so fast no reload, else hurts to re-request resources.

Capacity Patterns
=================

Pool Connections
----------------

-   **Pool connections**. Just do it.
-   **Protect request-handling threads**. Make infinite blocks impossible. Use timeouts.
-   **Size the pools for maximum throughput**. Monitor callers for wait times.

Use Caching Carefully
---------------------

-   **Limit cache sizes**.
-   **Build a flush mechanism**. Clock, calendar, or event based, needs flushing eventually. Rate-limit, else could happen too often.
-   **Don't cache trivial objects**.
-   **Compare access and change frequency**. Don't change write-heavy objects.

Precompute content
------------------

-   **Precompute content that changes infrequently**. Consider cost of generation into change probability and request frequency and cost.

Tune the Garbage Collector
--------------------------

-   **Tune the garbage collector in production**. Need actual usage pattern to tune against.
-   **Keep it up**. Tune every cycle.
-   **Don't pool ordinary objects**. Try to rely on garbage collector.


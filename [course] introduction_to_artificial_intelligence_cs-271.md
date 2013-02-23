# Introduction to Artificial Intelligence

Via Udacity (CS-271)

## Student

[Asim Ihsan](http://www.asimihsan.com)

## 1.3: Intelligent Agents

-    **Agents** interact with **environment**.
-    Agents input via **sensors**.
-    Agents output via **actuators**.
-    Mapping sensors to actuators via **control policies**.
-    **Perception-action cycle**.

## 1.4: Applications of AI
-  AI in finance
    -    input: news, data
    -    output: trades
-    AI in robotics
    -    input: camera, microphone, touch
    -    output: motors, voice
-    etc. for games, medicine

## 1.5: Terminology

-    **Fully observable**: full information, sensors are sufficient to make optimal choice. e.g. chess.
-    **Partially observable**: partial information. e.g. poker.
-    Environment has internal **state**.
-    Fully observable => sensors can see all of state.
-    Partially observable => sensors cannot, but **memory** helps.
    -    Partially observable => memory required.

-    **Deterministic environment**: your agent's actuators uniquely determine the environment's state. e.g. chess.
-    **Stochastic environment**: actuators don't uniquely determine the environment's state, e.g. dice games.

-    **Discrete**: finite number of actions, senses, and states. e.g. chess.
-    **Continuous**: infinite number of actions, senses, and states. e.g. darts.

-    **Benign**: state or other actions can affect you but they aren't out to get you, non-zero-sum. e.g. weather.
-    **Adversarial**: state or other actions are out to get you, zero-sum. More difficult to act. e.g. chess.

## 1.8: AI and Uncertainty

-    AI as uncertainty management.
-    AI: *what to do when you don't know what to do*.
-    Why uncertain?
    -    Sensor limits.
    -    Adversaries.
    -    Stochastic environments.
    -    Laziness.
    -    Ignorance.
    
## 1.9: Machine Translation

-    At Google.
-    Use examples between languages.
-    Offline, build model.
-    Chinese food menu.
-    Common token on left (in Chinese) with another on right (in English) implies that the left token is probably the right token.
    -    Correlation implies causation.

## 2.1: Problem Solving, Intro

-    Problems
    -    Environment state space and/or valid actions is large.
    -    State isn't fully observable.
-    Definition of a problem
    -    **Initial state**
    -    **Action(s)**, a function.
        -    Input: state.
        -    Output: set of actions {a_1, a_2, …, a_n}
        -    In some problems output is identical for all states.
    -    **Result(s, a)**, another function
            -    Input: state, action
            -    Output: state, i.e. new state.
    -    **GoalTest(s)** -> true or false
        -    Is state the goal?
    -    **PathCost(s ->a s ->a s)** -> n.
        -    Cost of path of sequence of actions, state to state.
        -    Usually define as additive.
        -    **StepCost(s, a, s')** -> n.
            -    state, action, new state.
    -    PathCost is sum of StepCosts.

## 2.3: Problem Solving: Example Route Finding

-    **Frontier**: outer edge of explored state space.
	-	First layer outside of explored space.
-    **Unexplored**: unencountered state space.
-    **Explored**: encountered routes.

## 2.4: Problem Solving: Tree Search

        function TreeSearch(problem):
            frontier = { [intial] }
            loop:
                if frontier is empty: return FAIL
                
                # how to make choice is differentiator
                path = remove_choice(frontier)
                
                s = path.end
                if s is a goal: return path
                
                # expand the path
                for a in actions:
                    add [path + a -> Result(s, a)] to frontier
                    
-	Note that we only check if we're at the goal for explored points, not points on the frontier.
	-	Hence when you first encounter a node you cannot just finish.
-	TreeSearch very general, differentiated by `remove_choice`. How do we decide what part of the frontier to explore next?
-    **Breath-first search**, aka **Shortest-first search**.
	-	Guaranteed to find path with fewest steps.
-    Tree searches don't notice that they're back tracking.
    -    All paths are valid, even if we've gone over them before.
    -    Tree search superimposes a tree on top of the state space.
    -    You may encounter previously encountered states, but tree of actions expands outwards.
    -    Frontier is always the leaves of the tree.
    -    Once you backtrack you remember, because you've already encountered it, so don't need to continue exploring.
    
-    How to avoid backtracking: **GraphSearch**.

        function GraphSearch(problem):
            frontier = { [initial] }
            explored = {}
            loop:
                if frontier is empty: return FAIL
                path = remove_choice(frontier)
                s = path.end
                add s to explored
                if s is a goal: return path
                
                for a in actions:
                    if Result(s, a) not in frontier + explored:
                        add [path + a -> Result(s,a)] to frontier
                        
-    When `s is a goal` TreeSearch and GraphSearch doesn't terminate, because it might not be the best path.
-    BFS will find shortest path in terms of steps, not cost of path.

-    **Uniform-cost search**, aka **Cheapest-first search**.
	-	Guaranteed to find cheapest path, where edges have costs.
	-	If there are two paths to the same node we drop the more expensive one.
		-	!!AI what if they're the same cost? Probably don't drop.

-	**Depth-first search**, aka opposite of breadth-first search.
	-	Always expand the longest path first.

## 2.19: Search Comparison

### Optimal

-	Which search is **optimal**, i.e. guaranteed to find the shortest path?
-	BFS is optimal for a balanced binary tree.
	-	It will always expand level-by-level.
	-	Guaranteed to encounter shortest path first.
-	UCS is optimal for a balanced binary tree.
	-	Assume all individual step costs are non-negative.
	-	Guaranteed to encounter cheapest path.
-	DFS is not optimal for a balanced binary tree.
	-	As it expands longest-path first it may encounter a goal which is longer than the shortest path.

-	So why use DFS it if it isn't optimal?
	-	Consider a very large, or infinite, state space.
	-	Assume at level `n`. How many nodes are in the frontier, i.e. what are we tracking?
	-	BFS will have 2^n nodes.
	-	UCS will have ~2^n nodes.
	-	DFS will have n nodes. Cheap!
	-	This assumes we're not keeping track of the explored space. If we are, don't have this saving.

### Completeness

-	**Completeness**: if there is a solution in an infinite state space will the algorithm find it?
-	BFS is complete.
	-	Even if infinite state space we'll find it.
-	UCS is complete.
	-	Only complete if:
		-	Each action has a non-zero cost separate from the path cost.
		-	No node has an infinite number of successors.
	-	Imagine a path with costs sum: 1 + 1/2 + 1/4 + 1/8 + 1/16 + ...
		-	This sums to 2. (1 / 1 - 0.5)
		-	If there is another path which is the shortest path of cost > 2 UCS is incomplete.
		-	There must be some non-zero action cost to prevent an infinite geometric cost path affecting us.
-	DFS is not complete.
	-	An infinite path that DFS follows will always be followed, because it follows the longest path.

## 2.22: More on Uniform Cost.

-	Looks like a contour map.
-	On average explore half the space before we encounter a goal.
-	We explore outwards, with no particular direction.
-	If we want to explore faster we need to add knowledge.
-	Can add an *estimate of the distance between the start state and the goal*.

-	**Greedy best-first search** (GBFS)
	-	Expand first the frontier node that is closest to the goal, i.e. the smallest estimate.
	-	Rather than circular contours for UCS, looks like elliptical contours.
	-	Still a risk that, if there's an obstacle, it will consider overly long paths.
	-	Ideally we want GBFS and when we encounter an obstacle we want UCS.

## 2.23: A\* Search

-    Always expand path with minimum `f`:

        f = g + h
        
        g(path) = path cost
        
        h(path) = h(state) = estimated distance to goal
        
-    Minimizing `g` keeps path short.
-    Minimizing `h` keeps focus on goal.
-    A\* aka *best estimated total path cost first*.
-    Applying to our Romania map example, define `h` as straight line distance to goal.

-    A\* finds the lowest cost path if

        h(s) < true cost
        
-    i.e. `h` must never overestimate
-    i.e. `h` is **optimistic**.
-    i.e. `h` is admissable.
-    Why does optimistic h find lowest-cost path?
    -    At goal with path p of cost c is actual cost, because h is 0.
    -    When at goal all other paths on frontier are more expensive, because we explore to minimize f.
    -    h is optimistic, so estimated cost is less than true cost for all frontier paths.
    -    Hence path p must have smaller cost than the true cost of all other paths on frontier.
    -    Because step cost is 0 or more then path p is also smaller than paths beyond frontier.
-    General intuition holds for graph search too.

## 2.30: State Spaces

-    Robot vacuum cleaner.
-    Two positions, that may or may not have dirt in it.
-    8 states.
    -    2 dirt states in place A
    -    2 dirt states in place B
    -    2 robot positions

-    Robot power switch is on, off, or sleep.
-    Robot has camera which can be on or off.
-    Robot has brush with five height levels.
-    Now 10 positions.
-    10 positions x 3 powers x 2 camera x 5 brushes x 2^10 dirt states = 307200 states.
-    All variables independent, cross product.

-    Draw out a giant FSM, full of all states and actions.
-    Could possibly say "Given this state what is the most efficient way to clean up the environment?"
    -    Literally a shortest path problem through the giant FSM from a start state to an end state.

## 2.34: Sliding Blocks Puzzle

-    4 by 4 grid of number, one number empty, sliding around into order.
-    What heuristic to use?
-    h_1 = number of misplaced blocks.
-    h_2 = sum(distances of blocks)
    -    distance = shortest number of moves a block would have to move in order to get into place.
-    Both are admissble heuristics; both are optimistic.
-    Both notice that h_2 is always >= h_1
    -    Hence A\* using h_2 always expands fewer paths than h_1, with the exception of breaking ties.

-    But surely providing a heuristic function is the hard part. Not a very intelligent agent if we need to give it intelligence.
-    Can we derive a good heuristic from a problem description?
-    **Generating a relaxed problem**.
    -    Imagine a giant FSM state space.
    -    We're adding new connections between states that were previously invalid. Only makes the problem easier.
-    What is the problem?
    -    A block can move A -> B if (A adjacent to B) and (B is blank).
    -    If we remove the second condition…
    -    A block can move A -> B if (A adjacent to B)
        -    This is h_2.
    -    If we remove the first condition…
    -    A block can move A -> B if (B is blank).
        -    This is h_1.
-    Hence, can generate candidate heuristics.
-    Additional heuristics comes from maximum of combinations:

        h = max(h_1, h_2)
        
-    The combination is still optimistic, and we want to maximize the value of heuristics to minimize A\* paths.
    -    There is a computational cost to calculating this combination heuristic.
    
## 2.37: Problems with Search

-    Problem solving works when
    -    Domain must be *fully observable*.
    -    Domain must be *known*. Must know set of available actions.
    -    Domain must be *discrete*, finite set of actions.
    -    Domain must be *deterministic*, must know the results of our actions.
    -    Domain must be *static*, nothing else can change the world except our actions.
    
## 2.38: A Note on Implementation

-    class Node
    -    state: state at end of path.
    -    action: action it took to get there.
    -    cost: total cost.
    -    parent: pointer to another node.
-    Linked list of Nodes representing a path.
-    Frontier and explored lists both have Nodes.
-    Frontier:
    -    Removing best item, in some measure.
    -    Adding in new ones.
        -    Suggests need a priority queue.
    -    But also need membership test, i.e. is item already in Frontier.
        -    Suggests need a set.
    -    Most efficient implementations have both a priority queue and a set.
-    Explored
    -    Add new members, check for membership.
    -    Represent as a single set; hash table or tree.
    
## Problem 1.1: Peg Solitaire

-    Fully observable.
-    Deterministic.
-    Discrete.
-    Benign (not adversarial).

## Problem 1.2: Loaded Coin

-    Partially observable.
    -    Because it is useful to have memory.    
-    Stochastic.
    -    You're flipping a coin.
-    Discrete.
-    Benign.

## Problem 1.3: Maze

-    Fully observable.
-    Deterministic.
-    Discrete, finite number of paths.
-    Benign.

## 3. Probability in AI

### 3.1: Introduction

-    **Bayes network**, aka influences network.
    -    Directed graph.
    -    Nodes are typically referred to as **random variables**, i.e. events.
    -    Child of parent is influenced in a non-deterministic way.
    -    All leading towards one node, which is a root event.
    -    Helps identify hidden causes.
-    Even if assume events are binary (i.e. **discrete**, 2^(events) different configurations.
-    Can test hypotheses.
    -    If oil light on (root event), what is the probability that the battery is old?
-    Uses:
    -    Diagnostics
    -    Prediction
    -    Machine learning.
    -    Building blocks to more advanced techniques:
        -    Particle filters
        -    HMM
        -    MDPs and POMDPs
        -    Kalman filters

### 3.7: Probability Summary

-    **Complements**

        P(A) = p, => P(!A) = 1 - p
        
-    **Independence**: If A and B are independent events then

        P(A and B) = P(A) * P(B).

-    **Dependence**
    -    Assume P(X_1 = H) = 0.5
    -    If X_1 is H then we choose one coin, such that:
    
            P(X_2 = H | X_1 = H) = 0.9
            
    -    If X_1 is T then we choose a completely different coin, such that:
    
            P(X_2 = T | X_1 = T) = 0.8
            
    -    What is P(X_2 = H), i.e. the probability of getting H in both cases?
    
            P(X_2 = H) = P(X_2 = H | X_1 = H) * P(X_1 = H) + P(X_2 = H | X_1 = T) * P (X_1 = T)
            = 0.9 * 0.5 + (1 - 0.8) * 0.5
            = 0.55

-    **Total probability**
    
        P(Y) = sum_i P(Y | X=i) * P(X=i)
            
-    **Negation of probabilities**:
            
        P(!X | Y) = 1 - P(X | Y)
            
    -    but *this is not true*:
    
            P(X | !Y) != 1 - P(X | Y)
            
### 3.17: Bayes Rule

-    **Posterior**: P(A|B)
-    **Likelihood**: P(B|A)
-    **Prior**: P(A)
-    **Marginal likelihood**: P(B)

        Posterior = Likelihood * Prior / Marginal Likelihood
        
        P(A|B) = P(B|A) * P(A) / P(B)

-    Posterior sounds like "probability of cause given evidence".
    -    e.g probability of cancer given positive test result.

-    Marginal likelihood is often determined using **total probability**:

        P(B) = sum_a P(B|A=a) * P(A=a)
        
### 3.18: Bayes Network

-    Directed graph. Nodes: A and B.
-    A is not observable (state of having cancer).
-    B is observable (positive test result).
-    Edge from A to B.
-    **Diagnostic reasoning**. Inverse of causal reasoning.
-    The graph above has three parameters:
    -    `P(B | A)`
    -    `P(B | !A)`
    -    `P( A )`

### 3.19: Computing Bayes Rule

        P(A|B) = eta * P'(A|B)
        
        eta = ( P'(A|B) + P'(!A|B) )^(-1)
        
        where
        
        P'(A|B) = P(B|A) * P(A)
        
-    Use this to defer the calcuation of P(B), which is difficult.
-    Why do we do this?
    -    e.g. 2-test cancer example. Run the same test twice.
    
### 3.22: Conditional Independence

-    **Conditional independence**: Given we know a hidden event's state the probability of two observable events are independent of one another.

        P(T_2 | C T_1) = P(T_2 | C)
        
-    This pops out of the Bayes network diagram.
    -    C -> T_1, and C -> T_2.
    -    No causal connection between T_1 and T_2.
    
-    Does this imply that T_1 and T_2 are independent, without knowing anything about C?
    -    *No*. e.g. T_1 giving positive result implies C is a bit more likely, which makes T_2 more likely.
    
### 3.23: Conditional Independence 2

    P(+_2 | +_1) =
    
    P(+_2 | +_1 C) * P(C | +_1) + P(+_2 | +_1 !C) * P(!C | +_1) =
    
Note that:

    P(+_2 | +_1 C) = P(+_2 | C)
        
The test result `+_1` gives us no information about the test result `+_2`, so we can drop it.

    P(+_2 | C) * P(C | +_1) + P(+_2 | !C) * P(!C | +_1)
    
### 3.24: Absolute and Conditional

-    A absolutely independent of B: Two nodes, no edges.
-    A independent of B given C: Three nodes, C -> A, C -> B.

-    We just saw that conditional independence does not imply absolute independence.
-    Also, absolute independence doesn't imply conditional independence.

### 3.25: Confounding Cause

-    Already seen single hidden cause affecting two observational events.
-    Now, two hidden causes **counfounding** a single observational event.
-    e.g. happiness affected by sunniness and getting a raise.
-    Hence, probability of one confounding cause occurring given another is simply the probability of the first. They are absolutely independent.
-    They are not conditionally independent; the single observational element adds information, and links the previously independent hidden causes.

### 3.27: Explaining Away

-    If we know an observation, then a cause can explain the cause of the observation away.
-    If we know one confounding cause, the probability of other confounding causes are decreased; they can be explained away.0.97*0.01
-    Corollary: given an observation event any confounding event which is known not to occur increases the probability of other confounding events occurring.
-    3.27 and 3.28 are excellent videos showing the calculations behind this.

### 3.30: Conditional Dependence

-    A -> C, B -> C.
-    A and B are absolutely independent.
-    However, given information about C, A and B are no longer independent.
-    Additional information explains away the causes.

### 3.31: General Bayes Net

-    **Bayes networks** define probability distributions over graphs of random variables.
-    e.g. A -> C, B -> C, C -> D, C -> E.
-    Don't need to enumerate 2^5 - 1 = 31 probability distributions. This network is characterised by:

        P(A)
        P(B)
        P(C | A,B)
        P(D | C)
        P(E | C)
        
        P(A, B, C, D, E) = P(A) . P(B) . P(C | A,B) . P(D | C) . P(E | C)
        
-    The above only need 10 values, not 31.

        P(A) is 1.
        P(B) is 1.
        P(C | A,B) is 4.
        P(D | C) is 2.
        P(E | C) is 2.

-    Bayes networks scale much better than the combinatorial approach.
-    Any node with `k` incident edges requires `2^k` variables to specify it.

### 3.35: D Separation

-    Any two variables are independent if their respective nodes are not linked by just unknown variables, i.e.
    -    Follow *directed* version of graph. If any variables are known in path then independent.
-    Don't forget about confounding variables! Known variables link these together. The *explain away effect*.

-    **D-Separation**, aka **Reachability**.
-    Simple chain.
    -    Given A -> B, B -> C.
    -    A is dependent with C.
    -    But if B is known, A is independent of C.
-    One hidden, two observations.
    -    Given A -> B, A -> C.
    -    B is dependent with C.
    -    But if A is known, B is independent of C.
-    Two hidden, one observation.
    -    Given A -> C, B -> C.
    -    If C is known, A and B are dependent.
    -    But if C is unknown, A and B are independent.
-    Known successor.
    -    Given A -> C, B -> C, C -> … -> Z.
    -    If Z is known, get information about C, hence A and B are dependent.
    -    Only counts if Z is in a chain of direct successors.
    
-    **Active triplets** vs. **inactive triplets**.

## Unit 4: Probabilistic Inference

### 4.1: Overview and example

-    Just went over:
    -    Probability theory
    -    Bayes Nets, represents a joint probability distribution, include random variables. dependence and dependence.
-    Now, will cover **inference**: how to answer probability questions using bayes nets.

-    Example
    -    Burglary (B) -> Alarm (A)
    -    Earthquake (E) -> A
    -    A -> John (J)
    -    A -> Mary (M).
-    What questions can be asked?

-    **Given some inputs, what are the outputs?**
-    Given B and E, what are J and M?
-    B and E are **evidence** variables.
-    J and M are **query** variables.
-    A is a **hidden** variable.
-    This question is also known as the **posterior distribution given the evidence**.

        P(Q_1, Q_2, … | E_1 = e_1, E_2 = e_2)

-    Another question: **what is the most likely explanation?**

        argmax_q P(Q_1 = q_1, Q_2 = q_2, … | E_1 = e_1, …)

-    Out of all the possible combinations of query variable values, which combination has the highest probability?

-    Unlike regular programming functions, Bayes nets are bidirectional.
-    Right now we're going in the causal direction.
-    Could go inverse, and make J and M be the evidence and B and E be the evidence.
-    Or in any other combination.

### 4.2: Enumeration

-    **Enumeration**: go through all possibilities, add them up.

        P(+b | +j, +m)
        
-    i.e. what is the probability that there is a burglary given that John called and Mary called.
-    Note that `P(+b)` is `P(b=True)`, etc. 
-    In these notes can't draw negation operator, so put `P(!b)`.

        Conditional probability
        P(Q|E) = P(Q,E) / P(E)
        
        = P(+b, +j, +m) / P(+j, +m)

-    Looking at numerator. We want to enumerate over the hidden variables, in this case `A` and `E`.

        P(+b, +j, +m)
        = sum_e sum_a P(+b, +j, +m, e, a)

-    Now going to re-write this in terms of the parents of the nodes in the network:

        = sum_e sum_a P(+b) P(e) P(a|+b,e) P(+j|a) P(+m|a)
        = sum_e sum_a f(e,a)
        
-    (Recall D-Separation, and how nodes are determined by their parents).
-    Now we enumerate over all values of `e` and `a`. Recall they are binary random variables.

        = f(+e,+a) + f(+e,!a) + f(!e,+a) + f(!e,!a)
        
-    Each `f(e,a)` is the product of 5 numbers. We will do this 4 times.

### 4.3: Speeding Up Enumeration

-    Theoretically we're done, have tools to do inference.
-    But with complex bayes nets this gets tricky.
-    **Pulling out terms**

        sum_e sum_a P(+b) P(e) P(a|+b,e) P(+j|a) P(+m,a)
        
-    `P(+b)` doesn't vary with `e` or `a`:

        P(+b) sum_e sum_a P(e) P(a|+b,e) P(+j|a) P(+m|a)
        
-    `P(e)` doesn't vary with `a`:

        P(+b) sum_e P(e) sum_a P(a|+b,e) P(+j|a) P(+m|a)
        
-    This reduces inner loop cost.

-    **Maximize independence** of variables.
-    For a linear network, X_1 -> … -> X_n, inference cost is O(n).
-    A complete network (every node points to every other node), cost is O(2^n).
-    Dependence does not imply anything about causality, it just results on "if one is present or not present does that provide information about the other?"
-    By reasoning about dependence, we take our original graph above and add these edges:
    -    J -> M. Because knowing if J did or didn't call gives information about A, and hence M.
    -    B -> E. Because knowing if B occurred gives information about A, and hence E. Explain away effect.
-    Bayes nets are at their most compact when written in the **causal direction**.
    -    When network flows from causes to effects.

### 4.8: Variable Elimination

-    **Variable elimination**
-    Consider nodes:
    -    R: is it raining.
    -    T: are there problems with traffic.
    -    L: will I be late for appointment.
    -    R -> T -> L.
    -    Get their conditional probability tables: `P(R)`, `P(T|R)`, `P(L|T)`.
-    We already know how to enumerate, which works for this simple cause but not for complex ones:

        P(+l) = sum_r sum_t P(r) P(t|r) P(+l|t)
        
-    1st operation: **Joining factors**
-    Choose two factors, `P(R)` and `P(T|R)`.
-    Join them as `P(R,T)`.
    -    e.g. first row of `P(R)` is `+r = 0.1`.
    -    first row of `P(T|R)` is `+r,+t = 0.8`.
    -    first row of `P(R,T)` is `+r`, `+t`.
    -    we know that first row of `P(R,T)`is `P(+t|+r)*P(+r)` = `0.08`.
-    Now, the network is RT -> L. Joined factors.

-    2nd operation: variable elimination, aka **marginalisation**, aka **summing out**.
-    We have tables for `P(R,T)` and `P(L|T)`.
-    We can get a table `P(T)`.
-    We can sum out `R` in first table, leaving us a table `P(T)` with rows `+t` and `!t`.
    -    Add together probabilities to determine this.
-    Now have a new network T -> L.
-    Now want to join on `P(T)` and `P(L|T)`, to give one table `P(T,L)`.

-    Final step, want to sum out to give `P(L)`.

### 4.12: Approximate Inference

-    by means of **sampling**.
-    e.g. want to determine joint distribution of two coins coming up heads / tails.
-    Flip them, put into 4-row table.
-    Then estimate the joint distribution.
-    Advantage:
    -    Simpler to compute than exact inference.
    -    Can be used in cases where precise joint probabilities are not available.
    
-   Can sample a bayes net with defined conditional probabilities.
    -    Just use a random number generator to pick values for evidence variables.
    -    Then can model the probability of the query variables, without needing to do any calculations.
-    This sampling method is **consistent**.

### 4.15: Rejecting Sampling

-    But what if we wanted to use this to calculate a conditional probability, e.g. `P(W|-C)`?
-    **Rejection sampling**: generate samples and reject those that don't fit our conditional requirement.
-    However, if probabilities are low then we'll reject most the samples.
-    e.g. B -> A. What is `P(B|+a)`?
-    B, burglary, is very rare, hences `+a` is rare, so rejection sampling rejects most.

### 4.16: Likelihood Weighting

-    **Likelihood weighting**: fix the evidence variables.
-    But just fixing the evidences variables is **inconsistent**. Need to add a **probabilistic weight** to each sample.
-    Going back to cloudy / rain example.
-    For each choice we're forced to make multiply-in the respective probability from the probability table to the weight.
-    Likelihood weighting is consistent, because we weight samples.
-    Still has a problem. If we choose a question such that a variables chooses others to pick low probabilities they'll have very small weights. Not rejecting them but they're unlikely.

### 4.19: Gibbs Sampling

-    **Markov Chain Monte Carlo**, i.e. **MCMC**.
-    Assign random values, get one sample.
-    At iteration through the loop, select one non-evidence variable and resample it based on all the other variables.

        +c +s -r -w
        
        Choose s.
        
        +c -s -r -w
        
        Choose r.
        
        +c -s +r -w
        
-    In rejection and likelihood weighting sampling each sample was independent of the others.
-    In MCMC samples are not independent.
-    Adjacent samples are very similar!
-    This technique is still **consistent**.

### 4.20: Monty Hall Problem

-    Three node Bayes net.
    -    Prize (P). 3 options: D1, D2, D3.
    -    First selection (F): 3 options: D1, D2, D3.
    -    Monty opens (M): 3 options: D1, D2, D3.
    -    P -> M.
    -    F -> M.
-    P and F are absolutely independent.
-    However, if we know M, P and F become dependent.
-    This is basic D Separation - we already know P and F are dependent!
-    There are no hidden variables.
-    Just work through the problem, drawing four tables:
    -    `P(P)`. (all 1/3)
    -    `P(F)`. (all 1/3)
    -    `P(M|F)`.
    -    `P(M|P)`.
-    `P(P=D1 | F=D1, M=D3)` is `a`.
-    `P(P=D2 | F=D1, M=D3)` is `b`.
-    Should we switch (`b > a`) or stay (`a <= b`)?
-    Recall that `P(Q|M) = P(Q,M) / P(M)`.
-    Key point is here:

        P(M=D3, P=D2, F=D1) = 1 (!!)
        
-    If we choose D1, and the prize is behind D2, Monty *must pick* D3.
-    Above implies `b = 2/3`.

## Unit 5: Machine Learning

### 5.1: What is Machine Learning?

-    We've talked about Bayes networks, where topology is known.
-    **Machine learning**: learn models from data.
-    We're going to go through **supervised learning** in this unit.

### 5.2: Taxonomy

-    What?
    -    **Parameters**: probabilities of Bayes net.
    -    **Structure**: edges of Bayes Net.
    -    **Hidden concepts**.
        -    e.g. types of customer.
-    What from?
    -    Always some sort of target data.        
    -    **Supervised** learning, target labels are present.
    -    **Unsuperivsed** learning, target labels are missing and we use methods to determine hidden concepts.
    -    **Reinforcement** learning. Interact with environment, process feedback.
-    What for?
    -    **Prediction**: future.
    -    **Diagnostics**: explain events.
    -    **Summarisation**: shorten articles.
-    How?
    -    **Passive**: agent has no impact on data itself.
    -    **Active**: agent has impact on data.
    -    **Online**: while data is being generated.
    -    **Offline**: data is already present.
-    Outputs?
    -    **Classification**: outputs are discrete number of classes. e.g. chair or not chair.
    -    **Regression**: continuous, e.g. 66C.
-    Details?
    -    **Generative**: model the data as generally as possible.
    -    **Discriminative**: distinguish data, particulars.
-    This is a very complex list!
-    Won't learn them all, but at least can identify machine learning methods.

### 5.5: Supervised learning

-    **Feature vector**: x_1, x_2, …, x_n
-    **Target label**: y

        x_1, x_2, …, x_n -> y
        
-    e.g. for credit agency:

        x_1: what is their income?
        x_2: have they ever defaulted on credit card
        …
        y: will the person default on their credt?
        
-    e.g. credit agency will take *previous data* of x_n and y and then wish to *predict* for future customers.
-    Imagine a massive matrix, for all y_n. This is **data**.
-    With a certain amount of error, want a function:

        f(x_m) = y_m
        
-    Then use f(x_k) for future data to get y_k that wasn't encountered before.

### 5.6: Occam's Razor

-    *Everything else being equal, choose the less complex hypothesis*.
-    Tradeoff between data fit and low complexity.
-    Chart.
    -    More complexity => asymptotic lower **training data error**.
    -    More complexity => initially lower then much higher **generalisation error**.
    -    More complexity => every increasing **overfitting error**.
-    There is a sweet spot of complexiy, which is the minima of the generalisation error.
-    Can try to measure overfitting error using **Bayes variance methods**.
-    In practice you know the training data error, and you should push back and accept increasing amounts of training data error in order to reduce complexiy.

### 5.7: Spam detection

-    Email -> f(x) -> [Spam, Ham]
-    Supervised learning, use user input.
-    How to represent emails?
-    **Bag of words**: count frequencies of words, in lookup data structure.
    -    Compare to a fixed list of words in a dictionary.
    
### 5.9: Maximum Likelihood

-    **Maximum likelihood**: what is the probability of a query that maximizes the likelihood of the data?
    -    Infer probabilities from data.
    -    Assumes data instances are independent.
-    Going through email example.
    
        Emails:
        
        SSSHHHHH
        
        p(S) = pi
        
        P(y_i) = pi if y_i = S
                = 1 - pi if y_i = H
                
        Imagining Spam and Ham as 1's and 0's:
        
        11100000
        
        p(y_i) = pi^(y_i) * (1 - pi)^(1 - y_i)
            
        Assuming independence:
        
        p(data) = product (i = 1 to N) p(y_i)
                = pi^(count(y_i=1)) * (1-pi)^(count(y_i=0))
                = pi^3 * (1-pi)^5
                
-    What is the `pi` that maximizes this expression?
-    Can also maximize the log of this expression because log is monotonic with respect to p.

        log p(data) = 3*log(pi) + 5*log(1-pi)
   
-    Maximum is where derivative is 0.

        d/dp p(data) = 0 = 3/pi = 5/(1-pi)
        3/pi = 5/(1-pi)
        3(1-pi) = 5pi
        
        pi = 3/8  
        
-    We've derived that the data likelihood maximizing number for the probability is indeed the empircal count.
-    Derivation is not important for class.

### 5.10: Relationship to Bayes Network

-    We're building up a Bayes Network, where the *parameters* of the Bayes Network are *estimated* using *supervised learning* by a *maximum likelihood estimator* based on *training data*.
-    For spam detection, root node is "spam".
-    Directed edges to children.
-    One child node for each word in a message.
-    Each word has a probability, `P(word|spam)`.
-    Given spam and 12 words, how many parameters?
    -    23.
    -    One for the prior, P(spam).
    -    P(w_i|SPAM), 11 of these.
        -    The 12th can be figured out as `1 - the rest`.
    -    P(w_i|HAM), 11 of these.
        -    The 12th can be figured out as `1 - the rest`.
-    In example, P(spam|M), where M is message "sports"

        P(spam|M)
        = P(M|spam) * P(spam) / (P(M|spam)*P(spam) + P(M|ham)*P(ham))
        
-    In next example, can do the same with an email with three words by treating each word as independent, hence product.
-    In a surprising twist if you encounter a word that has never been encountered as spam before then the email cannot ever be spam.
    -    It can't be that a single word determines this!
    -    This is **overfitting**.

### 5.14: Laplace smoothing

-    **Laplace smoothing** to deal with overfitting.
-    In Maximum-Likelihood (ML):

        ML: p(x) = count(x) / N
        
-    e.g. in 8 messages, 3 of which are spam, the prior for spam:

        p(spam) = count(spam) / 8 = 3 / 8

-    In Laplace Smoothing:

        LS(k): p(x) = (count(x) + k) / (N + k * |x|)
        
-    Add `k` to each observation count. **Smoothing parameter**.
    -    `k = 0` is Maximum-Likelihood estimator.
-    `N`: total number of occurrences, e.g.  spam + ham.
-    `|x|` is the number of values that variable `x` can take on. Think of it as degrees of freedom.
    -    In this case either spam or ham, so `|x| = 2`.

-    In the case of the bag of words model of spam detection, how to do:

        P("today" | SPAM)
        ML version = 0 / 9
        LS version = (0 + 1) / (9 + 12)
        
-    The degrees of freedom for the random variable spread over all classes, i.e. both ham and spam, and is the number of classes of words.
-    Don't forget in bag of words model the words are independent, so multiword messages can have word-probabilities multiplied together. 
    -    In LS the probabilities get the k on top and `|x|` on bottom.
    
### 5.17: Summary of Naive Bayes

-    Input: features of documents, training data. `x_1 … x_n`.
-    Output: label, spam or not spam. `y`.
-    We made a *generative model* for the spam class and non spam class, that described the c*onditional probability of each individual feature*.
    -    Root node: `y`, the label.
    -    Directed edges to child nodes, the features.
    -    Each edge has two parameters: `P(x_n|+y)` and `P(x_n|-y)`.
-    Then used *maximimum likelihood* and a *Laplacian smoother* to determine the edge parameters.
-    Then used *Bayes rule* to take any particular, new training examples and determine the probability of labels.
-    **Generative model**: the conditional probabilities of each feature all aim to maximize the probability of individual features as if those describe the physical world (?).
-    **Bag of words model**: representation fo each email counts occurrences of words, irrespective of order.
-    Powerful spam filtering method, but now not powerful enough.

### 5.18: Advanced spam filters

-    Known spamming IP?
-    Have you ever emailed this person before?
-    Have 1,000 other people received the same message?
-    Is email header consistent? (e.g. if `blah@hsbc.co.uk` do the headers indicate it came from `hsbc.co.uk`?)
-    Is the email in all capitals?
-    Do the inline URLs point to pages where they say they point to?
-    Are you addressed by name?

### 5.19: Digit recognition

-    Hand-written digit recognition.
-    Data set from US postal service.
-    Naive bayes.
    -    Input vector: *pixel values*.
        -    16x16 input image.
        -    Hence 256 different values that is brightness of each pixel.
        -    But this is not **shift invariant**.
        -    Transposition is mis-recognised.
    -    Input vector: *pixel values + weight of neighbours*.
        -    Still 16x16 input image.        
        -    But a given cell includes a weight of its neighbours.
        -    An attempt to recognise transposition.
        -    **Input smoothing**.
        -    **Convolve the input with a Gaussian variable**.
-    Naive bayes is not a good choice.
    -    Assumption of conditional independent of each input vector element for a target class is not true.

### 5.20: Overfitting

-    Overfitting prevention.
-    Occam's Razor: tradeoff between how well we fit the data and how smooth our method is.
    -    Laplacian smoothing one way to make our method smoother.
    -    For digit recognition using input convolution is another way to make our method smoother.
-    But what `k` do we choose for Laplacian smoothing?
-    **Cross validation**
    -    Divide training data into three *non-overlapping* buckets.
        1.    **Train** ~80%.
        2.    **Cross-validate** ~10%.
        3.    **Test** ~10%.
    -    Use 'train' to determine parameters. 
    -    Use 'cross-validate' to determine value of `k`.
        -    Train for a given `k` using 'train' data.
        -    Evaluate performance on 'cross-validate' data.
        -    Output: best `k`.
    -    Only use 'test' data once.
        -    Evaluate performance of your model.
        -    This is how you report its validity.
-    **Ten-fold smoothing**: often run cross-validation in batches of ten to find an optimal `k`.

### 5.21: Classification vs. Regression

-    We've been doing classification.
    -    Target labels are discrete, in our case binary.
-    Often we need continuous labels.
-    **Regression**.
    -    e.g. line of best fit.
    
### 5.22: Linear Regression

-    Data:

        x_11 x_12 … x_1n -> y_1
        …
        x_m1 x_m2 … x_mn -> y_m
        
        Want:
        
        y = f(x)
        
-    In linear regression for single-variant x:

        f(x) = w_1 * x + w_0
        
-    Where x is a vector, `w` and `w_0` are also vectors:

        f(x) = w . x + w_0
        
        # w.x is inner product!
        
### 5.23: More Linear Regression

-    **Loss function**: what we're trying to minimize.
    -    Defined as the **residual error** after fitting our regression equation.
    
            Loss = sum_j (y_j - (w_1 * x_j + w_0))^2
            
-    Quadratic error between our *target labels in reality* and *what our best hypothesis can produce*.
-    Solution to regression problem `w^*`:

        w_1^* = argmin_w Loss
        
-    Argmin of `Loss` over all possible vectors `w`.
-    Over all possible `w` what minimizes `Loss`?

### 5.24: Quadratic Loss

        min_w sum(y_i - (w_1 * x_i + w_0))^2

-    Where is derivative 0? Do partial derivative over `w_0`.

        dL/dw_0 = -2 * sum(y_i - (w_1 * x_i + w_0)) = 0
               => sum(y_i) - w_1 * sum(x_i) = M * w_0
               
        # M is number of training samples
        
               => w_0 = 1/M * sum(y_i) - (w_1/M) * sum(x_i)
              
        # But we don't know w_1, so do this again:
        
        dL/dw_1 = -2 * (sum(y_i - (w_1 * x_i + w_0)) * x_i = 0
               =>  sum_i(x_i * y_i) - w_0 * sum(x_i) = w_1 * sum(x_i^2)
               
        # Plug in w_0
        
        sum(x_i * y_i) - (1/M) * sum(y_i) * sum(x_i) = (w_1/M)*(sum(x_i))^2
        
-    Finally:

        w_1 = M * sum(x_i * y_i) - sum(x_i) * sum(y_i)
              ----------------------------------------
              M * sum(x_i^2) - (sum(x_i))^2
              
-    Noting, from before: 
        
        w_0 = 1/M * sum(y_i) - (w_1/M) * sum(x_i)

### 5.25: Problems with Linear Regression

-    Can't capture nonlinear behaviour.
-    Bad for predicting outliers.
-    Bad for data with concentrated x values of large variences in y values. 
-    No plausible way of predicting data outside of the training data; does the linear behaviour continue?
    -    **Logistic regression** addresses this.
    -    Let `f(x)` be the linear function.
    -    Logistic function is:
    
            z = 1
                -------------
                1 + e^(-f(x))

### 5.26: Linear Regression and Complexity Control

-    **Regularization**.

        Loss = Loss(data) + Loss(parameters)
        
        where:
        
        Loss(data) = sum_j (y_j - w_i * x_j - w_0)^2
        
        and:
        
        Loss(parameters) = sum_i (w_ii |^P), where P is usually 1 or 2.
        
-    `Loss(data)` is as before.
    -    On plot of w_1 vs. w_0 sits somewhere away from origin.
-    `Loss(parameters)` might just be a function that penalizes large parameters up to some `P`, where `P` is usually 1 or 2
    -    On plot of w_1 vs. w_0 it tries to pull solution back in towards origin.
    -    If quadratic error it pulls into a circle around origin. (aka L2 regularization).
    -    For L1 regularization (?) it pulls into a diamond around origin.

###  5.27: Minimizing More Complicated Loss Functions

-    Need numerical methods to minimize complex loss functions; no closed/analytic solutions.
-    **Gradient descent**.
    -    Start with guess w_0.
    -    Update iteratively:
    
            w_i <- w_i - \alpha * gradient(L(w_i)) 
            
    -    alpha is **learning rate**, ~0.01.
    -    Won't usually find global minima, will only find local minima.
    -    Over time we need to reduce alpha in order to reach a final answer.
-    Books can cover how to use better methods than gradient descent.

-    Let's apply gradient descent to linear regression, even though we already have a closed/analytic solution:

        dL/dw_1 = -2 * sum_j (y_j - (w_1 * x_j + w_0)) * x_j
        
        dL/dw_0 = -2 * sum_j (y_j - (w_1 * x_j + w_0))
        
-    So start with (w_1)^0 and (w_0)^0, initial guesses.
-    Use iterative method for each of `w_1` and `w_0`:

        w_i <- w_i - \alpha * gradient(L(w_i)) 
        
### 5.32: Perceptron

-    **Perceptron algorithm**.
-    Suppose we have data of positive sample and negative samples.
-    A **linear separator** is a linear equation that separates positive from negative samples.
-    Not all data have a linear separation, but if it does a perceptron will always converge and find it.

        f(x) = 1 if w_1 * x + w_0 >= 0
             = 0 if w_1 * x + w_0 < 0
             
-    **Perceptron update**, an *online* algorithm
    -    Start with random guess for w_1 and w_0.
    
            (w_i)^m <- (w_i)^(m-1) + \alpha * (y_j - f(x_j))
            
            Error := y_j - f(x_j)
            \alpha := learning rate, small
            
    -    If error is 0 then no update occurs.
    -    Perceptron converges if a linear separation exists.
    
-    Given many possible separators, which one do you prefer?
    -    The separator that has largest minimum distance from actual samples.
    -    Samples are actually noisy.
    -    Want to maximize the **margin** := distance from separator to the closest training example.
    
-    **Maximum margin algorithms**
    -    **Support vector machines**.
    -    **Boosting**
    
### 5.33: Support Vector Machines.

-    Won't cover in detail in this class.
-    Derives a linear separator that maximizes the margin.
-    Use linear techniques to solve non-linear problems.
    -    e.g. a circle of `+` samples surrounded by a ring of `- samples.
    -    No linear separation.
    -    **Kernel trick**: augment the feature set with new features.
    -    In our example derive a new feature.
    
            x_1 and x_2 are axes for features
            
            Now derive:
            
            x_3 = sqrt( (x_1)^2 + (x_2)^2 )
            
    -    i.e. `x_3` is the distance from the origin.
    -    `x_3` *is* linearly separatable.

-    Can take any non-linear problem and use the kernel trick and add features that subsequent linear methods better.
-    In SVMs features are added by the kernel, implicitly represented.

### 5.34: Linear Methods Summary

-    Regression vs. classification
-    Exact vs iterative solutions
-    Smoothing
-    Linear methods fro non-linear problems.

### 5.35: K Nearest Neighbours.

-    **Parametric methods**: methods that use parameters, like probabilities or weights, where number of parameters is *independent* of the training set size.
-    **Nonparametric methods**: number of parameters can grow.

-    **K-nearest neighbours**. (aka KNN)
    -    Learning: memorize all data.
    -    New input comes in and you want to classify it.
        -    Find K nearest neighbours.
        -    Return the majority class label.
-    KNN is non-parametric.        

### 5.37: K as a Smoothing Parameter

-    **Voronoi graph**: depicition of results of KNN boundary (of course, non-linear and very complex).
-    High `k` => smoother boundaries in Voronoi graph.
-    `k` is a **regulalizer**: it controls the complexity.
-    Can use *cross-validation* to determine `k`.

### 5.38: Problems of KNN

-    Very large data sets.
    -    Length searches.
    -    Want to avoid a O(n) by using a **kdd tree** to make it O(log n)
-    Very large feature spaces.
    -    Much more difficult problem.
    -    As input dimension increases the edge length to neighbours increases. All neighbours are very far away.
    -    With more dimensions need more points to be close in order to count as "near".
  
## Section 6: Unsupervised learning

### 6.1: Unsupervised learning

-    Given features, but no labels.

        x_11 x_12 ... x_1n
        x_21 x_22 ... x_2n
        ...
        x_m1 x_m2 ... x_mn

-   `m` data items
-   `n` features
-   Is there structure?
-   Are there clusters?

### 6.2: Dimensions

-   Data can have a given dimensionality.
-   However, the major variation of the data may lie along a smaller number of different dimensions.
-   *Lower dimensionality* is another kind of structure. **Dimensionality reduction**.

### 6.3: Terminology

-   Assume **IID**
    -   **Independentally drawn**.
    -   **Identically Distributed**.
-   **Density estimation**: determine underlying model parameters.
    -   **Clustering**.
    -   **Dimensionality reduction**.
-   **Blind Signal Separation**.
    -   Two people talk simultaneously.
    -   Can you recover those two speakers and filter into two separate streams?
    -   Very difficult, yet unsupervised.
    -   **Factor analysis**: each speaker is a factor in the recording.
 
### 6.4: Google Street View and Clustering

-   One of the great unanswered questions is: can you take a look at a collection of images and observe invariant features like houses, pavements, stop signs, cars, and correlate between images?
-   This class won't teach you that!
-   Clustering
    -   **k-means**: intuitive method to derive clusters.
    -   **Expectation maximization**: probabilistic generalization of k-Means, derived from first principles.

### 6.5: k-means clustering

-   Given points in space.
-   Guess points at random which are centres of clusters.
-   Assign each point to its most likely cluster point, using Euclidean distances.
-   Divide the space such that points on the boundary are equidistant from each cluster point.
    -   **Vornoi graph**.
-   For each set of points in a cluster, determine a new cluster centre that is optimal for those points.
    -   The cluster points will move, and the boundary in the Vornoi graph will move.
    -   Since the boundary moves the points are reassigned to different clusters.
-   Iterate

### 6.6: k-means algorithm

-   Initially: select k cluster centres at random.
-   Repeat:
    -   Correspond data points to nearest cluster.
    -   Update cluster centre by mean of corresponding data points.
    -   Empty cluster centres: restart at random.
    -   Until no change, convergence.
-   Algorithm is known to converge to a *locally optimal* solution.
    -   General problem is NP-hard.
    -   So locally optimal is the best we can do.

-   Problems with k-means.
    -   Need to know k.
    -   Local minimum.
    -   Can't handle high dimensionality.
    -   Lack of mathematical basis.

### 6.9: Expectation Maximization

-   Discourse: Gaussian normal distribution.
-   Bell curve.
-   Mean is 'mu'.
-   Variance is 'sigma^2'.
-   Probability density function, i.e. probability that given `x` will be drawn:

        exp(-0.5*(x - mu)^2/(sigma)^2)
        ------------------------------
        sqrt(2*pi)*sigma

-   Can use over interval range `[a,b]`.

-   **Multi-variate Gaussian**: over more than one variables.
-   Drawn from **level sets**, sets with equal probability.
-   For two variables looks like a 3D bell curve.
-   Multi-variate Gaussian probability density function:

        (2*pi)^(-N/2) * |$\Sigma$|^(-0.5) * exp(-0.5*(x-mu)^T * $\Sigma$^(-1) * (x-mu))

-   N is number of dimensions in input space.
-   $\Sigma$ is a covariance matrix that generalises the single-variate $\sigma$ variance.
-   The exponential is done using vectors and linear algebra.

### 6.10: Gaussian Learning

        f(x | mu, sigma^2) = (sqrt(2*pi*sigma^2))^(-1) * exp(-0.5*(x-mu)^2/(sigma^2))

-   Fitting data to determine mu and sigma.

        mu = 1/M * sum(j=1 to M) (x_j) # average

        sigma^2 = 1/M * sum(j=1 to M) (x_j - mu)^2 # average quadratic deviation

-   Convince yourself that this is the *maximum likelihood* estimate for the Gaussian parameters.

        Data: x_1, x_2, ..., x_m

        p(x_1, ..., x_m  | mu, sigma^2) = product(i) f(x_i | mu, sigma^2) # because variables are IID
        = (2*pi*sigma^2)^(-0.5*M) * exp(-0.5*sum(i)(x_i-mu)^2/sigma^2)

-   Note that in doing the product
    -   the left hand side gets raised to the power of M.
    -   recalling that `exp(x+y) = exp(x)*exp(y)` the products of the RHS result in a single `exp()` with a summation inside.
-   Maximum likelihood => we want to maximize this probability using mu, sigma^2.
-   Trick: we can maximize the logarithm instead, as the logarithm is a monotonic function.

        = M/2 * log(1/(2*pi*sigma^2)) - (1/2*sigma^2) * sum(i=1 to M)(x_i - mu)^2

-   Maximum is where the partial derivative is 0.

        dlogf/dmu = 1/sigma^2 * sum(i=1 to M)(x_i-mu) = 0
                0 = sum(i=1 to M)(x_i - mu)
                0 = -M*mu + sum(i=1 to M)(x_i)
             M*mu = sum(i=1 to M)(x_i)
               mu = 1/M * sum(i=1 to M)(x_i), QED.

-   Recall that:

        d/dx(log_b(x)) = 1/(x*ln(B))
        d/dx(ln(x))    = 1/x
        d/dx[ln(f(x))] = ln'(f(x)) * f'(x) = f'(x) / f(x)

-   Doing the LHS first:

        dlogf/dsigma = M/2 * (2*pi*sigma^2) * (1/2*pi) * d/dsigma(1/(sigma^2))
                     = M*sigma^2/2 * (-2*(sigma)^-3)
                     = -M/sigma 

-   Now the RHS:

        dlogf/dsigma = 1/sigma^3 * sum(i=1 to M)(x_i - mu)^2

-   Add both, set equal to 0:

        sigma^2 = 1/M * sum(i=1 to M)(x_i - mu)^2, QED.

-   For multivariate Gaussian, the maximum likelihood estimates:

        mu = 1/M * sum_i (x_i)

        Sigma = 1/M * sum(j){(x_i-mu)^T * (x_i-mu)}

### 6.15: Expection Maximization (EM) as Generlization of k-means

-   In k-means we have *hard correspondance*: each data point is attracted to one and only one cluster point.
-   In EM we have **soft correspondance**: each data point is attracted to all cluster points in proportion to the data point's posterior likelihood.
    -   This is **expectation**.
-   In the adjustment step the cluster centres are being optimized like before, but correspond to all data points.
    -   This is **maximization**.
-   In EM cluster points don't move as much as in k-means.

### 6.16: Expectation Maximization algorithm

-   Each data point is generated from a **mixture**.

        P(x) = sum(i=1 to k) p(C=i) * p(x | C=i)

        k: number of classes

-   Intuition.
    -   Each cluster point as a Gaussian variable associated with it.
    -   In generative version of EM we first draw cluster centre, `P(C=i)`, and then draw from the Gaussian associated with the cluster centre, `P(x | C=i)`.
-   Unknowns:
    -   *Prior probability for each cluster centre*: `p(C=i)`, i.e. $\pi_i$.   
    -   Gaussians: `P(x|C=i)`, i.e. $\mu_i$ for single-variate and $\Sigma_i$ for multi-variate.
    -   i = 1 ... k.

-   Steps
-   **E-Step**
    -   Assume we know $\pi_i$, $\mu_i$, $\Sigma_i$.

            e_ij = $\pi_i$ * normalizer * Gaussian expr.

            normalizer = (2*pi)^(-M/2) * |$\Sigma$|^(-1)

            Gaussian = exp(-0.5*(i_j-mu_i)^T * $\Sigma$^(-1) * (x_j-mu_i)

    -   e_ij is the probability that the j-th data point corresponds to the i-th cluster centre.

-   **M-Step**
        
        $\pi_i$ <- sum_j(e_ij) / M

        M: total number of data points

        $\mu_i$ <- sum_j(e_ij * x_j) / sum_j(e_ij)

        $\Sigma_i$ <- sum_j(e_ij * (x_j - mu_i)^T * (x_j - mu_i)) / sum_j(e_ij)

-   EM calculates the best Gaussian over all data points given a cluster centre.
    -   If points are in a straight line and cluster point is on this line $\Sigma$ is elliptical, not circular.

-   EM converges at a slower rate than k-means.
    -   All points have soft correspondence in EM.

### 6.19: Choosing k

-   Number of clusters, k?
-   At random, for data points that seem unexplained add a new random cluster point near them and see if the fit gets better.
-   Minimize this expression:

        -sum_j(log( p(x_j | sigma_1 Sigma_1 k))) + cost * k

-   LHS: EM already minimizes this.
    -   `p(x_i | ...)` is posterior probability of data
    -   `log(...)` is a monotonic function.
    -   negate it so it becomes a minimization problem.
-   RHS: constant cost per new cluster.
-   Typically balances out to good k.

-   Method
    -   Guess initial k
    -   Run EM
    -   Remove unnecessary clusters.
    -   Create new random clusters.
    -   Go back to "run EM".

-   This algorithm also overcomes local minima.
    -   Removes redundant clusters.
    -   Restarts by putting removed clustered somewhere else at random.
    -   Hence get a better solution.

### 6.20: Clustering summary

-   k-means, EM
    -   find cluster centres.
    -   EM is probabilistically sound, can prove convergence in a log-likelihood space.
    -   k-means also converges.
    -   Both are prone to local minima; need to know number of clusters k.
        -   Trick explained before for EM overcomes needing to know k, and local minima to some extent.

### 6.23: Linear Dimensionality Reduction

-   Find a linear subspace onto which to project the data.
    -   Non-linear is cutting-edge research.
-   Algorithm is very simple.
    1.  Fit Gaussian
        -   Will look elliptical around the dimension(s).
    2.  Calculate eigenvalues and eigenvectors.
        -   One eigenvector per linear dimension in subspace.
    3.  Pick eigenvectors with maximum eigenvalues.
    4.  Project data onto your chosen eigenvectors.

-   Intuition.

        x = [[0, 1.9],
             [1, 3.1],
             [2, 4],
             [3, 5.1],
             [4, 5.9]]

        mu = [[2, 4]]

        Sigma = [[2, 2],
                 [2, 2.008]]

        eigenvectors -> eigenvalues of Sigma, the covariance matrix:

            [[0.7064, 0.7078]] -> 4.004
            [[-0.7078, 0.7064]] -> 0.004

        Hence the first eigenvector dominates, and it is centred around the mean.

-   Used in face recognition. "Eigenfaces".

### 6.26: Piece Wise Linear Projection

-   Non-linear projection.
-   Project onto a set of disjoint lines, rather than one single line.
-   Two common methods
    -   **Local linear embedding**
    -   **ISO Map**

### 6.27: Spectral Clustering

-   Cluster by affinity
    -   EM and k-means work for clusters *centred* around a point.
    -   What if clusters are just nearby points, not centred around another point?
    -   Think of a 2D hollow shape with hyperbolic arcs, like a croissant. 
        -   Cluster centre at the focus point, which is outside the cluster! 
-   The *connectedness*, aka **affinity**, of the data points ties them together, not centre points.

### 6.28: Spectral Clustering Algorithm

-   **Affinity matrix**, MxM matrix, where M is number of data points.
-   Put each point in row i and column i.
-   Affinity is the inverse quadratic distance between two given data points; this is used for matrix cell values.
-   Assume 9 points in 3 clear clusters.
-   This is an approximately **rank-deficient** matrix.
    -   **Column rank**: number of linearly independent column vectors.
    -   Column rank and row rank are always equal, hence we just talk about **rank**.
    -   Rank of mxn matrix cannot be > `min(m, n)`.
    -   Matrix with maximum possible rank is said to have **full rank**.
    -   Matrix without maximum possible rank is **rank deficient**.
    -   9x9 matrix, but rank ~3, hence rank-deficient.
-   **Principal component analysis**, aka PCA: method to identify vectors that are similar in an approximately rank-deficient matrix.
    -   PCA identifies eigenvectors with large eigenvalues.
    -   There might be additional eigenvectors, but PCA will not return these because they don't explain much data.
-   **Dimensionality = number of large eigenvalues**.
-   When you plot data onto these PCA-returned eigenvectors the points will be very well separated and easily analysed by EM or k-means.

-   **Spectral clustering**, aka **affinity-based clustering**:
    -   Builds an affinity matrix of the data points.
    -   Extracts the eigenvectors with the largest eigenvalues.
    -   Re-maps the data points onto the eigenvectors.
    -   Clusters using conventional methods (EM, k-means).

-   Consider 9 data points arranged in a 3 x 3 grid.
    -   The 9x9 affinity matrix will look familiar, in blocks of 3x3 going down the leading diagonal.
    -   However each sub-block is missing pair of non-leading-diagonal elements, because of 1st-3rd elements in line being far apart.
    -   This doesn't prevent the same large eigenvalues from appearing.

### 6.30: Supervised vs unsupervised learning

-   Supervised learning is the dominant paradigm.
-   Unsupervised learning is much less explored, but equally and even more important.
-   Data is cheap! Web crawlers, logs, sensors.
-   Labels are expensive! Analysis, humans.
-   The future is data-cheap and label-expensive.
-   Hence unsupervised learning is one of the most interesting, open research topics in machine learning.
-   Half-way between: **semi-supervised**, **self-supervised**.

## Unit 7: Representation with Logic

### 7.1: Introduction

-   Search: sequences of actions to solve problems.
-   Probability theory: represent and reason with uncertainty.
-   Machine learning: learn and improve.

-   AI big, dynamic, due to pushing in three directions:
    1.  Agent design.
        -   Reflex based agents, the simplest.
        -   Move into goal/utility based agents.
    2.  Complexity of environment
        -   Simple.
        -   Partial observability.
        -   Stochastic actions of multiple agents.
    3.  Representation
        -   Of the environment, becomes complex.

### 7.2: Propositional Logic

-   Recall the alarm example (Burglary, Earthquake, Alarm, Mary, John).
-   Denote these with symbols `B E A M J`.
-   In probabilistic models, these are True or False.
-   In propositional logic, our degree of belief is True, False, or Unknown.

$(E \lor B) \implies A$
    
-   If Earthquake or Burglary then Alarm.

$A \implies (J \land M)$

-   If Alarm then John calls or Mary calls. (and symbol looks like an A for AND without the crossbar)

-   This is subtle:
    -   $P = false, Q = false, P \implies Q = true$
    -   $P = false, Q = true, P \implies Q = true$
    -   $P = true, Q = false, P \implies Q = false$
    -   $P = true, Q = true, P \implies Q = true$

$J \iff M$

-   John calls if and only if Mary calls.

$J \iff \neg M$

-   John calls if and only if Mary does not call.
-   This is subtle.
    -   $P = false, Q = false, P \iff Q = true$
    -   $P = false, Q = true, P \iff Q = false$
    -   $P = true, Q = false, P \iff Q = false$
    -   $P = true, Q = true, P \iff Q = true$

-   A **model** is a set of True/False values for all the propositional logic statements.

        {B: True, E: False, ...}

-   Truth of a statement implied by the truth of statements, represented in a *truth table*.

### 7.3: Truth Tables

-   Lists all possiblities of symbols in rows.
-   For each possibility it lists the values of all the compound values.

\begin{tabular}{|l|l||l|l|l|l|l|}\hline
P & Q & $\neg$ P & P $\land$ Q & P $\lor$ Q & P $\implies$ Q & P $\iff$ Q \\ \hline
false & false & true & false & false & true & true  \\ \hline
false & true & true & false & true & true & false \\ \hline
true & false & fase & false & true & false & false  \\ \hline
true & true & false & true & true & true & true  \\ \hline
\end{tabular}

### 7.5: Propositional Logic Question

-   In a particular model of the world we know the following propositional logic statements are true:

$(E \lor B) \implies A$

$A \implies (J \land M)$

$B$

-   For each propositional symbol, is that symbol True, False, or Unknown?
    -   E is Unknown
    -   B is True
    -   A is True
    -   J is True
    -   M is true
    -   Work through the implies and iff truth tables to satisfy yourself this is correct.

### 7.6: Terminology

-   **Valid sentence**: true in every possible model, i.e. every possible combination of values for all symbols.
-   **Satisfiable**: true for some models, but not all models.
-   **Unsatisfiable**: false in every possible model.

### 7.7: Propositional Logic Limitations

-   Can only handle True/False values.
-   Can't handle *uncertainty*, as in probability theory.
-   Can't talk about *objects* that have *properties* (size, weight, colour), or *relations between objects*.
-   No *shortcuts*.
    -   e.g. vacuum world with 1000 places, each without direct.
    -   Need 1000 statements!

### 7.8: First Order Logic

-   First-order logic vs. propositional logic vs. probability theory.
-   **Ontological commitment**: how does a model talk about the world?
-   **Epistomological commitments**: what types of beliefs may agents in the world hold?

\begin{tabular}{|l||l|l|}\hline
Type & World & Beliefs \\ \hline
First-order logic & Relations, objects, functions & True/False/Unknown \\ \hline
Propositional logic & Facts & True/False/Unknown \\ \hline
Probability theory & Facts & $\mathbb{R}[0..1]$ \\ \hline
\end{tabular}

-   Types of representation.
-   **Atomic**: representation of a state is just an individual state, no pieces.
    -   We used it in problem solving an search.
    -   State A transitions to state B. Are states identical, is one a goal state? Nothing internal.
-   **Factored**: representation of an individual state of the world is factored into several variables.
    -   Boolean in propositional logic.
    -   Other types of variables.
-   **Structured**: individual state is not just one or a set of values for variables but can have connections between objects.
    -   Branches, relations.
    -   See in programming languages, relational databases.
    -   Structured Query Language (SQL).
    -   This is what we get in first-order logic.

### 7.9: Models

-   How to model four scrabble pieces laid out in a 2 x 2 grid and their scores:

        A (1)
        B (3)
        C (3)
        D (2)

-   Constants: {A, B, C, D, 1, 2, 3, CEE}
    -   Does not need to be a one-to-one mapping between constants and objects.
    -   'CEE' refers to the letter C.
-   **Function**: mapping from objects to objects.
-   Functions:

        NumberOf:
            {A -> 1, B -> 3, C -> 3, D -> 2}

-   Relations:

        Above:
            { [A, B], [C, D] }

        (A is above B, C is above C)

        Vowel: { [A] }

        Rainy: { }
        # it isn't rainy today.

        Rainy: { [] }
        # it is rainy today. "arity" of rainy is zero, so a set of one empty tuple.

### 7.10: Syntax

-   **Sentence**: describes facts that are true or false.
    -   **Atomic sentences** are predicates corresponding to relations.
    -   Equality relation is an example of a distinguished relation.
-   **Term**: describes an object.

-   Sentences
    -   `Vowel(A)`
    -   `Above(A, B)`
    -   `2 = 2`
    -   Can be combined by propositional logic operators

-   Terms
    -   `A, B, 2`.
    -   Variables: `x, y`
    -   Functions: `NumberOf(A)`

-   **Quantifiers**
    -   For all, $\forall x$
    -   There exists, $\exists y$.

    -   Example:

    $\forall x$ $Vowel(x) \implies NumberOf(x) = 1$

    $\exists x$ $NumberOf(x) = 2$

    -   The above is saying "there is some object in the domain such that applying `NumberOf` to it results in the number 2", but we're not saying which particular object it is.

    -   Sometimes we omit quantifiers. Assume that we mean "for all".

### 7.11: Vacuum World

-   Two-location vacuum world.
    -   Vacuum can be in one location.
    -   Each location may have dirt or not have dirt.

-   Locations: A (left), B (right)
-   Vacuum: V
-   Dirt: D1, D2
-   Relations
    -   Loc (true of any location)
    -   Vacuum (true of vacuum)
    -   Dirt (true of dirt)
    -   At(Obj,Loc)

Vacuum at location A  
$At(V,A)$

No dirt at location  
$\forall d, \forall l$ $Dirt(d) \land Loc(l) \implies \neg At(d, l)$  

-   If there were thousands of locations instead of 2 then this statement still holds. This is the power of first-order logic.

The vacuum is in a location with dirt, without specifying which location it's in.  
$\exists l, \exists d$ $Dirt(d) \land Loc(l) \land At(V, l) \land At(d, l)$

-   What does first order mean?
    -   The relations are on objects, but not on relations.
    -   In higher order logica we could define the notion of a transitive relation.
-   e.g., defining the notion of a transitive relation:

$\forall R$ $Transitive(R) \iff (\forall_{c,b,c}~R(a,b) \land R(b,c) \implies R(a,c))$

### 7.12: FOL Question

- - -

$\exists x, y~~ x=y$

-   This is valid, always true.
-   Every model has to have at least one object.
-   We can have x and y refer to the same object.
-   So object must be equal to itself.

- - -

$(\exists x~~x=x) \implies (\forall y~ \exists z~~ y=z)$

-   This is valid.
-   LHS always true - object is always equal to itself.
-   The RHS is true. For all y we can choose a z like y itself, and an object is always equal to itself.

- - -

$\forall x~~P(x) \lor \neg P(x)$

-   This is valid.
-   Always true. Everything has to be either in the relation for P or not in the relation for P.

- - -

$\exists x~~P(x)$

-   This is satisfiable.
-   True for models in which some x that is a member of P.
-   But P might be an empty relation.

- - -

### 7.13: FOL Question 2

-   Do the following first-order logic statement(s) apply to the given English sentences?

- - -

-   Sam has two different jobs.

$\exists x, y~~Job(Sam, x) \land Job(Sam, y) \land \neg (x=y)$

-   Yes, it does.

- - -

-   The concept of set membership.

$\forall x, s~~Member(x, Add(x,s))$
$\forall x, s~~Member(x,s) \implies (\forall y~~Member(x, Add(y,s)))$

-   No, it does not.
    -   It tells you what is a member.
    -   But it doesn't tell you about what x is not a member of.

- - -

-   The concept of horizontally/vertically adjacent blocks.

$\forall x, y~~Adj(Sq(x,y), Sq(+(x,1),y)) \land Adj(Sq(x,y), Sq(x,+(y,1)))$

-   No, it does not.
    -   It'll tell you that (1,1) is adjacent (2,1) and (1,2).
    -   Doesn't tell you any other directions, e.g. (2,1) to (1,1).
    -   Doesn't tell you (1,1) is not adjancent to (8,9).

- - -

-   Moral: if you want to do a definition, like adjacent or member, you want a sentence with an "if and only if".

## Unit 8: Planning

### 8.1: Introduction

-   We want to know what an agent should do in an environment.
-   Existing problem solving methods, e.g. A\* require a fully observable and deterministic.
-   We're going to relax those constraints.
-   We need to interleave planning and executing and need feedback from the environment.

### 8.3: Planning vs. Execution

-   *Stochastic* environment, we don't know what an action is going to do.
-   *Multiagent*, other agents => we need to determine what they are doing and then act accordingly.
-   *Partial observability*.
    -   If we want to go `[A, S, F, B]`.
    -   But sometimes at `S` we see a sign that says `Road to F closed`.
    -   But we can't see this sign yet.
    -   We can't differentiate between states `A given road from S to F open` and `A given road from S to F closed`.
-   *Unknowns*.
    -   e.g. inaccurate GPS or maps.
-   *Hierarchical*.
    -   Want high-level plans, that drill down to lower-level details, etc.

-   Change our point of view.
-   From planning in the space of *world* states.
-   To planning in the space of **belief** states.

### 8.4: Vacuum Cleaner Example.

-   8 possible states, with all transitions depending on how vacuum cleaner moves (L and R) or sucks up dirt (S).
-   If environment fully observable can plan a route to clean both rooms.
-   What if the robot's sensor breaks, such that it can't tell where it is or if there's dirt in the room?
    -   Could draw a big circle around all states and say "we could be in any state".
    -   But this is the state space of world states.
    -   What if we consider the state space of belief states?

### 8.5: Sensorless Vacuum Cleaner Problem

-   Yes, intial state is full of all world states.
-   But as we perform actions we move to a subset of world states, which in itself is a state of the belief states.
    -   starting state has 8 world states.
    -   e.g. if we move right we must be in the right, with dirt in either square, hence 4 world states.
    -   if we then suck then we move to a state with only 2 world states left, which is whether or not there's dirt in the other room.
-   Inverse operations
    -   In the world, going left and going right are inverses.
    -   In the state space of belief states, going left and going right are not inverses. We still know something at the end, i.e. we're on the left.

-   **Conform-it plan**: execute a series of actions and reach a goal without ever observing the world.
    -   e.g. if the goal is to be in a clean location, then suck.

-   It is also possible to transition to a state where we know where we are, without every observing the world.

### 8.6: Partially Observable Vacuum Cleaner

-   Suppose we can sense where we are and if there's dirt in our current location, but can't tell if there's dirt in any other location.
-   And suppose observing if there's dirt is an explicit action.
-   Act-observe cycle.
    -   As we act the size of the state space of belief states may stay the same or may decrease.
    -   As we observe, we're taking an existing state and partitioning it up into pieces.
        -   Observations can't introduce new states, but they could put them into correct locations.

### 8.7: Stochastic Environment Problem

-   Assume suck action always works properly.
-   Assume actions aren't always successful.
-   In this case actions will increase the the state space, as we're not sure if they've worked!
-   **Stochastic**: multiple outcomes for each action.
    -   Actions are now **indeterministic**.
-   An observation partitions the belief state into smaller believe states, as it allows us to determine our location and dirt state.
-   How do we plan in a stochastic environment?
    -   Regardless of the particulars, **you must observe**.
-   No finite plan is guaranteed to work, as actions may not work.

### 8.8: Infinite Sequences

-   Finite sequence, e.g. `[S, R, S]` (suck, right, suck).
-   Infinite sequences: as DFAs.
-   Each action paired with an observation: act-observe cycle.
-   If an action fails we repeat it. Else we continue.

        [S, while A:R, S]

-   (suck, while we observe A then R, suck)
-   With probability 1 at the limit this plan will succeed, but we can't specify a bounded number of steps at which it'll succeed (countably infinite steps).

### 8.9: Finding a Successful Plan

-   Draw out a tree of possible states, expressed as DFAs as this is a stochastic environment.
-   We start off in a single world state.
-   We pick in this tree a single path to a goal state.
-   Our backward loops due to failed actions aren't part of the search path, but will be used when acting (!!AI maybe?).

-   In order to guarantee an unbounded solution, every leaf in the plan must end up at a goal.
    -   We can't pick the results of observations.
    -   Observations are causing the belief state space to partition.
    -   Hence all leafs must be goals.
-   In order to guarantee a bounded solution, there must be no loops in the search path.



# Introduction to Artificial Intelligence

Via Udacity (CS-271)

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
    
        P(Y) = sum_i P(Y | X=i) * P(x=i)
            
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


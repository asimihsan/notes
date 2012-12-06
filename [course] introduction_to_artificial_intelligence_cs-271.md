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
	-	Ideally we want UCS and when we encounter an obstacle we want UCS.

## 2.23: A\* Search
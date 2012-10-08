z# Social Network Analysis - 2012 - 001

(via Coursera)

## Lecture notes

### 1A Why Social Network Analysis?

-	Can use Gephi to do auto community and clustering detection.
-	Organisation hierarchies often reflected in clustered graphs, but shortcuts present too.
-	Characterising networks and nodes.
	-	Are nodes connected?
	-	How far apart are nodes?
	-	Are some nodes more important due to position?
	-	Are there communities in the network?
-	Modelling networks (where structure comes from).
	-	Randomly generated.
	-	Small-world structures.
-	How network structure affects processes.

###  1B Software Tools

-	In this course:
	-	Gephi - visualization and basic network metrics
		-	http://gephi.org, download dining.gephi.
	-	NetLogo - modelling network dynamics
	-	iGraph - programming
-	Alternatives:
	-	Pajek (http://pajek.iimfm.si/doku.php), Windows only
	-	UINet (not free, Windows)
	-	NodeXL (http://nodexl.codeplex.com) (Windows, free, beta)
	-	NetworkX (Python)
	-	sna package for R (http://cran.r-project.org/web/packages/sna/index.html)
		-	Test hypotheses
	-	SoNIA (Social Network Image Animator) (http://www.stanford.edu/group/sonia)
-	Using Gephi
	-	Load dataset.
	-	Select Layout -> ForceAtlas 2. Want to put nodes into communities.
	-	Right click on colour/size, select, close dialog, then left click on the button again to apply.
	-	Layout -> Label adjust to adjust labels.
	-	Partition -> Edges, then reload, then select a parameter, then click run. Edges coloured by parameter.
	-	Buttons at top (Overview, Data Laboratory, Preview)
		-	Can explore data in Data Laboratory.
		-	Can export using Preview.
	-	(bottom) big T to show node labels.

### 1C Degree and Connected Components

-	Tufte principles
	-	Above all else show the data.
	-	Maximise the data-ink ratio, within reason.
	-	Erase non-data ink, within reason.
	-	Erase redundant data-ink.
	-	Revise and edit.
-	Aesthetic criteria for network visualisations.
	-	Minimise edge crossings.
	-	Uniform edge lengths (but not if edges have weight).
	-	Don't allow nodes to overlap with edges that's aren't incident on them.
-	Edge attributes
	-	Weight (positive and negative)
	-	Ranking  (1st, 2nd, ...)
	-	Type
	-	Properties depending on the rest of the graph, e.g. betweenness.
-	Data representation
	-	**Adjacency matrix**
		-	N x N for N nodes. Row 1 is node 1, ...
		-	A_ij is 1 if node i has edge to node j.
		-	A_ii = 0, unless there are self loops.
		-	A_ij = A_ji if undirected.
	-	**Edge list**
		-	[2,3], [2,4], ...
	-	**Adjacency list**
		-	If graph very large and very sparse.
		-	For each node a list of neighbours.
-	**Node degree** - number of edges incident to node
	-	Indegree, outdegree, or degree (in and out).
-	Graph properties: betweenness, centrality.
-	**Outdegree** = Sum of row in adjacency matrix.
-	**Indegree** = Sum of column in adjacency matrix.
-	**Indegree sequence** = ordered list of indegree of each node.
-	**Outdegree sequence** = ordered list of outdegree of each node.
-	**Degree sequence** = order list of degree of each node.
-	**Degree distribution** = freqency count of each degree.
-	**Strongly connected components** - each node can reach every other node by following directed edges.
-	**Weakly connected components** - each node can be reached from every other node by following edges in either direction (even if directed).
-	**Giant component** - if largest component encompasss a significant fraction of graph.

### 1D Gephi demo

-	(top left) Ranking -> Nodes -> Indegree, set min/max size by clicking on the red ruby icon, spline, apply. Nodes sized by indegree.
-	(right) Statistics -> Network Overview -> Average degree -> Run.
	-	Not only visual but will put new columns in Data Laboratory.
-	(right) Statistics -> Network Overview -> Connected Components -> Run. Then should be able to Partition -> Edges -> refresh, choose strongly connected ID.

### 2A Introduction to random graph models

-	simple representation to test and predict properties.
-	a strawman: how is the real world different, what insights are there?
-	Erdos and Renyi, random network model.
-	Assumptions:
	-	Nodes connect at random.
	-	Undirected.
-	Two parameters:
	-	N: number of nodes.
	-	p: probability that any two nodes share an edge, OR
	-	M: total number of edges.
-	(N, p) model is binomial (review this). p = node, (1 - p) = no node.
-	Average degree = (N - 1) * p.
	-	Each node has (N - 1) tries to get an edge. 
-	Binomial cofficient
	-	N choose k. = n! / (k!) * (n - k)!
-	B(7;4;p) = 7_C_4 * p^4 * (1-p)^3.
-	In general average degree is the mean, expected(x) = sum(x) * p(x).
-	Variance in degree = (n-1) * p * (1-p)
-	In general variance = E[(X-u)^2] = sum(X-u)^2 * p(x).
-	Binomial approximations:
	-	Small p => Poisson. p_k = z^k * e^(-z) / k!
	-	Large n => Normal.
-	Insights:
	-	No hubs, no nodes with very high degrees.

### 2B: Random graphs and alternative models

-	For a growing random graph there's a marked increase in the giant component size when average degree = 1.
	-	NetLogo -> Sample Models -> Network -> Giant Component.
	-	Imagine network of friends. If average degree = 1 there's a chain of a friend to a friend to a …, hence giant component.
-	Lattice percolation.
	-	2D grid, each point has a probability p of being occupied.
	-	How far can infinite liquid starting at origin travel?
	-	Critical point at p = 0.5 - 0.55
-	In general: at what average degree (i.e. density) to giant components appear?
-	In random graphs degree distribution has an exponential distribution.
-	In random graphs size of giant components ~ N, whereas size of other components ~ log(n).
	-	Given two very large components any additional random edges are very likely to join them, hence intuitively only one giant component likely.
-	Given Erdos-Renyi graph with nodes N, average degree z, => average shortest path ~= log(N) / log(z).
	-	Very hard to derive.
	-	Intuitively N^l = z^l. i.e. the number of friends distance l away from you is z^l.
-	Closed triad: A -> B -> C -> A.
-	**Introduction model**
	-	Like ER except only (1 - p_intro) chance of random edge. Else we ask an adjacent node for one of their edges (friend of a friend).
	-	Relative to ER the **introduction model** has:
		-	more closed triads (friends introduce you to friends)
		-	longer average shortest path (instead of randomly connecting to distant nodes edges kept more local).
		-	more uneven degree distribution (people with more connections get more edges, increasing returns)
		-	smaller giant component at low p.
-	**Static geographical model**
	-	Randomly place nodes on a 2D grid. Each node tries to connect to M neighbours.
	-	Relative to ER:
		-	narrower degree distribution (each node is aiming for the same number of neighbours).
		-	longer average shortest path (geographically localised)
		-	smaller giant component (less chance of random connections)
-	**Random encounter model**
	-	Nodes at random on 2D grid. Then each node moves randomly until it encounters a node, and then makes an edge.
	-	Relative to ER:
		-	longer average shortest path.
		-	smaller giant component.
		-	more closed triads.
-	**Growth model**
	-	Nodes added over time.
	-	Compared to ER:
		-	More nodes with degree 1, as there are more younger nodes.
		-	No more closed triads, because of yound nodes.
		-	Smaller giant component.
		
### 2C: Models of network growth

-	In real networks degree distribution is highly skewed.
	-	Question/answer forums, sexual contact.
-	The Poisson distribution of Erdos-Renyi has very fey high degree nodes.
-	The Power Law of real networks have log(n) high degree nodes.
	- p(k) (probability of degree k) = C * k ^ (-alpha).
	- C is constant such that probabilities of all k sum to 1.
	- i.e. log(p(k)) = c - alpha * log(k).
	- alpha > 3 => no longer heavy tailed distribution.
-	Preferential attachment / cumulative advantage is increasing returns, those with many edges get more edges.
-	Power law model networks **grow over time**, nodes make m edges per tick. (first ingredient)
	-	If at time t there are t nodes, k_i is degree of node i born at time i, then dk_i(t) / dt = m / t.
	-	k_i(t) = m * (log(t) + c)
	-	At t = i, k_i(t) = m, => m = m * (log(i) + c), => c = 1 - log(i)
	-	=> **k_i(t) = m * (1 + log(t/i))**
	
	-	If tau(100) is time when node of degree 100 is born, fraction of nodes that have degree <= 100 is (t - tau) / t, or 1 - tau/t.
	-	log(t/tau) = k/m - 1
	-	t/tau = e^(k/m - 1)
	-	tau/t = e^(-(k/m - 1)))
	-	P(k < k') = 1 - e^(-(k/m - 1))
-	Power law model networks show **preferential attachment** (second ingredient).
	-	Price [65] model for citations.
		-	Papers start with m citations.
		-	Probability of citing a paper with degree k proportional to k + 1.
		-	Power law, alpha = 2 + 1/m.
-	Barbasi-Albert model
	-	New nodes form m attachments. Form to nodes in proportion to vertex degree / sum of all degrees of all vertices.
	-	dk_i(t) / dt = m * (k_i/2tm) = k_i/2t, and k_i(i) = m.
	-	k_i(t) = m * (t/i) ^ (1/2)
	-	p(k) = 2m^2 / k^3
	-	Distribution is scale free (i.e. power law) with alpha = 3.
	-	Graph is connected.
	-	Older are richer.

### 3A: Centrality

-	www.moviegalaxies.com
-	Indegree/outdegree, discussed before.
-	Trade in petroleum, source: NBER / UN Trade Doha
-	Ask yourself what your network represents and what it's scope is.
-	Common tactic - size node by in-degree, colour node by out-degree or ratio of in/out degree.
-	**Normalization**
	-	Divide degree by maximum possible degree, $$N-1$$.
-	**Skew in distribution of degree centrality**
	-	Could just do stdev of degree.
	-	Freeman's general formula.
		-	Sum over all nodes of difference between maximum centrality and this node's centrality, divided by number of pairs [(N-1)(N-2)].

		sum[i = 1 to g](C_D(n*) - C_D(i)) / [(N-1)(N-2)]

-	**Brokerage**: how nodes lie between other nodes.
	-	Having to go through other key nodes to each everyone.
	-	How many pairs of nodes do you have to go through to reach one another in a minimum number of hops?
-	Degree centralization doesn't capture brokerage.
-	**Constraint**: how dependent on other nodes are you to communicate.
	-	In a brokerage position you experience low constraint.
-	**Betweenness** definition:

$$ C_B(i) = /sum{j<k} \frac{g_jk(i)}{g_jk} $$

-	$$g_jk$$ is number of shortest paths node $$i$$ is on between $$j$$ and $$k$$.
-	**Normalized betweenness**:

$$ C_B(i) = \frac{C_B(i)}{[(n-1)(n-2)/2]} $$

-	Denominator is number of pairs of nodes excluding the node itself.
-	Size nodes by degree, colour by betweenness.
	-	Notice low degree nodes with high betweenness, bridge networks.
-	What if it's not important to have many direct edges, but just to be "not too far"?
-	**Closenesss**: length of average shortest path between a node and all other nodes in the graph.

$$ C_c(i) = [\sum{j=1}^{N} d(i,j)]^(-1) $$

-	**Normalized closeness centrality**

$$ C'_C(i) = \frac{C_C(i)}{(N-1)} $$

-	Sometimes the graph isn't fully connected, so some distances are infinite. Instead can invert each distance and then sum those.

#### Readings:

-	Week 1
	-	Network Science - Chapter 1
		-	Networks have predictive power.
		-	Networks are remarkably stable.
		-	The choice of network we focus on makes a huge difference.
		-	Cascading faliures - where nodes depend on each other. Network structure critical.
		-	Behind each complex system is an intricate network.
		-	There are fundamental principles and reproducible mechanisms behind all networks.
		-	Interdisciplinary.
		-	Empirical, data driven.
		-	Quantitative and mathematical nature. Physics, engineering, statistics, etc.
		-	Computational nature. Big databases, algorithms, data mining.
		
-	Week 2
	-	Giant component (Wikipedia)
		-	For n nodes, p = 1 / n, size of giant component is likely to be proportional to n^(2/3).

## Assignment notes

## General notes
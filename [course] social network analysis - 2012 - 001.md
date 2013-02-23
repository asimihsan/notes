# Social Network Analysis - 2012 - 001

(via Coursera)

## Student

[Asim Ihsan](http://www.asimihsan.com)

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
		-	No more closed triads, because of young nodes.
		-	Smaller giant component.
		
### 2C: Models of network growth

-	In real networks degree distribution is highly skewed.
	-	Question/answer forums, sexual contact.
-	The Poisson distribution of Erdos-Renyi has very few high degree nodes.
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
-	Ask yourself what your network represents and what its scope is.
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

-	$g_jk(i)$ is number of shortest paths node $i$ is on between $j$ and $k$.
-	$g_jk$ is the total number of shortest paths between $j$ and $k$.
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

### 3B: Eigenvector and directed networks

-	**Eigenvector centrality**: you are as central as your neighbours, recursively.
	-	Solving for eigenvector of adjacency matrix with eigvenvalue = 1.
-	**Bonacich eigenvector centrality**
	-	Tunable via beta.

``c_i(\Beta) = \sum{j} (\alpha + \Beta c_j)A_(ji)``

``c(\Beta) = \alpha(I - \Beta A)^-1 \times A \times 1``

-	Meaning:
	-	alpha: normalization constant.
	-	beta: how important the centrality of your neighbours is.
	-	A: adjacency matrix (can be weighted)
	-	I: identity matrix
	-	1: matrix of all ones.

-	Beta:
	-	0 yields simple degree centrality.
	-	Small beta => high attenuation. Only your immediate friends matter.
	-	High beta => low atteuation. Global network structure matters.
	-	Negative => node is more central when connected to less central nodes.
	
-	**Betweenness centrality in directed networks**
	-	Watch out which paths you're actually on.
	-	Normalization denominator changes, loses factor of 2:
	
$$ C'_B(i) = \frac{C_B(i)}{[(N-1)(N-2)]} $$

-	**Directed closeness centrality**
	-	In-closeness (prestige in citation networks)
	-	Out-closeness.
	-	Only consider nodes you can reach.
	
-	**Eigenvector centrality in directed networks**
	-	**PageRank.**
	-	Recursive, directed. Difficult to artificially inflate it because it's recursive.
-	**Random walk** is like the eigenvector centrality measure.
	-	Just walk randomly, measure time you spend at each node.
	-	More time => more important.
	-	But could get trapped in circles!
	-	PageRank allows random teleportation to work around cycles.
	-	As you increase random teleportation probability PageRank score distribution flattens. Not walking, just jumping around.

### 3C: Centrality applications (optional)

-	**Hospital patient transfers**, simulation.
	-	Patients transfer, take diseases.
	-	Hospitals could collaborate to find hubs of key disease transfer points.
	-	Want to allocate money to hospitals to fight disease, but who to give money to?
	-	Strategies, and how they affect probability of getting infected:
		-	Random, no effective.
		-	Degree (some hospitals have more transfers than others), geometric mean (sqrt(indegree + outdegree)), a bit effective.
		-	Betweenness, even more effective.
		-	Greedy (simulation based), most effective.
		-	Eigenvector (as effective as greedy).
-	**Identifying expertise** in an expertise network
	-	Response time gap between the questions you ask and when they're answered.
	-	Directed edges.
		-	A -> thread => A asked the question.
		-	Thread -> B and C => B and C answered.
		-	Could weigh edges by:
			-	number of threads.
			-	shared credit (all responders get equal weight)
			-	backflow (questions that are answered get a backward edge).
	-	**Bow tie model** of web and forums
		-	Core: strongly connected component, everyone asks and answers.
		-	In: mostly askers
		-	Out: mostly helpers.
		-	Forums are skewed; indegree is much higher, small core. Not a community as such.
		-	Question: what is the indegree/outdegree of the largest connected component?
	-	Is centrality, using various measures, a good measure of expertise?
		-	Compared with human evaluation: yes.
	-	Very interesting is that recursive PageRank wasn't the best!
		-	To investigate, simulated two models:
			-	'Best' preferred. Experts answer questions that are high enough quality to be worth answering.
			-	'Just better' preferred: people answer questions just a bit more challenging than their expertise level.
			-	Centrality measure perform differently depending on model.

### 4A - Why detect communities?

-	Sometimes communities bridge different organisation units.
-	Strong communities => there are brokers, which are bottle-necks in information flow. Key influencers.
-	Communities can maintain divergent opinions; influenced by neighbours, less by other communities.
	-	Unlike Erdos-Renyi random graphs.
-	Community finding in scientific papers, how areas influence one another.

### 4B - Heuristics for finding communities

-	What makes a community?
	-	Mutuality of ties?
	-	Frequency of ties among members?
	-	Closeness of reachability of subgroup members?
	-	Relative frequency of ties within subgroup?
-	**Affiliation networks , i.e. bipartite graphs**.
	-	e.g. two types of nodes: people, and events they attended.
	-	People who attended the same event are connected.
	-	**Multi-modal network**.
-	**Clique**: fully connected subgraph.
	-	Every member connected to every other member.
	-	Cliques may overlap.
-	Communities are cliquish.
-	Meaningfulness of cliques.
	-	Not robust; just one missing link disqualifies it.
	-	Not interesting; no core, no centrality.
	-	Overlaps are more interesting than just existence.
-	**k-cores**: similar idea, but just need to know k other nodes, not fully connected.
	-	But even this is too stringent.
-	**n-cliques**: maximal distance between any two nodes in subgroup is n.
	-	Reachability. 
	-	**Diameter**: longest path between any two nodes.
	-	Diameter may be greater than n, so paths go through nodes not in subgroup.
-	**n-club**: maximal subgraph of diameter 2.
-	**p-cliques**: cluster has vertices with at least proportion p of neighbours in cluster.
-	Cohesion in directed and weighted networks
	-	Could only keep edges above a threshold weight

### 4C - Community Finding

-	**Hierarchical clustering**
	-	Calculate some notion of distance between all pairs of nodes (e.g. number of shared neighbours, weight).
	-	Add edges between pairs one by one in order of decreasing weight.
	-	Can choose when to stop. Early => fine structure, late => coarse structure.
-	Pajek has efficient and successful implementation, not in Gephi, igraph, networkx.
-	Pajek can random permute rows of adjacency matrix such that same graph but clear clusters appear.
-	**Dendrogram**: view of hierarchical clustering.
-	**Betweenness clustering** (Girvan and Newman)
	-	Compute betweenesss of all edges.
	-	while (betweenness of any edges > threshold)
		-	Remove edge with highest betweeneness
		-	Recalculate betweenness.
	-	Very inefficient; all pairs shortest path is O(N^3), need to do it up to N times but intuitive.
	-	Does not scale > 100 nodes.
-	How do you know when to stop for hierarchical and betweenness clustering?
	-	**Modularity**, maximize it.
	-	How many more edges in community than would be expected randomly?
	
Q = 1/2m * sum(all pairs)[A_vw - k_v * k_w / 2m] * delta(c_v, c_w)

i.e.

sum over all pairs of difference between adjacency matrix and probability of an edge between two vertices proportional to their degrees.

delta is 1 if in same community, using any metric you want, 0 if not.

-	Modularity used to find community structure in graphs with > 400,000 nodes and > 2 million edges

-	Very large, dense graphs like Orkut and Flickr difficult to partition. Communities no larger than 100 nodes because traditional algorithms do not allow overlap.
	-	*Statistical Properties of Community Structure in Large Social and Information Networks* (Leskovec et. al 2008)
	
-	Key is to *allow overlap*, nodes belong to more than one community.
	-	*Uncovering the overlapping community structure of complex networks in nature and society* (Palla et. al 2005).
	-	http://cfinder.org.
	-	Finding cliques by removing a given node then adding someone nearby?
	-	"Natural" community boundaries.

-	Ingredient networks - what goes with what?

### 5A - Small world experiments

-	Small world phenomenon: Stanley Milgran's experiment.
	-	"Six degrees of separation".
	-	Send a message to someone far from you by sending to "closest".
-	In random graphs with noone sharing any neighbours you'd expect massive numbers of neighbours-of-neighbours etc.
	-	So if friendship networks are random six degrees of separation not surprising.
	-	But what if network is very cliquish? Worst case, what if all neighbours-of-neighbours were your neighbours?
	-	In this case impossible to reach rest of network.
-	Is 6 an accurate number?
	-	**Attrition**. As path gets longer smaller probability of successfully passing on message. Bias to shorter paths.
		-	Research indicates attrition rate is constant over position in path. See "An Experimental Study of Search in Global Social Networks", Dodds et al.
	-	**Navigation and accuracy**. Do people find shortest paths? Of course not.
		-	See "Killworth, McCarty, Bernard, & House", 2005. Less than optimal choice for next hop is made 0.5 of the time.

### 5B - Clustering and motifs

-	Local phenomenon.
-	**Transitivity**
	-	If A -> B and B -> C, what is probability that A -> C?
-	**Triadic closure** - A, B, and C connected.
-	**Global clustering coefficient**: to what extent is clustering present?
	-	C = 3 x number of triangles in graph / number of connected triples of vertices.
-	**Local clustering coefficient**
	-	C_i = number of connections between i's neighbours / maximum possible connections.
	-	n_i = number of neighbours of i.
	-	C_i directed = number of directed connections / n_i * (n_i - 1)
	-	C_i undirected = number of undirected connections / 0.5 * n_i * (n_i - 1)
	-	C = 1/n * sum(C_i) over all i.
-	**Embeddedness**: number of common neighbours that two endpoints have.
	-	E = nodes that are neighbours of both A and B / nodes that are neighbours of at least one of A or B.
	-	Implies shared context, e.g. high school class, but not necessarily closeness, i.e. actually friends.
-	Snowball sampling (souce: Information and Social Capital, Alstyne).
	-	Ask to name 1st and 2nd best friends, more clustered (i.e. embedded).
	-	Ask to name 7th and 8th best friend, less clustered and hence longest possible path is larger so easier to reach more people.
	-	Hence being more embedded can limit your ability to project information and intercept varied information.
-	Onnella et al., 2007. (10:12)
	-	Characterizing the large-scale structure and the tie strengths of the mobile call graph.
		-	Tie strength is how frequently two people communicate.
	-	Log distribution of degree (skewed, very few with high degree).
	-	Log distribution of link weight (skewed, very few with high weight).
	-	Embeddedness of the tie (?)
	-	Edge neighbourhood overlap (embeddedness) as a function of tie strength.
		-	Positive linear. => more embedded means greater tie strength.
	-	Intermediate tie strength neighbours are whom you spread most novel information with, not weak or strong.
-	Can do better if you look at directionality in local structure.
	-	**Motif**: particular directed configuration of a closed triad and closed four-node subgraphs.
	-	**Feed forward loop**: X -> Y, Y -> Z, X -> Z.
		-	Filters out noise.
	-	Compare number of instances of motifs to "equivalent" random graph.
		-	Generate a random graph where the degree distribution matches the actual graph.
		-	Then calculate Z-score (x - mean_x / stdev_x). Z > 0 => more often than random, Z < 0 => less often than random.
	-	Software: use FANMOD or igraph.
-	Onnella found that there are superfamilies of networks. (16:47)
	-	**Motif profiles**: characterise using graphs by Z-scores for 3-node motifs.
	-	e.g. graphs of different languages have similar distribution of Z-scores of motifs. (e.g. to->be->or->not->to->be).
	-	Web and social graphs have similar distributions. Suggests similar mechanisms.
-	**Forbidden triad**: A -> B, B -> C, but not A -> C.
-	Can use motif profiles to compare models to actual networks.

### 5C - Small world models

-	Small world phenomenon
	-	*High clustering*: C_network >> C_{random_graph}
	-	*Low average shortest path*: l_network ~= ln(N)
	-	ER graphs also have similar low average shortest path.
	-	Many closed triads.
-	Watts/Strogatz model reconciles these two observations.
	-	Generating small world graphs.
	-	Take a ring of nodes, connect each node to its two physical neighbours on either side (four edges).
	-	Either:
		-	Randomly reposition edges, or
		-	Add fraction p of new edges, leaving the old ones.
	-	Disallow self-edges and multiple edges.
	-	At p ~= 0.01 high clustering and low average shortest path.
	-	At p > 0.1 clustering coefficient collapses, as expected; become ER network.
	-	Probability that a connected triple stays connected is (1 - p)^3.
	-	Hence clustering coefficient = C(p) = C(p=0) * (1-p)^3
	-	What is missing?
		-	Too many long range links.
		-	No hierarchical structure and groups.
		-	No hubs.
-	Kleinberg's geographical small world model.
	-	Nodes on 2-D lattice. Each node as local lattice edges (north, south, east, west)
	-	Additional links with p(link between u and v) = (distance(u, b)) ^ (-r).
	-	r is constant that determines navigability.
	-	Greedy search (i.e. choosing node that is closest to target) reveals pattern similar to Milgram's experiement: many large hops initially, small hops towards the end.
	-	r = 0 => randomly distributed, ASP ~= ln(n), so no very small local ties.
	-	r > 2, p ~ 1 / d^4. search time ~= N^{(r-2)/(r-1)}. No large ties.
	-	r = 2 is about right. p = ~ 1/d^2. (probabilty of forming tie is inverse squared). Greedy search works.
-	15:08: group affiliations.
	-	Bipartite networks. Individuals share contexts, imply edges between individuals as a unipartite network.
-	Kleinburg's hierarchical network models (Small-world phenomena and the dyanmics of information):
	-	h_ij = height of least common ancestor
	-	p_ij = b^{-alpha * h_ij}
	-	b is branching factor of the hierarchy.
	-	alpha is measured from network.
-	Kleinburg's group structure models (same paper):
	-	f(q) ~ q^(-alpha).p
-	Watts, Dodds, Newman (2001), Identity and Search in Social Networks
	-	Individual belong to hierarchically nested groups.
-	Columbia experiment
	-	Successful chains disproportionately use professional ties.
	-	Successful chains disproportionatly avoided hubs and family/friends.
	-	Strategy: Geography first then work when close to target.

### 5D - Origins of small worlds

-	Generating small-world networks.
-	Assign properties to nodes (spatial location, group membership)
-	Add or rewire links according to some rule
	-	Simulated annealing, optimize for property.
	-	Add links with probability, e.g. preferential attachment
	-	Simulate nodes as agents making decisions.
-	What to optimize for?
	-	E = lambda * L - (1 - lambda) * W // energy, want to minimize
	-	L = average shortest path.
	-	W = cartesian distance between two nodes.
	-	Want small number of hops and short distances.
-	Source: Small worlds: How and Why, Mathias et. al.
-	Idea is that can generate small world networks based on different constaints (navigation, group affiliation).

### 6A: Network topology and diffusion

-	How network structure affects diffusion.
-	Complex contagion thresholds; not enough for only one neighbour to affect you.
-	ER networks:
	-	Higher density in ER network => faster diffusion.
-	Scale-free, those that grow.
	-	With preferential attachment more hubs so diffusion faster.
-	Small world networks
	-	Recall: high clustering yet short average shortest path.
	-	In ring-lattice model of small-world networks rewiring gives us the short ASP.
	-	Hence as probability of rewiring increases the rate of diffusion increases.
	-	Even with a recovery rate greater than infection rate the rewiring allows a model that should die out to survive.

### 6B: Complex contagion

-	Complex contagion is less able to use shortcuts because such shortcuts are typically a single edge, whereas we need > 1 to exceed a threshold.
-	Network coordination.
	-	Want to maximize your payoff.
	-	Given `(p)` fraction play basketball, you get `a` payoff per friend for basketball.
	-	Given `(1-p)` fraction play football, you get `b` payoff per friend for football.
	-	If your friends don't play what you're playing you get no payoff.
	-	`d` neighbors.
	-	If chooses A, payoff = `p * d * a`
	-	If chooses B, payoff = `(1-p) * d * b`.
	-	So you should choose A if: `p d a >= (1-p) d b`.
	-	Or: `p >= b / (a + b)`.
-	In contagion networks one node changing color / preference can cause a cascade.
-	Implications for viral marketing - what small subset of nodes to choose to target for influence?
-	Community structure:
	-	Enable ideas to spread in the presence of thresholds; the dense intra-community ties allow this.
	-	Create isolated pockets impervious to outside ideas; the sparse inter-communiy ties allow this.
	-	Allow different opinions to take hold in different parts of the network, see the previous point.
-	What if you are bi-colour / bi-preference (i.e. both simultaneously), but with a cost `c`?
	-	e.g. being bilingual may mean you're average at both, not expert at one.
	-	Being bilingual reduces the incentive of others to choose between the two preferences, even if one is better or lower cost. Simply because bilingual nodes allow the choice to be avoided.
-	Nodes need to coordinate across a network but have limited horizons.
	-	Want x neighbours to be a colour / preference.
	
### 6C: Innovation in Networks

-    Innovate or imitate?
    -    Brainstorming: more minds, but groupthink.
    -    Isolation: independence, slower.
-    Kauffman's NK model.
    -    N dimensional problem space, N bits (0 or 1)
    -    K describes the smoothness of fitness of landscape.
    -    How similar is fitness of sequences with only 1-2 bits flipped (K=0 => no similarity, K=large => smooth fitness).
    -    K large => single maxima, smooth.
    -    K small => very noisy, many maxima.
    -    K medium => in between.
    -    Node starts with random bit string.
    -    Each iteration if neighbour has better solution then imiate by copynig, else innovate by flipping a bit.
-    If you start with a ring lattice, increasing probability of random edges causes much faster convergence at a worse solution.
    -    There is a sweet spot, single maxima parabola, some intermediate p.

### 7A: Cool and unusual applications

-    Watch other fun videos! !!AI TOWATCH
-    Laszlo Barbasi on the diseasome (http://youtu.be/10oQMHadGos)
-    Cesar Hidalgo on economic development (http://www.youtube.com/watch?v=GRp382ynu-Q)
-    YY Ahn on flavor network (http://www.santafe.edu/research/videos/play/?id=26c05e3e-0955-45ac-8c17-20315e576af7)

### 7B: Predicting recipe ratings using ingredient networks

-    Is a recipe good? Can you tweak it?
-    allrecipes.com, 46k recipes, 1.9 million reviews.
-    Cooking methods, ingredients (combination and suggested modifications in comments).
-    Undirected weighted edges. Weighted using **pointwise mutual information**.
    -    PMI = log( P(a,b) / P(a)P(b) ).
    -    P(a,b) = (no. recipes containing a and b) / (no. recipes).
    -    P(a) (no. recipes containing a) / (no. recipes)
    -    P(b) = (no. recipes containing b) / (no. recipes).
-    Compare recipe rating to PMI of its ingredient pairs.
-    4 star rating have the most suggestions for modifications (almost right!).
-    High recipe frequency => low deletion/recipe
-    High recipe frequency => low additon/recipe.
-    High recipe frequency => low increase/recipe.
-    Substitution network
    -    Replace 'a' with 'b'.
    -    Nodes: ingredients.
    -    Edge weights: p(b | a). Proportion of substitutions of ingredient a that suggests ingredent b.
-    Substitutions network and users' preferences.
    -    Create edge from ingredient a to b if rating(a) < rating(b).
    -    Only for recipes with sufficient overlap in ingredients (just one or two different ingredients).
-    Test prediction of ratings from ingredients.
-    Use *gradient boosting tree*.
-    Recipes encode our collective cooking knowledge.

### 8A: Network resilience

-    **Node percoluation**: lose nodes.
-    **Edge percolation**: edges disappear.
-    Resilience of random vs. preferential growth network.
-    Targeted attacks (e.g. edges with high betweenness).
-    In a network with average degree = 4.64, if you remove 25% of edges giant component stays the same before new average degree ~ 3, well above percolation threshold of 1.
-    Node removal and site percolation
    -    Fill each square with probability p, then fill with liquid.
    -    Low p => small island.
    -    p critical => giant component forms, occupying finite fraction of infinite lattice.
    -    p above critical value => giant component occupies an increasingly larger portion of the graph.
-    On node and edge percolation of proportion p, how is size of giant component affected?
-    On targeted node percolation of high centrality nodes (e.g. degree), how in comparison is size of giant component affected?
-    In e.g. scale-free networks targeting nodes much more effective.
-    Also, what is effect on average path length?
    -    For scale-free, targeting => more impactful on average path length.
    -    For ER graphs, targeting => no more impactful.
    
### 8B: Resilience and assortativity

-    **Assortativity**: like connect with like.
-    e.g. degree disassortative => hubs in periphery. Scale-free.
-    **Correlation profiles**
    -    Compare number of edges between nodes with connectivities k_0 and k_1 between a graph and a properly randomized network.
    -    Three-degree plot, where third degree is color heat map.
-    **Average degree of neighbors**
    -    Plot degree of node vs. average degree of neighbors.
    -    e.g. on internet negative trend (high node degree => low average degree of node's neighbors).
    -    another useful way of comparing graphs, to e.g. small-world or random models.
    -    Another 2D plot.
-    For a single number, take *Pearson correlation coefficient of nodes on each side of an edge*.
    -    cor(deg(i), deg(j)) for all edges {ij}.
    -    Internet is negative, so yes diassortive, but sometimes the correlation profile gives more useful information.
    -    One number is useful.
-    Assortative => more resilient. Disassortative => more hubs => less resilient.

### 8C: Resilience and the power grid

-    Internet, terrorist, crimial networks. Is it that simple to damage them?
-    Of course not; dynamism.
-    Power grid.
    -    As electricity flows simultaneously in all available paths failure affects everyone else.
    -    Each node has a *load* and *capacity*.
    -    When node removed its load is redistribted to remaining nodes.
    -    If load of node exceeds capacity then node fails.
-    Nodes: generators, substations.
-    Edges: high-voltage transmission lines.
-    Degree distribution is exponential.
-    Efficiency of path is 0 if no electricity flows on path, 1 if transmission lines are perfect.
-    Harmonic composition for path:

e_path = [ sum_edges (1/e_edge) ] ^ -1

-    e.g. path A, 2 edges, each e=0.5, e_path = 1/4.
-    e.g. path B, 3 edges, each e=0.5, e_path = 1/6.
-    e.g. path C, 2 edges, e=0 and e=1, e_path=0.
-    Assume electricity flows along most efficient path.
-    Efficiency of network is average of most efficient paths from each generator to each distribution center.

E = 1/(N_G N_D) * sum epsilon_ij for all paths ij.

epsilon_ij is efficiency of the most efficient path between i and j.

-    Assume capacity of each node is proportional to its initial load.

C_i = alpha * L_i(0), i = 1, 2, …, N.

-    L represents weighted betweenness of a node.
-    alpha is overload tolerance.
-    Failed nodes put extra load onto neighbors.
-    Overload capacity of 30% higher than initial load is sufficient for network's efficiency to remain roughly the same on loss of most connected node or two.
-    Power companies have no incentive to provide extra load, extra costs.
-    But research shows that just 30% extra is needed, not that high.

### 8D: Concluding remarks

-    "Introduction to Networks" by Mark Newman, a tomb.
    -    How to determine giant component size from degree distribution.
    -    Statistical look at clustering, is clustering different from random.
-    Matthew Jackson, "Social and Economic Networks"
    -    Strategically, if nodes are self-interested, how will network get wired?
    -    Prisoner's dilemma on networks.
-    Barbassi, "Network Science"
    -    Still being written.
    -    For beginner's.

# Readings:

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

-	Week 3
	-	**The Social Organization of Conspiracy - Illegal Networks in the Heavy Electrical Equipment Industry (Baker / Faulkner)**
		-	Price fixing.
		-	Conclusion: maximise concealment rather than efficiency.
		-	In switchgear "phase of the moon" price scheduling, i.e. decentralized. Product standardized, flow of orders predictable, easy to synchronize price fixing. Not true of more complex products like turbines.
		-	In transformers also decentralized price fixing.
		-	In turbines very lumpy market, low volume, non-standardized. High information processing requirements for conspirators.
		-	Industrial organization economics examines effects of market system imperfections on behaviour of producers, and how producers satisfy society's economic needs.
			-	Collusion likely in certain industry structures; few sellers, high seller concentration, homogenous products.
			-	Number of two-way flows is N(N-1)/2, so fewer sellers => easier to coordinate.
			-	Treat the internals of the conspiracy as a black box.
		-	Organizational crime examines individuals as agents, representing their organization and themselves.
			-	Makes many simplifications about conspirator social organization, almost a black box as well.
		-	Expect *sparse, decentralized networks* if secrecy is only factor. But also need to communicate efficiently.
		-	Small group research applies here: more routine tasks are more efficiently performed in centralized structures, more complex tasks in decentralized structures.
		-	Organizational theorists have similar conclusions - more information-processing requires more decentralization.
		-	Concealment vs. coordination.
		-	Centrality: more central => can get better illegal deals for your company, but also mean more personal culpability.
		-	Executives can delegate so can afford to be less central, hence predict less likely to get fined or prosectured.
		-	Degree => legal culpability, where betweenness and closensess amounts to hearsay.
		-	Undirected graph of Senate testimony where witnesses mention someone else. Also measure organizational rank.
		-	Freeman's three point centrality measures used. Also could have used Bonacich's measures of sociometric status (Bonacich 1972) and influence (Bonacich 1987), Coleman's measure of power (Coleman 1973), Burt's measure of prestige (1980).
		-	Also Stephenson and Zelen (1989)'s measure of point centrality where shortest paths are deliberately avoided.
		-	Graph density => observed number of edges as percentage of maximum possible.
		-	p849, figure 2: decentralized and centralized networks.
		-	Graph centralization => ratio of centrality of most central point to maxmium possible centrality.
		-	Results.
		-	Turbines (recall, most information processing) had highest density and most centralization, contradicting small group and organizational theory.
		-	Network decentralization did not protect against successful prosection; in turbine network less likely to be found guilty.
		-	Top executives in decentralized conspiracies able to shield themselves from prosection, but when found guilty had larger fines.
		-	Top executives in centralized conspiracies could not shield themselves, but when found guilty had smaller fines.
		-	Middle managers more vulnerable than junior managers.
		-	Degree centrality increases vulnerability. Not betweenness or closeness. However, degree does not affect penalities.
		-	In centralized networks, e.g. turbines, small connected core and large periphery. Core dominated by top executives, who need to be hands on. Hence lower conviction rate but more top executives found guilty.
	-	**Network Structure and Information Advantage (Aral / Alstyne)**
		-	How and why social structure affects economic outcomes.
		-	Burt (1992) shows that structurally diverse networks (low in cohesion and structural equivalence) are more successful in e.g. wages, promotion, job placement, creativity (Burt 2004a). Other studies show similar. More novel information.
			-	See p11 figure 1 for diagram of cohesion and structural equivalence.
			-	p12 => sructural equivalence of two actors is Euclidean distance of their contact vectors.
		-	Conclusion: total amount and diversity of novel information increases at decreasing rate with network size and network diversity.
		-	Weak ties to other parts of network important source of inormation (Granovetter 1973: 1371). Get redudant information from well connected local network (Burt 1992).
		-	Burt (2004b): "creativity is an import-export game, not a creation game".
		-	Do diverse networks actually provide access to more novel information? No.
			-	Less diverse, stronger connected links have less novel information but higher bandwidth, so maybe more information.
			-	Nodes aware of more redundant information in local network so they adjust their transmission to avoid redundancy.
		-	Even with new information does productivity necessarily rise? No.
		-	p19, vector space model of communication content. Emails categorized into set of topic vectors, individuals' email's diversity is variance of topic vectors.
		-	Results.
		-	Total and diversity of novel information increasing with node's network size and network diversity, but marginal increase decreses with network size.
		
		
**Week 4**

-	Modularity and community structure in networks

-	Uncovering the overlapping community structure of complex networks in nature and society

**Week 5**

-    The Small-World Phenomenon (Ch 20 of Networks, Crowds, and Markets)
    -    !!AI TOREAD

**Week 7**

-	The human disease network (Goh et. al)
	-	(This is an excellent paper, good basis for how to explore a bipartite network).
	-	**locus heterogeneity**: genetic disorders that arise from mutations in more than one single gene.
	-	**allelic heterogeneity**: different mutations in the same gene giving rise to phenotypes currently classified as different disorders.
	-	Should be able to do better than single-gene-single-disorder approach.
	-	Link all genetic disorders ("disease phenome") with complete list of disease genes ("disease genome").
	-	"diseasome".

	-	bipartite graph of two disjoint sets of nodes: genetic disorders and genes.
	-	edge if mutations in that gene are implicated in that disorder.
	-	with this diseasome bipartite graph generate two biologically relevant network projections:
		-	"human disease network". nodes are disorders, connected with they share at least one gene.
		-	"disease gene network". nodes are disease genes, connected if they are associated with same disorder.

	-	large giant component. => genetic origins of most disases are shared with other diseases.
	-	degree distribution => disorders only connected to a few other diseases.
	-	large cancer cluster tightly interconnected due to many genes associated with multiple types of cancer.
	-	Others diseases under-represented in giant component, do not form a single distinct cluster.

-	The Product Space Conditions the Development of Nations
	-	Imagine a product is a tree, set of products a forest.
	-	Firms are monkeys jumping tree to tree.
	-	Traditional growth theory assumes all trees equally within reach.
	-	However, if forest is heterogenous, with some dense areas and some sparse areas, monkeys may be unable to easily move through some parts of the forest.
	-	Distance between trees could be:
		-	intensity of labor, land, capital.
		-	level of technological sophistication,
		-	inputs and outputs involved in product's value chain.
		-	requisite institutions.
	-	Rather than make a-priori distance assumptions, instead assume that co-produced goods are related. "proximity".


## Assignment notes

## General notes

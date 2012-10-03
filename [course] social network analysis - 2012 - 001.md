# Social Network Analysis - 2012 - 001

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

#### Readings:

-	Week 1
	



## Assignment notes

## General notes
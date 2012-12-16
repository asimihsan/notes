# Machine Learning in Action

## Part 1: Classification

### Chapter 1: Machine learning basics

-    Turning data into information using statistics.
-    Massive amounts of data, unable to fully model the problem.
-    e.g. can magnometers be used to predict earthquakes?
    -    could invest in high-grade magnetometers, install around the world, monitor 24x7.
    -    or use consumer-grade smartphone magnetometers, gather orders of magnitude more data including temperature and GPS, then sift through it.
    
#### Glossary

-    **Expert systems**: computer programs that can classify observations into classes. e.g. a bird expert.
-    **Features**, aka attributes: what you measure. e.g. weight, wingspan, webbed feet?, back colour.
-    **Instance**: one complete collection of features, a vector.
-    **Classification**: given an instance, what is the class? In our example, bird species.
-    **Training set**: set of training examples.
-    **Training example**: vector of features (an instance) and one target variable.
-    **Target variable**: what we're predicting.
-    **Test set**: another set of data that doesn't interesct with the training set.
    -    Used to determine how good our model is.
-    **Knowledge representation**: what the machine has learned.
    -    Not always human readable.

#### Key tasks of machine learning

-    **Supervised learning**: where we tell the algorithm what to predict.
    -    **Classification**: predict what class an instance should fall into.
    -    **Regression**: prediction of a numeric value.
    -    k-Nearest Neighbours.
    -    Naive Bayes.
    -    Support Vector Machines.
    -    Decision trees.
    -    Linear.
    -    Locally weighted linear.
    -    Ridge.
    -    Lasso

-    **Unsupervised learning**: no target variables given, ask machine to find patterns.
    -    **Clustering**: group similar items together.
    -    **Density estimation**: find statistical values that describe data.
    -    k-Means.
    -    DBSCAN
    -    Expectation maximization.
    -    Parzen window.
    
-    Reducing data from many features to a small number.
    -    **Principle Component Analysis**: which values add information, and which just match others?
    -    **Singular Value Decomposition**: how many groups of numeric data are there?
    
#### How to choose the right algorithm

-    Not hard-and-fast rules.

-    Prediction, forecast => supervised learning.
-    Else, unsupervised learning.

-    Supervised learning.
    -    Target value is discrete => classification.
    -    Target value is continuous => regression.
    
-    Unsupervised learning.
    -    Fit into discrete groups => clustering.
    -    Numerical estimate of strength of fit into groups => density estimation.
    
-    Good questions.
    -    Features are discrete or continuous?
    -    Are there missing values in features?
        -    If so, why?
    -    Are there outliers?
    -    Are you looking for something very rare?
    
#### Steps to developing an application

1.    **Collect data**.
    -    RSS, API, analog sensor, public data.
2.    **Prepare the input data**.
    -    strings, inputs, lists, matrices.
3.    **Analyze the input data**.
    -    Mark 1 eyeball it. Does it look sane?
    -    Exploratory visualizations. 1D, 2D, 3D.
4.    **Train the algorithm**.
    -    Here is where the "core" algorithms go.
5.    **Test the algorithm**.
    -    If not satisfied, change something and re-test.
6.    **Use it**.
    -    Is it fit for purpose?

#### Using numpy

        import numpy

        # Random 4x4 matrix returned as array
        numpy.random.rand(4,4)
        
        # Random 4x4 matrix returned as matrix
        m1 = numpy.mat(numpy.random.rand(4,4))
        
        # Inverse of matrix
        m1.I
        
        # m1 * m1.I = identity matrix with very small non-zero numbers
        m1 * m1.I
        
        # identity matirx of size 4
        numpy.eye(4)
       
### Chapter 2: Classifying with k-Nearest Neighbours

-    If you measured number of kisses and number of kicks per movies, maybe you could automatically assign a genre to a movie.
        
1.    Collect
    -    Any method.
2.    Prepare
    -    Numeric values are needed for a distance calcuation. A structure data format is best.
3.    Analyze
    -    Any method.
4.    Train
    -    Does not apply to kNN.
5.    Test
    -    Calculate the error rate
6.    Use
    -    Get structured input.
    -    Determine which class the input data should be in.
    -    Act on the calculated class.

-    Method
    -    For every point in our data set:
        -    Calculate the distance between inX and the current point.
        -    Sort the distances in increasing order.
        -    Take k items with lowest distances to inX.
        -    Find the majority class among these items.
        -    Return the majority class as our prediction for the class of inX.


-    `numpy` time.
-    Input: `numpy.array` of M vectors. Each vector has N elements, one per feature, i.e. things we know.
-    Output: List of M strings.
-    p50: code.

        def createDataSet():
            group = numpy.array([[1.0,1.1], [1.0,1.0], [0,0], [0,0.1]])
            labels = ['A', 'A', 'B', 'B']
            return group, labels

        def classify0(inX, dataSet, labels, k):
        
            # get number of rows
            dataSetSize = dataSet.shape[0]
            
            # numpy.tile(inX, (dataSetSize, 1)) returns a new matrix with sime dimensions as dataSet, but with inX's values as each row.
            # subtracting from dataSet, then squaring and sum and sqrt, gives distance.
            diffMat = numpy.tile(inX, (dataSetSize, 1)) - dataSet
            sqDiffMat = diffMat ** 2
            sqDistances = sqDiffMat.sum(axis=1)
            distances = sqDistances ** 0.5
            sortedDistIndices = distances.argsort()
        
            # count numbers of each class in highest k labels.
            classCount={}
            for i in xrange(k):
                voteIlabel = labels[sortedDistIndices[i]]
                classCount[voteIlabel] = classCount.get(voteIlabel, 0) + 1
            sortedClassCount = sorted(classCount.iteritems(), key=operator.itemgetter(1), reverse=True)
            return sortedClassCount[0][0]

        group, labels = kNN.createDataSet()
        kNN.classify0([0,0], group, labels, 3)
        # = B. good!

-    To test.
    -    Feed in new data.
    -    **Error rate**: Number of times wrong / total number of tests
    
#### Improving dating site matches with kNN

-    Helen wants to use dating site inputs, plus other data, and her dating experiences, to figure out three types of dates.
-    Collect: test file provided.
-    Prepare: parse a text file in Python.
-    Analyze: Use `matplotlib` to make 2D plots.
-    Train: Doesn't apply to kNN.
-    Test: Use some data as test.
-    Use: Make a simple command-line tool.

-    Features
    -    Number of frequent flyer miles earned per year.
    -    Percentage of time spent playing video games.
    -    Liters of ice cream consumed per week.

-    p52: how to read in text file as matrix of integer features and list of string class labels.
-    p54: exploratory visualization.
-    p57: important to normalize data, as they have different ranges.
-    p58: how to test.
-    p59: making predictions.

#### Handwriting recognition

-    p61: import 32x32 binary pixel value representation as 1x1024 feature instances.
-    p62: use our existing `classify0` kNN algorithm on this data.
-    quite slow! Could use kD-trees to reduce cost of distance calculations.

### Chapter 3: Splitting data sets one feature at a time: decision trees

-    Decision trees are like Twenty Questions: you give it data and it generates discrete answers.
-    **Decision blocks**: rectangles, make a decision.
-    **Terminating blocks**: reach a conclusion, give output.
-    **Branches**: arrows coming out of decision blocks.
-    Unlike kNN, decision trees give an excellent knowledge representation.

-    Pros:
    -    Computationally cheap.
    -    Easy for humans to understand learned results.
    -    Missing values OK.
    -    Can deal with irrelevant features.
-    Cons:
    -    Prone to overfitting.
-    Works with:
    -    Numeric values
    -    Nominal values.
    
-    Method, `createBranch()`
-    Check if every item in the dataset is in the same class.
-    If so return the class label.
-    Else:
    -    Find the best feature to split the data.
    -    Split the dataset.
    -    Create a branch node.
        -    For each split
            -    Call `createBranch` and add the result to the branch node
    -    Return branch node.
    
-    Approach
    -    Collect: any method.
    -    Prepare: only discrete values, so any continuous values need to be quantized.
    -    Analyze: Any method. Should visually inspect tree.
    -    Train: Constract a tree data structure.
    -    Test: Calculate the error rate with the learned tree.
    -    Use: For any supervised learning task. Often, trees are used to better understand data.
    
-    Going to not restrict ourself to binary decision blocks, but split multiway.

-    Using ID3 algorithm to tell us how to split.
-    Split in a way that makes our unorganised data more organised.
-    **Gini impurity**
    -    Probability of choosing an item from the set and the probability of that item being misclassified.
    -    Not discussed further.
    -    Reference: *Introduction to Data Mining* by Tan et al., 2005.
-    **Information gain**: change in information before and after the split, using information theory.
-    **Shannon entropy**, aka **entropy**, is the expected value of information.

        l(x_i) = log_2( p(x_i) )

        # l(x_i) is information for symbol x_i        
        # p(x_i) is the probability of choosing this clas
        
        H = -sum(i=1 to n) p(x_i) * log_2( p(x_i) )
        # H is entropy, expected value of all information of all possible values of class.
        
-    p69: calculating entropy, as above.

        def calcShannonEnt(dataSet):
            # Create dictionary of all possible classes
            labelCounts = {}
            for featVec in dataSet:
                currentLabel = featVec[-1]
                labelCounts[currentLabel] = labelCounts.get(currentLabel, 0) + 1
        
            # Calculate the entropy.
            numEntries = len(dataSet)
            shannonEnt = 0.0
            for key, count in labelcount.iteritems():
                prob = float(count) / numEntries
                shannonEnt -= prob * math.log(prob, 2)
            return shannonEnt

-    Measure entropy, split on all features, and figure out which split causes the smallest entropy in new sets.
-    Here is how to split out by feature:

        def splitDataSet(dataSet, axis, value):
            retDataSet = []
            for featVec in dataSet:
                if featVec[axis] == value:
                    # Cut out the feature split on.
                    reducedFeatVec = featVec[:axis] + featVec[axis+1:]
                    retDataSet.append(reducedFeatVec)
            return retDataSet

-    p71: choosing the best feature to split on.
-    p74: tree building code.
-    p77: plotting tree nodes with text annotations.
-    p78: identifying the number of leaves in a tree and the depth.
-    p80: the `plotTree` function
-    p83: classification function for an existing decision tree.
-    p85: applying this to the classic `Lenses` data set.

-     We've probably overfit.
-     If leaf node only adds a little information we cut it off and merge it with another leave.
    -    Revisit in chapter 9.
-    Also in chapter 9 we investigate another algorithm, CART, that can handle continuous values, unlike ID3.

### Chapter 4: Classifying with probability theory: naive Bayes

   
import numpy
import math
import operator

def calcShannonEnt(dataSet):
    # Create dictionary of all possible classes
    labelCounts = {}
    for featVec in dataSet:
        currentLabel = featVec[-1]
        labelCounts[currentLabel] = labelCounts.get(currentLabel, 0) + 1

    # Calculate the entropy.
    numEntries = len(dataSet)
    shannonEnt = 0.0
    for key, count in labelCounts.iteritems():
        prob = float(count) / numEntries
        shannonEnt -= prob * math.log(prob, 2)
    return shannonEnt

def createDataSet():
    dataSet = [[1, 1, 'yes'],
               [1, 1, 'yes'],
               [1, 0, 'no'],
               [0, 1, 'no'],
               [0, 1, 'no']]
    labels = ['no surfacing', 'flippers']
    return dataSet, labels

def splitDataSet(dataSet, axis, value):
    retDataSet = []
    for featVec in dataSet:
        if featVec[axis] == value:
            # Cut out the feature split on.
            reducedFeatVec = featVec[:axis] + featVec[axis+1:]
            retDataSet.append(reducedFeatVec)
    return retDataSet

def chooseBestFeatureToSplit(dataSet):
    numFeatures = len(dataSet[0]) - 1
    dataSetSize = float(len(dataSet))
    baseEntropy = calcShannonEnt(dataSet)
    bestInfoGain = 0.0
    bestFeature = -1
    for i in xrange(numFeatures):
        # Create unique list of class labels
        featList = [example[i] for example in dataSet]
        uniqueVals = set(featList)

        # Calculate entropy for each split
        newEntropy = 0.0
        for value in uniqueVals:
            subDataSet = splitDataSet(dataSet, i, value)
            prob = len(subDataSet) / dataSetSize
            newEntropy += prob * calcShannonEnt(subDataSet)
        infoGain = baseEntropy - newEntropy

        # Find the best information gain
        if (infoGain > bestInfoGain):
            bestInfoGain = infoGain
            bestFeature = i
    return bestFeature

def majorityCnt(classList):
    classCount = {}
    for vote in classList:
        classCount[vote] = classCount.get(vote, 0) + 1
    sortedClassCount = sorted(classCount.iteritems(), key=operator.itemgetter(1), reverse=True)
    return sortedClassCount[0][0]

def createTree(dataSet, labels):
    # Stop when all classes are equal.
    classList = [example[-1] for example in dataSet]
    if classList.count(classList[0]) == len(classList):
        return classList[0]

    # When no more features, return majority.
    if len(dataSet[0]) == 1:
        return majorityCnt(classList)

    bestFeat = chooseBestFeatureToSplit(dataSet)
    bestFeatLabel = labels[bestFeat]
    myTree = {bestFeatLabel: {}}
    del(labels[bestFeat])

    # Get a list of unique values
    featValues = [example[bestFeat] for example in dataSet]
    uniqueVals = set(featValues)

    for value in uniqueVals:
        subLabels = labels[:]
        subDataSet = splitDataSet(dataSet,
                                  bestFeat,
                                  value)
        myTree[bestFeatLabel][value] = createTree(subDataSet, subLabels)
    return myTree


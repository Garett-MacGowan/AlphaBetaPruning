"""
graph to be represented as dicts within a dict.
{("node":{("MAX": True/False), (children: ["child1","child2"])})}

Using example from assignment:
{
    "A": {  "MAX": True,  "children": ["B","C"]  },
    "B": {  "MAX": False, "children": ["D","E"]  }
}

quick copy-paste section:
 to get a nodes children:
     children = graph[currentNode]['children']
 to get whether the current node is max or not:
     max = graph[currentNode]["MAX"]
"""

import math

inf = math.inf
leavesVisited = 0

def main():
    pass

# takes file name and returns list of graphs as strings ["set1 set2", "set1 set2"] 
def fileRead(filename):
    pass

# takes a graph as a string of two sets and returns the graph as
# {("node":{("MAX": True/False), (children: ["child1","child2"])})}
def graphParser(graphAsString):
    pass

# takes a graph as a dict of dicts and decides whether to call min or max based
# on the first node
def alphaBetaPruning(graph):
    global leavesVisited
    leavesVisited = 0
    pass

# this function attempts to minimize the score
# takes a graph, the current node, the alpha and beta values
# calls max() for each of its children to allow for taking turns
############ calls prune() when max() returns a value that is less than or equal to alpha
# returns the minimum value that it finds
def minNode(graph, currentNode, alpha, beta):
    global leavesVisited
    # alpha = best already explored node along the path to the root for maximizer (max() function)
    # beta = best already explored node along the path to the root for minimizer (min() function)
    # if currentNode is not an int it has no children, so it must be a leaf
    # if currentNode is a leaf node, return this value
    if representsInt(currentNode):
        leavesVisited += 1
        return currentNode

    # initially set to infinity
    val = inf
    newBeta = beta

    # currentNode is a child and had its own children (not a leaf node)
    children = graph[currentNode]['children']
    for child in children:
        currentVal = maxNode(graph, child, alpha, newBeta)
        if currentVal < val:
            val = currentVal
        elif currentVal < alpha or currentVal == alpha:
            return val
        elif currentVal < newBeta:
            newBeta = currentVal
    return val



""" {    "A": {  "MAX": True,  "children": ["B","C"]  },     "B": {  "MAX": False, "children": ["D","E"]  }      } """



# this function attempts to maximize the score
# takes a graph, the current node, the alpha and beta values
# calls max() for each of its children to allow for taking turns
############# calls prune() when min() returns a value that is greater than or equal to beta
# returns the maximum value that it finds
def maxNode(graph, currentNode, alpha, beta):
    global leavesVisited
    # alpha = best already explored node along the path to the root for maximizer (max() function)
    # beta = best already explored node along the path to the root for minimizer (min() function)
    # if currentNode is not an int it has no children, so it must be a leaf
    # if currentNode is a leaf node, return this value
    if representsInt(currentNode):
        leavesVisited += 1
        return currentNode

    # initially set to infinity
    val = -inf
    newAlpha = alpha

    # currentNode is a child and had its own children (not a leaf node)
    children = graph[currentNode]['children']
    for child in children:
        currentVal = minNode(graph, child, newAlpha, beta)
        if currentVal > val:
            val = currentVal
        elif currentVal > beta or currentVal == beta:
            return val
        elif currentVal > newAlpha:
            newAlpha = currentVal
    return val


# NOT NEEDED PROBABLY
# this function takes the graph and a node to prune
# it returns the graph without the node and all of its descendents
#def prune(graph, nodeToPrune):
#    pass


def representsInt(s):
    try:
        int(s)
        return True
    except ValueError:
        return False









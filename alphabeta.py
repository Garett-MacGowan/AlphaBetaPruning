"""
Below, graphs are represented as dictionaries within a dictionary:
    { "node": { "MAX": True/False , children: ["child1","child2"] } }

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
    graphsAsStrings = fileRead("alphabeta.txt")
    solutionStrings = []
    graphCount = 1
    for graphAsString in graphsAsStrings:
        graphAndRoot = graphParser(graphAsString)
        graph = graphAndRoot[0]
        root = graphAndRoot[1]
        solution = alphaBetaPruning(graph, root)
        fullSolution = "Graph " + str(graphCount) + ": " + solution
        solutionStrings.append(fullSolution)
        graphCount += 1
    writeSolutionsToFile("alphabeta_out.txt", solutionStrings)


"""
This function takes a file name and returns a list of graphs
as strings of the form ["set1 set2", "set1 set2"].
"""
def fileRead(filename):
    graphsAsStrings = []
    with open(filename, "r") as f:
        lineSkipper = False
        for line in f:
            if lineSkipper == False:
                graphAsString = line.rstrip()
                graphsAsStrings.append(graphAsString)
                lineSkipper = True
            else:
                lineSkipper = False
    return graphsAsStrings


"""
This function takes a filename and the solution to the solved
problems in the form of a list of strings. The strings are of
the form "Graph 1: Score: 4; Leaf Nodes Examined: 6". It then
writes the solutions line by line to the given filename.
"""
def writeSolutionsToFile(filename, solutionStrings):
    with open(filename, "w") as f:
        f.write('\n'.join(solutionStrings))


"""
This function takes a graph as a string of two sets. It returns
the the graph and the root. The returned graph is of the form
{ "node":{ "MAX":True/False, children:["child1", "child2"] } }
"""
def graphParser(graphAsString):
    splitGraph = graphAsString.split()
    nodeTypesString = splitGraph[0]
    graphEdgesString = splitGraph[1]
    graph = {}

    # process the nodes and their types
    newNode = ""
    nodeType = ""
    state = 0
    foundRoot = False # keep track of whether the root has been found
    # state 0 is the initial state
    # state 1 is getting the name of the node
    # state 2 is getting the type of the node
    for char in nodeTypesString:

        if state == 0:
            if char == "(":
                # '(' indicates next char is the start of the node's name
                state = 1
                # reset our holders for the name and type of the node
                newNode = ""
                nodeType = ""
            elif char == "," or char == "}":
                if not foundRoot:
                    root = str(newNode)
                    foundRoot = True
                # use this time to create the new node in the dict
                if nodeType == "MAX":
                    graph[newNode] = { "MAX":True, "children":[] }
                elif nodeType == "MIN":
                    graph[newNode] = { "MAX":False, "children":[] }
        elif state == 1:
            if char == ",":
                # comma indicates end of node name and start of node type next char
                state = 2
            else:
                newNode = newNode + char
        elif state == 2:
            if char == ")":
                # ')' indicates end of node type
                state = 0
            else:
                nodeType = nodeType + char

    # process the edges of the graph by populating the "children" lists
    currentNode = ""
    child = ""
    state = 0
    # state 0 is the initial state
    # state 1 is getting the name of the node
    # state 2 is getting the child of the node
    for char in graphEdgesString:

        if state == 0:
            if char == "(":
                # '(' indicates next char is the start of the node's name
                state = 1
                # reset our holders for the name and type of the node
                currentNode = ""
                child = ""
            elif char == "," or char == "}":
                # use this time to add the child to the current node's children
                if representsInt(child):
                    graph[currentNode]["children"].append(int(child))
                else:
                    graph[currentNode]["children"].append(child)
        elif state == 1:
            if char == ",":
                # comma indicates end of node name and start of child next char
                state = 2
            else:
                currentNode = currentNode + char
        elif state == 2:
            if char == ")":
                # ')' indicates end of child
                state = 0
            else:
                child = child + char
    return [graph, root]


"""
This function takes a graph as a dictionary of dictionaries. It decides
whether to call minNode() or maxNode() based on the first node. It then
returns the solution in the form of "Score: 4; Leaf Nodes Examined: 6"
"""
def alphaBetaPruning(graph, root):
    global leavesVisited
    leavesVisited = 0
    score = maxNode(graph, root, -inf, inf)
    result = "Score: " + str(score) + "; Leaf Nodes Examined: " + str(leavesVisited)
    return result


"""
This function attempts to minimize the score. It takes a graph, the current
node and the alpha and beta values. It also calls maxNode() for each of its
children to allow for taking turns. It returns the minimum value that it finds.
"""
def minNode(graph, currentNode, alpha, beta):
    # alpha = best already explored node along the path to the root for maximizer (max() function)
    # beta = best already explored node along the path to the root for minimizer (min() function)
    global leavesVisited
    # if currentNode is not an int it has no children, so it must be a leaf
    # if currentNode is a leaf node, return this value
    if representsInt(currentNode):
        leavesVisited += 1
        return currentNode

    val = inf
    newBeta = beta

    # currentNode is a child and had its own children (not a leaf node)
    children = graph[currentNode]['children']
    for child in children:
        currentVal = maxNode(graph, child, alpha, newBeta)
        if currentVal < val:
            val = currentVal
        if currentVal < alpha or currentVal == alpha:
            return val
        elif currentVal < newBeta:
            newBeta = currentVal
    return val


"""
This function attempts to maximize the score. It takes a graph, the current
node and the alpha and beta values. It also calls maxNode() for each of its
children to allow for taking turns. It returns the maximum value that it finds.
"""
def maxNode(graph, currentNode, alpha, beta):
    # alpha = best already explored node along the path to the root for the maximizer (maxNode() function)
    # beta = best already explored node along the path to the root for the minimizer (minNode() function)
    global leavesVisited
    # if currentNode is not an int it has no children, so it must be a leaf
    # if currentNode is a leaf node, return this value
    if representsInt(currentNode):
        leavesVisited += 1
        return currentNode

    val = -inf
    newAlpha = alpha

    # currentNode is a child and had its own children (not a leaf node)
    children = graph[currentNode]['children']
    for child in children:
        currentVal = minNode(graph, child, newAlpha, beta)
        if currentVal > val:
            val = currentVal
        if currentVal > beta or currentVal == beta:
            return val
        elif currentVal > newAlpha:
            newAlpha = currentVal
    return val


"""
This function returns true if its input is an integer and false
otherwise. It is a helper function for minNode() and maxNode().
"""
def representsInt(s):
    try:
        int(s)
        return True
    except ValueError:
        return False


main()







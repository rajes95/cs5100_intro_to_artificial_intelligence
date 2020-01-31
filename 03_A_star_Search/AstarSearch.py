'''
A* Search

@author: Rajesh Sakhamuru
@version: 9/26/2019
'''


class Node(object):
    """
    The Node class allows the creation of a Tree/Graph by hard coding the children 
    nodes to a dictionary. Each child node  Each node can hold a 'data' value, which in this case is going
    to be an integer value unique to that particular node.
    """

    def __init__(self, name, straightLineDistance):
        self.name = name
        self.sld = straightLineDistance
        self.children = {}

    def add_child(self, obj, dist):
        self.children[obj] = dist


def aStarPath(root):
    """
    This function takes as a parameter the root node to start searching a graph
    for the goal node (indicated by straight-line distance of 0) using an A* 
    search. The straight-line distance is a heuristic value and is used in 
    conjuction with the g(n) value to identify the best path to reach the goal 
    node.
    
    @param      root: The root node of the graph to be searched
    @return:    path: Ordered list of nodes describing the path taken to get 
                    from the root to goal as found by A* search
                closed: Order of all Nodes expanded in order visited by A* search
                parents: nodes and their parents learned during A* search
                gVals: Nodes and their lowest 'g' values learned during A* search
    
    """
    closed = []
    openNodes = [root]
    parents = {root:None}
    gVals = {root:0}

    while openNodes:

        # pick vertex v from openNodes list  with lowest f(n)
        lowf = 0
        vertex = root
        for i in openNodes:
            h = i.sld
            g = gVals[i]
            f = g + h
            if lowf == 0:
                lowf = f + 1
            if f < lowf:
                lowf = f
                vertex = i

        # vertex is goal if 'sld' or Straight Line Distance = 0
        if vertex.sld == 0:
            closed.append(vertex)
            path = []
            path.append(vertex)
            parent = parents[vertex]

            # works backwards from goal to root via Parents dictionary
            while (gVals[parent] != 0):
                path.append(parent)
                parent = parents[parent]

            path.append(parent)

            path.reverse()

            return path, closed, parents, gVals

        # for (m,distance) in vertex's neighbors:
        for m, distance in vertex.children.items():
            # if m is not in open and not in closed update data
            if openNodes.count(m) == 0 and closed.count(m) == 0:
                gVals[m] = gVals[vertex] + distance
                parents[m] = vertex
                openNodes.append(m)
            else:
                mInGVals = False
                # makes sure that if m is in gVals, the lower 'g' one is used
                for k in gVals.keys():
                    if m == k:
                        mInGVals = True
                # makes sure parent node is the one which gives it the lowest 'g' value
                if (mInGVals and gVals[m] > (gVals[vertex] + distance)) or (not mInGVals):
                    gVals[m] = gVals[vertex] + distance
                    parents[m] = vertex
                # if m is in closed move m to open
                for c in closed:
                    if c == m:
                        closed.remove(m)
                        openNodes.append(m)

        # remove v from open
        openNodes.remove(vertex)
        closed.append(vertex)


def main():

    # Creating all the nodes, with their names and straight line distance to Bucharest (the goal)
    Lugoj = Node("Lugoj", 244)
    Timisoara = Node("Timisoara", 329)
    Mehadia = Node("Mehadia", 241)
    Arad = Node("Arad", 366)
    Drobeta = Node("Drobeta", 242)
    Craiova = Node("Craiova", 160)
    RimnicuVilcea = Node("Rimnicu Vilcea", 193)
    Pitesti = Node("Pitesti", 100)
    Bucharest = Node("Bucharest", 0)

    # Adding child nodes to parent nodes, and the distance between the two nodes
    Lugoj.add_child(Timisoara, 111)
    Lugoj.add_child(Mehadia, 70)
    Timisoara.add_child(Arad, 118)
    Mehadia.add_child(Drobeta, 75)
    Drobeta.add_child(Craiova, 120)
    Craiova.add_child(RimnicuVilcea, 146)
    Craiova.add_child(Pitesti, 138)
    Pitesti.add_child(RimnicuVilcea, 97)
    Pitesti.add_child(Bucharest, 101)

    path, closed, parents, gVals = aStarPath(Lugoj)

    print("Path taken to get from Lugoj to Bucharest as found by A* search:")
    for n in path:
        print(n.name)

    print("")

    print("Order of Nodes visited by A* search:")
    for c in closed:
        print(c.name)

    print("")

    print("Nodes and their parents learned during A* search:")
    for node, parent in parents.items():
        if parent is not None:
            print("Node: " + str(node.name) + ", Parent: " + str(parent.name))
        else:
            print("Root: " + str(node.name))

    print("")

    print("Nodes and their lowest 'g' values learned during A* search:")
    for node, gVal in gVals.items():
            print("Node: " + str(node.name) + ", 'g' Value: " + str(gVal))


main()


'''
BFS and DFS 

@author: Rajesh Sakhamuru
@version: 9/21/2019
'''


class Node(object):
    """
    The Node class allows the creation of a Tree/Graph by hard coding the children 
    nodes to a list. Each node can hold a 'data' value, which in this case is going
    to be an integer value unique to that particular node.
    """

    def __init__(self, data):
        self.data = data
        self.children = []

    def add_child(self, obj):
        self.children.append(obj)


def dfs(root, visited=set()):
    """
    dfs() function takes as a parameter the root of a tree and searches through
    the node using a depth-first method and prints the data at each node accessed
    in the order that it is accessed.
    
    visited set is used to prevent cycles during search
    
    this function is recursive
    
    """
    visited.add(root)
    print(root.data)
    for n in root.children:
        if n not in visited:
            dfs(n)
    return visited

def bfs(root):
    """
    bfs() function takes as a parameter the root of a tree and searches through
    the node using a breadth-first method and prints the data at each node accessed
    in the order that it is visited.
    
    cycles are avoided by holding a set of visited nodes and making sure not to 
    visit them again
    
    this function is iterative
    
    This code takes heavy influence from the provided example at:
    https://eddmann.com/posts/depth-first-search-and-breadth-first-search-in-python/
    """
    queue = [root]
    visited = set()
    while queue:
        vertex = queue.pop(0)
        print(vertex.data)  # prints data in order of vertex visited
        if vertex not in visited:
            visited.add(vertex)
            queue.extend(set(vertex.children) - visited)

    return visited


def main():
    """
    representation of the tree hardcoded below
         6
        /
       2
      / \
     /   5
    0
     \   4
      \ / 
       1
        \
         3
    """
    a = Node(0)
    b = Node(1)
    c = Node(2)
    d = Node(3)
    e = Node(4)
    f = Node(5)
    g = Node(6)

    a.add_child(b)
    a.add_child(c)
    b.add_child(d)
    b.add_child(e)
    c.add_child(f)
    c.add_child(g)

    print("Breadth First Search:")
    bfs(a)
    print("-----\nDepth First Search:")
    dfs(a)


main()


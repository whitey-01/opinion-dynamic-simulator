import graph_tool.all as gt
import random
import math


# Hub that holds some native graph_tool topology generator (wrapped) and some custom additions like hypercubes


# generates an hypercube graph given a distance d
# the hypercube is built using bit-fix idea
def generateHypercubeGraph(d: int):
    vertices_num = pow(2, d)
    g = gt.Graph(directed=False)
    # creates a new vertex property to indicate the vertex using its binary representation
    binaryProperty = g.new_vertex_property("string")
    g.add_vertex(vertices_num)

    # time to add edges
    for vertex in g.vertices():
        # takes the decimal index of the vertex and calculate its binary representation
        index = g.vertex_index[vertex]
        binaryRepresentation = ('{0:0' + str(d) + 'b}').format(index)
        # also writes this representation to the vertex property
        binaryProperty[vertex] = binaryRepresentation

        # using bit-fix idea, finds the neighbours of the vertex by flipping every time a different bit
        # from its binary representation. For every of the d neighbours, re-calculates the decimal index
        # from their binary representation, used for indexing them vertex in the graph.
        bitPos = 0
        while bitPos < d:
            bitToFlip = binaryRepresentation[bitPos]
            if bitToFlip == "0":
                neighbourVertexBinary = binaryRepresentation[0:bitPos] + str(1) + binaryRepresentation[bitPos + 1:]
            else:
                neighbourVertexBinary = binaryRepresentation[0:bitPos] + str(0) + binaryRepresentation[bitPos + 1:]

            neighbourVertex = g.vertex(int(neighbourVertexBinary, 2))

            # Then adds the edge between the vertex and its neighbours
            if g.edge(vertex, neighbourVertex) is None:
                g.add_edge(vertex, neighbourVertex)
            bitPos += 1
    return g


# generates a k-clique given the number of vertices
# wraps graph_tool function in a custom one to maintain module integrity
def generateKCliqueGraph(vertices_num: int):
    return gt.complete_graph(vertices_num)


# generates a k-cycle given the number of vertices
# wraps graph_tool function in a custom one to maintain module integrity
def generateKCycleGraph(vertices_num: int):
    return gt.circular_graph(vertices_num)


# generates an Erdős–Rényi Graph(V,E) where every edge e(u,v) has probability p to be in E
# if you want graph to be connected (with high probability), p will be auto calculated to be > ((1+&)ln(n))/n
def generateERGraph(vertices_num: int, connected: bool = True, p: float = None):
    if connected:
        print("Auto-calculating p..")
        eps = 0.000001  # ???
        p = ((1 + eps) * math.log(vertices_num, 2)) / vertices_num
        print("p = " + str(p))
    elif not connected and not p:
        raise Exception("ERROR:- You can't set connected to false without providing a value for p!")

    g = gt.Graph(directed=False)
    g.add_vertex(vertices_num)
    for v1 in g.vertices():
        for v2 in g.vertices():
            if g.vertex_index[v1] != g.vertex_index[v2] and g.edge(v1, v2) is None and random.uniform(0, 1) <= p:
                g.add_edge(v1, v2)
    return g


# -------- W I P -------------------------------------------------------------------------
# generates a random connected graph with a max deg
def generateConnectedRandomGraph(vertices_num: int, max_deg: int):
    g = gt.Graph(directed=False)
    g.add_vertex(vertices_num)

    attempts = 0
    while not isConnected(g):
        if attempts > 1000:
            raise Exception("Error:- exceeded attempts on generating connected graph")

        deg_distribution = []
        for i in range(0, vertices_num):
            deg_distribution.append(random.choice(range(1, max_deg + 1)))

        adjacencyMatrix = getAdjacencyMatrix(deg_distribution, vertices_num)
        for i in range(vertices_num):
            for j in range(vertices_num):
                v1 = g.vertex(i)
                v2 = g.vertex(j)
                if adjacencyMatrix[i][j] == 1 and g.edge(v1, v2) is None:
                    g.add_edge(v1, v2)
        attempts += 1
        print("Attempt: " + str(attempts))
    return g


# return true if the graph is connected (iff g has no self loops or multiple edges)
# --------------------------WRONG-------------------------------------------------
def isConnected(g):
    vertices_num: int = len(list(g.vertices()))
    for v in g.vertices():
        v: gt.Vertex = v
        if v.out_degree() + v.in_degree() < (vertices_num - 1) / 2:
            return False
    return True


def getAdjacencyMatrix(deg_distribution: list, vertices_num: int):
    # n is number of vertices
    mat = [[0] * vertices_num for i in range(vertices_num)]

    for i in range(vertices_num):
        for j in range(i + 1, vertices_num):

            # For each pair of vertex decrement
            # the degree of both vertex.
            if deg_distribution[i] > 0 and deg_distribution[j] > 0:
                deg_distribution[i] -= 1
                deg_distribution[j] -= 1
                mat[i][j] = 1
                mat[j][i] = 1

    return mat


def printAdjacencyMatrix(mat, n):
    print("      ", end=" ")
    for i in range(n):
        print(" ", "(", i, ")", end="")
    print()
    print()
    for i in range(n):
        print(" ", "(", i, ")", end="")
        for j in range(n):
            print("     ", mat[i][j], end="")
        print()
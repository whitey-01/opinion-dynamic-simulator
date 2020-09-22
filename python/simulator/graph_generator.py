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
        eps = 0.00000001  # ???
        p = ((1 + eps) * math.log(vertices_num, 2)) / vertices_num
        print("p = " + str(p))
    elif not connected and not p:
        raise Exception("ERROR:- You can't set connected to false without providing a value for p!")

    g = gt.Graph(directed=False)
    g.add_vertex(vertices_num)
    for v1 in g.vertices():
        for v2 in g.vertices():
            if g.vertex_index[v1] != g.vertex_index[v2] and g.edge(v1, v2) is None:
                if random.uniform(0, 1) <= p:
                    g.add_edge(v1, v2)
    return g


# -------- W I P -------------------------------------------------------------------------
# generates a random, non directed, connected graph
def generateConnectedRandomGraph(vertices_num: int):
    g = gt.Graph(directed=False)
    g.add_vertex(vertices_num)

    while not isConnected(g):
        v1: gt.Vertex = random.choice(list(g.vertices()))
        v2: gt.Vertex = random.choice(list(g.vertices()))
        while g.vertex_index[v1] == g.vertex_index[v2] or g.edge(v1, v2) is not None:
            v2 = random.choice(list(g.vertices()))
        g.add_edge(v1, v2)
    return g


# return true if the graph is connected
def isConnected(g):
    for v1 in g.vertices():
        for v2 in g.vertices():
            if g.vertex_index[v1] != g.vertex_index[v2]:
                edges_num = len(list(gt.shortest_path(g, v1, v2)[1]))
                if edges_num == 0:
                    return False
    return True

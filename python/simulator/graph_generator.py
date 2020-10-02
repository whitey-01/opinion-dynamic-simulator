import graph_tool.all as gt
import random


# Hub that holds some native graph_tool topology generator (wrapped) and some custom additions like hypercubes


# utility that returns a map containing minimum, average and max degree of a graph
def getDegreeValuesOf(g: gt.Graph):
    # max deg (clique)
    min_deg = len(list(g.vertices())) - 1
    max_deg = 0
    avg_deg = 0
    for v in g.vertices():
        v: gt.Vertex = v
        # in_degree is 0 for undirected graphs
        if v.out_degree() + v.in_degree() > max_deg:
            max_deg = v.out_degree() + v.in_degree()
        if v.out_degree() + v.in_degree() < min_deg:
            min_deg = v.out_degree() + v.in_degree()
        avg_deg += v.out_degree() + v.in_degree()
    avg_deg = avg_deg / len(list(g.vertices()))
    return {"min_deg": min_deg, "avg_deg": avg_deg, "max_deg": max_deg}


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
def generateERGraph(vertices_num: int, p: float):
    g = gt.Graph(directed=False)
    g.add_vertex(vertices_num)
    for i in range(0, vertices_num):
        for j in range(i + 1, vertices_num):
            v1: gt.Vertex = g.vertex(i)
            v2: gt.Vertex = g.vertex(j)
            if random.uniform(0, 1) <= p:
                g.add_edge(v1, v2)
    return g
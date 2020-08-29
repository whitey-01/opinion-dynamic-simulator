import graph_tool.all as gt
import random


# Hub that holds some native graph_tool topology generator (wrapped) and some custom additions like hypercubes

# adds vertices to a graph taken in input. Then returns it
def addVerticesTo(graph: gt.Graph, vertices_num: int):
    for i in range(0, vertices_num):
        graph.add_vertex()
    return graph


# generates an hypercube graph given a distance d
# the hypercube is built using bit-fix idea
def generateHypercubeGraph(d: int):
    vertices_num = pow(2, d)
    g = gt.Graph(directed=False)
    # creates a new vertex property to indicate the vertex using its binary representation
    binaryProperty = g.new_vertex_property("string")
    g = addVerticesTo(g, vertices_num)

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


"""

--------------- WIP --------------------

# generates a random, non directed graph
def generateRandomGraph(vertices_num: int, average_deg: int):
    g = gt.Graph(directed=False)
    g = addVerticesTo(g, vertices_num)

    while average_deg > averageDegOf(g):
        v1: gt.Vertex = random.choice(list(g.vertices()))
        v2: gt.Vertex = random.choice(list(g.vertices()))

        if g.edge(v1, v2) is None:
            g.add_edge(v1, v2)

    return g


# returns the average degree of a graph
def averageDegOf(g: gt.Graph):
    avg = 0
    for vertex in g.vertices():
        vertex: gt.Vertex = vertex
        avg += len(list(vertex.all_neighbours()))
    return int(avg / len(list(g.vertices())))


# returns True if none of the vertices has total degree 0
def isConnected(g: gt.Graph):
    for vertex in g.vertices():
        vertex: gt.Vertex = vertex
        if vertex.out_degree() + vertex.in_degree() == 0:
            return False
    return True

"""

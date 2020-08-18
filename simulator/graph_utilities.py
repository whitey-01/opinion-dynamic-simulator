from graph_tool.all import *
import random

#adds vertices to a graph taken in input. Then returns it
def addVerticesTo(graph: Graph, vertices_num: int):
    for i in range(0,vertices_num):
        graph.add_vertex()
    return graph


#generate an hypercube graph given a distance d
#the number of vertices in the graph is 2^d
#every vertex has exactly deg(v) = d
#the hypercube is built using the bitfix idea
# --WILL CHANGE--return the graph and also the binary rappresentation of the vertices 
def generateHypercubeGraph(d: int):
    vertices_num = pow(2,d)
    g = Graph(directed = False)
    #creates a new vertex property to indicate the vertex using its binary rappresentation
    binaryProperty = g.new_vertex_property("string")
    g = addVerticesTo(g,vertices_num)
    
    #time to add edges 
    for vertex in g.vertices():
        #takes the decimal index of the vertex and calculate its binary rappresentation
        index = g.vertex_index[vertex]
        binaryRapresentation = ('{0:0'+ str(d) + 'b}').format(index)
        #also writes this rappresentation to the vertex property
        binaryProperty[vertex] = binaryRapresentation
        
        #using bitFix idea, finds the neighbours of the vertex by flipping every time a different bit
        #from its binary rappresentation. For every of the d neighbours, re-calculates the decimal index 
        #from theier binary rappresentation, used for indexing them vertex in the graph. 
        bitPos = 0
        while(bitPos < d):
            bitToFlip = binaryRapresentation[bitPos]
            if bitToFlip == "0":
                neighbourVertexBinary = binaryRapresentation[0:bitPos] + str(1) + binaryRapresentation[bitPos + 1:]
            else:
                neighbourVertexBinary = binaryRapresentation[0:bitPos] + str(0) + binaryRapresentation[bitPos + 1:]
            
            neighbourVertex = g.vertex(int(neighbourVertexBinary,2))
            
            #Then adds the edge between the vertex and its neighbours 
            if g.edge(vertex,neighbourVertex) is None:
                g.add_edge(vertex,neighbourVertex)
            bitPos += 1
    return g

#generates a k-clique given the number of vertices
def generateKCliqueGraph(vertices_num: int):
    g = Graph(directed = False)
    g = addVerticesTo(g,vertices_num)

    for v1 in g.vertices():
        for v2 in g.vertices():
            if (g.vertex_index[v1] != g.vertex_index[v2]) and (g.edge(v1,v2) is None):
                g.add_edge(v1,v2)
    return g


#generates a k-cycle given the number of vertices
def generateKCycleGraph(vertices_num: int):
    g = Graph(directed=False)
    g = addVerticesTo(g, vertices_num)

    for i in range(0,len(list(g.vertices()))):
        v1 = g.vertex(i)
        if i == len(list(g.vertices())) - 1:
            v2 = g.vertex(0)
        else:
            v2 = g.vertex(i+1)

        if g.edge(v1,v2) is None:
            g.add_edge(v1,v2)
    return g
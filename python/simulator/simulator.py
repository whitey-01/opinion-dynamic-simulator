import random
import matplotlib.colors as mc
import python.simulator.simulation_result as sr
import python.simulator.simulation_configurator as sc
import graph_tool.all as gt
import copy


# module that performs a simulation and holds the implementation of the opinion-update rules


# return correct color for a vertex based on its opinion
def __color_map(opinion):
    if opinion == 0:
        # red
        return mc.hex2color("#f3722c") + (1,)
    if opinion == 1:
        # green
        return mc.hex2color("#43aa8b") + (1,)


# simulates the process on a graph using the configuration parameters specified in the configurator
# returns an object containing the results of the simulation
def runSimulationOn(simulation_configurator: sc.SimulationConfigurator, animated: bool = False):
    g: gt.Graph = simulation_configurator.graph
    # initializes the graph with the original opinion data
    g = __init_properties(g)

    # map that stores the evolution of the graph during rounds saving its properties in a tuple
    evolutionMap = {0: (copy.copy(g.vertex_properties["opinion"]), copy.copy(g.vertex_properties["opinion_color"]))}
    rounds = 0

    if animated:
        win = None
        layout = gt.sfdp_layout(g)

    while not __absorptionStateReached(g):
        # select uniformly at random a vertex from graph g
        v: gt.Vertex = g.vertex(random.randint(0, len(g.get_vertices()) - 1))
        updated_opinion: int

        if random.uniform(0, 1) <= simulation_configurator.bias:
            # get opinion 1 with probability specified in the configurator
            updated_opinion = 1
        else:
            # get updated opinion according to update rule specified in configurator
            updated_opinion = simulation_configurator.opinion_update_rule.run(g, v)

        g.vertex_properties["opinion"][v] = updated_opinion
        g.vertex_properties["opinion_color"][v] = __color_map(updated_opinion)
        rounds += 1

        evolutionMap[rounds] = (
            copy.copy(g.vertex_properties["opinion"]), copy.copy(g.vertex_properties["opinion_color"]))

        if animated:
            win = gt.graph_draw(g=g,
                                pos=layout,
                                vertex_fill_color=g.vertex_properties["opinion_color"],
                                vertex_text=g.vertex_properties["opinion"],
                                window=win,
                                output_size=(900, 900),
                                return_window=True,
                                main=False)

    # return an object containing the information produced during the simulation
    return sr.SimulationResult(evolutionMap, simulation_configurator)


# initializes the graph with the original opinion data
def __init_properties(g: gt.Graph):
    # sets properties used to keep trace of the opinion of each vertex
    opinion = g.new_vertex_property("int", 0)
    g.vertex_properties["opinion"] = opinion

    # used for graphic representation
    opinion_color = g.new_vertex_property("vector<double>")
    g.vertex_properties["opinion_color"] = opinion_color

    for v in g.vertices():
        g.vertex_properties["opinion_color"][v] = __color_map(0)
    return g


# checks if the process has reached the absorption state
def __absorptionStateReached(g: gt.Graph):
    for vertex in g.vertices():
        if g.vertex_properties["opinion"][vertex] == 0:
            return False
    return True

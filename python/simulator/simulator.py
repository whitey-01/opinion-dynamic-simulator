import random
import matplotlib.colors as mc
import python.simulator.simulation_result as sr
import python.simulator.simulation_configurator as sc
import graph_tool.all as gt
import copy


# return correct color for a vertex based on its opinion
def color_map(opinion):
    if opinion == 0:
        # red
        return mc.hex2color("#f3722c") + (1,)
    else:
        # green
        return mc.hex2color("#43aa8b") + (1,)


# simulates the process on a graph using the configuration parameters specified in the configurator
# returns an object containing the results of the simulation
def runSimulationOn(simulation_configurator: sc.SimulationConfigurator):
    g: gt.Graph = simulation_configurator.graph
    # initializes the graph with the original opinion data
    g = init_properties(g)

    # map that stores the evolution of the graph during rounds saving its properties in a tuple
    evolutionMap = {}
    evolutionMap[0] = (copy.copy(g.vertex_properties["opinion"]), copy.copy(g.vertex_properties["opinion_color"]))

    rounds = 0
    while (not absorptionStateReached(g)):
        # select UAR a vertex from graph g
        v: gt.Vertex = g.vertex(random.randint(0, len(g.get_vertices()) - 1))
        # set its opinion to 1 with probability specified in the configurator
        if random.uniform(0, 1) <= simulation_configurator.bias:
            g.vertex_properties["opinion"][v] = 1
        else:
            # set its opinion according to the opinion update rule chosen in the configurator
            if simulation_configurator.opinion_update_rule == sc.OpinionUpdateRule.MAJORITY_DYNAMICS:
                g = simulateMajorityDynamics(v, g)

            if simulation_configurator.opinion_update_rule == sc.OpinionUpdateRule.VOTER_MODEL:
                g = simulateVoterModel(v, g)

        g.vertex_properties["opinion_color"][v] = color_map(g.vertex_properties["opinion"][v])
        rounds += 1

        evolutionMap[rounds] = (
        copy.copy(g.vertex_properties["opinion"]), copy.copy(g.vertex_properties["opinion_color"]))

    # return an object containing the information produced during the simulation
    return sr.SimulationResult(evolutionMap, simulation_configurator)


# initializes the graph with the original opinion data
def init_properties(g: gt.Graph):
    # sets properties used to keep trace of the opinion of each vertex
    opinion = g.new_vertex_property("int", 0)
    g.vertex_properties["opinion"] = opinion

    # used for graphic representation
    opinion_color = g.new_vertex_property("vector<double>")
    g.vertex_properties["opinion_color"] = opinion_color

    for v in g.vertices():
        g.vertex_properties["opinion_color"][v] = color_map(0)
    return g


# simulates the Voter model update rule
def simulateVoterModel(v: gt.Vertex, g: gt.Graph):
    neighbors = list(v.all_neighbors())
    u: gt.Vertex = random.choice(neighbors)
    g.vertex_properties["opinion"][v] = g.vertex_properties["opinion"][u]
    g.vertex_properties["opinion_color"][v] = color_map(g.vertex_properties["opinion"][v])
    return g


# simulates the Majority dynamics update rule
def simulateMajorityDynamics(v: gt.Vertex, g: gt.Graph):
    opinion0_counter = 0
    opinion1_counter = 0
    for vertex in v.all_neighbors():
        if g.vertex_properties["opinion"][vertex] == 0:
            opinion0_counter += 1
        else:
            opinion1_counter += 1

    if opinion0_counter > opinion1_counter:
        g.vertex_properties["opinion"][v] = 0
        g.vertex_properties["opinion_color"][v] = color_map(0)
        return g
    if opinion1_counter > opinion0_counter:
        g.vertex_properties["opinion"][v] = 1
        g.vertex_properties["opinion_color"][v] = color_map(1)
        return g

    g.vertex_properties["opinion"][v] = random.choice([0, 1])
    g.vertex_properties["opinion_color"][v] = color_map(g.vertex_properties["opinion"][v])
    return g


# checks if the process has reached the absorption state
def absorptionStateReached(g: gt.Graph):
    for vertex in g.vertices():
        if g.vertex_properties["opinion"][vertex] == 0:
            return False
    return True

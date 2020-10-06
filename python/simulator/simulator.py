import random
import matplotlib.colors as mc
import python.simulator.simulation_result as sr
import python.simulator.simulation_configurator as sc
import graph_tool.all as gt
import copy


# module that performs a simulation and holds the implementation of the opinion-update rules

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
def runSimulationOn(simulation_configurator: sc.SimulationConfigurator, animated: bool = False):
    g: gt.Graph = simulation_configurator.graph
    # initializes the graph with the original opinion data
    g = init_properties(g)

    # map that stores the evolution of the graph during rounds saving its properties in a tuple
    evolutionMap = {0: (copy.copy(g.vertex_properties["opinion"]), copy.copy(g.vertex_properties["opinion_color"]))}
    rounds = 0

    if animated:
        win = None
        layout = gt.sfdp_layout(g)

    while not absorptionStateReached(g):
        # select UAR a vertex from graph g
        v: gt.Vertex = g.vertex(random.randint(0, len(g.get_vertices()) - 1))
        updated_opinion: int

        if random.uniform(0, 1) <= simulation_configurator.bias:
            # set its opinion to 1 with probability specified in the configurator
            updated_opinion = 1
        else:
            # set its opinion according to the opinion update rule chosen in the configurator
            if simulation_configurator.opinion_update_rule == sc.OpinionUpdateRule.MAJORITY_DYNAMIC:
                updated_opinion = simulateMajorityDynamic(v, g)

            if simulation_configurator.opinion_update_rule == sc.OpinionUpdateRule.VOTER_MODEL:
                updated_opinion = simulateVoterModel(v, g)

        g.vertex_properties["opinion"][v] = updated_opinion
        g.vertex_properties["opinion_color"][v] = color_map(updated_opinion)
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


# simulates the Voter model update rule, returns the chosen opinion
def simulateVoterModel(v: gt.Vertex, g: gt.Graph):
    neighbors = list(v.all_neighbors())
    if not len(neighbors):
        return g.vertex_properties["opinion"][v]
    u: gt.Vertex = random.choice(neighbors)
    return g.vertex_properties["opinion"][u]


# simulates the Majority dynamic update rule, returns the chosen opinion
def simulateMajorityDynamic(v: gt.Vertex, g: gt.Graph):
    neighbors = list(v.all_neighbors())
    if not len(neighbors):
        return g.vertex_properties["opinion"][v]

    opinion0_counter = 0
    opinion1_counter = 0

    for vertex in neighbors:
        if g.vertex_properties["opinion"][vertex] == 0:
            opinion0_counter += 1
        else:
            opinion1_counter += 1

    if opinion0_counter > opinion1_counter:
        return 0
    if opinion1_counter > opinion0_counter:
        return 1

    return random.choice([0, 1])


# checks if the process has reached the absorption state
def absorptionStateReached(g: gt.Graph):
    for vertex in g.vertices():
        if g.vertex_properties["opinion"][vertex] == 0:
            return False
    return True

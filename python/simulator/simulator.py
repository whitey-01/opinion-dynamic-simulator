import random
import os
import time
from enum import Enum
import matplotlib.colors as mc
import simulator.graph_utilities as gu
import simulator.simulation_result as sr
import simulator.simulation_configurator as sc
import copy
import xml.dom.minidom

#return correct color for a vertex based on its opinion
def color_map(opinion):
    if opinion == 0:
        #red
        return mc.hex2color("#f3722c") + (1,)
    else:
        #green
        return mc.hex2color("#43aa8b") + (1,)


#simulates the process on a graph using the configuration parameters specified in the configurator
#returns an object containing the results of the simulaition
def runSimulationOn(simulation_configurator: sc.SimulationConfigurator):

    g: gu.Graph = simulation_configurator.graph
    # initializes the graph with the original opinion data
    g = init_properties(g)

    #map that stores the evolution of the graph during rounds saving its properties in a tuple
    evolutionMap = {}
    evolutionMap[0] = (copy.copy(g.vertex_properties["opinion"]), copy.copy(g.vertex_properties["opinion_color"]))

    rounds = 0
    while (not absorptionStateReached(g)):
        #select UAR a vertex from graph g
        v: gu.Vertex = g.vertex(random.randint(0, len(g.get_vertices()) - 1))
        #set its opinion to 1 with probability specified in the configurator
        if random.uniform(0, 1) <= simulation_configurator.bias:
            g.vertex_properties["opinion"][v] = 1
        else:
            #set its opinion according to the opinion update rule choosen in the configurator
           if simulation_configurator.opinion_update_rule == sc.OpinionUpdateRule.MAJORITY_DYNAMICS:
               g = simulateMajorityDynamics(v, g)

           if simulation_configurator.opinion_update_rule == sc.OpinionUpdateRule.VOTER_MODEL:
               g = simulateVoterModel(v, g)

        g.vertex_properties["opinion_color"][v] = color_map(g.vertex_properties["opinion"][v])
        rounds += 1

        evolutionMap[rounds] = (copy.copy(g.vertex_properties["opinion"]), copy.copy(g.vertex_properties["opinion_color"]))

    #return an object containing the informations produced during the simulation
    return sr.SimulationResult(evolutionMap, simulation_configurator)


#initializes the graph with the original opinion data
def init_properties(g: gu.Graph):
    # sets properties used to keep trace of the opinion of each vertex
    opinion = g.new_vertex_property("int", 0)
    g.vertex_properties["opinion"] = opinion

    # used for graphic rapresentation
    opinion_color = g.new_vertex_property("vector<double>")
    g.vertex_properties["opinion_color"] = opinion_color

    for v in g.vertices():
        g.vertex_properties["opinion_color"][v] = color_map(0)
    return g



#simulates the Voter model update rule
def simulateVoterModel(v: gu.Vertex, g: gu.Graph):
    neighbors = list(v.all_neighbors())
    u: gu.Vertex = random.choice(neighbors)
    g.vertex_properties["opinion"][v] = g.vertex_properties["opinion"][u]
    g.vertex_properties["opinion_color"][v] = color_map(g.vertex_properties["opinion"][v])
    return g


#simulates the Majority dynamics update rule
def simulateMajorityDynamics(v: gu.Vertex, g: gu.Graph):
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

    g.vertex_properties["opinion"][v] = random.choice([0,1])
    g.vertex_properties["opinion_color"][v] = color_map(g.vertex_properties["opinion"][v])
    return g


#checks if the process has reached the absorption state
def absorptionStateReached(g: gu.Graph):
    for vertex in g.vertices():
        if g.vertex_properties["opinion"][vertex] == 0:
            return False
    return True


#runs a simulation (same graph and configuration) multiple times
#returns a list of SimulationResult objects
def runMultipleSimulations(config: sc.SimulationConfigurator, repetitions: int):
    simulations = []
    g: gu.Graph = config.graph
    for i in range(0,repetitions):
        simulations.append(runSimulationOn(config))
        print("simulation " + str(i) + " processed")
    return simulations

#save as xml the results of multiple simulations on the same configuration
def saveMultipleSimulationsDataAsXML(config:sc.SimulationConfigurator, simulations: list, file_name, directory = ""):
    simulations_file = "<simulations>"
    simulations_file += "<simulations-config>" + config.configXMLSerializer() + "</simulations-config>"
    average_rounds = 0;
    for simulation in simulations:
        simulation: sr.SimulationResult = simulation
        simulation_tag = "<simulation>" \
                            "<simulation-id>" + simulation.simulation_id + "</simulation-id>"  \
                            "<simulation-rounds>" + str(simulation.rounds) + "</simulation-rounds>" \
                         "</simulation>"
        simulations_file += simulation_tag
        average_rounds += simulation.rounds

    average_rounds = int(average_rounds / len(simulations))
    simulations_file += "<simulations-average-rounds>" + str(average_rounds) + "</simulations-average-rounds>"
    simulations_file += "</simulations>"
    dom = xml.dom.minidom.parseString(simulations_file)
    pretty_xml_as_string = dom.toprettyxml()
    with open(directory + file_name + ".xml", "w") as f:
        f.write(pretty_xml_as_string)
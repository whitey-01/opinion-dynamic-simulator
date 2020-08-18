import random
import os
import time
from enum import Enum
import g
import matplotlib.colors as mc
import graph_utilities as gu

OUTPUT_DIR = "../output/"
SIMULATIONS_DIR = OUTPUT_DIR + "simulations/"

#return correct color for a vertex based on its opinion
def color_map(opinion):
    if opinion == 0:
        #red
        return mc.hex2color("#f3722c") + (1,)
    else:
        #green
        return mc.hex2color("#43aa8b") + (1,)


#defines two opinions update rules available
class OpinionUpdateRule(Enum):
    VOTER_MODEL = "voter-rule"
    MAJORITY_DYNAMICS = "majority-dynamics"

#defines an object used to configure the simulation correctly
#holds the graph and other config parameters
class SimulationConfigurator:
    def __init__(self, graph: gu.Graph, bias: float, opinion_update_rule: OpinionUpdateRule, comment: str = "OPTIONAL COMMENT"):
        self.graph = graph
        if opinion_update_rule != OpinionUpdateRule.MAJORITY_DYNAMICS and opinion_update_rule != OpinionUpdateRule.VOTER_MODEL:
            raise Exception("Error:- Invalid opinion update rule!")
        self.opinion_update_rule = opinion_update_rule
        #define how much agent are biased towards the dominant opinion
        self.bias = bias
        self.comment = comment



#simulates the process on a graph using the configuration parameters specified in the configurator
#returns an object containing the results of the simulaition
def runSimulationOn(simulation_configurator: SimulationConfigurator):

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
           if simulation_configurator.opinion_update_rule == OpinionUpdateRule.MAJORITY_DYNAMICS:
               g = simulateMajorityDynamics(v, g)

           if simulation_configurator.opinion_update_rule == OpinionUpdateRule.VOTER_MODEL:
               g = simulateVoterModel(v, g)

        g.vertex_properties["opinion_color"][v] = color_map(g.vertex_properties["opinion"][v])
        rounds += 1

        evolutionMap[rounds] = (copy.copy(g.vertex_properties["opinion"]), copy.copy(g.vertex_properties["opinion_color"]))

    #return an object containing the informations produced during the simulation
    return SimulationResult(evolutionMap, simulation_configurator)


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






#holds the informations produced during the simulation
#also provides methods to save these informations
class SimulationResult:
    def __init__(self, evolutionMap: dict, simulation_configurator: SimulationConfigurator):
        self.simulation_id = ts = str(time.time()).replace(".","")
        self.rounds = len(evolutionMap) - 1
        self.evolutionMap = evolutionMap
        self.simulation_configurator = simulation_configurator
        self.original_graph = simulation_configurator.graph

    #generates a folder in output/simulations named with the samulation id
    #in this folder saves an xml file of the graph, an xml file of the simulation, a .png of the graph
    #and a folder containing png's of the graph showing the evolution of process
    def saveSimulationData(self):

        if not os.path.isdir(OUTPUT_DIR):
            os.mkdir(OUTPUT_DIR)
        if not os.path.isdir(SIMULATIONS_DIR):
            os.mkdir(SIMULATIONS_DIR)

        simulation_dir = SIMULATIONS_DIR + "s_" + self.simulation_id + "/"
        os.mkdir(simulation_dir)
        evolution_img_dir = simulation_dir + "evolution_imgs/"
        os.mkdir(evolution_img_dir)

        with open(simulation_dir + "simulation.xml", "w") as f:
            f.write(self.getSimulationDataAsXML())

        self.original_graph.save(simulation_dir + "graph.xml")

        #0%, 25%, 50%, 75%, 100%
        steps = [0]
        steps.append(int(self.rounds / 100 * 25))
        steps.append(int(self.rounds / 100 * 50))
        steps.append(int(self.rounds / 100 * 75))
        steps.append(self.rounds)


        layout = gu.sfdp_layout(self.original_graph)
        gu.graph_draw(self.original_graph,
                      pos=layout,
                      vertex_text=self.original_graph.vertex_index,
                      vertex_text_color=(1, 1, 1, 1),
                      edge_color=(1, 1, 1, 0.7),
                      output=simulation_dir + "graph.png",
                      output_size=(1600, 1600),
                      adjust_aspect=False,
                      bg_color=(0.09411764705882353, 0.11372549019607843, 0.15294117647058825, 1))

        # print graph evolution in .png
        for step in steps:
            opinion = self.evolutionMap[step][0]
            opinion_color = self.evolutionMap[step][1]
            gu.graph_draw(self.original_graph,
                          pos= layout,
                          vertex_color=(1,1,1,0),
                          vertex_fill_color=opinion_color,
                          vertex_text=opinion,
                          vertex_text_color=(1,1,1,1),
                          edge_color=(1,1,1,0.7),
                          output=evolution_img_dir + "round-" + str(step) + ".png",
                          output_size=(1600,1600),
                          adjust_aspect=False,
                          bg_color=(0.09411764705882353, 0.11372549019607843, 0.15294117647058825,1))



    def printSimulationData(self):
        print("")
        print("-------Simulation-------")
        print("Simulation with id " + self.simulation_id)
        print("The opinion update rule choosen was " + self.simulation_configurator.opinion_update_rule.value)
        print("The bias towards the dominant opinion was " + str(self.simulation_configurator.bias))
        print("Reaching the absorption state took " + str(self.rounds) + " rounds")

    def getSimulationDataAsXML(self):
        xmlContent = "<simulation>\n"
        comment = "    <simulation-comment>" + self.simulation_configurator.comment + "</simulation-comment>\n"
        id = "    <simulation-id>" + self.simulation_id + "</simulation-id>\n"
        dynamic = "    <simulation-update-rule>" + self.simulation_configurator.opinion_update_rule.value + "</simulation-update-rule>\n"
        bias = "    <simulation-bias>" + str(self.simulation_configurator.bias) + "</simulation-bias>\n"
        rounds = "    <simulation-rounds>" + str(self.rounds) + "</simulation-rounds>\n"
        return xmlContent + comment + id + dynamic + bias + rounds + "</simulation>"


#runs a simulation (same graph and configuration) multiple times
#returns a list of SimulationResult objects
def runMultipleSimulations(config: SimulationConfigurator, repetitions: int):
    simulations = []
    g: gu.Graph = config.graph
    for i in range(0,repetitions):
        simulations.append(runSimulationOn(config,g))
    return simulations
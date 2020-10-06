import python.simulator.simulation_configurator as sc
import time
import os
import graph_tool.all as gt
import xml.dom.minidom

OUTPUT_DIR = "output/"
SIMULATIONS_DIR = OUTPUT_DIR + "simulations/"


# module that defines the simulation results and provides methods to output those results

# holds the information produced during the simulation
# also provides methods to save these information
class SimulationResult:
    def __init__(self, evolutionMap: dict, simulation_configurator: sc.SimulationConfigurator):
        self.simulation_id = str(time.time()).replace(".", "")
        self.rounds = len(evolutionMap) - 1
        self.evolutionMap = evolutionMap
        self.simulation_configurator = simulation_configurator
        self.original_graph = simulation_configurator.graph

    # generates a folder in output/simulations named with the simulation id
    # in this folder saves an xml file of the graph, an xml file of the simulation, a .png of the graph
    # and a folder containing images of the graph showing the evolution of process
    def saveSimulation(self):

        if not os.path.isdir(OUTPUT_DIR):
            os.mkdir(OUTPUT_DIR)
        if not os.path.isdir(SIMULATIONS_DIR):
            os.mkdir(SIMULATIONS_DIR)

        simulation_dir = SIMULATIONS_DIR + "s_" + self.simulation_id + "/"
        os.mkdir(simulation_dir)
        evolution_img_dir = simulation_dir + "evolution_imgs/"
        os.mkdir(evolution_img_dir)

        self.exportSimulationOutputAsXML(dir=simulation_dir)

        # exports graph structure  in xml: key0 and key1 are respectively opinion property and opinion color property
        self.original_graph.save(simulation_dir + "graph.xml")

        # 0%, 25%, 50%, 75%, 100%
        steps = [0]
        steps.append(int(self.rounds / 100 * 25))
        steps.append(int(self.rounds / 100 * 50))
        steps.append(int(self.rounds / 100 * 75))
        steps.append(self.rounds)

        layout = gt.sfdp_layout(self.original_graph)
        gt.graph_draw(self.original_graph,
                      pos=layout,
                      vertex_text=self.original_graph.vertex_index,
                      vertex_text_color=(1, 1, 1, 1),
                      edge_color=(1, 1, 1, 0.7),
                      output=simulation_dir + "graph.png",
                      output_size=(1600, 1600),
                      adjust_aspect=False,
                      bg_color=(0.09411764705882353, 0.11372549019607843, 0.15294117647058825, 1))

        # prints graph evolution in .png
        for step in steps:
            opinion = self.evolutionMap[step][0]
            opinion_color = self.evolutionMap[step][1]
            gt.graph_draw(self.original_graph,
                          pos=layout,
                          vertex_color=(1, 1, 1, 0),
                          vertex_fill_color=opinion_color,
                          vertex_text=opinion,
                          vertex_text_color=(1, 1, 1, 1),
                          edge_color=(1, 1, 1, 0.7),
                          output=evolution_img_dir + "round-" + str(step) + ".png",
                          output_size=(1600, 1600),
                          adjust_aspect=False,
                          bg_color=(0.09411764705882353, 0.11372549019607843, 0.15294117647058825, 1))

    def exportSimulationOutputAsXML(self, dir):
        simulations_file = "<simulation>"
        simulations_file += "<simulation-id>" + self.simulation_id + "</simulation-id>"
        simulations_file += "<!-- Configuration used during the simulation -->"
        simulations_file += "<simulation-config>" + self.simulation_configurator.configXMLSerializer() + "</simulation-config>"
        simulations_file += "<!-- rounds needed to reach absorbing state -->"
        simulations_file += "<simulation-rounds>" + str(self.rounds) + "</simulation-rounds>"
        simulations_file += "</simulation>"
        dom = xml.dom.minidom.parseString(simulations_file)
        pretty_xml_as_string = dom.toprettyxml()
        with open(dir + "simulation_result.xml", "w") as f:
            f.write(pretty_xml_as_string)

    def printSimulationData(self):
        print("")
        print("-------Simulation-------")
        print("Simulation with id " + self.simulation_id)
        print("The opinion update rule chosen was " + self.simulation_configurator.opinion_update_rule.__class__.__name__)
        print("The bias towards the dominant opinion was " + str(self.simulation_configurator.bias))
        print("Reaching the absorption state took " + str(self.rounds) + " rounds")

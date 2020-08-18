import simulator.simulation_configurator as sc
import time
import os
import simulator.graph_utilities as gu
import xml.dom.minidom



OUTPUT_DIR = "output/"
SIMULATIONS_DIR = OUTPUT_DIR + "simulations/"


#holds the informations produced during the simulation
#also provides methods to save these informations
class SimulationResult:
    def __init__(self, evolutionMap: dict, simulation_configurator: sc.SimulationConfigurator):
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

        self.saveConfigurationDataAsXML("s_" + self.simulation_id + "/")
        self.saveSimulationOutputAsXML("s_" + self.simulation_id + "/")
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




    def saveConfigurationDataAsXML(self, simulation_id_path = ""):
        dom = xml.dom.minidom.parseString(self.simulation_configurator.configXMLSerializer())
        pretty_xml_as_string = dom.toprettyxml()
        with open(SIMULATIONS_DIR + simulation_id_path +  "configuration.xml", "w") as f:
            f.write(pretty_xml_as_string)

    def saveSimulationOutputAsXML(self, simulation_id_path):
        simulations_file = "<simulation>"
        rounds = "<simulation-rounds>" + str(self.rounds) + "</simulation-rounds>"
        simulations_file = simulations_file + rounds + "</simulation>"
        dom = xml.dom.minidom.parseString(simulations_file)
        pretty_xml_as_string = dom.toprettyxml()
        with open(SIMULATIONS_DIR + simulation_id_path +  "simulation_result.xml", "w") as f:
            f.write(pretty_xml_as_string)

    def printSimulationData(self):
        print("")
        print("-------Simulation-------")
        print("Simulation with id " + self.simulation_id)
        print("The opinion update rule choosen was " + self.simulation_configurator.opinion_update_rule.value)
        print("The bias towards the dominant opinion was " + str(self.simulation_configurator.bias))
        print("Reaching the absorption state took " + str(self.rounds) + " rounds")

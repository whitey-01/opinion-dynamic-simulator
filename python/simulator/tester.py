import graph_tool.all as gt
import python.simulator.simulation_configurator as sc
import python.simulator.simulator as sim
import python.simulator.simulation_result as sr
import xml.dom.minidom
import os
import time

# module that define what is a test. A est is an execution of multiple simulations on the same graph and configuration
# also provides method to output the test results

OUTPUT_DIR = "output/"
TESTS_DIR = OUTPUT_DIR + "tests/"


# returns a list of SimulationResult objects
def runTest(config: sc.SimulationConfigurator, repetitions: int):
    simulations = []
    for i in range(0, repetitions):
        simulations.append(sim.runSimulationOn(config))
        print("simulation " + str(i) + " processed")
    return simulations


# save as xml the results of multiple simulations on the same configuration
def saveTestDataAsXML(config: sc.SimulationConfigurator, simulations: list):
    if not os.path.isdir(OUTPUT_DIR):
        os.mkdir(OUTPUT_DIR)
    if not os.path.isdir(TESTS_DIR):
        os.mkdir(TESTS_DIR)

    testID = str(time.time()).replace(".", "")
    testDir = TESTS_DIR + "/t_" + testID + "/"
    os.mkdir(testDir)

    config.graph.save(testDir + "graph.xml")
    gt.graph_draw(config.graph,
                  vertex_text=config.graph.vertex_index,
                  vertex_text_color=(1, 1, 1, 1),
                  edge_color=(1, 1, 1, 0.7),
                  output=testDir + "graph.png",
                  output_size=(1600, 1600),
                  adjust_aspect=False,
                  bg_color=(0.09411764705882353, 0.11372549019607843, 0.15294117647058825, 1))

    test = "<test>"
    test += "<test-id>" + testID + "</test-id>"
    test += "<!-- Number of simulations executed during the test -->"
    test += "<test-repetitions>" + str(len(simulations)) + "</test-repetitions>"
    test += "<!-- Test configuration shared by simulations -->"
    test += "<test-config>" + config.configXMLSerializer() + "</test-config>"
    average_rounds = 0
    for simulation in simulations:
        simulation: sr.SimulationResult = simulation
        simulation_tag = "<simulation>" \
                         "<simulation-id>" + simulation.simulation_id + "</simulation-id>" \
                                                                        "<simulation-rounds>" + str(
            simulation.rounds) + "</simulation-rounds>" \
                                 "</simulation>"
        test += simulation_tag
        average_rounds += simulation.rounds

    average_rounds = int(average_rounds / len(simulations))
    test += "<!-- average rounds needed to reach absorbing state -->"
    test += "<test-average-rounds>" + str(average_rounds) + "</test-average-rounds>"
    test += "</test>"
    dom = xml.dom.minidom.parseString(test)
    pretty_xml_as_string = dom.toprettyxml()
    with open(testDir + "test_result.xml", "w") as f:
        f.write(pretty_xml_as_string)

    print("Test saved with ID " + testID)

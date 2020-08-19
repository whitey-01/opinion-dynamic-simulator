import simulator.graph_utilities as gu
import simulator.simulation_configurator as sc
import simulator.simulator as sim
import xml.dom.minidom
import os
import time

#a Test is an execution of multiple simulation on the same graph and configuration

OUTPUT_DIR = "output/"
TESTS_DIR = OUTPUT_DIR + "tests/"

#returns a list of SimulationResult objects
def runTest(config: sc.SimulationConfigurator, repetitions: int):
    simulations = []
    g: gu.Graph = config.graph
    for i in range(0,repetitions):
        simulations.append(sim.runSimulationOn(config))
        print("simulation " + str(i) + " processed")
    return simulations


#save as xml the results of multiple simulations on the same configuration
def saveTestDataAsXML(config:sc.SimulationConfigurator, simulations: list):
    if not os.path.isdir(OUTPUT_DIR):
        os.mkdir(OUTPUT_DIR)
    if not os.path.isdir(TESTS_DIR):
        os.mkdir(TESTS_DIR)

    testID = str(time.time()).replace(".","")

    test = "<test>"
    test += "<test-id>" + testID + "</test-id>"
    test += "<test-config>" + config.configXMLSerializer() + "</test-config>"
    average_rounds = 0;
    for simulation in simulations:
        simulation: sr.SimulationResult = simulation
        simulation_tag = "<simulation>" \
                            "<simulation-id>" + simulation.simulation_id + "</simulation-id>"  \
                            "<simulation-rounds>" + str(simulation.rounds) + "</simulation-rounds>" \
                         "</simulation>"
        test += simulation_tag
        average_rounds += simulation.rounds

    average_rounds = int(average_rounds / len(simulations))
    test += "<test-average-rounds>" + str(average_rounds) + "</test-average-rounds>"
    test += "</test>"
    dom = xml.dom.minidom.parseString(test)
    pretty_xml_as_string = dom.toprettyxml()
    with open(TESTS_DIR + "t_" + testID +  ".xml", "w") as f:
        f.write(pretty_xml_as_string)
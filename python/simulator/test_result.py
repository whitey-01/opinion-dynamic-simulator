import graph_tool.all as gt
import python.simulator.test_configurator as tc
import time
import os
import xml.dom.minidom
import math

OUTPUT_DIR = "output/"
TESTS_DIR = OUTPUT_DIR + "tests/"


class TestResult:
    def __init__(self, testConfigurator: tc.TestConfigurator, results: list):
        self.testConfigurator = testConfigurator
        self.results = results
        self.test_id = str(time.time()).replace(".", "")

    def saveTest(self, draw: bool = False):
        if not os.path.isdir(OUTPUT_DIR):
            os.mkdir(OUTPUT_DIR)
        if not os.path.isdir(TESTS_DIR):
            os.mkdir(TESTS_DIR)

        test_dir = TESTS_DIR + "/t_" + self.test_id + "/"
        os.mkdir(test_dir)

        self.exportTestOutputAsXML(test_dir=test_dir)
        self.testConfigurator.simulationConfigurator.graph.save(test_dir + "graph.xml")

        if draw:
            gt.graph_draw(self.testConfigurator.simulationConfigurator.graph,
                          vertex_text=self.testConfigurator.simulationConfigurator.graph.vertex_index,
                          vertex_text_color=(1, 1, 1, 1),
                          edge_color=(1, 1, 1, 0.7),
                          output=test_dir + "graph.png",
                          output_size=(1600, 1600),
                          adjust_aspect=False,
                          bg_color=(0.09411764705882353, 0.11372549019607843, 0.15294117647058825, 1))

    def exportTestOutputAsXML(self, test_dir: str):
        test = "<test>"
        test += "<!-- Test Configuration -->"
        test += self.testConfigurator.configXMLSerializer()
        test += "<test-simulations>"

        mean = 0
        for result in self.results:
            simulation_tag = "<simulation>" \
                             "<simulation-id>" + result["simulation_id"] + "</simulation-id>" \
                                                                           "<simulation-rounds>" + str(
                result["simulation_rounds"]) + "</simulation-rounds>" \
                                               "</simulation>"
            test += simulation_tag
            mean += result["simulation_rounds"]
        test += "</test-simulations>"
        mean = int(mean / self.testConfigurator.iterations)
        test += "<!-- average rounds needed to reach absorbing state -->"
        test += "<test-average-rounds>" + str(mean) + "</test-average-rounds>"
        test += "<!-- standard deviation from the mean -->"
        test += "<test-standard-deviation>" + str(self.calcStandardDeviation(mean)) + "</test-standard-deviation>"
        test += "</test>"

        dom = xml.dom.minidom.parseString(test)
        pretty_xml_as_string = dom.toprettyxml()
        with open(test_dir + "test_result.xml", "w") as f:
            f.write(pretty_xml_as_string)

        print("Test saved with ID " + self.test_id)

    def calcStandardDeviation(self, mean: int):
        variance = 0
        for result in self.results:
            variance += math.pow((result["simulation_rounds"] - mean), 2)

        variance = variance / (self.testConfigurator.iterations - 1)
        return math.sqrt(variance)

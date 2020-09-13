import xml.etree.ElementTree as et
import os as os
import math

# simple module that allows you to unifies different tests in one.

OUTPUT_DIR = "output/"
TESTS_DIR = OUTPUT_DIR + "tests/"


def getListOfTest():
    tests = list()
    for root, dirs, files in os.walk(TESTS_DIR, topdown=False):
        for name in dirs:
            tests.append(os.path.join(root, name))
    return tests


class TestUnifier:

    # if auto_retrieve_tests is true then you don't need to pass tests list
    def __init__(self, auto_retrieve_tests: bool = True, my_tests: list = None):
        if auto_retrieve_tests and my_tests is None:
            print("Auto-retrieving tests\n")
            self.tests = getListOfTest()
        else:
            print("Using passed tests list")
            self.tests = []
            for test in my_tests:
                self.tests.append(TESTS_DIR + test)

    def obtainMeanAndDeviation(self):
        rounds_list = list()
        mean = 0
        count = 0
        for test in self.tests:
            root = et.parse(test + "/test_result.xml").getroot()

            for simulation in root.iter("simulation"):
                mean += int(simulation.find("simulation-rounds").text)
                rounds_list.append(int(simulation.find("simulation-rounds").text))
                count += 1
        mean = round(mean / count, 2)

        variance = 0
        for rounds in rounds_list:
            variance += math.pow((rounds - mean), 2)

        variance = variance / (count - 1)
        stdDeviation = round(math.sqrt(variance), 2)
        print("Mean = " + str(mean))
        print("Standard Deviation = " + str(stdDeviation))
        return mean, stdDeviation


# mean, deviation = TestUnifier(auto_retrieve_tests=True).obtainMeanAndDeviation()

mean, deviation = TestUnifier(my_tests=["t_15996928933660312"]).obtainMeanAndDeviation()
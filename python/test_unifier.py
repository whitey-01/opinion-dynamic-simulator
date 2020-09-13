import xml.etree.ElementTree as et
import os
import math

# simple module that allows you to unifies different tests in one.


# WIP:- recreate new XML with references to original test files

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

    # WARNING:- if you use auto retrieving, make sure that all tests in test directory
    # are made on the same configuration or will have unusable data
    def __init__(self, auto_retrieve_tests: bool = True, testIDsList: list = None):
        if auto_retrieve_tests and not testIDsList:
            print("Auto-retrieving tests from " + TESTS_DIR + "\n")
            self.tests = getListOfTest()
        elif testIDsList:
            print("Using passed tests list\n")
            self.tests = []
            for id in testIDsList:
                self.tests.append(TESTS_DIR + "t_" + id)
        else:
            raise Exception("Error:- Invalid initializer. Either the list in NOT empty or auto-retrieve is left to True")

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


# auto-retrieving tests example
mean, deviation = TestUnifier().obtainMeanAndDeviation()

# passing data manually example
# mean, deviation = TestUnifier(testIDsList=["15996928933660312", "15997520452320051"]).obtainMeanAndDeviation()

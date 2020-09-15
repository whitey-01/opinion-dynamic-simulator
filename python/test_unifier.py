import xml.etree.ElementTree as et
import os
import math

# simple module that allows you to unifies different tests in one.


# WIP:- recreate new XML with references to original test files

OUTPUT_DIR = "output/"
TESTS_DIR = OUTPUT_DIR + "tests/"


def getListOfTests():
    tests = list()
    for root, dirs, files in os.walk(TESTS_DIR, topdown=False):
        for name in dirs:
            tests.append(os.path.join(root, name))
    return tests


def calcStandardDeviation(data: list, mean: float, count: int):
    variance = 0
    for d in data:
        variance += math.pow((d - mean), 2)

    variance = variance / (count - 1)
    return round(math.sqrt(variance), 2)


class TestUnifier:

    # if auto_retrieve_tests is true then you don't need to pass tests list

    # WARNING:- if you use auto retrieving, make sure that all tests in test directory
    # are made on the same configuration or it will output unusable/inconsistent data
    def __init__(self, auto_retrieve_tests: bool = True, testIDsList: list = None):
        if auto_retrieve_tests and not testIDsList:
            print("Auto-retrieving tests from " + TESTS_DIR + "\n")
            self.tests = getListOfTests()
        elif testIDsList:
            print("Using provided tests list\n")
            self.tests = []
            for ID in testIDsList:
                self.tests.append(TESTS_DIR + "t_" + ID)
        else:
            raise Exception(
                "Error:- Invalid initializer. Either the list in NOT empty or auto-retrieve is left to True")

    def obtainMeanAndDeviation(self):
        rounds_list = list()
        mean = 0
        count = 0
        for test in self.tests:
            try:
                root = et.parse(test + "/test_result.xml").getroot()
            except:
                print("Test " + test + " not found. Skipping it.")
                continue

            for simulation in root.iter("simulation"):
                mean += int(simulation.find("simulation-rounds").text)
                rounds_list.append(int(simulation.find("simulation-rounds").text))
                count += 1
        if mean == 0:
            raise Exception("Error:- No test has been found")

        mean = round(mean / count, 2)
        return mean, calcStandardDeviation(rounds_list, mean, count)


# auto-retrieving tests example
mean, deviation = TestUnifier().obtainMeanAndDeviation()

# Providing data manually example
# mean, deviation = TestUnifier(testIDsList=["12343242345345"]).obtainMeanAndDeviation()

print("Mean = " + str(mean))
print("Standard Deviation = " + str(deviation))

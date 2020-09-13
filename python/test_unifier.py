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


# if obtainAllTest is true then you don't need to pass tests list
def obtainMeanAndDeviationFrom(obtainAllTest: bool = True, tests: list = None):
    if obtainAllTest and tests is None:
        print("Auto-obtaining tests\n")
        tests = getListOfTest()
    else:
        print("Using passed tests list")

    rounds_list = list()
    mean = 0
    count = 0
    for test in tests:
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
    return mean, round(math.sqrt(variance), 2)


mean, stdDeviation = obtainMeanAndDeviationFrom(obtainAllTest=True)
print("Mean = " + str(mean))
print("Standard Deviation = " + str(stdDeviation))
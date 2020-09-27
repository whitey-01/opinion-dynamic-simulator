import math
import random
import python.simulator.test_configurator as tc
import python.simulator.test_result as tr
import python.simulator.tester as ts
import python.simulator.simulation_configurator as sc
import python.simulator.graph_generator as gg

# simple main that performs a test by running multiple simulation on a fixed config.
ITERATIONS = 100

n = 128
p = 1/n
print(p)

graph = gg.generateERGraph(n, p)

simulationConfigurator = sc.SimulationConfigurator(graph=graph,
                                                   bias=0.25,
                                                   opinion_update_rule=sc.OpinionUpdateRule.MAJORITY_DYNAMICS,
                                                   comment="Erdos–Renyi " + str(n) + " nodi, p = 1/n")

testConfigurator = tc.TestConfigurator(simulationConfigurator=simulationConfigurator, iterations=ITERATIONS)

# returns a list of dicts containing simulations id and rounds
results = ts.runTest(testConfigurator=testConfigurator)

testResult = tr.TestResult(testConfigurator=testConfigurator, results=results)
testResult.saveTest(draw=True)

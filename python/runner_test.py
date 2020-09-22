import python.simulator.test_configurator as tc
import python.simulator.test_result as tr
import python.simulator.tester as ts
import python.simulator.simulation_configurator as sc
import python.simulator.graph_generator as gg

# simple main that performs a test by running multiple simulation on a fixed config.
ITERATIONS = 10

graph = gg.generateHypercubeGraph(d=12)
# graph = gg.generateKCliqueGraph(64)
# graph = gg.generateKCycleGraph(1024)
# graph = gg.generateERGraph(32)

simulationConfigurator = sc.SimulationConfigurator(graph=graph,
                                                   bias=0.25,
                                                   opinion_update_rule=sc.OpinionUpdateRule.MAJORITY_DYNAMICS,
                                                   comment="Ipercubo 4096 nodi")

testConfigurator = tc.TestConfigurator(simulationConfigurator=simulationConfigurator, iterations=ITERATIONS)

# returns a list of dicts containing simulations id and rounds
results = ts.runTest(testConfigurator=testConfigurator)

testResult = tr.TestResult(testConfigurator=testConfigurator, results=results)
testResult.saveTest(draw=False)


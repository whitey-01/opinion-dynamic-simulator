import python.simulator.tester as ts
import python.simulator.simulation_configurator as sc
import python.simulator.graph_generator as gg

#simple main that performs a test by running multiple simulation on a fixed config.
ITERATIONS = 50

graph = gg.generateHypercubeGraph(9)
#graph = gu.generateKCycleGraph(45)
config = sc.SimulationConfigurator(graph=graph,
                                   bias=0.40,
                                   opinion_update_rule=sc.OpinionUpdateRule.VOTER_MODEL)


#returns a list of SimulationResult objects
simulations = ts.runTest(config, ITERATIONS)

#file_name without extension, separated optional param directory
ts.saveTestDataAsXML(config=config, simulations=simulations)

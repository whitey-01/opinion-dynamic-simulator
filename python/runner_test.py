import simulator.tester as ts
import simulator.simulation_configurator as sc
import simulator.simulation_result as sr
import simulator.graph_utilities as gu

#simple main that performs a test by running multiple simulation on a fixed config.
ITERATIONS = 150

#graph = gu.generateHypercubeGraph(8)
graph = gu.generateKCycleGraph(45)
config = sc.SimulationConfigurator(graph=graph,
                                   bias=0.30,
                                   opinion_update_rule=sc.OpinionUpdateRule.MAJORITY_DYNAMICS)


#returns a list of SimulationResult objects
simulations = ts.runTest(config, ITERATIONS)

#file_name without extension, separated optional param directory
ts.saveTestDataAsXML(config=config, simulations=simulations)
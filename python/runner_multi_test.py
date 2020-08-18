import simulator.simulator as sim
import simulator.simulation_configurator as sc
import simulator.simulation_result as sr
import simulator.graph_utilities as gu

#simple main that runs a simulation multiple times and output a list of simulation objects
ITERATIONS = 100

graph = gu.generateKCycleGraph(20)
config = sc.SimulationConfigurator(graph=graph, bias=0.5, opinion_update_rule=sc.OpinionUpdateRule.MAJORITY_DYNAMICS)


#returns a list of SimulationResult objects
simulations = sim.runMultipleSimulations(config, ITERATIONS)

#file_name without extension, separated optional param directory
sim.saveMultipleSimulationsDataAsXML(config=config, simulations=simulations, file_name="test1")
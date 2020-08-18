import simulator.simulator as sim
import simulator.simulation_configurator as sc
import simulator.simulation_result as sr
import simulator.graph_utilities as gu

#simple main that runs a simulation multiple times and output a list of simulation objects
ITERATIONS = 200

graph = gu.generateKCliqueGraph(20, False)
config = sc.SimulationConfigurator(graph=graph, bias=0.75, opinion_update_rule=sc.OpinionUpdateRule.MAJORITY_DYNAMICS)


#returns a list of SimulationResult objects
simulations = sim.runMultipleSimulations(config, ITERATIONS)

sim.saveMultipleSimulationsData()
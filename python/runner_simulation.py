import python.simulator.simulator as sim
import python.simulator.simulation_configurator as sc
import python.simulator.simulation_result as sr
import python.simulator.graph_generator as gg

# simple main that performs a simulation of the process

graph = gg.generateHypercubeGraph(3)
# graph = gg.generateKCliqueGraph(28)
# graph = gg.generateKCycleGraph(25)

config = sc.SimulationConfigurator(graph=graph,
                                   bias=0.6,
                                   opinion_update_rule=sc.OpinionUpdateRule.VOTER_MODEL)

simulationResult: sr.SimulationResult = sim.runSimulationOn(config)

# print simulation data such as rounds, configuration parameters ecc..
simulationResult.printSimulationData()

# save all information about simulation
# save images of the graph showing the diffusion of the opinion at rounds: 0, 25%, 50%, 75%, 100%
# save in output/simulations
simulationResult.saveSimulation()

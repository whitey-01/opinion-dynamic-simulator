import python.simulator.simulator as sim
import python.simulator.simulation_configurator as sc
import python.simulator.simulation_result as sr
import python.simulator.graph_generator as gg

# simple main that performs a simulation of the process


graph = gg.generateERGraph(vertices_num=256, p=1/256)

config = sc.SimulationConfigurator(graph_desc="Erdos–Renyi 256 nodi, p = 1/n",
                                   graph=graph,
                                   bias=0.25,
                                   opinion_update_rule=sc.OpinionUpdateRule.MAJORITY_DYNAMIC)

simulationResult: sr.SimulationResult = sim.runSimulationOn(config)

# print simulation data such as rounds, configuration parameters ecc..
simulationResult.printSimulationData()

# save all information about simulation
# save images of the graph showing the diffusion of the opinion at rounds: 0, 25%, 50%, 75%, 100%
# save in output/simulations
simulationResult.saveSimulation()

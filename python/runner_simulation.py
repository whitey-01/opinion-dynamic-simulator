import simulator.simulator as sim
import simulator.simulation_configurator as sc
import simulator.simulation_result as sr
import simulator.graph_utilities as gu

#simple main that performs a simulation of the process

#graph = gu.generateHypercubeGraph(8)
#graph = gu.generateKCliqueGraph(20)
graph = gu.generateKCycleGraph(25)

config = sc.SimulationConfigurator(graph=graph,
                                    bias=0.45,
                                    opinion_update_rule=sc.OpinionUpdateRule.VOTER_MODEL)

simulationResult: sr.SimulationResult = sim.runSimulationOn(config)

#print simulation data such as rounds, configuration parameters ecc..
simulationResult.printSimulationData()

#save all informations about simulation
#save png's of the graph showing the diffusion of the opinion at rounds: 0, 25%, 50%, 75%, 100%
#save in output/simulations
simulationResult.saveSimulation()

import simulator.simulator as sim
import simulator.simulation_configurator as sc
import simulator.simulation_result as sr
import simulator.graph_utilities as gu

#simple main that generate a graph and test the simulator

graph = gu.generateHypercubeGraph(6)
#graph = gu.generateKCliqueGraph(15)
#graph = gu.generateKCycleGraph(60)

config = sc.SimulationConfigurator(graph=graph,
                                    bias=0.35,
                                    opinion_update_rule=sc.OpinionUpdateRule.MAJORITY_DYNAMICS,
                                    comment="Ipercubo di distanza 6")
simulationResult: sr.SimulationResult = sim.runSimulationOn(config)

#print simulation data such as rounds, configuration parameters ecc..
simulationResult.printSimulationData()

#save all informations about simulation
#save png's of the graph showing the diffusion of the opinion at rounds: 0, 25%, 50%, 75%, 100%
#save in output/simulations
simulationResult.saveSimulationData()

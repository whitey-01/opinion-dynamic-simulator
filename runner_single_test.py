import simulator as sim
import graph_utilities as gu


#simple main that generate a graph and test the simulator

#graph = gu.generateHypercubeGraph(d=4, draw=False)
graph = gu.generateKCliqueGraph(15, False)

config = sim.SimulationConfigurator(graph=graph, bias=0.55, opinion_update_rule=sim.OpinionUpdateRule.VOTER_MODEL, comment="Clique di 15 nodi")
simulationResult: sim.SimulationResult = sim.runSimulationOn(config)

#print simulation data such as rounds, configuration parameters ecc..
simulationResult.printSimulationData()

#save all informations about simulation
#save png's of the graph showing the diffusion of the opinion at rounds: 0, 25%, 50%, 75%, 100%
#save in output/simulations
simulationResult.saveSimulationData()

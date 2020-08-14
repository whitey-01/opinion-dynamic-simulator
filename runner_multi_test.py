import simulator as sim
import graph_utilities as gu
import matplotlib.pyplot as plt


#simple main that runs a simulation multiple times


graph = gu.generateKCliqueGraph(20, False)
config = sim.SimulationConfigurator(graph=graph, bias=0.75, opinion_update_rule=sim.OpinionUpdateRule.MAJORITY_DYNAMICS)

#returns a list of SimulationResult objects
simulations = sim.runMultipleSimulations(config,200)

x_axis = [item for item in range(1, len(simulations) + 1)]
y_axis = []
for s in simulations:
    simulationResult: sim.SimulationResult = s
    y_axis.append(s.rounds)
    print(simulationResult.rounds)

plt.title("200 simulazioni eseguite su una clique di " + str(len(list(config.graph.vertices()))) + " nodi, con " + config.opinion_update_rule.value + " e bias " + str(config.bias))
plt.scatter(x_axis, y_axis, color='darkblue', marker='x')

plt.xlabel("tentativo")
plt.ylabel("rounds impiegati")

plt.grid(True)
plt.legend()

plt.show()
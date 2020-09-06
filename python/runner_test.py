import python.simulator.tester as ts
import python.simulator.simulation_configurator as sc
import python.simulator.graph_generator as gg

# simple main that performs a test by running multiple simulation on a fixed config.
ITERATIONS = 100

graph = gg.generateHypercubeGraph(d=11)
# graph = gg.generateKCycleGraph(vertices_num=1024)
config = sc.SimulationConfigurator(graph=graph,
                                   bias=0.5,
                                   opinion_update_rule=sc.OpinionUpdateRule.MAJORITY_DYNAMICS,
                                   comment="Ipercubo 2048 nodi")

# returns a list of SimulationResult objects
simulations = ts.runTest(config, ITERATIONS)

# file_name without extension, separated optional param directory
# on big graphs (1024+ nodes) drawing the graph can take quite some time and require a lot of power
ts.saveTestDataAsXML(config=config, simulations=simulations, draw=False)

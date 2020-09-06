import python.simulator.simulation_configurator as sc
import python.simulator.simulation_result as sr
import python.simulator.simulator as sim


# returns a list of dicts containing simulations id and rounds
# without storing each time the same configuration included in simulationResults obj
def runTest(config: sc.SimulationConfigurator, repetitions: int):
    simulations = []
    for i in range(0, repetitions):
        simulation: sr.SimulationResult = sim.runSimulationOn(config)
        temp = {"simulation_id": simulation.simulation_id, "simulation_rounds": simulation.rounds}
        simulations.append(temp)
        print("simulation " + str(i) + " processed")
    return simulations

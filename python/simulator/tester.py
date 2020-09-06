import python.simulator.test_configurator as tc
import python.simulator.simulation_result as sr
import python.simulator.simulator as sim


# returns a list of dicts containing simulations id and rounds
# without storing each time the same configuration included in simulationResults obj
def runTest(testConfigurator: tc.TestConfigurator):
    iterations = testConfigurator.iterations
    simulations = []
    for i in range(0, iterations):
        simulation: sr.SimulationResult = sim.runSimulationOn(testConfigurator.simulationConfigurator)
        temp = {"simulation_id": simulation.simulation_id, "simulation_rounds": simulation.rounds}
        simulation = None
        simulations.append(temp)
        print("simulation " + str(i) + " processed")
    return simulations

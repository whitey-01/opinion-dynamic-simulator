import python.simulator.test_configurator as tc
import python.simulator.test_result as tr
import python.simulator.simulation_result as sr
import python.simulator.simulator as sim


# return an object containing test results
def runTest(testConfigurator: tc.TestConfigurator):
    iterations = testConfigurator.iterations
    simulations = []
    for i in range(0, iterations):
        simulation: sr.SimulationResult = sim.runSimulationOn(testConfigurator.simulationConfigurator)
        temp = {"simulation_id": simulation.simulation_id, "simulation_rounds": simulation.rounds}
        simulation = None
        simulations.append(temp)
        print("simulation " + str(i) + " processed")
    return tr.TestResult(testConfigurator=testConfigurator, results=simulations)

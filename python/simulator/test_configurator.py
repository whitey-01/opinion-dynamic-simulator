import python.simulator.simulation_configurator as sc


class TestConfigurator:
    def __init__(self, simulationConfigurator: sc.SimulationConfigurator, iterations: int):
        self.simulationConfigurator = simulationConfigurator
        self.iterations = iterations

    def configXMLSerializer(self):
        config = "<config>"
        simulationsConfig = "<!-- Configuration shared by the simulations -->"
        simulationsConfig += "<simulations-config>" + self.simulationConfigurator.configXMLSerializer() + "</simulations-config>"
        iterations = "<!-- number of simulations executed -->"
        iterations += "<test-iterations>" + str(self.iterations) + "</test-iterations>"
        return config + simulationsConfig + iterations + "</config>"

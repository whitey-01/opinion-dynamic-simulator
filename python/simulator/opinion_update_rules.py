from abc import ABC, abstractmethod
import graph_tool as gt
import random


# module containing interface and various opinion update rules

# interface that defines the method to perform a certain opinion update rule
class UpdateRuleInterface(ABC):
    @abstractmethod
    def run(self, g: gt.Graph, v: gt.Vertex) -> int:
        pass


# implementation of Majority Dynamic update rule
class MajoritySimulator(UpdateRuleInterface):
    def run(self, g: gt.Graph, v: gt.Vertex) -> int:
        neighbors = list(v.all_neighbors())
        if not len(neighbors):
            return g.vertex_properties["opinion"][v]

        opinion0_counter = 0
        opinion1_counter = 0

        for vertex in neighbors:
            if g.vertex_properties["opinion"][vertex] == 0:
                opinion0_counter += 1
            else:
                opinion1_counter += 1

        if opinion0_counter > opinion1_counter:
            return 0
        if opinion1_counter > opinion0_counter:
            return 1

        return random.choice([0, 1])


# implementation of Voter Model update rule
class VoterSimulator(UpdateRuleInterface):
    def run(self, g: gt.Graph, v: gt.Vertex) -> int:
        neighbors = list(v.all_neighbors())
        if not len(neighbors):
            return g.vertex_properties["opinion"][v]
        u: gt.Vertex = random.choice(neighbors)
        return g.vertex_properties["opinion"][u]

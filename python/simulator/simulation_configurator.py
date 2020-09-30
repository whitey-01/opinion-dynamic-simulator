import graph_tool as gt
from enum import Enum
import python.simulator.graph_generator as gg


# module used to define how a simulation must be configured

# defines the opinions update rules available for the configurator
class OpinionUpdateRule(Enum):
    VOTER_MODEL = "voter-rule"
    MAJORITY_DYNAMICS = "majority-dynamics"


# defines an object used to configure the simulation correctly
# holds the graph and other config parameters
class SimulationConfigurator:
    def __init__(self, graph: gt.Graph, bias: float, opinion_update_rule: OpinionUpdateRule,
                 graph_desc: str = "OPTIONAL GRAPH DESCRIPTION"):
        self.graph = graph
        if opinion_update_rule != OpinionUpdateRule.MAJORITY_DYNAMICS and opinion_update_rule != OpinionUpdateRule.VOTER_MODEL:
            raise Exception("Error:- Invalid opinion update rule!")
        self.opinion_update_rule = opinion_update_rule
        # defines how much agent are biased towards the dominant opinion
        self.bias = bias
        self.graph_desc = graph_desc

    # returns a xml string of the configurator
    def configXMLSerializer(self):
        config = "<config>"
        graphDeg = "<config-graph-deg>" + self.getXMLDeg() + "</config-graph-deg>"
        comment = "<config-graph-desc>" + self.graph_desc + "</config-graph-desc>"
        updateRule = "<config-update-rule>" + self.opinion_update_rule.value + "</config-update-rule>"
        bias = "<config-bias>" + str(self.bias) + "</config-bias>"
        return config + comment + graphDeg + updateRule + bias + "</config>"

    # returns XML block containing graph degree information
    def getXMLDeg(self):
        deg = gg.getDegreeValuesOf(self.graph)
        degTag = "<min_deg>" + str(deg["min_deg"]) + "</min_deg>"
        degTag += "<avg_deg>" + str(deg["avg_deg"]) + "</avg_deg>"
        degTag += "<max_deg>" + str(deg["max_deg"]) + "</max_deg>"
        return degTag
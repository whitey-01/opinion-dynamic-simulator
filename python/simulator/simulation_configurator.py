import graph_tool as gt
from enum import Enum


# defines two opinions update rules available
class OpinionUpdateRule(Enum):
    VOTER_MODEL = "voter-rule"
    MAJORITY_DYNAMICS = "majority-dynamics"


# defines an object used to configure the simulation correctly
# holds the graph and other config parameters
class SimulationConfigurator:
    def __init__(self, graph: gt.Graph, bias: float, opinion_update_rule: OpinionUpdateRule,
                 comment: str = "OPTIONAL COMMENT"):
        self.graph = graph
        if opinion_update_rule != OpinionUpdateRule.MAJORITY_DYNAMICS and opinion_update_rule != OpinionUpdateRule.VOTER_MODEL:
            raise Exception("Error:- Invalid opinion update rule!")
        self.opinion_update_rule = opinion_update_rule
        # defines how much agent are biased towards the dominant opinion
        self.bias = bias
        self.comment = comment

    # returns a xml string of the configurator
    def configXMLSerializer(self):
        config = "<config>"
        comment = "<config-comment>" + self.comment + "</config-comment>"
        updateRule = "<config-update-rule>" + self.opinion_update_rule.value + "</config-update-rule>"
        bias = "<config-bias>" + str(self.bias) + "</config-bias>"
        return config + comment + updateRule + bias + "</config>"

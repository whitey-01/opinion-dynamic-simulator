import graph_tool as gt
import python.simulator.graph_generator as gg
import python.simulator.opinion_update_rules as our


# module used to define how a simulation must be configured


# defines an object used to configure the simulation correctly
# holds the graph and other config parameters
class SimulationConfigurator:
    def __init__(self, graph: gt.Graph, bias: float, opinion_update_rule: our.UpdateRuleInterface,
                 graph_desc: str = "OPTIONAL GRAPH DESCRIPTION"):
        self.graph = graph
        self.opinion_update_rule = opinion_update_rule
        # defines how much agent are biased towards the dominant opinion
        self.bias = bias
        self.graph_desc = graph_desc

    # returns a xml string of the configurator
    def configXMLSerializer(self):
        config = "<config>"
        config += "<config-update-rule>" + self.opinion_update_rule.__class__.__name__ + "</config-update-rule>"
        config += "<config-bias>" + str(self.bias) + "</config-bias>"
        config += "<config-graph>"
        config += "<config-graph-desc>" + self.graph_desc + "</config-graph-desc>"
        config += "<config-graph-deg>" + self.getXMLDeg() + "</config-graph-deg>"
        config += "</config-graph>"
        return config + "</config>"

    # returns XML block containing graph degree information
    def getXMLDeg(self):
        deg = gg.getDegreeValuesOf(self.graph)
        degTag = "<total-edges>" + str(len(list(self.graph.edges()))) + "</total-edges>"
        degTag += "<min_deg>" + str(deg["min_deg"]) + "</min_deg>"
        degTag += "<avg_deg>" + str(deg["avg_deg"]) + "</avg_deg>"
        degTag += "<max_deg>" + str(deg["max_deg"]) + "</max_deg>"
        return degTag
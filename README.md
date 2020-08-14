# opinion-dynamic-simulator
python-based software that simulate a binary opinion system where agents are biased towards a superior opinion

#REQUIRES graph_tool lib available here -> https://graph-tool.skewed.de/

#you will find 2 runner script:
  -1: Performs a single simulation on a graph with a specific configuration and creates a folder named with an auto-generated simulation id, containing:
      - a png rappresentation of the graph
      - an xml file containing basic information about the configuration parameters (such as id, opinion update rule, bias towards dominant opinion) and the 
        output result ( num of rounds needed to reach the absorbing state)
      - an xml rappresentation of the graph provided by the graph_tool library
      - a folder containing png's showing the evolution of the simulation (start-stage, 25%, 50%, 75%, final-stage)
        (stored in output/simulations/<SIMULATION_ID>/evolution_imgs)

  -2: Performs multiple simulations on a fixed graph and configuration. Produce a list of Simulation objects that you can analyze.

#two opinion update rules are available: Majority-Dynamic and Voter-Model

# Opinion-dynamic-simulator 
## Python-based software that simulates a binary opinion system where agents are biased towards a superior opinion ##

### REQUIRES graph_tool lib available here -> https://graph-tool.skewed.de/ ###


### Main classes and functions are situated in /simulator

### Runner scripts:
  1. Performs a single simulation on a graph with a specific configuration and creates a folder named with an auto-generated simulation id, containing:
      - a png rappresentation of the graph
      - an xml file containing basic information about the configuration parameters (such as id, opinion update rule, bias towards dominant opinion)
      - an xml file containing the simulation result ( num of rounds needed to reach the absorbing state)
      - an xml rappresentation of the graph (at the end of the process) provided by the graph_tool library
      - a folder containing png's showing the evolution of the simulation (start-stage, 25%, 50%, 75%, final-stage)
        (stored in output/simulations/<SIMULATION_ID>/evolution_imgs)

  2. Performs multiple simulations on a fixed graph and configuration. Produces a list of Simulation objects that you can analyze.

Opinion update rules available: 
- Majority-Dynamic (update opinion of agent A based on the most diffused one among its neighbours)
- Voter-Model (update opinion of agent A by copying the opinion of a randomly selected neighbour)
Utilities for creating different graph topologies (some of them are custom, some other are provided by graph_tool) such as k-clique and hypercubes.


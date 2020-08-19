# Opinion-Dynamic-Simulator 
## Python-based software that simulates a binary opinion system where agents are biased towards a superior opinion ##

### REQUIRES:
  - Python (3.8 recommended)
  - graph_tool lib available here -> https://graph-tool.skewed.de/ 

### Main modules
In /simulator you will find some modules useful to define, perform and save simulations, as well as tester.py which contains functions used to perform 
and save tests.

### Runner scripts:
  1. Performs a single simulation on a graph with a specific configuration and creates a folder, named with an auto-generated simulation id, containing:
      - a png rappresentation of the graph
      - an xml file containing basic information about the configuration parameters (such as id, opinion update rule, bias towards dominant opinion)
      - an xml file containing the simulation result ( num of rounds needed to reach the absorbing state)
      - an xml rappresentation of the graph (at the end of the process) provided by the graph_tool library
      - a folder containing png's showing the evolution of the simulation (start-stage, 25%, 50%, 75%, final-stage)
        (stored in output/simulations/<SIMULATION_ID>/evolution_imgs)

  2. Performs a test (multiple simulations on a fixed graph and configuration). Produces an xml file containing the configuration, the rounds needed for each            simulation and the average rounds. These xml tests are stored under output/tests/<TEST_ID>, where TEST_ID is auto-generated.

Opinion update rules available: 
- Majority-Dynamic (update opinion of agent A based on the most diffused one among its neighbours)
- Voter-Model (update opinion of agent A by copying the opinion of a randomly selected neighbour)

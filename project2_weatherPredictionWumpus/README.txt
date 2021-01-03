Rajesh Sakhamuru

11/30/19
# Problem:

We must implement weather to each room in the wumpus and then
using given data, generate 3 predictive models which vote to determine the ability of
the agent to shoot the wumpus from each given room.


The Wumpus game implementation is taken directly from:
https://github.com/greeder59/Wumpus

# Solution:

Decision Tree, ANN and SVM models are all generated upon initialization of a
predictive object and stored within the object for use throughout the game. At each
room, the weather components (Outlook, Temperature, Humidity, Windy) are all
accessed and passed to the predictive object which runs the data through all 3 models
which then vote to determine whether an arrow can or cannot be fired from that room.
The rest of the game will function the same.


In order to run the game, wumpus.py can be run using the console command:


python3 wumpus.py


pandas, numpy, sklearn, and keras are required dependencies.

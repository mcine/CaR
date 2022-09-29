Code A Robot - CaR

You are a robot and you are trying to find your way to a goal.

Your goal is to  code the logic (to your own file) to get the robot to the goal.
As input, you will get information in current state dictionary and you return a dictionary (targets) that
will contain target values for the robot. game ends when you reach the goal. Everything in between is in your hands. 

How the code works:
At the start of the game "start" function is called from user code and then game will enter gameloop, that will draw the map, ask robot directions from user code (getRobotTargets function) and update robot status.
And ofcourse check if robot has reached the goal. After wich game will end and time taken to solve the maze, will be displayed.

Currently there is no physics in this game, but the robot has a maximum speed. It can rotate lightning fast.

There is couple examples profided for you to see how the robot works (examples directory).

Robot features:
 - Distance sensor in your forehead that casts a laser and returns the distance to nearest wall. 
 - Adjustable direction and speed.
 - Safety logic that stops the robot always a bit before a wall.

Running the game:
- python .\CaR.py {level here} {code file here}
- default level is level1.py and default code file is code.py
- level file has to end with .lvl and code file has to end with .py

command example:
"python .\CaR.py level2.lvl examples\bouncearound.py"

happy coding!

done with python3, uses pygame
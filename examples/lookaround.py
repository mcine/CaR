import sys

#modify and return the targets
def getRobotTargets(currentState, targets):    
    #print(currentState, targets)
    targets["DIRECTION"] += 3
    return targets
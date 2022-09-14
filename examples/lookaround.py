import sys

def start():
    pass

#modify and return the targets
def getRobotTargets(currentState, targets):    
    #print(currentState, targets)
    targets["PLAYER_DIRECTION"] += 3
    return targets
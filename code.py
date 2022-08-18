

isTurning = False;
turnAmount = 0;

#modify and return the targets
def getRobotTargets(currentState, targets):    
    global turnAmount, isTurning
    if(not isTurning):
        if(targets["PLAYER_SPEED"] > currentState["PLAYER_SPEED"]):  # forced to slow before wall
            isTurning = True
            turnAmount = 360 + 45
        else:
            targets["PLAYER_SPEED"] = currentState["PLAYER_MAX_SPEED"] / 2
    else:
        x = 8
        targets["PLAYER_DIRECTION"] = currentState["PLAYER_DIRECTION"] + x
        targets["PLAYER_SPEED"] = 0
        turnAmount -= x
        if (turnAmount<0):
            isTurning = False
    
    #print(currentState, targets)
    return targets
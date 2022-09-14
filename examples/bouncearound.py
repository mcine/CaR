def start():
    pass

isTurning = False;
turnAmount = 0;
visitedTiles = [];
#modify and return the targets
def getRobotTargets(currentState, targets):    
    global turnAmount, isTurning, visitedTiles
    if(not isTurning):
        if(targets["PLAYER_SPEED"] > currentState["PLAYER_SPEED"]):  # forced to slow before wall
            isTurning = True
            turnAmount = 360 + 45
        else:
            targets["PLAYER_SPEED"] = currentState["PLAYER_MAX_SPEED"] / 2
    else:
        x = 3
        targets["PLAYER_DIRECTION"] = currentState["PLAYER_DIRECTION"] + x
        targets["PLAYER_SPEED"] = 0
        turnAmount -= x
        if (turnAmount<0):
            isTurning = False
            
    currentTile = (int(currentState['PLAYER_POSITION'][0]/currentState['TILE_WIDTH']),int(currentState['PLAYER_POSITION'][1]/currentState['TILE_HEIGHT'])) 
    if(currentTile not in visitedTiles):
        visitedTiles.append(currentTile)
    #print(currentState, targets)
    #print(visitedTiles)
    return targets
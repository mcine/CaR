
import random

def start():
   # print('\n',locals())
  #  print('\n',globals())
    pass
longestRay = 0;
isTurning = False
turnAmount = 0.03

#modify and return the targets
def getRobotTargets(currentState, targets):
    global longestRay
    #print('\n',currentState, targets, isTurning, turnAmount)
    #print(random.randint(0,10))
    if("test" in targets and targets['test']=="test" ):
        targets['test'] = 'TEST'
    else:
        targets['test'] = "test"
    targets["PLAYER_DIRECTION"] = targets["PLAYER_DIRECTION"] - turnAmount
    
    raylen = currentState["RAY_LENGTH"]
    if(raylen > longestRay):
        longestRay = raylen
        #print("longest ray: ", raylen, " dir: ", currentState["PLAYER_DIRECTION"])
    return targets
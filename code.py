
import random

def start():
   # print('\n',locals())
  #  print('\n',globals())
    pass
isTurning = False;
turnAmount = 0;

#modify and return the targets
def getRobotTargets(currentState, targets):    
    print('\n',currentState, targets, isTurning, turnAmount)
    print(random.randint(0,10))
    if("test" in targets and targets['test']=="test" ):
        targets['test'] = 'TEST'
    else:
        targets['test'] = "test"
    targets["PLAYER_DIRECTION"] = targets["PLAYER_DIRECTION"] - 5 
    return targets
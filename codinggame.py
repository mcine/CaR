from turtle import update
import pygame
import sys
import math
import time
import types

X=0
Y=1
script_filename = "code.py"
level_filename = "level1.lvl"

def handleArgument(a):
    global script_filename, level_filename
    if ".py" in a:
        script_filename = a
    if ".lvl" in a:
        level_filename = a

args = sys.argv[1:]
for arg in args:
    handleArgument(arg)

## read user code    
globals_ = {'num':0, 'print': print}
script_locals = {}



script_object = compile(open(script_filename).read(), "scriptstr", "exec")
exec(script_object, globals_, script_locals)

#print(globals_)
script_locals.update(globals_)
idx = script_object.co_consts.index('start') -1
print(idx)
if(idx>=0): 
    types.FunctionType(script_object.co_consts[idx], globals=script_locals)()

idx = script_object.co_consts.index('getRobotTargets') -1
updatefunc = script_object.co_consts[idx];
#result = types.FunctionType(updatefunc, globals=script_locals)({},{})
#print("ret", result)
#exec(updatefunc, globals_, script_locals)
#if "getRobotTargets" not in locals():
if (idx < 0):    
    print("Needed function not implemented, check your script")
    sys.exit(-1)

SCREEN_HEIGHT = 720
SCREEN_WIDTH = 1080
SCREEN_FPS : int = 30
MAP_HEIGHT = 8
MAP_WIDTH = 8
PLAYER_DIRECTION : float = math.radians(5)
PLAYER_SPEED = 0
PLAYER_MAX_SPEED = 100
RAY_MAX_LENGTH = math.sqrt(MAP_HEIGHT*MAP_HEIGHT + MAP_WIDTH*MAP_WIDTH)
RAY_LENGTH = 0;
GOAL_SIZE = 20

lvlfile = open(level_filename, 'r')
MAP = lvlfile.readlines()
MAP_WIDTH = len(MAP[0])-1 # discard \n
MAP_HEIGHT = len(MAP)
MAP = ''.join(MAP)
MAP = MAP.replace('\n','')
TILE_WIDTH = int(SCREEN_WIDTH / MAP_WIDTH)
TILE_HEIGHT = int(SCREEN_HEIGHT / MAP_HEIGHT)

FOW = pygame.Surface((MAP_WIDTH*TILE_WIDTH, MAP_HEIGHT*TILE_HEIGHT),  pygame.SRCALPHA)
FOW.fill((0,0,0))
FOW.set_alpha(255)
#pygame.draw.circle(FOW, (255, 255, 255,0), (100,100), 100)        

def get_position(character):
    for row in range(0,MAP_HEIGHT):
        for col in range(0,MAP_HEIGHT):
            index = row * MAP_WIDTH + col
            if(MAP[index] == character):
                return (int(col * TILE_WIDTH + TILE_WIDTH / 2 ), int(row * TILE_HEIGHT + TILE_HEIGHT / 2))
    (int(SCREEN_WIDTH / 2), int(SCREEN_HEIGHT / 2))




pygame.init()
window = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
pygame.display.set_caption('Game')
clock = pygame.time.Clock()

PLAYER_POSITION = get_position('P')
GOAL_POSITION = get_position('G')

print(PLAYER_POSITION)
dir = (-math.sin(PLAYER_DIRECTION), math.cos(PLAYER_DIRECTION))
print (dir)
def draw_map():
    for row in range(0,MAP_HEIGHT):
        for col in range(0,MAP_WIDTH):
            square = row * MAP_WIDTH + col # map is just a string, calculate char..
            pygame.draw.rect(window, 
                             (200, 200, 200) if MAP[square] == '#' else (50,50,50),  # color for wall or not
                             (col * TILE_WIDTH, row * TILE_HEIGHT, TILE_WIDTH, TILE_HEIGHT)
                             #(col * TILE_WIDTH +1, row * TILE_HEIGHT +1, TILE_WIDTH -2, TILE_HEIGHT-2)
                             )

def draw_player(pos):
    pygame.draw.circle(window, (0, 0, 255) , pos, 10)

def draw_goal(pos):
    global GOAL_SIZE
    pygame.draw.circle(window, (0, 255, 0) , pos, GOAL_SIZE)

def draw_background():
    pygame.draw.rect(window, (255,50,50), (0,0,SCREEN_WIDTH, SCREEN_HEIGHT))
    
# trying to cast ray with DDA algorithm
oldcollision = (0,0)
raycount = 0;
def draw_ray(fromx_coord:float, fromy_coord:float, angle):
    global oldcollision, raycount
    # to map coordinates 
    raycount+=1
    if (raycount == 144):
        pass
    fromx = fromx_coord / TILE_WIDTH
    fromy = fromy_coord / TILE_HEIGHT
    dirx, diry = (-math.sin(PLAYER_DIRECTION), math.cos(PLAYER_DIRECTION))
    unitstepsizes = [math.sqrt(1+(diry/dirx) * (diry/dirx)) if dirx != 0 else 0, math.sqrt(1+(dirx/diry)*(dirx/diry)) if diry != 0 else 0]
    mapcheck = [int(fromx), int(fromy)]
    raylengths = [0.0,0.0]
    stepdirs = [0,0]
    
    if(dirx<0):
        stepdirs[X] = -1 
        raylengths[X] = (fromx - float(mapcheck[X]))*unitstepsizes[X]
    else:
        stepdirs[X] = 1
        raylengths[X] = ((mapcheck[X]+1)-fromx)*unitstepsizes[X]
    
    if(diry<0):
        stepdirs[Y] = -1 
        raylengths[Y] = (fromy - mapcheck[Y])*unitstepsizes[Y]
    else:
        stepdirs[Y] = 1
        raylengths[Y] = ((mapcheck[Y]+1)-fromy)*unitstepsizes[Y]
            
    tilefound = False
    if(MAP[mapcheck[Y]*MAP_WIDTH + mapcheck[X]] == '#'):
            tilefound = True;
    fdistance = 0.0
    
    while (tilefound == False and fdistance < RAY_MAX_LENGTH):
        #and (mapcheck[X] + int(stepdirs[X]))>0 or (mapcheck[Y] + int(stepdirs[Y])) < 0
        if(raylengths[X] < raylengths[Y] ):          
            mapcheck[X] += int(stepdirs[X])            
            fdistance = raylengths[X]
            raylengths[X] += unitstepsizes[X]
            
        else:
            mapcheck[Y] += int(stepdirs[Y])                    
            fdistance = raylengths[Y]
            raylengths[Y] += unitstepsizes[Y]
    
        #if(mapcheck[X] > 0 and mapcheck[X]< MAP_WIDTH and mapcheck[Y]>0 and mapcheck[Y]<MAP_HEIGHT):
        if(MAP[mapcheck[Y]*MAP_WIDTH + mapcheck[X]] == '#'):
            tilefound = True;
    
    collisionpoint = PLAYER_POSITION
    
    if(tilefound == True):
        collisionpoint = (fromx + dirx*fdistance, fromy + diry*fdistance)
        if(collisionpoint[Y] != oldcollision[Y]):
            pass
        oldcollision = collisionpoint
        pygame.draw.circle(FOW, (255, 255, 255,0), (collisionpoint[X]*TILE_WIDTH, collisionpoint[Y]*TILE_HEIGHT ), 10)        
        
    #to screen coordinates. 
    pygame.draw.line(window, (255,55,55), (fromx_coord, fromy_coord), 
                        (collisionpoint[X]*TILE_WIDTH, collisionpoint[Y]*TILE_HEIGHT), 
                        #(fromx_coord - math.sin(angle)*50,fromy_coord + math.cos(angle) * 50),
                        5) 
    pygame.draw.line(FOW, (255,255,255,0), (fromx_coord, fromy_coord), 
                        (collisionpoint[X]*TILE_WIDTH, collisionpoint[Y]*TILE_HEIGHT), 
                        #(fromx_coord - math.sin(angle)*50,fromy_coord + math.cos(angle) * 50),
                        5)   
    return collisionpoint

currentTargets = {"PLAYER_SPEED":0, "PLAYER_DIRECTION":math.degrees(PLAYER_DIRECTION)}

def updatePlayer(collisionpoint):
    global PLAYER_POSITION, TILE_HEIGHT, TILE_WIDTH, PLAYER_SPEED, PLAYER_MAX_SPEED, PLAYER_DIRECTION, SCREEN_FPS, currentTargets, updatefunc
    dx = collisionpoint[X]*TILE_WIDTH - PLAYER_POSITION[X]
    dy = collisionpoint[Y]*TILE_HEIGHT - PLAYER_POSITION[Y]
    raylength = math.sqrt(dx*dx + dy*dy)
    currentData = {"SCREEN_HEIGHT":SCREEN_HEIGHT, "SCREEN_WIDTH":SCREEN_WIDTH, "SCREEN_FPS":SCREEN_FPS, "PLAYER_DIRECTION": math.degrees(PLAYER_DIRECTION), 
                    "RAY_LENGTH":raylength, "PLAYER_POSITION":PLAYER_POSITION, "TILE_HEIGHT":TILE_HEIGHT, "TILE_WIDTH":TILE_WIDTH, "PLAYER_SPEED":PLAYER_SPEED,
                    "PLAYER_MAX_SPEED":PLAYER_MAX_SPEED, "GOAL_POSITION":GOAL_POSITION}
    currentTargets = types.FunctionType(updatefunc, globals=script_locals)(currentData, currentTargets)    
    
    if(currentTargets["PLAYER_SPEED"] < 0):
        currentTargets["PLAYER_SPEED"] = 0;
    elif(currentTargets["PLAYER_SPEED"] > PLAYER_MAX_SPEED):
        currentTargets["PLAYER_SPEED"] = PLAYER_MAX_SPEED
        
    if(raylength > 50):
        PLAYER_SPEED = currentTargets["PLAYER_SPEED"] 
        dirx, diry = (-math.sin(PLAYER_DIRECTION)*TILE_WIDTH, math.cos(PLAYER_DIRECTION)*TILE_HEIGHT)
        
        xmovement = dirx * PLAYER_SPEED / 10  / SCREEN_FPS  if raylength > 0 else 0 
        ymovement = diry * PLAYER_SPEED / 10 / SCREEN_FPS if raylength > 0 else 0
        PLAYER_POSITION = (PLAYER_POSITION[0]+xmovement, PLAYER_POSITION[1]+ymovement)        
    else:
        PLAYER_SPEED = 0

    while(currentTargets["PLAYER_DIRECTION"] < 0):
        currentTargets["PLAYER_DIRECTION"] = currentTargets["PLAYER_DIRECTION"] + 360
    PLAYER_DIRECTION=math.radians(currentTargets["PLAYER_DIRECTION"])
    PLAYER_DIRECTION = PLAYER_DIRECTION % math.radians(360)

def isWithinRange(pos1, pos2, range):
    dx = abs(pos1[X] - pos2[X])
    dy = abs(pos1[Y] - pos2[Y])
    diff = math.sqrt(dx*dx + dy*dy)
    return range > diff

start = time.time()



if __name__ == "__main__":
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)
        
        draw_background()
        draw_map()                
       
        collisionpoint = draw_ray(PLAYER_POSITION[X], PLAYER_POSITION[Y], PLAYER_DIRECTION)
        window.blit(FOW,FOW.get_rect())
        
        draw_goal(GOAL_POSITION)
        draw_player(PLAYER_POSITION)
        
        pygame.display.flip()
        
        updatePlayer(collisionpoint)
        
        if(isWithinRange(PLAYER_POSITION, GOAL_POSITION, GOAL_SIZE)):
            print("GOAL!!!!!!")
            print("you made it, try to solve another level ")
            print(time.time()-start)
            pygame.quit()
            sys.exit(0)
        
        clock.tick(SCREEN_FPS)   # ensures FPS below parameter
        #print("FPS:", int(clock.get_fps()))
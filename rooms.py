# refer to pygame as pg
import pygame as pg
# other game files
from settings import *
from sprite_list import *
from sprites import *
from random import randint

################################################################################

# ROOM CLASSES

# test room with only grass
class BaseRoom(object):
    def __init__(self, game, tileType, entrance=(6,0), enemyType=randint(0,4), \
                 difficulty=randint(3, 5)):
        # instance variables are instantiated
        self.enemyType = enemyType
        self.tileType = tileType
        self.obsType = self.tileType
        self.entrance = tuple(entrance)
        # the map is created
        self.reserve()
        self.game = game
        self.createFloor()
        self.placePlayer(game.player)
        self.placeMobs(difficulty)
        self.createExit()
        # obstacles should be placed last because they do most accounting
        # for objects already placed
        self.placeObstacles()

    # creates an exit on the map
    def createExit(self):
        # selects a random reserved tile to ensure accessibility
        # spot will be a tuple as every item in self.reserved is a tuple
        spot = self.randoCoord()
        # places the exit tile on that location
        self.exit = Tile_Exit(self.game, spot[0], spot[1])
        self.exitCoord = (self.exit.x, self.exit.y)
        self.reserved.append(spot)

    # reserves straight lines at random x and y coordinates
    # such that the player won't get blocked in by obstacles
    def reserve(self):
        self.reserved = list()
        # x and y axis for below
        ranX = self.entrance[0]
        ranY = randint(1, TILE_TO_GRID-2)
        # reserves space such that the player won't get walled 
        # in or out of an area
        for x in range(0, TILE_TO_GRID):
            # makes a straight line for the x axis
            # along a random y coordinate
            self.reserved.append((x, ranY))
        for y in range(0, TILE_TO_GRID):
            # makes a straight line for the y axis
            # along a random x coordinate
            self.reserved.append((ranX, y))

    # create the base floor for the room
    def createFloor(self):
        for x in range(0, TILE_TO_GRID):
            for y in range(0, TILE_TO_GRID):
                # pass each tile an x and y coordinate
                # game parameter is for sprite grouping
                self.tileInterpreter(self.tileType, x, y)

    # interprets which tile should be placed
    def tileInterpreter(self, tileType, x, y):
        if tileType == 0:
            Tile_Grass(self.game, x, y)
        elif tileType == 1:
            Tile_Dirt(self.game, x, y)
        else:
            Tile_Stone(self.game, x, y)

    # places obstacles such as cave walls or rocks
    def placeObstacles(self):
        # picks a random amount of obstacles to place
        # throughout the map
        # there's a margin of error I can't seem to fix ###
        obstacles = randint(15, 20)
        # set for tracking coordinates already used to place an obstacle
        # important for not placing obstacles on top of one another
        used = set()
        # while there are still obstacles to place
        while obstacles > 0:
            # creates a random (x, y) coordinate as a tuple
            randCoord = self.randoCoord(used)
            # adds current coordinates to used set
            used.add(randCoord)
            # creates a new stump at given coordinates
            self.obsInterpreter(randCoord[0], randCoord[1])
            # reduces amount of obstacles to place
            obstacles -= 1

    # interprets which obstacle should be placed
    def obsInterpreter(self, x, y):
        if self.obsType == 0:
            Obs_Stump(self.game, x, y)
        elif self.obsType == 1:
            Obs_Dirtmound(self.game, x, y)
        else:
            Obs_Rock(self.game, x, y)

    # returns random x and y coordinates in the form of a tuple
    # takes in a list of already used coodinates as well
    def randoCoord(self, used=[]):
        # return variable
        coord = None
        # continues until a valid coordinate is found
        while True:
            # random x coordinates are created
            randX = randint(0, TILE_TO_GRID-1)
            randY = randint(0, TILE_TO_GRID-1)
            # then stored as a tuple
            coord = (randX, randY)
            # skips if coord is previously reserved
            if (coord in self.reserved) or (coord in used):
                continue
            # otherwise returns the random coordinate
            else:
                return coord
                        
    # places the player appropriately
    # this function will change later in the developement of the game
    def placePlayer(self, player):
        # later the player will be placed toward the exit of the previous room
        # for now the character is placed at the bottom of the map
        player.place(self.entrance[0],self.entrance[1])
        # reserves this spot for the player
        self.reserved.append(player.bounds['c'])

    # will place the mobs throughout the map
    def placeMobs(self, num):
        # set of already used coordinates
        used = set()
        for mob in range(num):
            # creates a random (x,y) coordinate as a tuple
            randCoord = self.randoCoord(used)
            used.add(randCoord)
            currentMob = self.enemyInterpreter(randCoord[0], \
                                               randCoord[1], \
                                               self.enemyType)
            # adds currentMob to reserved placement list
            self.reserved.append(currentMob.bounds['c'])

    # takes an int, x, and y, and returns a mob at (x, y)
    # coordinates based on int given
    def enemyInterpreter(self, x, y, enType):
        # return variable will be a mob, set to None for initialization
        retMob = None
        if enType == 0:
            retMob = Actor_Ghoul(self.game, x, y)
        elif enType == 1:
            retMob = Actor_Zombie(self.game, x, y)
        elif enType == 2:
            retMob = Actor_Skeleton(self.game, x, y)
        elif enType == 3:
            retMob = Actor_Ghost(self.game, x, y)
        else:
            retMob = Actor_Slime(self.game, x, y)
        return retMob

####################################################################################################

# Grass room
class Room_Grass(BaseRoom):
    # CLASS VARIABLES
    # tile will be grass
    tile_type = 0
    # mobs will all be slimes
    mob_type = 4

    # game is passed in as self in main program
    # difficulty determines amount of enemies
    def __init__(self, game, entrance, difficulty = randint(3,5)):
        BaseRoom.__init__(self, game, self.tile_type, entrance, \
                          self.mob_type, difficulty)

# Dirt room
class Room_Dirt(BaseRoom):
    # CLASS VARIABLES
    # tile will be dirt
    tile_type = 1
    # mobs will be skeletons
    mob_type = 2

    # game is passed in as self in main program
    # difficulty determines amount of enemies
    def __init__(self, game, entrance, difficulty = 4):
        BaseRoom.__init__(self, game, self.tile_type, entrance, \
                          self.mob_type, difficulty)

# Stone room
class Room_Stone(BaseRoom):
    # CLASS VARIABLES
    # tile will be dirt
    tile_type = 2

    # game is passed in as self in main program
    # difficulty determines amount of enemies
    def __init__(self, game, entrance, difficulty = randint(4, 5)):
        # mob types will be random
        self.mob_type = randint(0, 3)
        BaseRoom.__init__(self, game, self.tile_type, entrance, \
                          self.mob_type, difficulty)

    # takes an int, x, and y, and returns a mob at (x, y)
    # coordinates based on int given
    def enemyInterpreter(self, x, y, enType):
        # creates a percentage based "chance" of a certain mob spawning
        enChance = [0,0,0,0,1,1,1,1,2,2,3,3,3,4]
        # mob types will be random
        enType = enChance[randint(0, len(enChance)-1)]
        # return variable will be a mob, set to None for initialization
        retMob = None
        if enType == 0:
            retMob = Actor_Ghoul(self.game, x, y)
        elif enType == 1:
            retMob = Actor_Zombie(self.game, x, y)
        elif enType == 2:
            retMob = Actor_Skeleton(self.game, x, y)
        elif enType == 3:
            retMob = Actor_Ghost(self.game, x, y)
        else:
            retMob = Actor_Slime(self.game, x, y)
        return retMob


    

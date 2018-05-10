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
    def __init__(self, game, tileType, enemyType=randint(0,4), \
                 difficulty=randint(3, 5)):
        self.enemyType = enemyType
        self.tileType = tileType
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
        while True:
            spot = self.reserved[randint(0, len(self.reserved)-1)]
            spot = (spot[0]-1, spot[1]-1)
            if spot not in self.reserved:
                break
        # places the exit tile on that location
        self.exit = Tile_Exit(self.game, spot[0], spot[1])
        self.reserved.append(spot)

    # reserves straight lines at random x and y coordinates
    # such that the player won't get blocked in by obstacles
    def reserve(self):
        self.reserved = list()
        # x and y axis for below
        ranX = randint(1, TILE_TO_GRID-2)
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
            Obs_Stump(self.game, randCoord[0], randCoord[1])
            # reduces amount of obstacles to place
            obstacles -= 1

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
        player.place(3,6)
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
            currentMob = self.enemyInterpreter(randCoord[0], randCoord[1], self.enemyType)
            # adds currentMob to reserved placement list
            self.reserved.append(currentMob.bounds['c'])

    # takes an int, x, and y, and returns a mob at (x, y) coordinates based on int given
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
    def __init__(self, game, difficulty = randint(3, 4)):
        BaseRoom.__init__(self, game, self.tile_type, self.mob_type, difficulty)
            

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
    def __init__(self, game, difficulty=1):
        self.reserve()
        self.game = game
        self.createFloor()
        self.placePlayer(game.player)
        self.placeMobs(difficulty)
        self.createExit()
        # obstacles should be placed last because they do most accounting
        # for objects already placed
        self.placeObstacles()
        game.drawMap

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
                Tile_Grass(self.game, x, y)

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
            for x in range(randint(0,3), TILE_TO_GRID, \
                           randint(randint(1,2), 7)):
                for y in range(randint(0,3), TILE_TO_GRID, \
                               randint(randint(1,2), 4)):
                    if tuple((x, y)) not in used:
                        # gives the obstacle a 50% chance to be placed
                        chance = randint(0, 100)
                        # skips over reserved coordinates
                        if (x, y) in self.reserved:
                            break
                        # keeps the loop from overplacing
                        if obstacles <= 0:
                            break
                        # places the obstacle if chance > 50%
                        if chance >= 50:
                            # adds current coordinates to used set
                            used.add(tuple((x, y)))
                            # creates a new stump at given coordinates
                            Obs_Stump(self.game, x, y)
                            # reduces amount of obstacles to place
                            obstacles -= 1
                        
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
        # for now only places one mob
        # will be developed futher in the future
        for mob in range(1):
            currentMob = Actor_Ghost(self.game, 3, 4)
            # adds currentMob to reserved placement list
            self.reserved.append(currentMob.bounds['c'])

# refer to pygame as pg
import pygame as pg
# other game files
from settings import *
from sprites import *
from random import randint

################################################################################

# ROOM CLASSES

# test room with only grass
class Room_GrassTest(object):
    def __init__(self, game, difficulty=1):
        self.game = game
        self.createFloor()
        self.placePlayer(game.player)
        self.placeObstacles()
        self.placeMobs(difficulty)

    # create the base floor for the room
    def createFloor(self):
        for x in range(0, TILE_TO_GRID):
            for y in range(0, TILE_TO_GRID):
                # pass each tile an x and y coordinate
                # game parameter is for sprite grouping
                Tile_Grass(self.game, x, y)

    # places obstacles such as cave walls or rocks
    def placeObstacles(self):
        obstacles = 6
        while obstacles > 0:
            for x in range(0, TILE_TO_GRID, randint(1, 3)):
                for y in range(0, TILE_TO_GRID, randint(1, 3)):
                    chance = randint(0, 100)
                    if chance >= 50:
                        Obs_Stump(self.game, x, y)
                        obstacles -= 1
                        
    # places the player appropriately
    # this function will change later in the developement of the game
    def placePlayer(self, player):
        # later the player will be placed toward the exit of the previous room
        # for now the character is placed at the bottom of the map
        player.place(3,6)

    def placeMobs(self, num):
        for n in range(num):
            pass
        Actor_Ghost(self.game, 3, 4)

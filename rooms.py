# refer to pygame as pg
import pygame as pg
# other game files
from settings import *
from sprites import *

################################################################################

# test room with only grass
class Room_GrassTest(object):
    def __init__(self,game):
        self.createFloor(game)
        self.placePlayer(game.player)

    # create the base floor for the room
    def createFloor(self, game):
        for x in range(0, TILE_TO_GRID):
            for y in range(0, TILE_TO_GRID):
                # pass each tile an x and y coordinate
                # game parameter is for sprite grouping
                GrassTile(game, x, y)

    # places obstacles such as cave walls or rocks
    def placeObstacles(self):
        pass

    # places the player appropriately
    # this function will change later in the developement of the game
    def placePlayer(self, player):
        # later the player will be placed toward the exit of the previous room
        # for now the character is placed at the bottom of the map
        player.place(7, 15)

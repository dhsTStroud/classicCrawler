# refer to pygame as "pg"
import pygame as pg
# other game files
from settings import *

################################################################################

# SUPERCLASSES

# base actor sprite with basic functionality and required functions
class ActorSprite(object):
    def __init__(self, game, x, y):
        self.game = game
        self.x = x
        self.y = y

    # every actor sprite needs a move method
    def move(self):
        raise NotImplementedError("ACTOR SPRITES NEED TO MOVE")

    # checks for border in the direction the player is trying to move
    def borderCheck(self, key):
        retVar = True
        # if the player is at the border, retVar is set to False
        if (key == "a") and (self.rect.x <= min(MAP_BORDER)):
            retVar = False
        if (key == "d") and (self.rect.x >= max(MAP_BORDER)):
            retVar = False
        if (key == "w") and (self.rect.y <= min(MAP_BORDER)):
            retVar = False
        if (key == "s") and (self.rect.y >= max(MAP_BORDER)):
            retVar = False
        # if retVar is True at this point the player will be able to move
        # else they are at the border and will not be able to go that way
        return retVar

    # places the actor at specific coordinates
    def place(self, x, y):
        self.x = x
        self.y = y

    # sets the sprite at the right x and y coordinates
    def update(self):
        raise NotImplementedError("ACTOR SPRITES NEED UPDATE FUNCTIONS")

################################################################################

# SPRITE CLASSES

# player sprite
class Player(pg.sprite.Sprite, ActorSprite):
    def __init__(self, game, x, y):
        self.groups = game.allSprites
        pg.sprite.Sprite.__init__(self, self.groups)
        ActorSprite.__init__(self, game, x, y)
        self.image = pg.image.load("assets/images/player.png")
        # creates bounding box for sprite
        self.rect = self.image.get_rect()

    # moves the sprite
    def move(self, key):
        # checks for border
        goodForGo = self.borderCheck(key)
        # if no border, player is moved
        if goodForGo:
            # moves player left
            if key == "a":
                self.x -= 1
            # moves player right
            elif key == "d":
                self.x += 1
            # moves player up
            elif key == "w":
                self.y -= 1
            # moves player down
            else:
                self.y += 1

    # sets the sprite at the right x and y coordinates
    def update(self):
        # kinda complicated to explain
        # places tiles in multiples of tile size so that they line
        # up at the right pixel number
        self.rect.x = self.x * TILE_SIZE
        self.rect.y = self.y * TILE_SIZE

# class for grass tile (might switch this out for a blit)
class GrassTile(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.tiles
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.image.load("assets/images/tile_grass.png")
        # creates bounding box
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILE_SIZE
        self.rect.y = y * TILE_SIZE
        


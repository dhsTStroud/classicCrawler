# refer to pygame as "pg"
import pygame as pg
# other game files
from settings import *
from random import randint

################################################################################
# USEFUL SPRITE CONSTANTS

IMAGE_PATH = "assets/images/"
# list comprehension makes so we only have to add the file name
# to list for correct path. saves a lot of time typing
# list of actor sprite images
ACTOR_IMG_LIST = [(IMAGE_PATH+"act_"+i+".png") for i in ["player", "ghoul",\
                                                         "zombie", "skeleton",\
                                                         "ghost"]]
# list of slime sprite images
SLIME_IMG_LIST = [(IMAGE_PATH+"act_slime_"+i+".png") for i in ["blue", "gold",\
                                                               "green", "purple",\
                                                               "red", "steel"]]
# list of tile sprite images
TILE_IMG_LIST = [(IMAGE_PATH+"tile_"+i+".png") for i in ["exit", "grass",\
                                                         "dirt", "stone",]]
# list of obsacle sprite images
OBS_IMG_LIST = [(IMAGE_PATH+"obs_"+i+".png") for i in ["stump"]]

################################################################################

# SUPERCLASSES

# Tile superclass
class Tile(object):
    def __init__(self, game, x, y):
        self.game = game
        # rotates tile so to make the map look more unique
        self.image = pg.transform.rotate(self.image, float(90 * randint(0, 4)))
        # creates bounding box
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILE_SIZE
        self.rect.y = y * TILE_SIZE
    

# base actor sprite with basic functionality and required functions
class Actor(object):
    def __init__(self, name, game, x=0, y=0):
        self.name = str(name)
        self.game = game
        self.x = x
        self.y = y
        self.boundary()

    # moves the sprite
    # pass in 'w' for up
    # 's' for down, 'd' for right
    # and 'a' for left
    def move(self, key):
        # checks for obstructions
        # could be obstacles or other actors
        noBlock = self.collide(key)
        # checks for border
        noBorder = self.borderCheck(key)
        # if no border, player is moved
        if (noBorder and noBlock):
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
        # recreates the object's bounds after every move
        self.boundary()

    # creates a collision if something is in the way
    def collide(self, key):
        retVar = True
        # defines an area in movable tiles
        for sprite in self.game.allActorSprites:
            # object skips itself if in sprite group
            if sprite == self:
                continue
            # if the current sprite's bounds are in the direction
            # the current object is trying to move, then the movement is canceled
            if sprite.bounds['c'] in self.bounds.values():
                for k, v in self.bounds.iteritems():
                    if (sprite.bounds['c'] == v) and (key == k):
                        retVar = False
        return retVar

    # checks for border in the direction the player is trying to move
    def borderCheck(self, key):
        retVar = True
        # if the player is at the border, retVar is set to False
        if ((key == "a") and (self.rect.x <= min(MAP_BORDER))) or\
           ((key == "d") and (self.rect.x >= max(MAP_BORDER))) or\
           ((key == "w") and (self.rect.y <= min(MAP_BORDER))) or\
           ((key == "s") and (self.rect.y >= max(MAP_BORDER))):
            retVar = False
        # if retVar is True at this point the player will be able to move
        # else they are at the border and will not be able to go that way
        return retVar

    # defines interact range
    def boundary(self):
        self.bounds = {'d':((self.x+1), self.y), 'w':(self.x, (self.y-1)),\
                       'a':((self.x-1), self.y), 's':(self.x, (self.y+1)),\
                       'c':(self.x, self.y)}

    # places the actor at specific coordinates
    def place(self, x, y):
        self.x = x
        self.y = y
        self.boundary()

    # returns the sprite's name if called to print
    def __str__(self):
        return self.name

    # update function doesn't seem to work when put in the
    # superclass, will have to be unique for all instances
    def update(self):
        raise NotImplementedError("ACTOR SPRITES NEED UPDATE FUNCTIONS")

# monster base class
class Monster(Actor, pg.sprite.Sprite):
    # image should be an integer refering to the respective image list above
    def __init__(self, name, game, x, y, imageNum):
        self.groups += game.mobSprites
        pg.sprite.Sprite.__init__(self, self.groups)
        # loads respective image from image list
        self.image = pg.image.load(ACTOR_IMG_LIST[imageNum])
        # creates the bounding box for the sprite
        self.rect = self.image.get_rect()
        Actor.__init__(self, name, game, x, y)

    # monsters will autopath towards the player
    def autoPath(self):
        target = (self.game.player.x, self.game.player.y)
        pass

    # update function doesn't seem to work when put in the
    # superclass, will have to be unique for all instances
    def update(self):
        self.enemies = self.game.player
        self.rect.x = self.x * TILE_SIZE
        self.rect.y = self.y * TILE_SIZE     

################################################################################

# SPRITE CLASSES

# player sprite
class Actor_Player(pg.sprite.Sprite, Actor):
    def __init__(self, game, x, y):
        # adds self to appropriate spritelist in game
        self.groups = game.allActorSprites
        pg.sprite.Sprite.__init__(self, self.groups)
        # loads player image from image list
        self.image = pg.image.load(ACTOR_IMG_LIST[0])
        # creates bounding box for sprite
        self.rect = self.image.get_rect()
        Actor.__init__(self, "Player", game, x, y)

    # sets the sprite at the right x and y coordinates
    def update(self):
        # for distinguishing enemy sprites from mundane sprites
        self.enemies = self.game.mobSprites
        # kinda complicated to explain
        # places tiles in multiples of tile size so that they line
        # up at the right pixel number
        self.rect.x = self.x * TILE_SIZE
        self.rect.y = self.y * TILE_SIZE

class Actor_Ghost(Monster):
    def __init__(self, game, x, y):
        self.groups = [game.allActorSprites]
        Monster.__init__(self, "Ghost", game, x, y, 4)

################################################################################

# TILE CLASSES

# class for grass tile (might switch this out for a blit)
class GrassTile(pg.sprite.Sprite, Tile):
    def __init__(self, game, x, y):
        # adds self to appropriate spritelist in game
        self.groups = game.tiles
        # runs pygame inbuilt sprite class constructor
        pg.sprite.Sprite.__init__(self, self.groups)
        # sets unique image
        self.image = pg.image.load(TILE_IMG_LIST[1])
        # runs Tile superclass contructor
        Tile.__init__(self, game, x, y)

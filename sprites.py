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

# game base class that all superclasses should inherit from
class Game_Class(object):
    def __init__(self, game, x, y):
        self.game = game
        self.x = x
        self.y = y

    ############################################################################
# Obtacle superclass
class Obstacle(Game_Class, pg.sprite.Sprite):
    def __init__(self, game, x, y, imgNum):
        self.groups = game.obs_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        Game_Class.__init__(self, game, x, y)
        # sets obstacle image
        self.image = pg.image.load(OBS_IMG_LIST[imgNum])
        # creates sprite bounding box
        self.rect = self.image.get_rect()
        # places at correct pixel numbers per x and y
        self.rect.x = x * TILE_SIZE
        self.rect.y = y * TILE_SIZE
        # bounds for actor interaction
        self.bounds = {'c':(self.x, self.y)}

    ############################################################################
        
# Tile superclass
class Tile(Game_Class, pg.sprite.Sprite):
    def __init__(self, game, x, y, imgNum):
        Game_Class.__init__(self, game, x, y)
        # sets tile image
        self.image = pg.image.load(TILE_IMG_LIST[imgNum])
        self.rotate()
        # creates sprite bounding box
        self.rect = self.image.get_rect()
        # places at correct pixel numbers per x and y
        self.rect.x = x * TILE_SIZE
        self.rect.y = y * TILE_SIZE

    # rotates tile so to make the map look more unique
    def rotate(self):
        # rotates the picture such that (image, degree of rotation)
        # the picture is rotated in random intervals of 90 degrees
        self.image = pg.transform.rotate(self.image, float(90 * randint(0, 4)))
        

    ############################################################################

# base actor sprite with basic functionality and required functions
class Actor(Game_Class):
    def __init__(self, name, game, x=0, y=0):
        Game_Class.__init__(self, game, x, y)
        self.name = str(name)
        self.act_boundary()

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
        self.act_boundary()

    # creates a collision if something is in the way
    def collide(self, key):
        # variable to be returned
        retVar = True
        # defines an area in movable tiles
        for spriteGroup in self.game.allActorSprites, self.game.obs_sprites:
            for sprite in spriteGroup:
                # object skips itself if in sprite group
                if sprite == self:
                    continue
                # if the current sprite's bounds are in the direction
                # the current object is trying to move,
                # then the movement is canceled
                if sprite.bounds['c'] in self.bounds.values():
                    # for key, value pair in own bounds
                    for k, v in self.bounds.iteritems():
                        # if target sprite is in target direction return false
                        # false meaning you can't move in that direction
                        if (sprite.bounds['c'] == v) and (key == k):
                            # will initiate combat if an enemy is encountered
                            if (sprite in self.enemies):
                                # for now just changes return variable to false
                                retVar = False
                            else:
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
    def act_boundary(self):
        self.bounds = {'d':((self.x+1), self.y), 'w':(self.x, (self.y-1)),\
                       'a':((self.x-1), self.y), 's':(self.x, (self.y+1)),\
                       'c':(self.x, self.y)}

    # places the actor at specific coordinates
    def place(self, x, y):
        self.x = x
        self.y = y
        self.act_boundary()

    # returns the sprite's name if called to print
    def __str__(self):
        return self.name

    # update function doesn't seem to work when put in the
    # superclass, will have to be unique for all instances
    def update(self):
        raise NotImplementedError("ACTOR SPRITES NEED UPDATE FUNCTIONS")

    ############################################################################

# monster base class
class Monster(Actor, pg.sprite.Sprite):
    # image should be an integer refering to the respective image list above
    def __init__(self, name, game, x, y, imageNum):
        self.groups = game.mob_sprites, game.allActorSprites
        pg.sprite.Sprite.__init__(self, self.groups)
        # loads respective image from image list
        self.image = pg.image.load(ACTOR_IMG_LIST[imageNum])
        # creates the bounding box for the sprite
        self.rect = self.image.get_rect()
        Actor.__init__(self, name, game, x, y)
        # sets the player as it's enemy
        self.enemies = [self.game.player]
        self.autoPath()

    # monsters will autopath towards the player
    def autoPath(self):
        target = (self.enemies[0].bounds['c'])
        self.act_boundary()

    # what to do when called to update
    def update(self):
        # calculates the pixel representation of x and y
        # if x = 3, then 3 * TILE_SIZE = where the image will be placed
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
        self.enemies = self.game.mob_sprites
        # kinda complicated to explain
        # places tiles in multiples of tile size so that they line
        # up at the right pixel number
        self.rect.x = self.x * TILE_SIZE
        self.rect.y = self.y * TILE_SIZE

    ############################################################################

# MOB CLASSES

# ghost mob class
class Actor_Ghost(Monster):
    def __init__(self, game, x, y):
        Monster.__init__(self, "Ghost", game, x, y, 4)

################################################################################

# TILE CLASSES

# class for grass tile (might switch this out for a blit)
class Tile_Grass(Tile):
    def __init__(self, game, x, y):
        # adds self to appropriate spritelist in game
        self.groups = game.tile_sprites
        # runs pygame inbuilt sprite class constructor
        pg.sprite.Sprite.__init__(self, self.groups)
        # runs Tile superclass contructor
        Tile.__init__(self, game, x, y, 1)

    ############################################################################

class Obs_Stump(Obstacle):
    def __init__(self, game, x, y):
        Obstacle.__init__(self, game, x, y, 0)

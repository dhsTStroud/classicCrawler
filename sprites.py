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
OBS_IMG_LIST = [(IMAGE_PATH+"obs_"+i+".png") for i in ["stump", "dirtmound",\
                                                       "rock"]]

################################################################################

# SUPERCLASSES

# game base class that all superclasses should inherit from
class Game_Class(object):
    def __init__(self, game, x, y):
        self.temp_groups = []
        self.game = game
        self.x = x
        self.y = y

    @property
    def x(self):
        return self._x
    @x.setter
    def x(self, value):
        # performs range checking
        if (value >= 0) and (value <= TILE_TO_GRID):
            self._x = value
        else:
            self._x = 0

    @property
    def y(self):
        return self._y
    @y.setter
    def y(self, value):
        # performs range checking
        if (value >= 0) and (value <= TILE_TO_GRID):
            self._y = value
        else:
            self._y = 0

    # multiplies 
    def placeAtTile(self):
        # places at correct pixel numbers per x and y
        self.rect.x = self.x * TILE_SIZE
        self.rect.y = self.y * TILE_SIZE

    # defines an interact range
    # in the form of set boundaries
    def boundary(self):
        self.bounds = {'d':((self.x+1), self.y), 'w':(self.x, (self.y-1)),\
                       'a':((self.x-1), self.y), 's':(self.x, (self.y+1)),\
                       'c':(self.x, self.y)}
                
    # sets the sprite at the right x and y coordinates
    def update(self):
        # places tiles in multiples of tile size so that they line
        # up at the right pixel number
        self.rect.x = self.x * TILE_SIZE
        self.rect.y = self.y * TILE_SIZE

    # sets up groups
    def setup_groups(self, base, extra):
        # adds to the existing base
        self.temp_groups.append(base)
        # adds any extra groups given as parameters
        if extra != None:
            # will add more than one group if extra is a list or tuple
            if isinstance(extra, list or tuple):
                for group in extra:
                    self.temp_groups.append(group)
            # otherwise will add single item
            else:
                self.temp_groups.append(extra)
                    
        # finally sets groups variable that will be given
        # as a parameter to pygame.sprite.Sprite() constructor
        self.groups = tuple(self.temp_groups)
        

    ############################################################################

# Obtacle superclass
class Obstacle(Game_Class, pg.sprite.Sprite):
    # KEYWORDS AND CLASS VARIABLES
    spr_type = "obstacle"
    
    # imgnum will be an index in the corresponding 
    # image direcory list found above
    def __init__(self, game, x, y, imgNum):
        self.groups = game.obs_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        Game_Class.__init__(self, game, x, y)
        # sets obstacle image
        self.image = pg.image.load(OBS_IMG_LIST[imgNum])
        self.flipImage()
        # creates sprite bounding box
        self.rect = self.image.get_rect()
        # places on grid
        self.placeAtTile()
        self.boundary()
        self.update()

    def flipImage(self):
        amount = randint(0, 10)
        for i in range(amount):
            self.image = pg.transform.flip(self.image, True, False)

    # creates object bounds
    def boundary(self):
        # bounds for actor interaction
        self.bounds = {'c':(self.x, self.y)}
        

    ############################################################################
        
# Tile superclass
class Tile(Game_Class, pg.sprite.Sprite):
    # KEYWORDS AND CLASS VARIABLES
    spr_type = "tile"
    
    # imgnum will be an index in the corresponding 
    # image direcory list found above
    def __init__(self, game, x, y, imgNum, group=None):
        Game_Class.__init__(self, game, x, y)
        # set up groups
        # first group is base group, second is extra
        self.groupon = group
        self.setup_groups(self.game.tile_sprites, group)
        self.groups = self.temp_groups
        # runs pygame inbuilt sprite class constructor
        pg.sprite.Sprite.__init__(self, self.groups)
        # sets tile image
        self.image = pg.image.load(TILE_IMG_LIST[imgNum])
        self.rotate()
        # creates sprite bounding box
        self.rect = self.image.get_rect()
        self.boundary()
        self.update()

    # creates object bounds
    def boundary(self):
        # bounds for actor interaction
        self.bounds = {'c':(self.x, self.y)}

    # rotates tile so to make the map look more unique
    def rotate(self):
        # rotates the picture such that (image, degree of rotation)
        # the picture is rotated in random intervals of 90 degrees
        self.image = pg.transform.rotate(self.image, float(90 * randint(0, 4)))
        

    ############################################################################

# base actor sprite with basic functionality and required functions
class Actor(Game_Class, pg.sprite.Sprite):
    # group is an optional extra for subclasses that require more than one
    def __init__(self, game, x=0, y=0, name="ACTOR", group=None):
        Game_Class.__init__(self, game, x, y)
        # set up groups
        # first group is base group, second is extra
        self.setup_groups(self.game.allActorSprites, group)
        # Sprite constructor, pygame built in
        pg.sprite.Sprite.__init__(self, self.groups)
        # sets Actor name
        self.name = name
        # creates initial boundaries
        self.boundary()
        self.living = True
        try:
            # actor health at given time
            self.curHealth = self.maxHealth
        except:
            print "{} does not have maxHealth stat".format(self)

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
            if (key == "a"):
                self.x -= 1
            # moves player right
            elif (key == "d"):
                self.x += 1
            # moves player up
            elif (key == "w"):
                self.y -= 1
            # moves player down
            else:
                self.y += 1
        # recreates the object's bounds after every move
        self.boundary()

    # creates a collision if something is in the way
    def collide(self, key):
        # variable to be returned
        retVar = True
        # defines an area in movable tiles
        for spriteGroup in self.game.allActorSprites, self.game.obs_sprites,\
            self.game.special_tiles:
            for sprite in spriteGroup:
                # object skips itself if in sprite group
                if (sprite == self):
                    continue
                # if the current sprite's bounds are in the direction
                # the current object is trying to move,
                # then the movement is canceled
                if (sprite.bounds['c'] in self.bounds.values()):
                    # for key, value pair in own bounds
                    for k, v in self.bounds.iteritems():
                        # if target sprite is in target direction return false
                        # false meaning you can't move in that direction
                        if (sprite.bounds['c'] == v) and (key == k):
                            # will initiate combat if an enemy is encountered
                            if (self.enemies == sprite.spr_type):
                                # for now just changes return variable to false
                                retVar = False
                            elif (self == self.game.player) and\
                                 (sprite.spr_type == "exit"):
                                self.game.setRoom()
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

    # places the actor at specific coordinates
    def place(self, x, y):
        self.x = x
        self.y = y
        self.boundary()

    def heal(self, amount):
        self.curhealth += amount
        if self.curHealth > self.maxHealth:
            self.curHealth = self.maxHealth

    # takes damage
    def takeDamage(self, amount):
        self.curHealth -= amount
        if self.curHealth < 0:
            self.living = False
        return self.living

    # MAGIC METHODS
    
    # returns the sprite's name if called to print
    def __str__(self):
        return "{}_{}".format(self.spr_type, self.name)

    # ABSTRACT METHODS

    # sets or adds levels depending on the actor
    def levelUp(self):
        raise NotImplementedError("{} needs levelUp method.".format(self))

    ############################################################################

# monster base class
class Monster(Actor):
    # KEYWORDS AND CLASS VARIABLES
    spr_type = "mob"
    enemies = "player"
    
    # image should be an integer refering to the respective image list above
    # if monster is a slime input 1 for slime parameter
    def __init__(self, game, x, y, imgNum, name, slime=False):
        # adds self to game.mob_sprites sprite group
        self.temp_groups = game.mob_sprites
        Actor.__init__(self, game, x, y, name, self.temp_groups)
        # loads respective image from image list
        if (slime == True):
            self.slime = slime
            self.image = pg.image.load(SLIME_IMG_LIST[imgNum])
        else:
            self.image = pg.image.load(ACTOR_IMG_LIST[imgNum])
        # creates the bounding box for the sprite
        self.rect = self.image.get_rect()

    # monsters will autopath towards the player
    def autoPath(self):
        self.boundary()

    # what to do when called to update
    def update(self):
        # calculates the pixel representation of x and y
        # if x = 3, then 3 * TILE_SIZE = where the image will be placed
        self.rect.x = self.x * TILE_SIZE
        self.rect.y = self.y * TILE_SIZE

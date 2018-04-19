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
        self.temp_groups = []
        self.game = game
        self.x = x
        self.y = y

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
        # places on grid
        self.placeAtTile()
        self.boundary()
        self.update()

    # creates object bounds
    def boundary(self):
        # bounds for actor interaction
        self.bounds = {'c':(self.x, self.y)}
        

    ############################################################################
        
# Tile superclass
class Tile(Game_Class, pg.sprite.Sprite):
    def __init__(self, game, x, y, imgNum):
        Game_Class.__init__(self, game, x, y)
        # adds self to appropriate spritelist in game
        self.temp_groups.append(game.tile_sprites)
        self.groups = self.temp_groups
        # runs pygame inbuilt sprite class constructor
        pg.sprite.Sprite.__init__(self, self.groups)
        # sets tile image
        self.image = pg.image.load(TILE_IMG_LIST[imgNum])
        self.rotate()
        # creates sprite bounding box
        self.rect = self.image.get_rect()
        self.update()

    # rotates tile so to make the map look more unique
    def rotate(self):
        # rotates the picture such that (image, degree of rotation)
        # the picture is rotated in random intervals of 90 degrees
        self.image = pg.transform.rotate(self.image, float(90 * randint(0, 4)))
        

    ############################################################################

# base actor sprite with basic functionality and required functions
class Actor(Game_Class, pg.sprite.Sprite):
    def __init__(self, game, x=0, y=0, name="ACTOR", group=None):
        Game_Class.__init__(self, game, x, y)
        # set up groups
        self.act_groups(group)
        # Sprite constructor, pygame built in
        pg.sprite.Sprite.__init__(self, self.groups)
        # sets Actor name
        self.name = str(name)
        # creates initial boundaries
        self.boundary()

    # sets up Actor groups
    def act_groups(self, extra=None):
        # Actor sprites goes in allActorSprites
        self.temp_groups.append(self.game.allActorSprites)
        # adds any extra groups given as parameters
        if extra != None:
            self.temp_groups.append(extra)
        # finally sets groups variable that will be given
        # as a parameter to pygame.sprite.Sprite() constructor
        self.groups = tuple(self.temp_groups)

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

    # places the actor at specific coordinates
    def place(self, x, y):
        self.x = x
        self.y = y
        self.boundary()

    # MAGIC FUNCTIONS
    
    # returns the sprite's name if called to print
    def __str__(self):
        return "{}_{}".format(self.actor_type, self.name)

    # ABSTRACT METHODS
    
    # all actors must have a setEnemies method
    def setEnemies(self):
        raise NotImplementedError(\
            "{} does not have a setEnemies method".format(self.name))

##    # update function doesn't seem to work when put in the
##    # superclass, will have to be unique for all instances
##    def update(self):
##        raise NotImplementedError("ACTOR SPRITES NEED UPDATE FUNCTIONS")

    ############################################################################

# monster base class
class Monster(Actor):
    # KEYWORDS AND CLASS VARIABLES
    actor_type = "mob"
    
    # image should be an integer refering to the respective image list above
    def __init__(self, game, x, y, imgNum, name):
        # adds self to game.mob_sprites sprite group
        self.temp_groups = game.mob_sprites
        Actor.__init__(self, game, x, y, name, self.temp_groups)
        # loads respective image from image list
        self.image = pg.image.load(ACTOR_IMG_LIST[imgNum])
        # creates the bounding box for the sprite
        self.rect = self.image.get_rect()
        self.autoPath()

    # satisfies parent abstract method
    # sets monster enemy as player when called
    # should only be called in room classes
    def setEnemies(self):
        # sets the player as it's enemy
        self.enemies = [self.game.player]
        # sets the player as this sprite's target
        target = (self.enemies[0].bounds['c'])

    # monsters will autopath towards the player
    def autoPath(self):
        self.boundary()

    # what to do when called to update
    def update(self):
        # calculates the pixel representation of x and y
        # if x = 3, then 3 * TILE_SIZE = where the image will be placed
        self.rect.x = self.x * TILE_SIZE
        self.rect.y = self.y * TILE_SIZE     

################################################################################

# SPRITE CLASSES

# player sprite
class Actor_Player(Actor):
    # KEYWORDS AND CLASS VARIABLES
    # loads player image from image list
    image = pg.image.load(ACTOR_IMG_LIST[0])
    actor_type = "player"
    def __init__(self, game, x, y):
        # creates bounding box for sprite
        self.rect = self.image.get_rect()
        Actor.__init__(self, game, x, y, "Player")

    # set or clear self.enemies
    # either pass in a list of enemies or leave empty to clear the list
    # clearing would be used for switching maps
    # can also set enemies to "all" to set all mobs in mob_sprites as enemies
    def setEnemies(self, varEnemies=None):
        self.enemies = []
        # if enemies != 1
        if varEnemies != (None or "all"):
            # add each enemy to the list
            for enemy in varEnemies:
                self.varEnemies.append(enemy)
        # will set enemies to all existing mob sprites
        if varEnemies == "all":
            for enemy in self.game.mob_sprites:
                # for distinguishing enemy sprites from mundane sprites
                self.enemies.append(enemy)

    ############################################################################

# MOB CLASSES

# follows this format:
# (if you copy paste this, just change the class name and image number)
'''
class _Mob_Template(Monster):
    # KEYWORDS AND CLASS VARIABLES
    # respective image index from TILE_IMAGE_LIST (see at top)
    image = 4
    
    def __init__(self, game, x, y):
        # passes in (self, game, x, y, imgNum, name="ACTOR")
        Monster.__init__(self, game, x, y, self.image, "Ghost")
'''

# ghost mob class
class Actor_Ghost(Monster):
    # KEYWORDS AND CLASS VARIABLES
    # respective image index from TILE_IMAGE_LIST (see at top)
    image = 4
    
    def __init__(self, game, x, y):
        # passes in (self, game, x, y, imgNum, name="ACTOR")
        Monster.__init__(self, game, x, y, self.image, "Ghost")

################################################################################

# TILE CLASSES

# follows this format:
# (if you copy paste this, just change the class name and image number)
'''
class _Tile_Template(Tile):
    # KEYWORDS AND CLASS VARIABLES
    # respective image index from TILE_IMAGE_LIST (see at top)
    image = int()
    
    def __init__(self, game, x, y):
        # passes in (self, game, x, y, imgNum)
        Tile.__init__(self, game, x, y, self.image)
'''

# class for grass tile
class Tile_Grass(Tile):
    # KEYWORDS AND CLASS VARIABLES
    image = 1
    
    def __init__(self, game, x, y):
        # passes in (self, game, x, y, imgNum)
        Tile.__init__(self, game, x, y, self.image)

    ############################################################################

# OBSTACLE CLASSES

# follows this format:
# (if you copy paste this, just change the class name and image number)
'''
class _Obs_Template(Obstacle):
    # KEYWORDS AND CLASS VARIABLES
    # respective image index from OBS_IMAGE_LIST (see at top)
    image = int()
    
    def __init__(self, game, x, y):
        # passes in (self, game, x, y, imgNum)
        Obstacle.__init__(self, game, x, y, 0)
'''

# stump obstacle class
class Obs_Stump(Obstacle):
    # KEYWORDS AND CLASS VARIABLES
    image = 0
    
    def __init__(self, game, x, y):
        # passes in (self, game, x, y, imgNum)
        Obstacle.__init__(self, game, x, y, 0)

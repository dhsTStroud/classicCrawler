# refer to pygame as "pg"
import pygame as pg
# other game files
from settings import *
from random import randint
from sprites import *

################################################################################

# SPRITE CLASSES

# player sprite
class Actor_Player(Actor):
    # KEYWORDS AND CLASS VARIABLES
    # loads player image from image list
    image = pg.image.load(ACTOR_IMG_LIST[0])
    spr_type = "player"
    name = "Player"
    enemies = "mob"
    maxHealth = 100
    
    def __init__(self, game, x, y):
        # creates bounding box for sprite
        self.rect = self.image.get_rect()
        Actor.__init__(self, game, x, y, self.name)

    ############################################################################

# MOB CLASSES

# follows this format:
# (if you copy paste this, just change the class name and image number)
'''
# <mob name> mob class
class _Mob_Template(Monster):
    # KEYWORDS AND CLASS VARIABLES
    # respective image index from TILE_IMAGE_LIST (see at top)
    image = int()
    name = str()
    
    def __init__(self, game, x, y):
        # passes in (self, game, x, y, imgNum, name="ACTOR")
        # if mob is a slime, put True after self.name
        Monster.__init__(self, game, x, y, self.image, self.name)
'''


# ghost mob class
class Actor_Ghost(Monster):
    # KEYWORDS AND CLASS VARIABLES
    # respective image index from TILE_IMAGE_LIST (see at top)
    image = 4
    name = "Ghost"
    maxHealth = 100
    
    def __init__(self, game, x, y):
        # passes in (self, game, x, y, imgNum, name="ACTOR")
        Monster.__init__(self, game, x, y, self.image, self.name)


# zombie mob class
class Actor_Zombie(Monster):
    # KEYWORDS AND CLASS VARIABLES
    # respective image index from TILE_IMAGE_LIST (see at top)
    image = 2
    name = "Zombie"
    maxHealth = 50
    
    def __init__(self, game, x, y):
        # passes in (self, game, x, y, imgNum, name="ACTOR")
        Monster.__init__(self, game, x, y, self.image, self.name)


# ghoul mob class
class Actor_Ghoul(Monster):
    # KEYWORDS AND CLASS VARIABLES
    # respective image index from TILE_IMAGE_LIST (see at top)
    image = int(1)
    name = "Ghoul"
    maxHealth = 75
    
    def __init__(self, game, x, y):
        # passes in (self, game, x, y, imgNum, name="ACTOR")
        Monster.__init__(self, game, x, y, self.image, self.name)


# skeleton mob class
class Actor_Skeleton(Monster):
    # KEYWORDS AND CLASS VARIABLES
    # respective image index from TILE_IMAGE_LIST (see at top)
    image = int(3)
    name = "Skeleton"
    maxHealth = 25
    
    def __init__(self, game, x, y):
        # passes in (self, game, x, y, imgNum, name="ACTOR")
        Monster.__init__(self, game, x, y, self.image, self.name)

        
# blue slime mob class
class Actor_Slime(Monster):
    # KEYWORDS AND CLASS VARIABLES
    # respective image index from TILE_IMAGE_LIST (see at top)
    image = randint(0, len(SLIME_IMG_LIST))
    name = "Slime"
    maxHealth = 25
    
    def __init__(self, game, x, y):
        # passes in (self, game, x, y, imgNum, name="ACTOR")
        # if mob is a slime, put True after self.name
        Monster.__init__(self, game, x, y, self.image, self.name, True)

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
        # passes in (self, game, x, y, imgNum, group=None)
        Tile.__init__(self, game, x, y, self.image)
'''


# class for exit tile
class Tile_Exit(Tile):
    # KEYWORDS AND CLASS VARIABLES
    image = 0

    def __init__(self, game, x, y):
        # passes in (self, game, x, y, imgNum, group=None)
        Tile.__init__(self, game, x, y, self.image, game.special_tiles)


# class for grass tile
class Tile_Grass(Tile):
    # KEYWORDS AND CLASS VARIABLES
    image = 1
    
    def __init__(self, game, x, y):
        # passes in (self, game, x, y, imgNum, group=None)
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

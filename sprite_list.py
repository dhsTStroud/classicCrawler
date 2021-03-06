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
        self.score = 0
        self.healthPotions = 3
        # creates bounding box for sprite
        self.rect = self.image.get_rect()
        Actor.__init__(self, game, x, y, self.name)

    # changes score by given number
    def addScore(self, amount):
        self.score += amount

    # removes a potion when called
    def drinkHealthPotion(self):
        retString = "I'm out of health potions!"
        if self.curHealth >= self.maxHealth:
            self.curHealth = self.maxHealth
            retString = "My health is full."
        elif (self.healthPotions >= 1):
            retString = "I drank a health potion."
            self.heal(25)
            self.healthPotions -= 1
        return retString

    # adds an amount of health potions to player stockpile
    def addHealthPotions(self, amount):
        retString = "I have too many health potions already!"
        if self.healthPotions >= 99:
            return retString
        else:
            if amount <= 0:
                retString = "I got nothing for that, what a waste."
                return retString
            elif amount == 1:
                retString = "I recieved a health potion!"
            else:
                retString = "I recieved {} health potions!".format(amount)
            self.healthPotions += amount
        return retString
        

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
        # generates an amount of health potions to return when killed
        # should all three be ints and add up to 100
        self.hPotions = self.loot(chance1, chance2, chance3)

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
        # generates an amount of health potions to return when killed
        self.hPotions = self.loot(10, 40, 50)


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
        # generates an amount of health potions to return when killed
        self.hPotions = self.loot(25, 55, 20)


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
        # generates an amount of health potions to return when killed
        self.hPotions = self.loot(15, 60, 25)


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
        # generates an amount of health potions to return when killed
        self.hPotions = self.loot(25, 60, 15)

        
# blue slime mob class
class Actor_Slime(Monster):
    # KEYWORDS AND CLASS VARIABLES
    # respective image index from TILE_IMAGE_LIST (see at top)
    name = "Slime"
    maxHealth = 25
    
    def __init__(self, game, x, y):
        self.image = randint(0, len(SLIME_IMG_LIST)-1)
        # passes in (self, game, x, y, imgNum, name="ACTOR")
        # if mob is a slime, put True after self.name
        Monster.__init__(self, game, x, y, self.image, self.name, True)
        # generates an amount of health potions to return when killed
        self.hPotions = self.loot(10, 85, 5)

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
    spr_type = "exit"
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
		
# class for dirt tile
class Tile_Dirt(Tile):
    # KEYWORDS AND CLASS VARIABLES
    image = 2
    
    def __init__(self, game, x, y):
        # passes in (self, game, x, y, imgNum, group=None)
        Tile.__init__(self, game, x, y, self.image)
		
# class for stone tile
class Tile_Stone(Tile):
    # KEYWORDS AND CLASS VARIABLES
    image = 3
    
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
    hand = # the hand it plays if forced to fight
    maxHealth = int()
    
    def __init__(self, game, x, y):
        # passes in (self, game, x, y, imgNum)
        Obstacle.__init__(self, game, x, y, self.image)
'''

# stump obstacle class
class Obs_Stump(Obstacle):
    # KEYWORDS AND CLASS VARIABLES
    image = 0
    name = "Stump"
    hand = "paper"
    maxHealth = 25
    
    def __init__(self, game, x, y):
        # passes in (self, game, x, y, imgNum)
        Obstacle.__init__(self, game, x, y, self.image)

# dirt mound obstacle class
class Obs_Dirtmound(Obstacle):
    # KEYWORDS AND CLASS VARIABLES
    # respective image index from OBS_IMAGE_LIST (see at top)
    image = 1
    name = "Dirt Mound"
    hand = "rock"
    maxHealth = 50
    
    def __init__(self, game, x, y):
        # passes in (self, game, x, y, imgNum)
        Obstacle.__init__(self, game, x, y, self.image)

# rock obstacle class
class Obs_Rock(Obstacle):
    # KEYWORDS AND CLASS VARIABLES
    # respective image index from OBS_IMAGE_LIST (see at top)
    image = 2
    name = "Rock"
    hand = "rock"
    maxHealth = 100
    
    def __init__(self, game, x, y):
        # passes in (self, game, x, y, imgNum)
        Obstacle.__init__(self, game, x, y, self.image)

###################################################################################################

# BUTTONS

# health button
class Button_Health(Button):
	# CLASS VARIABLES
	image = 4
	button_type = "health"
	
	def __init__(self, game, x, y):
		Button.__init__(self, game, x, y, self.image)

        # heals the player for a 1/4 of their health
	def action(self):
            retString = self.game.player.drinkHealthPotion()
            return retString
		
# start button
class Button_Start(Button):
	# CLASS VARIABLES
	image = 3
	button_type = "start"
	
	def __init__(self, game, x, y):
		Button.__init__(self, game, x, y, self.image)

        # starts a new game for the game given
	def action(self):
            retString = "Out on a fresh new journey."
            self.game.newGame()
            return retString
		
# scissors button
class Button_Scissors(Button):
	# CLASS VARIABLES
	image = 2
	button_type = "scissors"
	
	def __init__(self, game, x, y):
		Button.__init__(self, game, x, y, self.image)

# rock button
class Button_Rock(Button):
	# CLASS VARIABLES
	image = 0
	button_type = "rock"
	
	def __init__(self, game, x, y):
		Button.__init__(self, game, x, y, self.image)
		
# paper button
class Button_Paper(Button):
	# CLASS VARIABLES
	image = 1
	button_type = "paper"
	
	def __init__(self, game, x, y):
		Button.__init__(self, game, x, y, self.image)

# run button
class Button_Run(Button):
    # CLASS VARIABLES
    image = 5
    button_type = "run"
	
    def __init__(self, game, x, y):
            Button.__init__(self, game, x, y, self.image)

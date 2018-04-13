# refer to pygame as "pg"
import pygame as pg
from settings import *

# player sprite
class Player(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.allSprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.image.load("assets/images/player.png")
        # creates bounding box for sprite
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y

    # moves the sprite
    def move(self, key):
        if key == "a":
            self.x -= 1
        elif key == "d":
            self.x += 1
        elif key == "w":
            self.y -= 1
        else:
            self.y += 1

    def update(self):
        self.rect.x = self.x * TILE_SIZE
        self.rect.y = self.y * TILE_SIZE

# class for grass tile
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
        


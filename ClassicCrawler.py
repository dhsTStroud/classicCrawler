# refer to pygame with "pg"
import pygame as pg
from settings import *
from sprites import *

class Game(object):
    # sets up the GUI 
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        pg.key.set_repeat(500, 100)
    
    # initialize all variables and setup a new game
    def newGame(self):
        # spritegroup for sprites
        self.allSprites = pg.sprite.Group()
        # spritegroup for tiles
        self.tiles = pg.sprite.Group()
        # creates a starting map (room 1)
        self.room1()

    # first map (can and will make a class for maps later)
    def room1(self):
        for x in range(0, TILE_TO_GRID):
            for y in range(0, TILE_TO_GRID):
                GrassTile(self, x, y)
        # places the player somewhere in the room
        # (self, x, y)
        # y should not be greater than 15 or less than 0
        # x should not be greater than 
        self.player = Player(self, 7, 15)
            
    # game loop
    def run(self):
        # set self.playing to False at any time to end game
        self.playing = True
        while self.playing:
            # game ticks at 30 frames a second
            self.dt = self.clock.tick(FPS) / 100
            self.events()
            self.update()
            self.drawMap()

    # closes the window
    def quitGame(self):
        pg.quit()

    # update portion of game loop
    def update(self):
        # updates "allSprites" sprite group
        self.allSprites.update()

    # draws the grid for the map portion of the screen
    def drawGrid(self):
        # draws lines for grid along the x axis to the center
        for x in range(0, WIDTH_CENTER, TILE_SIZE):
            # line(surface, color, start_pos, end_pos)
            pg.draw.line(self.screen, LIGHT_GREY, (x, 0), (x, HEIGHT))
        # draws lines for grid along the y axis to the center
        for y in range(0, HEIGHT, TILE_SIZE):
            # line(surface, color, start_pos, end_pos)
            pg.draw.line(self.screen, LIGHT_GREY, (0, y), (WIDTH_CENTER, y))

    # running draw method
    def drawMap(self):
        self.screen.fill(BG_COLOR)
        self.tiles.draw(self.screen)
        self.drawGrid()
        self.allSprites.draw(self.screen)
        # flips the display each time it's called
        # prevents lag
        pg.display.flip()

    # catches all events
    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quitGame()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_LEFT:
                    self.player.move("a")
                if event.key == pg.K_RIGHT:
                    self.player.move("d")
                if event.key == pg.K_UP:
                    self.player.move("w")
                if event.key == pg.K_DOWN:
                    self.player.move("s")

    # shows the start menu
    def startMenu(self):
        pass

################################################################################
# creates the game object
GAME = Game()
GAME.startMenu()
while True:
    GAME.newGame()
    GAME.run()

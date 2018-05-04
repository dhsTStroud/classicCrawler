# refer to pygame with "pg"
import pygame as pg
# other game files
from settings import *
from sprites import *
from rooms import *
from sprite_list import *
# for testing when not on the pi
try:
    from breadboard import *
    CONTROLLER = True
except:
    CONTROLLER = False

################################################################################

# Game class
class Game(object):
    # sets up the GUI 
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        pg.key.set_repeat(500, 100)
        if CONTROLLER == True:
            self.controller = Controller(self)
    
    # initialize all variables and setup a new game
    def newGame(self):
        self.spriteGroups()
        # creates the player sprite
        self.player = Actor_Player(self, 1, 1)
        # sets player at level 0
        self.roomLevel = 0
        # instantiates all rooms
        self.setRoom()
        # creates the player UI
        self.drawMenu()
        # starts turns 'counter'
        self.playerHasMoved = False

    def spriteGroups(self):
        # spritegroup for sprites
        self.allActorSprites = pg.sprite.Group()
        # spritegroup for monsters
        self.mob_sprites = pg.sprite.Group()
        # spritegroup for tiles
        self.tile_sprites = pg.sprite.Group()
        self.special_tiles = pg.sprite.Group()
##        # spritegroup for UI menu sprites
##        self.menus = pg.sprite.Group()
        # spritegroup for obstacle sprites
        self.obs_sprites = pg.sprite.Group()
        

    # creates the rightside user interface
    def drawMenu(self):
        # loads the image (pg.image.load())
        uiImage = pg.image.load(IMAGE_PATH + "ui_right_menu.png")
        # screen.blit() plasters the image's pixels where you tell it to
        # the picture is not really interactable, only a background
        self.screen.blit(uiImage, (WIDTH_CENTER, 0))

    # sets the room (currently only one)
    def setRoom(self):
        if self.roomLevel == 0:
            currentRoom = BaseRoom(self)
            
    # game loop
    def run(self):
        # set self.playing to False at any time to end game
        self.playing = True
        while self.playing:
            # game ticks at 30 frames a second
            self.fps = self.clock.tick(FPS) / 100
            self.events()
            while self.playerHasMoved == True:
                pass
            self.update()
            self.drawMap()

    # closes the window
    def quitGame(self):
        pg.quit()

    # update portion of game loop
    def update(self):
        # updates "allSprites" sprite group
        self.allActorSprites.update()

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
        self.tile_sprites.draw(self.screen)
        self.obs_sprites.draw(self.screen)
        self.special_tiles.draw(self.screen)
        self.drawGrid()
        self.allActorSprites.draw(self.screen)
        # flips the display each time it's called
        # prevents lag
        pg.display.flip()

    # catches all events
    def events(self):
        button = None
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quitGame()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_LEFT:
                    button = "a"
                if event.key == pg.K_RIGHT:
                    button = "d"
                if event.key == pg.K_UP:
                    button = "w"
                if event.key == pg.K_DOWN:
                    button = "s"
        if CONTROLLER == True:
            button = self.controller.movement()
        return button

    # switches to fight mode
    def startFight(self, enemy):
        plyr = self.player
        enmy = enemy

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

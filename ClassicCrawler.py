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
    # alt-4 if testing controller functionality
    CONTROLLER = True

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
    
    # initialize all variables and setup a new game
    def newGame(self):
        self.spriteGroups()
        # creates the player sprite
        self.player = Actor_Player(self, 1, 1)
        # sets player at level 0
        self.roomLevel = 0
        # instantiates rooms
        self.roomLevel = 0
        self.setRoom()
        # creates the player UI
        self.drawMenu()
        # starts turns 'counter'
        self.playerHasMoved = 0
        self.playerCanMove = True
        self.inBattle = False
        if CONTROLLER:
            self.controller = Controller(self)

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
        self.game_buttons = pg.sprite.Group()

    # empties all sprite groups
    def clearSpriteGroups(self):
        self.allActorSprites.empty()
        self.mob_sprites.empty()
        self.tile_sprites.empty()
        self.special_tiles.empty()
        self.obs_sprites.empty()

    # creates the rightside user interface
    def drawMenu(self):
        # loads the image (pg.image.load())
        uiImage = pg.image.load(IMAGE_PATH + "ui_right_menu.png")
        # screen.blit() plasters the image's pixels where you tell it to
        # the picture is not really interactable, only a background
        self.screen.blit(uiImage, (WIDTH_CENTER, 0))

    # clears the room
    def clearRoom(self):
        # preserves the player
        player = self.player
        # clears all sprite groups
        self.clearSpriteGroups()
        # adds the player back to the appropriate sprite group
        self.allActorSprites.add(player)

    # sets the room (currently only one)
    def setRoom(self):
        self.clearRoom()
        self.roomLevel += 1
        # starting area is grass
        if self.roomLevel == 1:
            self.currentRoom = Room_Grass(self, (0,6))
        # second level is dirt
        elif self.roomLevel == 2:
            self.currentRoom = Room_Dirt(self, self.currentRoom.exitCoord)
        # the rest of the game is stone
        else:
            self.currentRoom = Room_Stone(self, self.currentRoom.exitCoord)
            
    # game loop
    def run(self):
        # set self.playing to False at any time to end game
        self.playing = True
        while self.playing:
            # game ticks at 30 frames a second
            self.fps = self.clock.tick(FPS) / 100
            if CONTROLLER:
                # updates controller health
                self.controller.healthbar()
            # button pressed and button type are returned
            # (movement or action types)
            b = self.events()
            # presses the corresponding button
            self.buttonPress(b)
            if self.playerHasMoved > 3:
                for mob in self.mob_sprites:
                    mob.autoPath()
                self.playerHasMoved = 0
            self.update()
            if (not self.inBattle):
                self.drawMap()
                
    # executes button press
    # takes in a button and it's type
    def buttonPress(self, b):
        #Checks if b is a key
        if (b):
            # if type is true, a movement key was pressed
            if (b != "m"):
                # as long as the player didn't just run into something
                if(self.player.collide(b) and self.player.borderCheck(b)):
                    # a movement is consumed
                    self.playerHasMoved += 1
                    self.player.move(b)
            # mouse was pressed
            if (b == "m"):
                loser, damage = battleSelect(button.button_type)
                actorDeath(loser, loser.takeDamage(damage))
            else:
                pass
    def battleSelect(self, pc, mob):
        #pc = players attack choice
        #monsters attack choice
        mc = mob.attack

        #player and monster tie
        if (pc == mc):
            return self.player, 0

        #player chooses rock
        elif (pc == "rock"):
            #player loses
            if (mc == "paper"):
                return self.player, 25
            #player wins
            else:
                return mob, 25
            
        #player chooses paper        
        elif (pc == "paper"):
            if (mc == "scissors"):
                return self.player, 25
            else:
                return mob, 25
            
        #player chooses scissors
        elif (pc == "scissors"):
            if (mc == "rock"):
                return self.player, 25
            else:
                return mob, 25

    def actorDeath(actor, living):
        if (not actor.living):
            self.inBattle = False
        else:
            self.inBattle = True

    def battleUI(self, enemy):
        self.game_buttons.empty()
        enemy.enlarge()
        Button_rock(UI_CENTER - 105, UI_CENTER)
        Button_scissors(UI_CENTER, UI_CENTER)
        Button_paper(UI_CENTER + 105, UI_CENTER)
        self.playerCanMove = False
        self.inBattle = True

    def mapUI(self):
        self.inBattle = False
        self.game_buttons.empty()
            
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
        buttonType = False
        for event in pg.event.get():
            if event.type == pg.QUIT:
                if CONTROLLER:
                    GPIO.cleanup()
                self.quitGame()
            if (not self.inBattle):
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_LEFT:
                        button = "a"
                    if event.key == pg.K_RIGHT:
                        button = "d"
                    if event.key == pg.K_UP:
                        button = "w"
                    if event.key == pg.K_DOWN:
                        button = "s"
            if event.type == pg.MOUSEBUTTONDOWN:
                #founds where mouse was pressed
                mouse_pos = event.pos
                #Checks which button was pressed
                for button in self.game_buttons:
                    if button.rect.collidepoint(mouse_pos):
                        button = "m"
        if CONTROLLER:
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

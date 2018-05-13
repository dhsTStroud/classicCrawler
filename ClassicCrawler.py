# refer to pygame with "pg"
import pygame as pg
from time import sleep
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
##    CONTROLLER = True

################################################################################

# Game class
class Game(object):
    # sets up the GUI 
    def __init__(self):
        pg.init()
        self.gFont = pg.font.SysFont('Sans', 20)
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        pg.key.set_repeat(500, 100)
    
    # initialize all variables and setup a new game
    def newGame(self):
        self.status = "Out on a fresh new journey."
        self.spriteGroups()
        # creates the player sprite
        self.player = Actor_Player(self, 1, 1)
        # sets player at level 0
        self.roomLevel = 0
        # instantiates rooms
        self.roomLevel = 0
        self.setRoom()
        # creates the player UI
        self.drawMenuBackground()
        # starts turns 'counter'
        self.playerHasMoved = 0
        self.mapUI()
        if CONTROLLER:
            self.controller = Controller(self)

    def spriteGroups(self):
        # spritegroup for sprites
        self.allActorSprites = pg.sprite.Group()
        # spritegroup for monsters
        self.mob_sprites = pg.sprite.Group()
        # spritegroup for special mobs
        self.special_mob = pg.sprite.Group()
        # spritegroup for tiles
        self.tile_sprites = pg.sprite.Group()
        self.special_tiles = pg.sprite.Group()
##        # spritegroup for UI menu sprites
##        self.menus = pg.sprite.Group()
        # spritegroup for obstacle sprites
        self.obs_sprites = pg.sprite.Group()
        # spritegroup for button sprites
        self.game_buttons = pg.sprite.Group()

    # empties all sprite groups
    def clearSpriteGroups(self):
        self.allActorSprites.empty()
        self.mob_sprites.empty()
        self.tile_sprites.empty()
        self.special_tiles.empty()
        self.obs_sprites.empty()

    # creates the rightside user interface
    def drawMenuBackground(self):
        # loads the image (pg.image.load())
        uiImage = pg.image.load(IMAGE_PATH + "ui_right_menu.png")
        # screen.blit() plasters the image's pixels where you tell it to
        # the picture is not really interactable, only a background
        self.screen.blit(uiImage, (WIDTH_CENTER, 0))

    # draws a given image to the screen
    def drawImage(self, image, location):
        self.screen.blit(image, location)

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

    # creates the default map UI
    def mapUI(self):
        self.inBattle = False
        self.drawMenuBackground()
        self.special_mob.empty()
        self.enemy = None
        self.game_buttons.empty()
        Button_Health(self, UI_CENTER[0]-180, UI_CENTER[1]-10)

    # creates the battle UI screen
    def battleUI(self, enemy):
        self.special_mob.add(enemy)
        self.enemy = enemy
        self.status = "I've picked a fight with a {}".format(self.enemy.name)
        self.game_buttons.empty()
        enemy.enlarge()
        Button_Rock(self, UI_CENTER[0]-180, UI_CENTER[1]-10)
        Button_Scissors(self, UI_CENTER[0], UI_CENTER[1]+90)
        Button_Paper(self, UI_CENTER[0] , UI_CENTER[1]-10)
        Button_Run(self, UI_CENTER[0]-180, UI_CENTER[1]+90)
        self.playerCanMove = False
        self.inBattle = True
                
    # executes button press
    # takes in a button and it's type
    def buttonPress(self, b):
        # checks if b is a key
        # key returns None by default so if statement is necessary
        if (b != None):
            print b
            # if type is true, a movement key was pressed
            if (b != "m"):
                # as long as the player didn't just run into something
                if(self.player.collide(b) and self.player.borderCheck(b)):
                    # a movement is consumed
                    self.playerHasMoved += 1
                    self.player.move(b)
            # mouse was pressed
            if (b == "m"):
                print "AHH"
                self.detButton()
            else:
                pass

    # determines button type
    def detButton(self):
        if self.inBattle:
            loser, damage = self.detWinner(self.butDown.button_type)
            if (damage == "run"):
                loser.shrink()
                self.mapUI()
            else:
                loser.takeDamage(damage)
                # passes in the loser and the loser's health after taking damage
                self.actorDeath(loser)
        else:
            self.status = self.butDown.action()

    # determines the winner of a hand
    # returns the loser and damage amount (25 unless draw)
    def detWinner(self, pc):
        # pc = players attack choice
        # monsters attack choice
        mc = self.enemy.attack()
        if (not pc):
            pc = mc

        # player and monster tie
        if (pc == mc):
            self.status = "We played the same thing!"
            return self.player, 0
        # player chooses rock
        elif (pc == "rock"):
            self.status = "They played {}".format(mc)
            # player loses
            if (mc == "paper"):
                return self.player, 25
            # player wins
            else:
                return self.enemy, 25
        # player chooses paper
        elif (pc == "paper"):
            self.status = "They played {}".format(mc)
            if (mc == "scissors"):
                return self.player, 25
            else:
                return self.enemy, 25
        # player chooses scissors
        elif (pc == "scissors"):
            self.status = "They played {}".format(mc)
            if (mc == "rock"):
                return self.player, 25
            else:
                return self.enemy, 25
        # player chooses run
        elif (pc == "run"):
            self.status = "I ran away..."
            return self.enemy, "run"

    # determines if the actor is still alive and whether or not to continue
    # the battle
    def actorDeath(self, actor):
        if (not actor.living):
            # draws the battle one last time
            # to let the player know the enemy has run out of health
            self.drawBattle()
            sleep(1.5)
            self.status = "I won that fight!"
            # all instances of that enemy are destroyed
            self.mob_sprites.remove(actor)
            self.mapUI()

    # draws text to the screen
    # 1 is default, for drawing a mob's health
    # 2 is for debugging
    # 3 is for statuses
    def drawText(self, actor=None, num = 1):
        # 3 just prints status
        if num == 3:
            # makeshift image for text
            status = self.gFont.render(self.status, False, (BLACK))
        else:
            # makeshift image for text
            health = self.gFont.render("{} Health: {}/{}".\
                                       format(actor.name,\
                                              actor.curHealth, \
                                              actor.maxHealth),\
                                       False, (BLACK))
        if num == 1:
            self.screen.blit(health, (UI_CENTER[0]-180, UI_CENTER[1]-30))
        elif num == 2:
            self.screen.blit(health, (UI_CENTER[0]-180, UI_CENTER[1]-50))
        elif num == 3:
            self.screen.blit(status, (UI_CENTER[0]-180, UI_CENTER[1]-100))
        
    # update portion of game loop
    def update(self):
        # updates "allSprites" sprite group
        self.allActorSprites.update()
            
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
            # draws the appropriate scenes depending
            # on whether or not you're in battle
            if self.inBattle:
                self.drawBattle()
            else:
                self.drawMap()

    # draws the battle scene to the screen
    def drawBattle(self):
        self.drawMenuBackground()
        self.special_mob.draw(self.screen)
        self.game_buttons.draw(self.screen)
        # draws enemy health
        self.drawText(self.enemy)
        # draw's current status
        self.drawText(None, 3)
        if (not CONTROLLER):
            self.drawText(self.player, 2)
        pg.display.flip()

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
        self.drawMenuBackground()
        self.tile_sprites.draw(self.screen)
        self.obs_sprites.draw(self.screen)
        self.special_tiles.draw(self.screen)
        self.drawGrid()
        self.allActorSprites.draw(self.screen)
        self.game_buttons.draw(self.screen)
        # draw's current status
        self.drawText(None, 3)
        if (not CONTROLLER):
            self.drawText(self.player, 2)
        # flips the display each time it's called
        # prevents lag
        pg.display.flip()

    # catches all events
    def events(self):
        button = None
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
                for screenButton in self.game_buttons:
                    if screenButton.rect.collidepoint(mouse_pos):
                        self.butDown = screenButton
                        button = "m"        
        #Only allowed to move if not in battle                
        if (not self.inBattle):
            if (CONTROLLER and button != "m"):
                button = self.controller.movement()
        print button  
        return button

    # shows the start menu
    def startMenu(self):
        pass
            
    # closes the window
    def quitGame(self):
        pg.quit()

################################################################################
# creates the game object
GAME = Game()
GAME.startMenu()
while True:
    GAME.newGame()
    GAME.run()

# refer to pygame with "pg"
import pygame as pg
from time import sleep
from copy import deepcopy
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

# UI GLOBALS

FULL_STATUS_LOC = [30, 35]
HALF_STATUS_LOC = [UI_CENTER[0]-180, 15]
STATUS = ['' for x in range(11)]

################################################################################

# Game class
class Game(object):
    # sets up the GUI 
    def __init__(self):
        pg.init()
        # normal game font
        self.gFont = pg.font.SysFont('Sans', 20)
        # health potions font
        self.hFont = pg.font.SysFont('Sans', 30)
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        pg.key.set_repeat(500, 100)
        
    # initialize all variables and setup a new game
    def newGame(self):
        self.resetStatus()
        # creates the player sprite
        self.player = Actor_Player(self, 1, 1)
        # sets player at level 0
        self.roomLevel = 0
        # instantiates rooms
        self.setRoom()
        # creates the player UI
        self.drawMenuBackground()
        # starts/resets turns 'counter'
        self.playerHasMoved = 0
        self.enemyKillCount = 0
        self.mapUI()
        if CONTROLLER:
            self.controller = Controller(self)

    # resets self.status
    def resetStatus(self):
        self.status = STATUS

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
        if self.player.score >= 50:
            self.player.addScore(-50)
        # starting area is grass
        if self.roomLevel == 1:
            self.currentRoom = Room_Grass(self, (0,6))
        # second level is dirt
        elif self.roomLevel == 2:
            self.currentRoom = Room_Dirt(self, self.currentRoom.exitCoord)
        # the rest of the game is stone
        else:
            self.currentRoom = Room_Stone(self, self.currentRoom.exitCoord)

    # creates the rightside user interface
    def drawMenuBackground(self):
        # sets appropriate UI image
        if (self.atScreen == "title") or (self.atScreen == "dead"):
            image = "ui_full_displayScreen.png"
            location = (0,0)
        elif (self.atScreen == "map") or (self.atScreen == "battle"):
            image = "ui_half_displayScreen.png"
            location = (WIDTH_CENTER, 0)
        # loads the image (pg.image.load())
        uiImage = pg.image.load(IMAGE_PATH + image)
        # screen.blit() plasters the image's pixels where you tell it to
        # the picture is not really interactable, only a background
        self.screen.blit(uiImage, location)

    # creates the default title screen
    def titleUI(self):
        self.atScreen = "title"
        self.inBattle = False
        self.spriteGroups()
        Button_Start(self, 30, HEIGHT_CENTER+70)

    # creates the initial death screen
    def deathUI(self):
        self.clearRoom()
        self.atScreen = "dead"
        self.inBattle = False
        self.special_mob.empty()
        self.drawMenuBackground()
        self.constructDeathText()
        self.game_buttons.empty()
        Button_Start(self, 30, HEIGHT_CENTER+70)

    # creates the default map UI
    def mapUI(self):
        self.status[2] = " "
        self.atScreen = "map"
        self.inBattle = False
        self.drawMenuBackground()
        self.special_mob.empty()
        self.enemy = None
        self.game_buttons.empty()
        Button_Health(self, UI_CENTER[0]-180, UI_CENTER[1])

    # creates the battle UI screen
    def battleUI(self, enemy):
        self.atScreen = "battle"
        self.special_mob.add(enemy)
        self.enemy = enemy
        self.status[0] = "I've picked a fight with a {}".format(self.enemy.name)
        self.game_buttons.empty()
        enemy.enlarge()
        Button_Rock(self, UI_CENTER[0]-180, UI_CENTER[1])
        Button_Scissors(self, UI_CENTER[0], UI_CENTER[1]+100)
        Button_Paper(self, UI_CENTER[0] , UI_CENTER[1])
        Button_Run(self, UI_CENTER[0]-180, UI_CENTER[1]+100)
        self.inBattle = True

    # constructs a health status
    def constructHealthStatus(self, actor=None, location = 2):
        # makeshift image for text
        healthText = ("{} Health: {}/{}".format(actor.name,\
                                                actor.curHealth, \
                                                actor.maxHealth))
        self.status[location] = healthText

    # constructs final score screen
    def constructDeathText(self):
        self.status = deepcopy(STATUS)
        # enemy kill multiplyer
        enKillMult = self.enemyKillCount
        # score at death
        score1 = self.player.score
        # health potions and health potion score
        hPotions = self.player.healthPotions
        hPScore = 25 * hPotions
        # Score after adding health potion score
        score2 = score1 + hPScore
        # final score
        score3 = score2 * enKillMult
        
        self.status[0] = "You made it to level {}".format(self.roomLevel)
        self.status[1] = "Your killer: a {}".format(self.enemy.name)
        self.status[2] = "Score at death: {}".format(score1)
        self.status[3] = "Enemies killed multiplier: {}".format(enKillMult)
        self.status[4] = "Health Potion score: (25 * {}) = {}".format(hPotions, \
                                                                    hPScore)
        self.status[5] = "Score + Health Potion score: ({} + {}) = {}".format(\
            score1, hPScore, score2)
        self.status[6] = "Enemy Kill Multiplier * Score: ({} * {}) = {}".format(\
            enKillMult, score2, score3)
        self.status[7] = "You recieve a final score of {}".format(score3)
        self.status[8] = " "
        self.status[10] = "Press START below to play again!"

    # draws statuses to title or death screens
    def drawStatus(self, loc = FULL_STATUS_LOC, actor = None):
        location = deepcopy(loc)
        text = []
        for status in self.status:
            curText = self.gFont.render(status, False, (BLACK))
            text.append(curText)
        for statusText in text:
            self.screen.blit(statusText, (location))
            location[1] += 20

    # draws the amount of health potions the player has to the screen
    def drawHealthPotions(self):
        location = (UI_CENTER[0]-170, UI_CENTER[1]+5)
        count = str(self.player.healthPotions)
        if len(count) < 2:
            count = '0' + count
        # takes amount from player variable
        text = self.hFont.render(count, False, (BLACK))
        self.screen.blit(text, location)

    # draws score to screen
    def drawScore(self):
        self.status[8] = "Score: {}".format(str(self.player.score))
                
    # executes button press
    # takes in a button and it's type
    def buttonPress(self, b):
        # checks if b is a key
        # key returns None by default so if statement is necessary
        if (b != None):
            # if type is true, a movement key was pressed
            if (b != "m"):
                # as long as the player didn't just run into something
                if(self.player.collide(b) and self.player.borderCheck(b)):
                    # a movement is consumed
                    self.playerHasMoved += 1
                    self.player.move(b)
            # mouse was pressed
            if (b == "m"):
                self.detButton()
                sleep

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
                self.actorDeathCheck(loser)
        else:
            # activates touchscreen button action method and returns a status
            # for status[0]
            self.status[0] = self.butDown.action()

    # determines the winner of a hand
    # returns the loser and damage amount (25 unless draw)
    def detWinner(self, pc):
        # pc = players attack choice
        # monsters attack choice
        mc = self.enemy.attack()
        # if player choice is None, player choice = monster choice
        if (not pc):
            pc = mc
        # player and monster tie
        if (pc == mc):
            self.status[0] = "We played the same thing!"
            return self.player, 0
        # player chooses rock
        elif (pc == "rock"):
            self.status[0] = "They played {}".format(mc)
            # player loses
            if (mc == "paper"):
                return self.player, 25
            # player wins
            else:
                return self.enemy, 25
        # player chooses paper
        elif (pc == "paper"):
            self.status[0] = "They played {}".format(mc)
            if (mc == "scissors"):
                return self.player, 25
            else:
                return self.enemy, 25
        # player chooses scissors
        elif (pc == "scissors"):
            self.status[0] = "They played {}".format(mc)
            if (mc == "rock"):
                return self.player, 25
            else:
                return self.enemy, 25
        # player chooses run
        elif (pc == "run"):
            self.status[0] = "I ran away from the {}...".format(self.enemy.name)
            return self.enemy, "run"

    # determines if the actor is still alive and whether or not to continue
    # the battle
    def actorDeathCheck(self, actor):
        # if player dies, game is over
        if (self.player.living == False):
            self.drawBattle()
            sleep(1.5)
            self.status[0] = "You were killed by a {}.".format(self.enemy.name)
            self.drawBattle()
            sleep(2)
            self.deathUI()
        elif (not actor.living) and (self.player.living):
            self.player.addScore(actor.score)
            try:
                if actor.enemy:
                    self.enemyKillCount += 1
            except:
                '''actor not a valid enemy'''
            # draws the battle one last time
            # to let the player know the enemy has run out of health
            self.drawBattle()
            sleep(1.5)
            self.status[0] = self.player.addHealthPotions(actor.hPotions)
            self.drawBattle()
            sleep(1.5)
            self.status[0] = "I beat the {}!".format(actor.name)
            # all instances of that enemy are destroyed
            self.mob_sprites.remove(actor)
            self.mapUI()
        
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
            if (self.atScreen == "map") and (self.playerHasMoved > 3):
                for mob in self.mob_sprites:
                    mob.autoPath()
                self.playerHasMoved = 0
            # draws the appropriate scenes depending
            # on whether or not you're in battle
            if self.atScreen == "battle":
                self.update()
                self.drawBattle()
            elif self.atScreen == "map":
                self.update()
                self.drawMap()
            elif self.atScreen == "title":
                self.drawStartMenu()
            elif self.atScreen == "dead":
                self.drawDeathScreen()

    # draws the battle scene to the screen
    def drawBattle(self):
        self.drawMenuBackground()
        self.special_mob.draw(self.screen)
        self.game_buttons.draw(self.screen)
        # draws enemy health
        self.constructHealthStatus(self.enemy)
        self.drawScore()
        # draw's current status
        self.drawStatus(HALF_STATUS_LOC)
        if (not CONTROLLER):
            self.constructHealthStatus(self.player, 1)
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
        self.drawHealthPotions()
        self.drawScore()
        # draw's current status
        self.drawStatus(HALF_STATUS_LOC)
        if (not CONTROLLER):
            self.constructHealthStatus(self.player, 1)
        # flips the display each time it's called
        # prevents lag
        pg.display.flip()

    # draws start menu to screen
    def drawStartMenu(self):
        self.drawMenuBackground()
        self.game_buttons.draw(self.screen)
        self.drawStatus()
        pg.display.flip()

    # draws death screen to screen
    def drawDeathScreen(self):
        self.drawMenuBackground()
        self.game_buttons.draw(self.screen)
        self.drawStatus()
        pg.display.flip()

    # catches all events
    def events(self):
        button = None
        for event in pg.event.get():
            if event.type == pg.QUIT:
                if CONTROLLER:
                    GPIO.cleanup()
                self.quitGame()
            if (self.atScreen == "map"):
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
        if (self.atScreen == "map"):
            if (CONTROLLER and button != "m"):
                button = self.controller.movement()
        return button

    # shows the start menu
    def startMenu(self):
        self.titleUI()
        self.status = ["You are about to enjoy a classic crawler!", \
                       " ", \
                       "In this game you will fight deadly monsters" + \
                       " in a battle of wits (rock-paper-scissors)", \
                       "to rack up a high score worth bragging to your " + \
                       "friends about! You must use health ", \
                       "potions to stay alive, and battle your way " + \
                       "through an endless" + \
                       " series of rooms!", "Going through an exit costs you" + \
                       " a toll of 50 points, so be absolutely sure you're", \
                       "ready to advance, cause there's no going back.",
                       " ", \
                       "Press the start button below to play the game."]
        self.run()
            
    # closes the window
    def quitGame(self):
        pg.quit()

################################################################################
# creates the game object
GAME = Game()
GAME.startMenu()
while True:
    GAME.startMenu()

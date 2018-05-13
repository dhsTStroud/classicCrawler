import RPi.GPIO as GPIO
from time import sleep

class Controller(object):
    RGB = [6,5,4]
    #       W   A   S   D
    WASD = [18, 21, 20, 19]

    def __init__(self, game):
        self.game = game
        #LED and Button Pins
        GPIO.setmode(GPIO.BCM)
        
        #Setup output pins
        GPIO.setup(self.RGB, GPIO.OUT)
        
        #Setup input pins
        GPIO.setup(self.WASD, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        
    def healthbar(self):
        H = self.game.player.curHealth
        maxH = self.game.player.maxHealth
        R = 0
        G = 0
        B = 0
        if (((float(H)/maxH)*100) > 25):
            G = 1
        if (75 >= ((float(H)/maxH)*100) > 25):
            B = 1
        if (((float(H)/maxH)*100) <= 25):
            R = 1
        GPIO.output(self.RGB[0], R)
        GPIO.output(self.RGB[1], G)
        GPIO.output(self.RGB[2], B)

    def movement(self):
        retvar = None
        #Move through the WASD keys
        for i in range(len(self.WASD)):
            #Check if pressed
            if (GPIO.input(self.WASD[i]) == True):
                #Check which is pressed
                if (self.WASD[i] == 18):
                    print "UP"
                    retvar = 'w'
                if (self.WASD[i] == 20):
                    print "RIGHT"
                    retvar = 'd'
                if (self.WASD[i] == 21):
                    print "LEFT"
                    retvar = 'a'
                if (self.WASD[i] == 19):
                    print "DOWN"
                    retvar = 's'
                sleep(.25)
        return retvar                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           

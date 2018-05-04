import RPi.GPIO as GPIO
from time import sleep

class Controller(object):
    RGB = [6,5,4]
    actions = [12,16,17]
    #       W   A   S   D
    WASD = [18, 21, 20, 19]
    #     A   B
    AB = [22, 24]
    
    def __init__(self):
        #LED and Button Pins
        GPIO.setmode(GPIO.BCM)
        
        #Setup output pins
        GPIO.setup(self.actions,GPIO.OUT)
        GPIO.setup(self.RGB, GPIO.OUT)
        
        #Setup input pins
        GPIO.setup(self.WASD, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(self.AB, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    

    def healthbar(self, H, maxH):
        R = 0
        G = 0
        B = 0
        if (((H/maxH)*100) > 25):
            G = 1
        if (75 >= ((H/maxH)*100) > 25):
            B = 1
        if (((H/maxH)*100) <= 25):
            R = 1
        GPIO.output(self.RGB[0], R)
        GPIO.output(self.RGB[1], G)
        GPIO.output(self.RGB[2], B)

    def change_action(self, num):
        for i in self.actions:
            GPIO.output(self.actions, False)
        for i in range(num):
            GPIO.output(self.actions[i], True)

    def movement(self, moves):
        while (moves > 0):
            retvar = None
            #Move through the WASD keys
            for i in range(len(self.WASD)):
                #Check if pressed
                if (GPIO.input(self.WASD[i]) == True):
                    #Check which is pressed
                    if (self.WASD[i] == 18):
                        print "UP"
                        retvar = 'w'
                    elif (self.WASD[i] == 20):
                        print "RIGHT"
                        retvar = 'd'
                    elif (self.WASD[i] == 21):
                        print "LEFT"
                        retvar = 'a'
                    elif (self.WASD[i] == 19):
                        print "DOWN"
                        retvar = 's'
                    self.change_action(moves-1)
                    print "moves: {}".format(moves-1)
                    sleep(1)
                    moves -= 1
            #move through AB buttons
            for i in range(len(self.AB)):
                #Check if pressed
                if (GPIO.input(self.AB[i]) ==True):
                    #Select button
                    if (self.AB[i] == 22):
                        retvar = 'j'
                    #Deselect button
                    elif(self.AB[i]== 24):
                        retvar = 'k'
                    sleep(1)
c = Controller()
c.healthbar(100,100)
c.change_action(3)
c.movement(3)
sleep(1)
print "ALL DONE"
GPIO.cleanup()

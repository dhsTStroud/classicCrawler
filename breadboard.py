                                                                                                               ##########
# setup
#########
import RPi.GPIO as GPIO
from time import sleep
#      R G B
RGB = [6,5,4]
actions = [12,16,17]
#       W   A   S   D
WASD = [18, 21, 20, 19]
#     A   B
AB = [22, 24]                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         

#Use the broadcast pin mode
GPIO.setmode(GPIO.BCM)

#Setup output pins
GPIO.setup(actions,GPIO.OUT)
GPIO.setup(RGB, GPIO.OUT)
#Setup input pins
GPIO.setup(WASD, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(AB, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

def healthbar(life):
    B = 0
    if (life > 75):
        G = 1
        R = 0
    elif (life > 50):
        G = 1
        R = 1
    else:
        R = 1
        G = 0
    
    GPIO.output(RGB[0], R)
    GPIO.output(RGB[1], G)
    GPIO.output(RGB[2], B)

def LED_state(x):
    for i in actions:
        GPIO.output(actions, x)
        print x

def change_action(num):
    for i in actions:
        GPIO.output(actions, False)
        #print num
    for i in range(num):
        GPIO.output(actions[i], True)

def movement(moves):
    while (moves > 0):
        retvar = None
        for i in range(len(WASD)):
            if (GPIO.input(WASD[i]) == True):
                print "pressed"
                if (WASD[i] == 18):
                    print "UP"
                    retvar = 'w'
                elif (WASD[i] == 20):
                    print "RIGHT"
                    retvar = 'd'
                elif (WASD[i] == 21):
                    print "LEFT"
                    retvar = 'a'
                elif (WASD[i] == 19):
                    print "DOWN"
                    retvar = 's'
                change_action(moves-1)
                sleep(1)
                print "moves: {}".format(moves-1)
                moves -= 1
        for i in range(len(AB)):
            if (GPIO.input(AB[i]) ==True):
                if (AB[i] == 22):
                    #select
                    print "A"
                    retvar = 'j'
                elif(AB[i]== 24):
                    #go back
                    print "B"
                    retvar = 'k'
                sleep(1)
    #Next turn
    print "No moves left"
    

#change_action(2)
LED_state(True)
healthbar(90)
movement(3)
print "Game OVER"
sleep(2)
print "cleanup"
GPIO.cleanup()
print "all clean"

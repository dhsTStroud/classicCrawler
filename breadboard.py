##########
# setup
#########
import RPi.GPIO as GPIO
from time import sleep

actions = [12,16,17]
#       W   A   S   D
WASD = [18, 21, 20, 19]

#Use the broadcast pin mode
GPIO.setmode(GPIO.BCM)

#Setup output pins
GPIO.setup(WASD, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(actions,GPIO.OUT)

#Setup input pins


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
        for i in range(len(WASD)):
            if (GPIO.input(WASD[i]) == True):
                print "pressed"
                if (WASD[i] == 18):
                    print "UP"
                elif (WASD[i] == 20):
                    print "RIGHT"
                elif (WASD[i] == 21):
                    print "LEFT"
                elif (WASD[i] == 19):
                    print "DOWN"
                change_action(moves-1)
                sleep(1)
                print "moves: {}".format(moves-1)
                moves -= 1
    print "No moves left"

#change_action(2)
LED_state(True)
movement(3)
print "Game OVER"
sleep(2)
print "cleanup"
GPIO.cleanup()
print "all clean"

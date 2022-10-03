import keyboard
from blessed import Terminal
from translate_image import display_pix
import time
import os

delay = 0.05

def update_player(y,x,lastface):

    keypressed = keyboard.read_key()

    if keypressed =="up":
        y-=1
        if lastface =='right':
            display_pix('assets/walkright.png',t,pos=(y,x),bg=(0,0,0))
        elif lastface == 'left':
            display_pix('assets/walkleft.png',t,pos=(y,x),bg=(0,0,0))
        time.sleep(delay)
        #lastface = 'away'
    elif keypressed =="down":
        y+=1
        if lastface =='right':
            display_pix('assets/walkright.png',t,pos=(y,x),bg=(0,0,0))
        elif lastface == 'left':
            display_pix('assets/walkleft.png',t,pos=(y,x),bg=(0,0,0))
        time.sleep(delay)
        #lastface = forward
    elif keypressed =="left":
        x-=1
        display_pix('assets/walkleft.png',t,pos=(y,x),bg=(0,0,0))
        time.sleep(delay)
        lastface = 'left'
    elif keypressed =="right":
        x+=1
        display_pix('assets/walkright.png',t,pos=(y,x),bg=(0,0,0))
        time.sleep(delay)
        lastface = 'right'
    return y,x,lastface

t = Terminal()
y = 10
x = 10
image = 'assets/sprite2.png'
lastface = 'right'

while True:
    os.system('cls')

    if lastface == 'right':
        display_pix('assets/sprite2.png',t,pos=(y,x),bg=(0,0,0))
    elif lastface =='left':
        display_pix('assets/leftsprite.png',t,pos=(y,x),bg=(0,0,0))
    time.sleep(delay)
    y,x,lastface = update_player(y,x,lastface)

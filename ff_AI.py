import random
import math
from translate_image import display_pix

class AI:

    def __init__(self,name,symbol,x,y,desc):
        self.name = name
        self.x = x
        self.y = y
        self.last_x = x
        self.last_y = y
        self.desc = desc
        self.symbol = symbol
        self.speed =1
        self.hearing = 10

    def update(self):
        self.last_x = self.x
        self.last_y = self.y
        rand = random.randrange(1,5)
        if rand ==1:
            self.y +=self.speed
        elif rand ==2:
            self.y -=self.speed
        elif rand == 3:
            self.x -=self.speed
        elif rand ==4:
            self.x +=self.speed

    def respond(self,input):
        if input == "Hello!":
            return "Hello, my name is "+self.name
        elif input == "Fuck you all!":
            return "Go fuck youself!"
        elif input == "Help!":
            return "Not my problem..."

    def display_vis_symbol(self,t,tl_y,tl_x):
        with t.location(y=self.y-tl_y,x=self.x-tl_x):
            print(t.red_on_green(self.symbol))

    def clear_vis_symbol(self,t,tl_y,tl_x):
        with t.location(y=self.y-tl_y,x=self.x-tl_x):
            print(t.red_on_green(" "))

    def clear_invis_symbol(self,t,tl_y,tl_x):
        with t.location(y=self.y-tl_y,x=self.x-tl_x):
            print(t.red_on_darkseagreen4(" "))

    def display_vis_sprite(self,t,player,tl_y,tl_x):
        di = self.x-player.x
        dj = self.y-player.y
        distance = math.sqrt(di**2+ dj**2)
        display_pix('assets/m.png',t,pos=(self.y-tl_y,self.x-tl_x),bg=(0,0,0))

    def clear_vis_sprite(self,t,tl_y,tl_x):
        with t.location(y=self.y-tl_y,x=self.x-tl_x):
            print(t.red_on_green(" "))

    def clear_invis_sprite(self,t,tl_y,tl_x):
        with t.location(y=self.y-tl_y,x=self.x-tl_x):
            print(t.red_on_darkseagreen4(" "))

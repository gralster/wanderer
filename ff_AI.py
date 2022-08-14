import random

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
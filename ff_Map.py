import numpy as np
from perlin_noise import PerlinNoise
from ff_Object import Object
from ff_AI import AI

import matplotlib.pyplot as plt


class Map:

	def __init__(self,player,y,x):
		self.width = x
		self.height = y
		print(" ")
		print("	map width = "+str(self.width))
		print("	map height = "+str(self.height))

		# screen relative position within map
		self.tl_y = 20
		self.tl_x = 20
		self.last_tl_y = self.tl_y
		self.last_tl_x = self.tl_x

		self.player = player
		self.objects = list()
		self.ais = list()

		self.tiles = np.ndarray((y,x),dtype=np.object)
		self.explored = np.ndarray((y,x),dtype=np.object)
		self.explored.fill(False)

	def gen_features(self):

		map_width=self.width
		map_height = int(self.height)

		#replace with own eventually, this is not random
		noise = PerlinNoise(octaves=10)
		pic = [[noise([i/map_width, j/map_height]) for j in range(map_height)] for i in range(map_width)]

		tree_map = np.zeros((map_height,map_width))
		for i in range(map_width):
		    for j in range(map_height):
		        pixel = pic[i][j]
		        if pixel > 0.1:
		            tree_map[j,i]=1

		plt.imshow(tree_map, cmap='gray')
		plt.show()


		pot = Object(30,30,"Pot","P","A pot for cooking")
		self.gain(pot)

		Maximilian = AI("Maximilian","M",30,30,"a raven")
		self.populate(Maximilian)

		for i in range(0,map_width):
			for j in range(0,map_height):
				if tree_map[j,i]==1:
					self.tiles[j,i]=Tree("oak")
				else:
					self.tiles[j,i]=Empty()
		#print(self.tiles)

		self.tiles[11,10] = Wall(5)
		self.tiles[12,10] = Wall(5)
		self.tiles[13,10] = Wall(5)
		self.tiles[11,11] = Wall(5)

	def place_player(self,player):
		for i in range(15,self.width-270):
			for j in range(15,self.height-270):
				if self.tiles[j,i].can_walk:
					player.x = i
					player.y = j

	def gain(self,obj):
		self.objects.append(obj)

	def lose(self,index):
		obj = self.objects.pop(index)
		return(obj)

	def populate(self,ai):
		self.ais.append(ai)

	def get_at_location(self,y,x):
		at_loc = list()
		index = 0
		for obj in self.objects:
			if obj.x ==x and obj.y==y:
				at_loc.append(index)
			index += 1
		if len(at_loc)==0:
			return(at_loc)
		else:
			return(at_loc)



	def move_map(self,keypressed):

		self.last_tl_y = self.tl_y
		self.last_tl_x = self.tl_x

		if keypressed =="up":
			self.tl_y -= 1
		elif keypressed =="down":
			self.tl_y +=1
		elif keypressed =="left":
			self.tl_x -=1
		elif keypressed =="right":
			self.tl_x+=1

	def isSeeThrough(self,y,x):
		#print(x,y)
		return(self.tiles[y,x].opaque)

class Empty:
	def __init__(self):
		self.opaque = False
		self.symbol = " "
		self.prevState=False
		self.desc = "There's nothing there."
		self.can_walk = True


class Wall:
	def __init__(self,height):
		self.height = height
		self.opaque = True
		self.symbol = "H"
		self.prevState=False
		self.desc = "That's a wall."
		self.can_walk = False

class Tree:
	def __init__(self,type):
		self.opaque = True
		self.symbol = "T"
		self.desc = "A tree"
		self.can_walk = False

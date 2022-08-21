import numpy as np
from perlin_noise import PerlinNoise
from ff_Object import Object
from ff_AI import AI

import matplotlib.pyplot as plt


class Map:

	def __init__(self,player,y,x):
		self.width = x*2	# *2 makes move map function work without crashing, but why??
		self.height = y*2
		print(" ")
		print("	terminal width = "+str(self.width))
		print("	terminal height = "+str(self.height))

		self.player = player
		self.objects = list()
		self.ais = list()

		self.tiles = np.ndarray((int(y/2),x*2),dtype=np.object)
		self.explored = np.ndarray((int(y/2),x*2),dtype=np.object)
		self.explored.fill(False)

	def gen_features(self):

		map_width=self.width
		map_height = int(self.height/4)

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


		pot = Object(12,12,"Pot","P","A pot for cooking")
		self.gain(pot)

		Maximilian = AI("Maximilian","M",16,18,"a raven")
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
		for i in range(15,self.width-15):
			for j in range(15,int(self.height/4)-15):
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

	def player_near_edge(self):
		if self.width-self.player.x <5 or (self.height)/4-self.player.y <5 or self.player.x <5 or self.player.y <5 :
			return True
		else:
			 return False

	def move_map(self,keypressed):

		if keypressed =="up":
			newline = np.ndarray((self.player.speed,self.width),dtype=np.object)
			newexplored = np.ndarray((self.player.speed,self.width),dtype=np.object)

			for x in range(0,self.width):
				newline[0,x]=Empty()
				newexplored[0,x] = False

			self.tiles = np.vstack((newline,self.tiles))
			self.tiles = np.delete(self.tiles,np.s_[self.height-self.player.speed+1:self.height+1],0)

			self.explored = np.vstack((newexplored,self.explored ))
			self.explored  = np.delete(self.explored,np.s_[self.height-self.player.speed+1:self.height+1],0)

			for obj in self.objects:
				obj.y+=1

		elif keypressed =="down":
			newline = np.ndarray((self.player.speed,self.width),dtype=np.object)
			newexplored = np.ndarray((self.player.speed,self.width),dtype=np.object)

			for x in range(0,self.width):
				newline[0,x]=Empty()
				newexplored[0,x] = False

			self.tiles = np.vstack((self.tiles,newline))
			self.tiles = np.delete(self.tiles,np.s_[0:self.player.speed],0)

			self.explored = np.vstack((self.explored,newexplored))
			self.explored = np.delete(self.explored,np.s_[0:self.player.speed],0)

			for obj in self.objects:
				obj.y-=1

		elif keypressed =="left":
			newline = np.ndarray((self.height,self.player.speed),dtype=np.object)
			newexplored = np.ndarray((self.height,self.player.speed),dtype=np.object)

			for x in range(0,self.height):
				newline[x,0]=Empty()
				newexplored[x,0] = False

			self.tiles = np.hstack((newline,self.tiles))
			self.tiles = np.delete(self.tiles,np.s_[self.width-self.player.speed+1:self.width+1],1)

			self.explored = np.hstack((newexplored,self.explored))
			self.explored = np.delete(self.explored,np.s_[self.width-self.player.speed+1:self.width+1],1)

			for obj in self.objects:
				obj.x+=1

		elif keypressed =="right":
			newline = np.ndarray((self.height,self.player.speed),dtype=np.object)
			newexplored = np.ndarray((self.height,self.player.speed),dtype=np.object)

			for x in range(0,self.height):
				newline[x,0]=Empty()
				newexplored[x,0] = False

			self.tiles = np.hstack((self.tiles,newline))
			self.tiles = np.delete(self.tiles,np.s_[0:self.player.speed],1)

			self.explored = np.hstack((self.explored,newexplored))
			self.explored = np.delete(self.explored,np.s_[0:self.player.speed],1)

			for obj in self.objects:
				obj.x-=1


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

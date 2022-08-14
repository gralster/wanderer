import numpy as np

class Map:

	def __init__(self,player,y,x):
		self.width = x*2
		self.height = y*2

		self.player = player
		self.objects = list()
		self.ais = list()

		self.tiles = np.ndarray((y*2,x*2),dtype=np.object)
		self.explored = np.ndarray((y*2,x*2),dtype=np.object)
		self.explored.fill(False)

	def gain(self,obj):
		self.objects.append(obj)

	def lose(self,index):
		obj = self.objects.pop(index)
		return(obj)

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
		if self.width-self.player.x <5 or self.height-self.player.y <5 or self.player.x <5 or self.player.y <5 :
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





	def gen_features(self):

		for i in range(0,self.width):
			for j in range(0,self.height):
				self.tiles[j,i]=Empty()

		self.tiles[11,10] = Wall(5)
		self.tiles[12,10] = Wall(5)
		self.tiles[13,10] = Wall(5)
		self.tiles[11,11] = Wall(5)

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

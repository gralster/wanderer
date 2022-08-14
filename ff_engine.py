import keyboard 
import os
import math
import sys
from blessed import Terminal
import numpy as np

from ff_Map import Map
from ff_Player import Player
from ff_Object import Object



class Engine:

	### INITIALISATION ################################

	def __init__(self,mode):
		os.system('cls' if os.name == 'nt' else 'clear')
		np.set_printoptions(threshold = sys.maxsize)
		self.mode = mode
		self.t = Terminal()

		self.textbox_height = 8
		self.x = self.t.width
		self.y = self.t.height-self.textbox_height
		self.player = Player("grace",5,5)
		self.world = Map(self.player,self.x,self.y)

		self.last_vis = np.zeros((self.y,self.x))
		self.whole_screen_refresh=False

	def setup_world(self):
		pot = Object(12,12,"Pot","P")
		self.world.gain(pot)
		self.world.gen_features()
		
	### UPDATING #######################################

	def update_player(self):

		# movement

		self.player.last_x = self.player.x
		self.player.last_y = self.player.y
		
		keypressed = keyboard.read_key()

		if keypressed =="up":
			self.player.y -= self.player.speed
		elif keypressed =="down":
			self.player.y += self.player.speed
		elif keypressed =="left":
			self.player.x -= self.player.speed
		elif keypressed =="right":
			self.player.x += self.player.speed

		if self.world.player_near_edge():
			self.player.y = self.player.last_y
			self.player.x = self.player.last_x
			self.world.move_map(keypressed)
			self.whole_screen_refresh=True

		# actions

		elif keypressed ==".":
			obj_indexes =self.world.get_at_location(self.player.y,self.player.x)
			if obj_indexes==[]:
				self.print_bottom("nothing to pick up")
			else:
				for index in obj_indexes:
					self.transfer_object(index,self.world,self.player,(self.player.x,self.player.y))

		elif keypressed == ",":
			items = self.player.get_inventory()
			if items ==[]:
				self.print_bottom("you have nothing to drop!")
			else:
				self.print_bottomf(self.player.get_inventory())
				self.print_bottom("What do you want to drop? (0,1,2,...")

				selection = int(input()[-1])	
				self.transfer_object(selection,self.player,self.world,(self.player.x,self.player.y))

			
		elif keypressed == "i":
			self.print_bottom(self.player.get_inventory())
			
		elif keypressed == "esc":
			os.system('cls' if os.name == 'nt' else 'clear')
			quit()

		#testing for visibility :
		elif keypressed =="space":
			self.transfer_object(0,self.world,self.player,(12,12))

	def transfer_object(self,index,giver,receiver,loc):
		self.last_vis[loc[1],loc[0]]=-1
		obj=giver.lose(index)
		obj.x = loc[0]
		obj.y = loc[1]
		receiver.gain(obj)




	### DISPLAY SCREEN ############################################

	def clear(self):
		with self.t.hidden_cursor():
			with self.t.location(y=self.player.last_y,x=self.player.last_x):
				print(self.t.on_green(" "))
			print(self.t.home)#+self.t.on_darkgreen)#self.t.clear_eos)

	def display(self):

		current_vis = np.zeros((self.y,self.x))

		self.print_bottomf(self.whole_screen_refresh)

		for i in range(0,self.x):
			for j in range(0,self.y):
				canSee =self.inFOV(self.player,j,i)
				if canSee:
					self.world.explored[j,i]=True
					current_vis[j,i]=1
		
		changes = current_vis-self.last_vis

		if self.whole_screen_refresh:
			
			for i in range(0,self.x):
				for j in range(0,self.y):
					canSee =self.inFOV(self.player,j,i)
					if canSee:
						with self.t.location(y=j,x=i):
							print(self.t.on_green(self.world.tiles[j,i].symbol))
					else:
						if self.world.explored[j,i]:
							with self.t.location(y=j,x=i):
								print(self.t.on_darkseagreen4(self.world.tiles[j,i].symbol))
			
			for obj in self.world.objects:
				canSee =self.inFOV(self.player,obj.y,obj.x)
				self.print_bottomf(canSee,offset = 2)
				with self.t.location(y=obj.y,x=obj.x):
					if canSee:
						print(self.t.red_on_green(obj.symbol))
					else:
						if self.world.explored[obj.y,obj.x]:
							print(self.t.red_on_darkseagreen4(obj.symbol))

		else:
		# update display of ground:

			for i in range(0,self.x):
				for j in range(0,self.y):
					canSee =self.inFOV(self.player,j,i)
					if canSee:
						if changes[j,i]>=1:
							with self.t.location(y=j,x=i):
								print(self.t.on_green(self.world.tiles[j,i].symbol))
					
					#testblock
					else:
						if changes[j,i]>=1:
							with self.t.location(y=j,x=i):
								print(self.t.on_darkseagreen4(self.world.tiles[j,i].symbol))


					if changes[j,i] ==-1:
						with self.t.location(y=j,x=i):
							print(self.t.on_darkseagreen4(self.world.tiles[j,i].symbol))
					




			# update display of objects
			self.print_bottomf(len(self.world.objects),offset=4)
			for obj in self.world.objects:
				canSee =self.inFOV(self.player,obj.y,obj.x)
				self.print_bottomf(canSee,offset = 1)
				with self.t.location(y=obj.y,x=obj.x):
					if canSee:
						print(self.t.red_on_green(obj.symbol))
					if changes[obj.y,obj.x] ==-1:
						print(self.t.red_on_darkseagreen4(obj.symbol))
					#if changes[obj.y,obj.x] >=1:# and canSee:
					#	print(self.t.red_on_green(obj.symbol))
					#elif changes[obj.y,obj.x] ==-1:
					#	print(self.t.red_on_darkseagreen4(obj.symbol))

		# update display of player
	
		with self.t.location(y=self.player.y,x=self.player.x):
			print(self.t.on_green+self.t.bold(self.player.symbol))

		# reset last seen array
		# - must be last thing in display function

		self.last_vis = current_vis
		self.whole_screen_refresh=False

	def inFOV(self,player,j,i):

		di = i-player.x
		dj = j-player.y
		distance = math.sqrt(di**2+ dj**2)

		if  di == 0 and dj == 0:

			return(False)
		elif distance  > self.player.sight:
			return(False)
		elif distance  <= self.player.sight:
			l=0
			while l < 1:
			
				tilei = math.floor(player.x +l*di)
				tilej = math.floor(player.y +l*dj)

				obstacle = self.world.tiles[tilej,tilei].opaque
				isself = (tilej==i and tilei==j)
				if obstacle and not isself:
					return(False)
				l+=distance/500
			return(True)
		return(True)

	### DISPLAY TEXT ##############################################

	def print_bottom(self,text):
		with self.t.location(0, self.t.height - self.textbox_height):
   			print(text)
		keyboard.wait("enter")

	def print_bottomf(self,text,offset=0):
		with self.t.location(0, self.t.height - self.textbox_height+offset):
   			print(text)



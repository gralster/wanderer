import keyboard
import os
import math
import sys
from blessed import Terminal
import numpy as np

from ff_Map import Map
from ff_Player import Player
from ff_Object import Object
from ff_AI import AI
from UI import Selector



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
		self.highlight = Selector(None,None)

		self.last_vis = np.zeros((self.y,self.x))
		self.whole_screen_refresh=False

	def setup_world(self):
		self.world.gen_features()

	### UPDATING #######################################

	def update_player(self):

		if self.mode =="explore":

			# movement

			self.player.last_x = self.player.x
			self.player.last_y = self.player.y

			keypressed = keyboard.read_key()

			if keypressed =="up":
				if self.world.tiles[self.player.y-self.player.speed,self.player.x].can_walk:
					self.player.y -= self.player.speed
			elif keypressed =="down":
				if self.world.tiles[self.player.y+self.player.speed,self.player.x].can_walk:
					self.player.y += self.player.speed
			elif keypressed =="left":
				if self.world.tiles[self.player.y,self.player.x-self.player.speed].can_walk:
					self.player.x -= self.player.speed
			elif keypressed =="right":
				if self.world.tiles[self.player.y,self.player.x+self.player.speed].can_walk:
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

			elif keypressed == "l":
				self.print_bottomf("You look around...")
				self.mode ="look"
				self.highlight.x = self.player.x
				self.highlight.y = self.player.y

				self.highlight.last_x = self.highlight.x
				self.highlight.last_y = self.highlight.y

			#testing for visibility :
			elif keypressed =="space":
				self.transfer_object(0,self.world,self.player,(12,12))

			elif keypressed == "esc":
				os.system('cls' if os.name == 'nt' else 'clear')
				quit()

		elif self.mode =="look":

			self.highlight.last_x = self.highlight.x
			self.highlight.last_y = self.highlight.y

			keypressed = keyboard.read_key()

			if keypressed =="up":
				self.highlight.y-=1
			elif keypressed =="down":
				self.highlight.y+=1
			elif keypressed =="left":
				self.highlight.x-=1
			elif keypressed =="right":
				self.highlight.x+=1

			elif keypressed =="enter":

				if self.world.explored[self.highlight.y,self.highlight.x]==False:
					self.print_bottomf("You don't know what's over there.")

				something_there = False

				for obj in self.world.objects:
					if self.highlight.x == obj.x and self.highlight.y == obj.y:
						canSee =self.inFOV(self.player,self.highlight.y,self.highlight.x)
						if canSee:
							self.print_bottomf(obj.desc)
						else:
							self.print_bottomf(obj.desc)
						something_there = True

				for ai in self.world.ais:
					if self.highlight.x == ai.x and self.highlight.y == ai.y:
						canSee =self.inFOV(self.player,self.highlight.y,self.highlight.x)
						if canSee:
							self.print_bottomf(ai.desc)
						else:
							self.print_bottomf(ai.desc)
						something_there = True

				if something_there == False:
					self.print_bottomf(self.world.tiles[self.highlight.y,self.highlight.x].desc)


			elif keypressed == "esc":
				self.last_vis[self.highlight.y,self.highlight.x]=-1
				self.mode="explore"


	def update_ai(self):
		for ai in self.world.ais:
			ai.update()


	def transfer_object(self,index,giver,receiver,loc):
		self.last_vis[loc[1],loc[0]]=-1
		obj=giver.lose(index)
		obj.x = loc[0]
		obj.y = loc[1]
		receiver.gain(obj)




	### DISPLAY SCREEN ############################################

	def clear(self):

		with self.t.hidden_cursor():

			if self.mode =="explore":
				with self.t.location(y=self.player.last_y,x=self.player.last_x):
					print(self.t.on_green(" "))
				print(self.t.home)#+self.t.on_darkgreen)#self.t.clear_eos)

			if self.mode =="look":
				with self.t.location(y=self.highlight.last_y,x=self.highlight.last_x):
					if self.world.explored[self.highlight.last_y,self.highlight.last_x]:
						canSee =self.inFOV(self.player,self.highlight.last_y,self.highlight.last_x)
						if canSee:
							print(self.t.on_green(" "))
						else:
							print(self.t.on_darkseagreen4(" "))
					else:
						print(self.t.on_black(" "))
				print(self.t.home)

	def display(self):

		if self.mode =="explore":

			current_vis = np.zeros((self.y,self.x))

			self.print_bottomf(self.whole_screen_refresh)

			for i in range(0,self.x):
				for j in range(0,self.y):
					canSee =self.inFOV(self.player,j,i)
					if canSee:
						self.world.explored[j,i]=True
						current_vis[j,i]=1

			for ai in self.world.ais:
				if ai.x != ai.last_x or ai.y!=ai.last_y:
					current_vis[ai.y,ai.x]-=1
					current_vis[ai.last_y,ai.last_x]-=1

			changes = current_vis-self.last_vis

			if self.whole_screen_refresh:

				self.whole_screen_display()

			else:

				self.display_ground(changes)

				self.display_objects(changes)

				self.display_ai(changes)

			# update display of player
			with self.t.location(y=self.player.y,x=self.player.x):
				print(self.t.on_green+self.t.bold(self.player.symbol))

			# reset last seen array
			# - must be last thing in display function

			self.last_vis = current_vis
			self.whole_screen_refresh=False

		elif self.mode =="look":

			self.whole_screen_display()

			canSee =self.inFOV(self.player,self.highlight.y,self.highlight.x)
			with self.t.location(y=self.highlight.y,x=self.highlight.x):
				if canSee:
					print(self.t.on_green(self.highlight.symbol))
				else:
					print(self.t.on_darkseagreen4(self.highlight.symbol))

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

	def display_ground(self,changes):
		for i in range(0,self.x):
			for j in range(0,self.y):
				canSee =self.inFOV(self.player,j,i)
				if canSee:
					if changes[j,i]>=1:
						with self.t.location(y=j,x=i):
							print(self.t.on_green(self.world.tiles[j,i].symbol))

				if changes[j,i] ==-1:
					with self.t.location(y=j,x=i):
						print(self.t.on_darkseagreen4(self.world.tiles[j,i].symbol))

	def display_objects(self,changes):

		for obj in self.world.objects:
			canSee =self.inFOV(self.player,obj.y,obj.x)
			with self.t.location(y=obj.y,x=obj.x):
				if canSee:
					print(self.t.red_on_green(obj.symbol))
				if changes[obj.y,obj.x] ==-1:
					print(self.t.red_on_darkseagreen4(obj.symbol))

	def display_ai(self,changes):
		for ai in self.world.ais:
			canSee =self.inFOV(self.player,ai.y,ai.x)
			with self.t.location(y=ai.y,x=ai.x):
				if canSee:
					print(self.t.black_on_green(ai.symbol))
				if changes[ai.y,ai.x] ==-1:
					print(self.t.black_on_darkseagreen4(ai.symbol))

	def whole_screen_display(self):

		for i in range(0,self.x):
			for j in range(0,self.y):
				self.print_bottomf(i)
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
			with self.t.location(y=obj.y,x=obj.x):
				if canSee:
					print(self.t.red_on_green(obj.symbol))
				else:
					if self.world.explored[obj.y,obj.x]:
						print(self.t.red_on_darkseagreen4(obj.symbol))

	### DISPLAY TEXT ##############################################

	def print_bottom(self,text):
		with self.t.location(0, self.t.height - self.textbox_height):
			self.t.clear_eol()
			print(text)
		keyboard.wait("enter")

	def print_bottomf(self,text,offset=0):
		#self.clear_text_box()
		with self.t.location(0, self.t.height - self.textbox_height+offset):
			print(text)

	def print_bottom_time(self,text, time = 5):
		self.clear_text_box()
		with self.t.location(0, self.t.height - self.textbox_height):
			print(text)
			time.sleep(time)

	def clear_text_box(self):
		with self.t.location(0, self.t.height - self.textbox_height):
			print(self.t.clear_eos)

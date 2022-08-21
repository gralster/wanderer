from cmath import sqrt
from xml.etree.ElementTree import tostring
import keyboard
import os
import math
import sys
import time
from blessed import Terminal
import numpy as np


from ff_Map import Map
from ff_Player import Player
from ff_Object import Object
from ff_AI import AI
from UI import Selector



class Engine:

	### INITIALISATION ################################

	def __init__(self,mode,log =False):
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


		self.setup_disp() # just for debugging, delete later
		self.last_vis = np.zeros((int(self.world.height/4),self.world.width))
		self.whole_screen_refresh=False
		self.ui = np.zeros((int(self.world.height/4),self.world.width))

		self.log = log
		if log:
			os.remove('log.txt')
			self.errorfile =  open('log.txt', 'a')

	def setup_world(self):
		self.world.gen_features()
		self.world.place_player(self.player)

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
				if self.log:
					self.errorfile.write("pushing edge of map\n")
				self.player.y = self.player.last_y
				self.player.x = self.player.last_x
				self.world.move_map(keypressed)
				self.whole_screen_refresh=True




			# actions

			# pick up
			elif keypressed ==".":
				obj_indexes =self.world.get_at_location(self.player.y,self.player.x)
				if obj_indexes==[]:
					self.print_bottom("nothing to pick up")
				else:
					for index in obj_indexes:
						self.transfer_object(index,self.world,self.player,(self.player.x,self.player.y))

			#drop
			elif keypressed == ",":
				items = self.player.get_inventory()
				if items ==[]:
					self.print_bottom("you have nothing to drop!")
				else:
					self.print_bottomf(self.player.get_inventory())
					self.print_bottom("What do you want to drop? (0,1,2,...")

					selection = int(input()[-1])
					self.transfer_object(selection,self.player,self.world,(self.player.x,self.player.y))

			# see inventory
			elif keypressed == "i":
				self.print_bottom(self.player.get_inventory())

			# look around
			elif keypressed == "l":

				if self.log:
					self.errorfile.write("look mode activated\n")

				self.print_bottomf("You look around...")
				self.mode ="look"
				self.highlight.x = self.player.x
				self.highlight.y = self.player.y

				self.highlight.last_x = self.highlight.x
				self.highlight.last_y = self.highlight.y

			# talk
			elif keypressed == "t":

				self.print_bottomf("You call out!...")
				options = ["Hello!","Fuck you all!","Help!"]
				i = 0
				for option in options:
					self.print_bottomf(str(i)+": "+options[i],offset=i+1)
					i+=1

				while True:
					entry = keyboard.read_key()
					try:
						choice = int(entry)
						if choice in range(0,len(options),1):
							break
					except:
						pass

				self.print_overhead_time(self.player,options[choice],wait=1)

				#self.mode ="listen"
				i = 0
				for ai in self.world.ais:
					if self.in_hearing_range(ai,self.player) and self.in_hearing_range(self.player,ai):
						self.print_overhead_time(ai,ai.respond(options[choice]),wait=3)
						i+=1
				self.clear_text_box()



			#testing for visibility :
			elif keypressed =="space":
				self.transfer_object(0,self.world,self.player,(12,12))

			# quit game
			elif keypressed == "esc":
				if self.log:
					self.errorfile.write("player quit.\n")
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
				if self.log:
					self.errorfile.write("look mode ended\n")
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

	# test if two beings are within hearing range of eachother
	def in_hearing_range(self,person_a,person_b):
		distance = math.sqrt((person_a.x -person_b.x)**2 + (person_a.y -person_b.y)**2 )
		if distance < person_a.hearing:
			return True
		else:
			return False



	### DISPLAY SCREEN ############################################

	def clear(self):

		with self.t.hidden_cursor():

			if self.mode =="explore":
				with self.t.location(y=self.player.last_y,x=self.player.last_x):
					print(self.t.on_green(" "))
				print(self.t.home)#+self.t.on_darkgreen)#self.t.clear_eos)

			for ai in self.world.ais:
				canSee =self.inFOV(self.player,ai.y,ai.x)
				if canSee:
					if ai.x != ai.last_x or ai.y!=ai.last_y:
						self.last_vis[ai.last_y,ai.last_x]-=1

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

	def setup_disp(self):

		#draw bounding box:

		for i in range(0,int(self.world.width)):
			with self.t.location(y=0,x=i):
				print(self.t.on_red(" "))
			with self.t.location(y=int(self.world.height/4)-1,x=i):
				print(self.t.on_red(" "))
		for j in range(0,int(self.world.height/4)):
			with self.t.location(y=j,x=0):
				print(self.t.on_red(" "))
			with self.t.location(y=j,x=int(self.world.width)):
				print(self.t.on_red(" "))

	def display(self):

		if self.mode =="explore":

			# set up array to show what has changed in view
			current_vis = np.zeros((int(self.world.height/4),self.world.width))

			# make of record of what can currently be seen
			for i in range(0,self.world.width):
				for j in range(0,int(self.world.height/4)):
					canSee =self.inFOV(self.player,j,i)
					if canSee:
						self.world.explored[j,i]=True
						current_vis[j,i]=1

			# add position of ais
			for ai in self.world.ais:
				if ai.x != ai.last_x or ai.y!=ai.last_y:
					current_vis[ai.y,ai.x]=1
					#current_vis[ai.last_y,ai.last_x]-=1

			if self.ui.any() !=0:
				current_vis -= self.ui


			self.print_bottomf(self.whole_screen_refresh)

			if self.whole_screen_refresh:

				self.whole_screen_display()

			else:

				changes = current_vis-self.last_vis

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
		for i in range(0,self.world.width):
			for j in range(0,int(self.world.height/4)):
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

		if self.log:
			self.errorfile.write("refreshing whole screen\n")

		for i in range(0,self.x-1):
			for j in range(0,self.y-1):
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
		with self.t.location(0, self.t.height - self.textbox_height+offset):
			print(text)

	def print_bottom_time(self,text, wait = 5):
		self.clear_text_box()
		with self.t.location(0, self.t.height - self.textbox_height):
			print(text)
			time.sleep(wait)

	def clear_text_box(self):
		with self.t.location(0, self.t.height - self.textbox_height):
			print(self.t.clear_eos)

	def print_overhead_time(self,speaker,text,wait=5):

		over_pos_x = speaker.x
		over_pos_y = speaker.y-1
		with self.t.location(over_pos_x,over_pos_y):
			print(text)
			time.sleep(wait)
		for i in range(0,len(text)):
			self.ui[over_pos_y,over_pos_x+i]=-1
		#with self.t.location(over_pos_x, over_pos_y):
		#	print(" "*len(text))

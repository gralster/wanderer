from cmath import sqrt
from xml.etree.ElementTree import tostring
import keyboard
import os
import math
import sys
import time
from blessed import Terminal
import numpy as np
import re

from translate_image import display_pix
from translate_image import display_small

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

		print(" ")
		print("	terminal width = "+str(self.t.width))
		print("	terminal height = "+str(self.t.height))
		time.sleep(2)

		self.textbox_height = 8
		self.update_screen()
		self.player = Player("grace",5,5)
		self.world = Map(self.player,300,300)

		self.highlight = Selector(None,None)

		self.setup_disp()
		self.last_vis = np.zeros((self.screen_height,self.screen_width))
		self.whole_screen_refresh=False
		self.ui = np.zeros((self.screen_height,self.screen_width))

		self.log = log
		if log:
			os.remove('log.txt')
			self.errorfile =  open('log.txt', 'a')

	def update_screen(self):
		self.x = self.t.width
		self.y = self.t.height-self.textbox_height

	def setup_world(self):
		self.world.gen_features()
		self.world.place_player(self.player)


	def player_near_edge(self):
		tolerance =self.player.sight+1
		if self.screen_width-(self.player.x-self.world.tl_x) <tolerance or self.screen_height-(self.player.y-self.world.tl_y) <tolerance or (self.player.x-self.world.tl_x)<tolerance or (self.player.y-self.world.tl_y) <tolerance :
			return True
		else:
			 return False

	def near_edge(self,y,x):
		tolerance =self.player.sight+1
		if self.screen_width-x <tolerance or self.screen_height-y <tolerance or x<tolerance or y <tolerance :
			return True
		else:
			 return False

	### UPDATING #######################################

	def update_player(self):

		if self.mode =="map":

			# movement

			self.player.last_x = self.player.x
			self.player.last_y = self.player.y

			keypressed = keyboard.read_key()

			if keypressed =="up":
				self.player.move(+1,self.world.tiles)

			elif keypressed =="down":
				self.player.move(-1,self.world.tiles)
			elif keypressed =="left":
				self.player.rotate(-1)
			elif keypressed =="right":
				self.player.rotate(+1)
			self.print_bottomf(self.player.x,offset=2)
			self.print_bottomf(self.player.y,offset=3)
			if self.player_near_edge():

				if self.log:
					self.errorfile.write("pushing edge of map\n")
				self.player.y = self.player.last_y
				self.player.x = self.player.last_x
				self.world.move_map(keypressed)
				#self.whole_screen_refresh=True

				self.print_bottomf(self.world.tl_x,offset=1)
				self.print_bottomf(self.world.tl_y,offset=2)



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
					self.print_bottomf("What do you want to drop? (0,1,2,...")
					self.print_bottomf(self.player.get_inventory(),offset=1)

					while True:
						choice = keyboard.read_key()
						if choice =="esc":
							selection =-1
							break
						try:
							 selection = int(choice)
						except:
							 pass
						else:
							break

					#selection = int(choice[-1])
					self.clear_text_box()
					if selection >=0:
						self.print_bottom_time("You drop the "+self.player.objects[selection].name,1)
						self.transfer_object(selection,self.player,self.world,(self.player.x,self.player.y))

			#switch to explore mode:
			elif keypressed=="e":
				self.mode="explore"
				os.system('cls')
				if self.log:
					self.errorfile.write("explore mode activated\n")
			elif keypressed=="m":
				self.mode=="map"
				if self.log:
					self.errorfile.write("map mode activated\n")
			# see inventory
			elif keypressed == "i":
				self.print_bottom(self.player.get_inventory())

			# look around
			elif keypressed == "l":

				if self.log:
					self.errorfile.write("look mode activated\n")

				self.print_bottomf("You look around...")
				self.mode ="look"
				self.highlight.i = self.player.x-self.world.tl_x
				self.highlight.j = self.player.y-self.world.tl_y

				self.highlight.last_i = self.highlight.i
				self.highlight.last_j = self.highlight.j

				self.ui[self.highlight.last_j,self.highlight.last_i]+=1

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
						if entry =="esc":
							choice =-1
						choice = int(entry)
						if choice in range(0,len(options),1):
							break
					except:
						pass
				if choice >=0:
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
			time.sleep(0.15)
			self.highlight.last_i = self.highlight.i
			self.highlight.last_j = self.highlight.j

			keypressed = keyboard.read_key()

			if keypressed =="up":
				self.highlight.j-=1
			elif keypressed =="down":
				self.highlight.j+=1
			elif keypressed =="left":
				self.highlight.i-=1
			elif keypressed =="right":
				self.highlight.i+=1

			if self.near_edge(self.highlight.i,self.highlight.j):
				if self.log:
					self.errorfile.write("pushing edge of map with look\n")
				self.highlight.j = self.highlight.last_j
				self.highlight.i = self.highlight.last_i
				self.world.move_map(keypressed)
				#self.whole_screen_refresh=True

				self.print_bottomf(self.world.tl_x,offset=1)
				self.print_bottomf(self.world.tl_y,offset=2)

			elif keypressed =="enter":

				if self.world.explored[self.highlight.j+self.world.tl_y,self.highlight.i+self.world.tl_x]==False:
					self.print_bottomf("You don't know what's over there.")

				something_there = False

				for obj in self.world.objects:
					if self.highlight.i+self.world.tl_x == obj.x and self.highlight.j +self.world.tl_y== obj.y:
						canSee =self.inFOV(self.player,self.highlight.j+self.world.tl_y,self.highlight.i+self.world.tl_x)
						if canSee:
							self.print_bottomf(obj.desc)
						else:
							self.print_bottomf(obj.desc)
						something_there = True

				for ai in self.world.ais:
					if self.highlight.i +self.world.tl_x == ai.x and self.highlight.j+self.world.tl_y == ai.y:
						canSee =self.inFOV(self.player,self.highlight.j+self.world.tl_y,self.highlight.i+self.world.tl_x)
						if canSee:
							self.print_bottomf(ai.desc)
						else:
							self.print_bottomf(ai.desc)
						something_there = True

				if something_there == False:
					self.print_bottomf(self.world.tiles[self.highlight.j,self.highlight.i].desc)

			elif keypressed == "esc":
				if self.log:
					self.errorfile.write("look mode ended\n")
				self.last_vis[self.highlight.j,self.highlight.i]=-1
				self.mode="map"

	def update_ai(self):
		for ai in self.world.ais:
			ai.update()

	def transfer_object(self,index,giver,receiver,loc):
		i = loc[0]-self.world.tl_x
		j = loc[1]-self.world.tl_y

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

	#def add_rel(self,pos):
	#	return pos +


	def clear(self):

		with self.t.hidden_cursor():

			if self.mode =="map" or self.mode =="look":
				if (self.player.last_y-self.world.last_tl_y !=  self.player.y-self.world.tl_y) or (self.player.last_x-self.world.last_tl_x !=  self.player.x-self.world.tl_x):
					with self.t.location(y=self.player.last_y-self.world.tl_y,x=self.player.last_x-self.world.tl_x):
						print(self.t.on_green(" "))
				if self.mode =="look":
					with self.t.location(y=self.highlight.last_j,x=self.highlight.last_i):
						if self.world.explored[self.highlight.last_j+self.world.tl_y,self.highlight.last_i+self.world.tl_x]:
							canSee =self.inFrontFOV(self.player,self.highlight.last_j+self.world.tl_y,self.highlight.last_i+self.world.tl_x)
							if canSee:
								print(self.t.on_green(" "))
							else:
								print(self.t.on_darkseagreen4(" "))
						else:
							print(self.t.on_black(" "))
					print(self.t.home)

			for ai in self.world.ais:
				canSee =self.inFrontFOV(self.player,ai.y,ai.x)
				if canSee:
					if(( ai.x-self.world.tl_x )!=( ai.last_x-self.world.last_tl_x)) or ((ai.y-self.world.tl_y)!=(ai.last_y-self.world.last_tl_y)):
						self.last_vis[ai.last_y-self.world.tl_y,ai.last_x-self.world.tl_x]-=1

	def setup_disp(self):

		self.screen_width = self.t.width
		self.screen_height = self.t.height-self.textbox_height

		#draw bounding box:
		for i in range(0,int(self.screen_width)):
			with self.t.location(y=0,x=i):
				print(self.t.on_red(" "))
			with self.t.location(y=self.screen_height-1,x=i):
				print(self.t.on_red(" "))
		for j in range(0,self.screen_height):
			with self.t.location(y=j,x=0):
				print(self.t.on_red(" "))
			with self.t.location(y=j,x=int(self.screen_width)):
				print(self.t.on_red(" "))

	def display_sprite(self,t,i,j,object):
		#di = i-self.player.x
		dj = j-19 # for horizon line
		#distance = math.sqrt(di**2+ dj**2)
		if object.pix[-3:]=="png":
			display_pix(object.pix,t,pos=(j,i),bg=(0,0,0))
		else:
			display_small(object.pix,t,2*dj,pos=(j,i))
		#time.sleep(1)

	def display(self):

		if self.mode =="explore":
			horizon = 20

			#print sky
			for i in range(0,self.screen_width):
				for j in range(0,horizon):
					with self.t.location(y=j,x=i):
						print(self.t.on_blue(" "))

			#print ground and terrain

			fovwidth = 23
			j = 0
			for y in range(self.player.y-self.player.sight,self.player.y):

				ground_row = []
				object_row  = []
				people_row = []
				element_pos = []

				for x in range(self.player.x-int(fovwidth/2),self.player.x+int(fovwidth/2)):
					self.print_bottomf((y-self.world.tl_y,x-self.world.tl_x),offset = 2)

					canSee =self.inFrontFOV(self.player,y,x)
					if canSee:
						ground_row.append(self.world.tiles[y,x])
						for obj in self.world.objects:
							if y ==obj.y and x==obj.x:
								object_row.append(obj)
						for ai in self.world.ais:
							if y ==ai.y and x==ai.x:
								people_row.append(ai)
				print(len(ground_row))
				if len(ground_row) !=0:


					for i in range(len(ground_row)):
						ipos = int((self.screen_width/2)+((i-(len(ground_row)/2))*len(ground_row)))
						element_pos.append(ipos)

					tile = 0
					object = 0
					person = 0
					for i in range(self.screen_width):
						if i in element_pos:
							index = element_pos.index(i)
							self.display_sprite(self.t,i,j+horizon,ground_row[index])
							try:
								self.display_sprite(self.t,i,j+horizon,object_row[object])
							except:
								pass
							try:
								self.display_sprite(self.t,i,j+horizon,people_row[person])
							except:
								pass
						else:
							with self.t.location(y=horizon+j,x=i):
								print(self.t.on_green(" "))
						tile+=1
						object+=1
						person+=1

				j+=1
			self.display_sprite(self.t,int(self.screen_width/2),horizon+j,self.player)
			#time.sleep(1)
			#self.player.display_sprite(self.t,self.world.tl_y,self.world.tl_x)

		if self.mode =="map" or self.mode=="look":

			# set up array to show what has changed in view
			current_vis = np.zeros((self.screen_height,self.screen_width))

			# make of record of what can currently be seen
			for i in range(0,self.screen_width):
				for j in range(0,self.screen_height):
					canSee =self.inFrontFOV(self.player,j+self.world.tl_y,i+self.world.tl_x)
					if canSee:
						self.world.explored[j+self.world.tl_y,i+self.world.tl_x]=True
						current_vis[j,i]=1

			# add position of ais
			for ai in self.world.ais:

				canSee =self.inFrontFOV(self.player,ai.y,ai.x)

				if ( ai.x-self.world.tl_x != ai.last_x-self.world.last_tl_x or ai.y-self.world.tl_y!=ai.last_y-self.world.last_tl_y) and canSee:
					current_vis[ai.y-self.world.tl_y,ai.x-self.world.tl_x]=1
					#current_vis[ai.last_y,ai.last_x]-=1

			if self.ui.any() !=0:
				current_vis -= self.ui
				#self.whole_screen_refresh=True
				self.ui = np.zeros((self.screen_height,self.screen_width))

			#self.print_bottomf(self.whole_screen_refresh)

			if self.whole_screen_refresh:
				self.whole_screen_display()

			else:
				changes = current_vis-self.last_vis
				self.display_ground_on_map(changes)
				self.display_objects_on_map(changes)
				self.display_ai_on_map(changes)

			# update display of player

			self.player.display_symbol(self.t,self.world.tl_y,self.world.tl_x)



			# reset last seen array
			# - must be last thing in display function
			self.last_vis = current_vis


			if self.mode =="look":

				canSee =self.inFOV(self.player,self.highlight.j+self.world.tl_y,self.highlight.i+self.world.tl_x)
				with self.t.location(y=self.highlight.j,x=self.highlight.i):
					if canSee:
						print(self.t.on_green(self.highlight.symbol))
					else:
						print(self.t.on_darkseagreen4(self.highlight.symbol))

	def inFOV(self,player,y,x):

		di = x-player.x
		dj = y-player.y
		distance = math.sqrt(di**2+ dj**2)

		if  di == 0 and dj == 0:

			return(False)
		elif distance  > self.player.sight:
			return(False)
		elif distance  <= self.player.sight:
			l=0
			while l < 1:

				tilex = math.ceil(player.x +l*di)
				tiley = math.ceil(player.y +l*dj)

				obstacle = self.world.tiles[tiley,tilex].opaque
				isself = (tiley==x and tilex==y)

				if obstacle and not isself:
					return(False)
				l+=distance/500
			return(True)
		return(True)

	def inFrontFOV(self,player,y,x):
		widevision = 0.25
		if self.inFOV(player,y,x):

			di = x-player.x
			dj = y-player.y

			if player.facing ==0:
				if dj<0:
					return True
				else:
					return False
			if player.facing ==1:
				if dj<di:
					return True
				else:
					return False
			if player.facing ==2:
				if di>0:
					return True
				else:
					return False
			if player.facing ==3:
				if dj>-1*di:
					return True
				else:
					return False
			if player.facing ==4:
				if dj>0:
					return True
				else:
					return False
			if player.facing ==5:
				if  dj>di:
					return True
				else:
					return False
			if player.facing ==6:
				if di<0:
					return True
				else:
					return False
			if player.facing ==7:
				if dj<-1*di:
					return True
				else:
					return False



	def is_on_screen(self,thing):
		if (thing.x < self.world.tl_x+self.screen_width and thing.x >self.world.tl_x ) and (thing.y< self.world.tl_y+self.screen_height and thing.y >self.world.tl_y):
			return True
		else:
			return False

	def display_ground_on_map(self,changes):
		for i in range(0,self.screen_width):
			for j in range(0,self.screen_height):

				#canSee =self.inFOV(self.player,j+self.world.tl_y,i+self.world.tl_x)
				inFront = self.inFrontFOV(self.player,j+self.world.tl_y,i+self.world.tl_x)
				if inFront:
					if self.world.tiles[j+self.world.tl_y,i+self.world.tl_x].symbol != self.world.tiles[j+self.world.last_tl_y,i+self.world.last_tl_x].symbol or changes[j,i]>=1:
						with self.t.location(y=j,x=i):
							print(self.t.on_green(self.world.tiles[j+self.world.tl_y,i+self.world.tl_x].symbol))
				else:
					if (self.world.explored[j+self.world.tl_y,i+self.world.tl_x] and self.world.tiles[j+self.world.tl_y,i+self.world.tl_x].symbol != self.world.tiles[j+self.world.last_tl_y,i+self.world.last_tl_x].symbol)or(self.world.explored[j+self.world.tl_y,i+self.world.tl_x] != self.world.explored[j+self.world.last_tl_y,i+self.world.last_tl_x]) or changes[j,i]>=1 or changes[j,i] ==-1:
						with self.t.location(y=j,x=i):
							print(self.t.on_darkseagreen4(self.world.tiles[j+self.world.tl_y,i+self.world.tl_x].symbol))
					if (not self.world.explored[j+self.world.tl_y,i+self.world.tl_x] and self.world.explored[j+self.world.last_tl_y,i+self.world.last_tl_x]):
						with self.t.location(y=j,x=i):
							print(self.t.on_black(" "))

	def display_objects_on_map(self,changes):

		for obj in self.world.objects:
			#canSee =self.inFOV(self.player,obj.y,obj.x)
			canSee = self.inFrontFOV(self.player,obj.y,obj.x)

			self.print_bottomf(canSee)
			if canSee:
				# create
				#obj.display_vis_sprite(self.t,self.player,self.world.tl_y,self.world.tl_x)
				obj.display_vis_symbol(self.t,self.world.tl_y,self.world.tl_x)
				#
				# delete old if frame has moved
				if (obj.y-self.world.last_tl_y !=  obj.y-self.world.tl_y) or (obj.x-self.world.last_tl_x !=  obj.x-self.world.tl_x):
					obj.clear_vis_symbol(self.t,self.world.last_tl_y,self.world.last_tl_x)
			else:
				if (obj.y-self.world.last_tl_y !=  obj.y-self.world.tl_y) or (obj.x-self.world.last_tl_x !=  obj.x-self.world.tl_x):
					obj.clear_invis_symbol(self.t,self.world.last_tl_y,self.world.last_tl_x)
					obj.display_invis_symbol(self.t,self.world.tl_y,self.world.tl_x)

			if changes[obj.y-self.world.tl_y,obj.x-self.world.tl_x] ==-1:
				obj.display_invis_symbol(self.t,self.world.tl_y,self.world.tl_x)

	def display_ai_on_map(self,changes):
		for ai in self.world.ais:
			canSee =self.inFrontFOV(self.player,ai.y,ai.x)
			if canSee:
				#ai.display_vis_sprite(self.t,self.player,self.world.tl_y,self.world.tl_x)
				ai.display_vis_symbol(self.t,self.world.tl_y,self.world.tl_x)
				if (ai.last_y-self.world.last_tl_y !=  ai.y-self.world.tl_y) or (ai.last_x-self.world.last_tl_x !=  ai.x-self.world.tl_x):
					ai.clear_vis_symbol


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
		self.clear_text_box()

	def clear_text_box(self):
		with self.t.location(0, self.t.height - self.textbox_height):
			print(self.t.clear_eos)

	def print_overhead_time(self,speaker,text,wait=5):

		over_pos_i = speaker.x-self.world.tl_x
		over_pos_j = speaker.y-1-self.world.tl_y
		with self.t.location(over_pos_i,over_pos_j):
			print(text)
			time.sleep(wait)
		for i in range(0,len(text)):
			self.ui[over_pos_j,over_pos_i+i]+=1
		#with self.t.location(over_pos_i, over_pos_j):
		#	print(" "*len(text))

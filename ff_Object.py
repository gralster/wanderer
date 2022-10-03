from translate_image import display_pix
import math

class Object:

	def __init__(self,x,y,name,symbol,desc):
		self.x= x
		self.y = y
		self.symbol =symbol
		self.name = name
		self.desc = desc

	def display_vis_symbol(self,t,tl_y,tl_x):
		with t.location(y=self.y-tl_y,x=self.x-tl_x):
			print(t.red_on_green(self.symbol))

	def display_invis_symbol(self,t,tl_y,tl_x):
		with t.location(y=self.y-tl_y,x=self.x-tl_x):
			print(t.red_on_darkseagreen4(self.symbol))

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
		display_pix('assets/pot.png',t,pos=(self.y-tl_y,self.x-tl_x),bg=(0,0,0),scaleup=int(min(1,3/distance)))

	def clear_sprite(self,t,tl_y,tl_x):
		pass

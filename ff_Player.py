from translate_image import display_pix

class Player:

	def __init__(self,name,y,x):
		self.name = name
		self.x = x
		self.y = y
		self.last_x = x
		self.last_y = y
		self.speed = 1
		self.sight = 25
		self.symbol = "x"
		self.objects = list()
		self.hearing = 10
		self.pix = 'assets/sprite2.png'

	def gain(self,obj):
		self.objects.append(obj)

	def lose(self,index):
		obj = self.objects.pop(index)
		return(obj)

	def get_inventory(self):
		in_inv = list()
		for obj in self.objects:
			in_inv.append(obj.name)
		return(in_inv)

	def display_symbol(self,t,tl_y,tl_x):
		with t.location(y=self.y-tl_y,x=self.x-tl_x):
			print(t.on_green+t.bold(self.symbol))

	def display_sprite(self,t,tl_y,tl_x):
		display_pix('assets/sprite2.png',t,pos=(self.y-tl_y,self.x-tl_x),bg=(0,0,0))

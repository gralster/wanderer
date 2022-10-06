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
		self.facing = 0
		self.pix = 'assets/sprite2.png'

	def move(self,direction,map):
		aheadx = 0
		aheady = 0
		print(self.facing,self.speed*direction)
		if self.facing ==0:
			aheady = aheady + -1*self.speed*direction
		elif self.facing ==1:
			aheady = aheady + -1*self.speed*direction
			aheadx = aheadx + self.speed*direction
		elif self.facing ==2:
			aheadx = aheadx + self.speed*direction
		elif self.facing ==3:
			aheady = aheady + self.speed*direction
			aheadx = aheadx + self.speed*direction
		elif self.facing ==4:
			aheady = aheady + self.speed*direction
		elif self.facing ==5:
			aheady = aheady + self.speed*direction
			aheadx = aheadx + -1*self.speed*direction
		elif self.facing ==6:
			aheadx = aheadx + -1*self.speed*direction
		elif self.facing ==7:
			aheady = aheady + -1*self.speed*direction
			aheadx = aheadx + -1*self.speed*direction
		#print(map[aheady,aheadx].can_walk)
		if map[self.y + aheady,self.x + aheadx].can_walk:
			self.y += aheady
			self.x += aheadx

		#print(aheadx,aheady)

	def rotate(self,direction):
		self.facing = (self.facing + direction)%8

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

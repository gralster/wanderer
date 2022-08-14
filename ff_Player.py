
class Player:
	
	def __init__(self,name,y,x):
		self.name = name
		self.x = x
		self.y = y
		self.last_x = x
		self.last_y = y
		self.speed = 1
		self.sight = 15
		self.symbol = "x"
		self.objects = list()

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


		
		
	

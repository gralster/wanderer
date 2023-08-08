#own classes
from ff_Map import Map
from ff_Player import Player
from ff_Object import Object
from ff_engine import Engine

import time

def initiate():

	game = Engine("map",True)
	time.sleep(0.5)
	game.setup_world()
	game.clear()
	return(game)

def update(game):
	game.clear()
	game.display()
	game.update_player()
	game.update_ai()
	game.update_screen()
	time.sleep(0.05)


game = initiate()
print("done game initiation")

print("Running game...")

while True:
	update(game)


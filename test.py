from translate_image import display
from blessed import Terminal
import time
import keyboard

term = Terminal()

textbox_height=10

### functions copied from engine:

def print_bottom(text):
	with term.location(0, term.height - textbox_height):
		term.clear_eol()
		print(text)
	keyboard.wait("enter")

def print_bottomf(text,offset=0):
	with term.location(0, term.height - textbox_height+offset):
		print(text)

def print_bottom_time(text, wait = 5):
	self.clear_text_box()
	with term.location(0, term.height - textbox_height):
		print(text)
		time.sleep(wait)

def clear_text_box():
	with term.location(0, term.height -textbox_height):
		print(term.clear_eos)

###new

def print_bottom_slow(text):
    clear_text_box()
    with term.location(0, term.height - textbox_height):
        i=0
        j=0
        for char in text:

            with term.location(i, term.height - textbox_height+j):
                print(char)
                if char =="." or char =="!" or char == "?":
                    time.sleep(0.5)
                else:
                    time.sleep(0.05)
                i+=1
                if i == term.width:
                    j+=1
                    i=0
    return(j)

def print_options(choices,startline):
    j=0
    for choice in choices:
        print_bottomf(str(j)+": "+choices[j],offset=startline+j+1)
        j+=1

def skip_scene():
    pass

def search_around():
    text = "The ground around you is dark, but you can make out something large lying across your chest. Your clothing is in tatters but your pockets somehow still contain some cards."
    return text
def call_out():
    text = "You call out. Nearby there is a groan, and then nothing. Then from somewhere behind you a voice! \" Someone is alive! Over there!\" You hear footsteps and then a light shines down into your face, blinding you."
    return text
display('assets/stars.jpg',term)

intro = "You awaken among the remains of a passenger ship. Through the twisted, steaming carcass of the hull you can see that the sky is dark and full of stars. Space travel, safer than crossing the road, they said. Ha! But where were you going... and where did you come from? Your head aches and you want to sleep, but you know you must not."

line=print_bottom_slow(intro)
print(line)
choices = [term.bold+term.purple+"L"+term.normal+term.white+"isten to your surroundings",term.bold+term.yellow+"C"+term.normal+"all out: Help! Is anyone there?", term.bold+term.blue+"S"+term.normal+term.white+"earch around", term.bold+term.red+"T"+term.normal+term.white+"ry to get up",term.bold+term.orange+"W"+term.normal+term.white+"ait"]

print_options(choices,line)

keypressed = keyboard.read_key()

if keypressed == "L" or keypressed =="l":
    #choices = choices.remove()
    del choices[0]
    clear_text_box()
    print_bottom_slow("The wreckage groans as it cools. Somewhere out of sight you hear the crackle of an electrical fire. Could there be voices as well?")
    print_options(choices,line)
if keypressed == "C" or keypressed =="c":
    del choices[1]
    clear_text_box()
    print_bottom_slow(call_out())
if keypressed =="S" or keypressed =="s" :
    del choices[2]
    clear_text_box()
    line=print_bottom_slow(search_around())
    choices.append(term.bold+term.blue+"S"+term.normal+term.white+"earch your pockets")
    print_options(choices,line)
if keypressed == "T" or keypressed =="t":
    del choices[3]
    clear_text_box()
    print_bottom_slow("You try to sit up but there is something heavy lying across your chest. As you move it shifts, and pain tears through your ribs...")
    skip_scene()
if keypressed == "W" or keypressed =="w":
    del choices[4]
    clear_text_box()
    print_bottom_slow("Overhead, clouds begin to obscure the stars. A little rain begins to fall, wetting your face and  hissing on the hot metal around you.")
    print_options(choices,line)

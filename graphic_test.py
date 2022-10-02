from blessed import Terminal
from translate_image import display_small
import time
t = Terminal()
t.clear_eos()

t.move(0,4)
print(t.green("◭"))
t.move(1,3)
print(t.green("◭◭◭"))
t.move(2,2)
print(t.green("◭◭◭◭◭"))

display_small('assets/onetree.jpg',t,10,pos=(0,0))
display_small('assets/onetree.jpg',t,10,pos=(2,3))

time.sleep(2)
quit()
i=0
j=0
while i<20:
    if i >10:
        j+=1
        display_small('assets/onetree.jpg',t,10,pos=(j,(i-5)*10))

    display_small('assets/onetree.jpg',t,10,pos=(j,i*10))
    i+=1

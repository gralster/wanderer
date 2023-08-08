from translate_image import display_pix

def display_sprite(self,t,path,x,y,player,tl_y,tl_x):
    di = x-player.x
    dj = y-player.y
    distance = math.sqrt(di**2+ dj**2)
    display_pix(path,t,pos=(y-tl_y,x-tl_x),bg=(0,0,0))


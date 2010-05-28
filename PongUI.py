import time
import random
import pygame
from pygame.locals import *

from pgu import gui

W,H = 640,480
W2,H2 = 320,240

##You can initialize the screen yourself.
##::

##

class PongUI(gui.Table):
    def __init__(self,**params):
        gui.Table.__init__(self,**params)

        fg = (0,255,255)

        self.tr()
        self.td(gui.Label("Phil's Pygame GUI",color=fg),colspan=2)
        
        self.tr()
        self.td(gui.Label("Speed: ",color=fg),align=1)
        e = gui.HSlider(100,-500,500,size=20,width=100,height=16,name='speed')
        self.td(e)

app = gui.App()
ui = PongUI()

c = gui.Container(align=-1,valign=-1)
c.add(ui,0,0)

app.init(c)

pygame.init()
screen = pygame.display.set_mode((640,480),SWSURFACE)
clock = pygame.time.Clock()
        
done = False
while not done:
    app.paint(screen)
    pygame.display.flip()
    pygame.time.wait(10)
    for e in pygame.event.get():
        if e.type is QUIT: 
            done = True
        elif e.type is KEYDOWN and e.key == K_ESCAPE: 
            done = True
        else:
            app.event(e)



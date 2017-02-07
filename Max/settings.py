#import modules
from os import path
import pygame as pg

#screen settings
WIDTH = 600
HEIGHT = 600
FPS = 60

#colour settings
RED = (255,0,0)
GREEN  = (0,255,0)
BLUE = (0,0,255)
WHITE = (255,255,255)
BLACK = (0,0,0)
YELLOW = (255,155,0)

#tilemap folders
Root_dir = path.dirname(__file__)
Map_folder = path.join(Root_dir,'maps')
Map_file = path.join(Map_folder,'level1.tmx')

#player settings
PLAYER_ACC = 0.8
PLAYER_FRICTION = -0.10
PLAYER_GRAVITY = 0.50
JUMP_SPEED = 10
PLAYER_HIT_RECT = pg.Rect(0,0,35,35)
#load modules for main
import pygame as pg
from settings import *
from tilemap import *
from sprites import *
#creating a class (Game)
class Game:
    #initialize the game
    def __init__(self):
        pg.init()
        pg.mixer.init()
        self.clock = pg.time.Clock()
        self.last_update = pg.time.get_ticks()
        self.screen = pg.display.set_mode((WIDTH,HEIGHT))
        pg.display.set_caption('terraria')
        self.all_sprites = pg.sprite.Group()
        self.platforms = pg.sprite.Group()

    #creating a new game
    def new(self):
        self.player = Player(self)
        self.platform = Platform(self,250, HEIGHT / 1.5, 300, 20)
        self.platform = Platform(self,WIDTH * 6 / 7, HEIGHT / 2, 20, 100)
        self.platform = Platform(self, WIDTH * 2 / 7, HEIGHT / 2, 20, 100)
        self.tilemap = Tilemap(Map_file)
        self.newmap = self.tilemap.make_map()
    ##################################################################################################################
    #main game loop
    def run(self):
        self.clock.tick(FPS)
        self.dlt = pg.time.get_ticks() - self.last_update / 1000.0
        self.update()
        self.event()
        self.draw()
    #update the game while running
    def update(self):
        self.all_sprites.update()
    #checking if key pressed
    def event(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()

    #drawing sprites and screen
    def draw(self):
        self.screen.blit(self.newmap,(0,0))
        self.all_sprites.draw(self.screen)
        pg.display.flip()
    ###################################################################################################################
    #end game loop
    def show_str_screen(self):
        pass

g = Game()
g.new()
g.running = True
#while the game is running
while g.running:
    g.run()
pg.quit()
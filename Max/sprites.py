import pygame as pg
from settings import *
vec = pg.math.Vector2

def collide_with_walls(sprite,group,dir):

    if dir == 'x' :
        hits = pg.sprite.spritecollide(sprite,group,False)
        if hits:
            if sprite.vel.x > 0 :
                sprite.pos.x = hits[0].rect.left - sprite.rect.width / 2
            if sprite.vel.x < 0 :
                sprite.pos.x = hits[0].rect.right + sprite.rect.width / 2
            sprite.vel.x = 0

    if dir == 'y' :
        hits = pg.sprite.spritecollide(sprite,group,False)
        if hits:
            if sprite.vel.y  > 0:
                sprite.pos.y = hits[0].rect.top - sprite.rect.height / 2
            if sprite.vel.y < 0:
                sprite.pos.y = hits[0].rect.bottom + sprite.rect.height / 2
            sprite.vel.y = 0




class Player(pg.sprite.Sprite):
    def __init__(self,game):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self,self.groups)
        self.image = pg.Surface((50,50))
        self.image.fill(YELLOW)
        self.game = game
        self.rect = self.image.get_rect()
        self.hit_rect = PLAYER_HIT_RECT
        self.rect.center = (WIDTH / 2, HEIGHT / 2)
        self.pos = vec(WIDTH / 2, HEIGHT / 2)
        self.vel = vec(0,0)
        self.acc = vec(0,PLAYER_GRAVITY)



    def update(self):
        self.acc = vec(0, PLAYER_GRAVITY)
        self.get_keys()
        self.acc += self.vel * PLAYER_FRICTION
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc
        self.rect.center = self.pos
        if collide_with_walls(self, self.game.platforms, 'y'):
            collide_with_walls(self,self.game.platforms,'x')




    def get_keys(self):
        keys = pg.key.get_pressed()
        if keys[pg.K_d]:
            self.acc.x = PLAYER_ACC
        if keys[pg.K_a]:
            self.acc.x =- PLAYER_ACC
        if keys[pg.K_SPACE]:
            self.vel.y =- JUMP_SPEED


class Platform(pg.sprite.Sprite):
    def __init__(self,game,x,y,w,h):
        self.groups = game.all_sprites, game.platforms
        pg.sprite.Sprite.__init__(self,self.groups)
        self.image = pg.Surface((w,h))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y






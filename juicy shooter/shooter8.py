# Template for new Pygame project
# KidsCanCode 2014
import pygame
from pygame.locals import *
import sys
import random

# define some colors (R, G, B)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
FUCHSIA = (255, 0, 255)
GREY = (128, 128, 128)
DARKGREY = (64, 64, 64)
LIME = (0, 128, 0)
MAROON = (128, 0, 0)
NAVYBLUE = (0, 0, 128)
OLIVE = (128, 128, 0)
PURPLE = (128, 0, 128)
RED = (255, 0, 0)
SILVER = (192, 192, 192)
TEAL = (0, 128, 128)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 128, 0)
CYAN = (0, 255, 255)
BGCOLOR = DARKGREY

# basic constants for your game options
WIDTH = 800
HEIGHT = 640
FPS = 30
TITLE = "Shooter!"
GRAVITY = 1

level = [[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
         [1,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
         [1,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
         [1,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
         [1,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
         [1,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
         [1,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
         [1,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,1],
         [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
         [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
         [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
         [1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1],
         [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,1],
         [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,1],
         [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,1],
         [1,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,1],
         [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
         [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
         [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
         [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]]

# initialize pygame
pygame.init()
# initialize sound - remove if you're not using sound (always use sound!)
pygame.mixer.init()

def draw_text(text, size, x, y):
    # utility function to draw text at a given location
    font_name = pygame.font.match_font('arial')
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.topleft = (x, y)
    g.screen.blit(text_surface, text_rect)

class SpriteSheet:
    """Utility class to load and parse spritesheets"""
    def __init__(self, filename):
        self.sprite_sheet = pygame.image.load(filename).convert()

    def get_image(self, x, y, width, height):
        # grab an image out of a larger spritesheet
        image = pygame.Surface([width, height])
        image.blit(self.sprite_sheet, (0, 0), (x, y, width, height))
        image.set_colorkey([0, 0, 0])
        return image

class Game:
    def __init__(self):
        flags = DOUBLEBUF | HWSURFACE
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT), flags)
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.load_images()
        self.running = True
        self.shake = False
        self.explode_snd = pygame.mixer.Sound('snd/boom8.wav')
        self.all_sprites = pygame.sprite.Group()
        self.platforms = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.flashes = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.player = Player()
        for i in range(10):
            mob = Mob(self.mob_frames_r, self.mob_frames_l,
                      WIDTH/2+i*27, HEIGHT/3)
            self.all_sprites.add(mob)
            self.enemies.add(mob)
        self.all_sprites.add(self.player)
        self.create_platforms()

    def spawn(self):
        mob = Mob(self.mob_frames_r, self.mob_frames_l,
                  WIDTH/2, HEIGHT/3)
        self.all_sprites.add(mob)
        self.enemies.add(mob)

    def load_images(self):
        # mobs
        sprite_sheet = SpriteSheet('img/guardBlue64.png')
        self.mob_frames_l = []
        self.mob_frames_r = []
        image = sprite_sheet.get_image(5, 9, 48, 55)
        self.mob_frames_l.append(image)
        image = pygame.transform.flip(image, True, False)
        self.mob_frames_r.append(image)
        image = sprite_sheet.get_image(67, 9, 48, 55)
        self.mob_frames_l.append(image)
        image = pygame.transform.flip(image, True, False)
        self.mob_frames_r.append(image)
        image = sprite_sheet.get_image(134, 9, 48, 55)
        self.mob_frames_l.append(image)
        image = pygame.transform.flip(image, True, False)
        self.mob_frames_r.append(image)
        image = sprite_sheet.get_image(198, 9, 48, 55)
        self.mob_frames_l.append(image)
        image = pygame.transform.flip(image, True, False)
        self.mob_frames_r.append(image)
        # explosions
        sprite_sheet = SpriteSheet('img/puff_smoke.png')
        self.explode_frames = []
        for y in range(2, 332, 66):
            for x in range(2, 464, 66):
                image = sprite_sheet.get_image(x, y, 64, 64)
                self.explode_frames.append(image)
        del self.explode_frames[-3:]

    def create_platforms(self):
        plat_image = pygame.image.load("img/platform_square.png").convert()
        for row in range(0, HEIGHT, 32):
            for col in range(0, WIDTH, 32):
                if level[row//32][col//32]:
                    plat = Platform(plat_image, col, row)
                    self.all_sprites.add(plat)
                    self.platforms.add(plat)

    def run(self):
        while self.running:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

    def update(self):
        for sprite in self.flashes:
            if pygame.time.get_ticks() - sprite.time > 10:
                sprite.kill()
        if self.shake and pygame.time.get_ticks() - self.shake_time > 50:
            for sprite in self.all_sprites:
                sprite.rect.x -= self.shake_x
                sprite.rect.y -= self.shake_y
            self.shake = False
        # get rid of bullets that hit the wall
        pygame.sprite.groupcollide(g.platforms, g.bullets, False, True)
        # kill baddies
        hits = pygame.sprite.groupcollide(self.enemies, self.bullets, True, True)
        for hit in hits:
            expl = Explode(self.explode_frames, hit.rect.x, hit.rect.y-10)
            self.all_sprites.add(expl)
            self.explode_snd.play()
            self.screen_shake(12)

    def quit(self):
        pygame.quit()
        sys.exit()

    def draw(self):
        self.screen.fill(BGCOLOR)
        # text = 'FPS: %s' % (int(self.clock.get_fps()))
        # draw_text(text, 16, 35, 35)
        self.all_sprites.update()
        self.all_sprites.draw(self.screen)
        pygame.display.flip()

    def events(self):
        for event in pygame.event.get():
            # this one checks for the window being closed
            if event.type == pygame.QUIT:
                self.quit()
            # now check for keypresses
            elif event.type == pygame.KEYDOWN:
                # this one quits if the player presses Esc
                if event.key == pygame.K_ESCAPE:
                    self.quit()
                # add any other key events here
                if event.key == pygame.K_UP:
                    self.player.jump()
                if event.key == pygame.K_LEFT:
                    self.player.go('l')
                if event.key == pygame.K_RIGHT:
                    self.player.go('r')
                if event.key == pygame.K_SPACE:
                    self.player.shoot()
                if event.key == pygame.K_z:
                    self.spawn()
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    self.player.stop('l')
                if event.key == pygame.K_RIGHT:
                    self.player.stop('r')

    def go_screen(self):
        pass

    def start_screen(self):
        pass

    def screen_shake(self, amount):
        if not self.shake:
            self.shake_x = random.randrange(-amount, amount+1)
            self.shake_y = random.randrange(-amount, amount+1)
            for sprite in self.all_sprites:
                sprite.rect.x += self.shake_x
                sprite.rect.y += self.shake_y
            self.shake = True
            self.shake_time = pygame.time.get_ticks()

class Player(pygame.sprite.Sprite):
    speed = 8
    jump_speed = 18

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.shoot_snd = pygame.mixer.Sound("snd/gun_fire.wav")
        self.shoot_snd.set_volume(0.5)
        self.speed_x = 0
        self.speed_y = 0
        # load animation frames
        # 8 running frames for each dir
        # one standing for each dir
        # one jumping for each dir
        self.dir = 'r'
        self.walking = False
        self.current_frame = 0
        self.now = 0
        self.last_update = 0
        self.flash = None
        self.load_images()
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 50
        # load bullet images
        sprite_sheet = SpriteSheet('img/M484SpaceSoldier.png')
        self.bullet_frames = []
        image = sprite_sheet.get_image(204, 250, 9, 6)
        self.bullet_frames.append(image)
        image = sprite_sheet.get_image(188, 250, 9, 6)
        self.bullet_frames.append(image)

    def load_images(self):
        self.frames_running_l = []
        self.frames_running_r = []
        self.frames_jumping_l = []
        self.frames_jumping_r = []
        self.frames_standing_l = []
        self.frames_standing_r = []
        sprite_sheet = SpriteSheet('img/M484SpaceSoldier.png')
        image = sprite_sheet.get_image(8, 11, 50, 50)
        self.frames_standing_r.append(image)
        image = pygame.transform.flip(image, True, False)
        self.frames_standing_l.append(image)
        image = sprite_sheet.get_image(212, 11, 50, 50)
        self.frames_jumping_r.append(image)
        image = pygame.transform.flip(image, True, False)
        self.frames_jumping_l.append(image)
        for x in range(8, 365, 51):
            image = sprite_sheet.get_image(x, 67, 50, 50)
            self.frames_running_r.append(image)
            image = pygame.transform.flip(image, True, False)
            self.frames_running_l.append(image)

        # set starting frame
        self.image = self.frames_standing_r[0]
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        self.animate()
        # update the player's position
        # add gravity
        self.speed_y += GRAVITY
        # move the sprite
        self.rect.x += self.speed_x
        self.check_collisions('x')
        self.rect.y += self.speed_y
        self.check_collisions('y')
        if self.flash:
            if pygame.time.get_ticks() - self.flash.time > 10:
                g.all_sprites.remove(self.flash)

    def check_collisions(self, dir):
        if dir == 'x':
            hit_list = pygame.sprite.spritecollide(self, g.platforms, False)
            if hit_list:
                if self.speed_x > 0:
                    self.rect.right = hit_list[0].rect.left
                elif self.speed_x < 0:
                    self.rect.left = hit_list[0].rect.right
        elif dir == 'y':
            hit_list = pygame.sprite.spritecollide(self, g.platforms, False)
            if hit_list:
                if self.speed_y > 0:
                    self.rect.bottom = hit_list[0].rect.top
                elif self.speed_y < 0:
                    self.rect.top = hit_list[0].rect.bottom
                self.speed_y = 0

    def animate(self):
        if self.speed_x != 0 and self.speed_y == 0:
            self.walking = True
        now = pygame.time.get_ticks()
        if self.walking:
            if now - self.last_update > 75:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % 7
                if self.dir == 'l':
                    self.image = self.frames_running_l[self.current_frame]
                else:
                    self.image = self.frames_running_r[self.current_frame]
        else:
            if self.speed_y == 0:
                if self.dir == 'l':
                    self.image = self.frames_standing_l[0]
                else:
                    self.image = self.frames_standing_r[0]
            else:
                if self.dir == 'l':
                    self.image = self.frames_jumping_l[0]
                else:
                    self.image = self.frames_jumping_r[0]

    def go(self, dir):
        # move in the direction pressed
        self.walking = True
        if dir == 'l':
            self.dir = 'l'
            self.speed_x = -self.speed
        if dir == 'r':
            self.dir = 'r'
            self.speed_x = self.speed

    def stop(self, dir):
        self.walking = False
        # stop moving if that direction's key is released
        if dir == 'l' and self.speed_x < 0:
            self.speed_x = 0
        if dir == 'r' and self.speed_x > 0:
            self.speed_x = 0

    def jump(self):
        # need to see if there's a platform under us.  If not, can't jump
        # move down a little bit and see if there's a collision
        self.rect.y += 1
        hit_list = pygame.sprite.spritecollide(self, g.platforms, False)
        self.rect.y -= 1
        if hit_list:
            self.walking = False
            self.speed_y -= self.jump_speed

    def shoot(self):
        num_bullets = 5
        if self.dir == 'l':
            for i in range(num_bullets):
                b = Bullet(self.bullet_frames, self.rect.left+18,
                           self.rect.centery-5, self.dir)
                g.all_sprites.add(b)
                g.bullets.add(b)
            flash = Muzzle_Flash(self.rect.x-10, self.rect.y+8)
            self.rect.x += 3
            hit_list = pygame.sprite.spritecollide(self, g.platforms, False)
            if hit_list:
                self.rect.x -= 3
        else:
            for i in range(num_bullets):
                b = Bullet(self.bullet_frames, self.rect.right-18,
                           self.rect.centery-5, self.dir)
                g.all_sprites.add(b)
                g.bullets.add(b)
            flash = Muzzle_Flash(self.rect.x+20, self.rect.y+8)
            self.rect.x -= 3
            hit_list = pygame.sprite.spritecollide(self, g.platforms, False)
            if hit_list:
                self.rect.x += 3
        g.all_sprites.add(flash)
        g.flashes.add(flash)
        self.shoot_snd.play()
        g.screen_shake(3)

class Bullet(pygame.sprite.Sprite):
    def __init__(self, frames, x, y, dir):
        pygame.sprite.Sprite.__init__(self)
        self.frames = frames
        self.image = self.frames[0]
        self.rect = self.image.get_rect()
        if dir == 'l':
            self.speed_x = random.randrange(-20, -17)
        else:
            self.speed_x = random.randrange(17, 20)
        self.speed_y = random.randrange(-2, 3)
        self.rect.x = x
        self.rect.y = y

    def update(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        # frame = (self.rect.x // 50) % len(self.frames)
        # self.image = self.frames[frame]

class Muzzle_Flash(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        sprite_sheet = SpriteSheet('img/M484SpaceSoldier.png')
        image = sprite_sheet.get_image(153, 271, 49, 47)
        self.image = pygame.transform.scale(image, (35, 35))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.time = pygame.time.get_ticks()

class Platform(pygame.sprite.Sprite):
    def __init__(self, img, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self):
        pass

class Explode(pygame.sprite.Sprite):
    def __init__(self, frames, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.frames = frames
        self.image = self.frames[0]
        self.current_frame = 0
        self.last_update = pygame.time.get_ticks()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > 1:
            self.last_update = now
            self.current_frame += 1
            if self.current_frame == len(self.frames):
                self.kill()
            else:
                self.image = self.frames[self.current_frame]

class Mob(pygame.sprite.Sprite):
    def __init__(self, frames_r, frames_l, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.frames_l = frames_l
        self.frames_r = frames_r
        self.last_update = pygame.time.get_ticks()
        self.current_frame = 0
        if random.randrange(2) == 0:
            self.dir = 'r'
            self.image = self.frames_l[0]
            self.speed_x = random.randrange(2, 4)
        else:
            self.dir = 'l'
            self.image = self.frames_r[0]
            self.speed_x = random.randrange(-3, -1)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed_y = 0

    def update(self):
        self.animate()
        self.speed_y += GRAVITY
        self.rect.x += self.speed_x
        self.check_collisions('x')
        self.rect.y += self.speed_y
        self.check_collisions('y')

    def animate(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > 150:
            self.last_update = now
            self.current_frame += 1
            if self.current_frame == len(self.frames_r):
                self.current_frame = 0
            if self.dir == 'l':
                self.image = self.frames_l[self.current_frame]
            else:
                self.image = self.frames_r[self.current_frame]

    def check_collisions(self, dir):
        if dir == 'x':
            hit_list = pygame.sprite.spritecollide(self, g.platforms, False)
            if hit_list:
                if self.speed_x > 0:
                    self.rect.right = hit_list[0].rect.left
                    self.dir = 'l'
                elif self.speed_x < 0:
                    self.rect.left = hit_list[0].rect.right
                    self.dir = 'r'
                self.speed_x *= -1
        elif dir == 'y':
            hit_list = pygame.sprite.spritecollide(self, g.platforms, False)
            if hit_list:
                if self.speed_y > 0:
                    self.rect.bottom = hit_list[0].rect.top
                elif self.speed_y < 0:
                    self.rect.top = hit_list[0].rect.bottom
                self.speed_y = 0

g = Game()
g.start_screen()
while True:
    g.run()
    g.go_screen()

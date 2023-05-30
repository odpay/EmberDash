import pygame
import random
import math
import json

## config
WIDTH = 800
HEIGHT = 600
FPS = 60
FREQ = 7

## Constants

# Colours
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

pygame.font.init()
FONT = pygame.font.SysFont(None, 24)


SCREEN = pygame.display.set_mode((WIDTH, HEIGHT), vsync=1)
CLOCK = pygame.time.Clock()

## Classes
class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.x = WIDTH/2
        self.xVel = 0.0
        self.y = HEIGHT/2
        self.yVel = 0.0
        self.speed = 5
        self.width = 20
        self.height = 20
        self.colour = WHITE
    
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(self.colour)
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)

    def update(self): # TODO: slow down diagonal movements, use sqrt
        vec = pygame.math.Vector2(self.xVel, self.yVel)
        if vec.x != 0 or vec.y != 0: vec.scale_to_length(self.speed)
        self.x += vec.x
        self.xVel = 0 # make self.speed 'max_speed', have an accel speed for smoother accel & decel <- maybe
        self.y += vec.y
        self.yVel = 0
        self.rect.center = (round(self.x), round(self.y))
        self.rect.clamp_ip(SCREEN.get_rect())
        self.x = self.rect.centerx
        self.y = self.rect.centery
        if pygame.sprite.spritecollideany(self, projectiles):
            self.kill()
        else:
            global score
            score += 1

    def up(self):
        
        self.yVel -= self.speed
    
    def down(self):
        self.yVel += self.speed
    
    def left(self):
        self.xVel -= self.speed
    
    def right(self):
        self.xVel += self.speed
    



class Projectile(pygame.sprite.Sprite):
    def __init__(self, x, y, xVel, yVel):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.xVel = xVel
        self.y = y
        self.yVel = yVel
        self.speed = 2.5
        self.width = 8
        self.height = 8
        self.colour = RED
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(self.colour)
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)
        self.outTime = 0

    def update(self):
        self.x += self.xVel
        self.y += self.yVel
        self.rect.center = (round(self.x), round(self.y))
        if not SCREEN.get_rect().contains(self.rect):
            self.outTime += 1
            if self.outTime > 100:
                self.kill()


## init
# pygame.init()

score = 0

pygame.display.set_caption("game")


p1 = pygame.sprite.GroupSingle()
p1.add(Player())

projectiles = pygame.sprite.Group()

ticker = 0
def populate(num):
    global ticker
    ticker += 1
    if ticker >= FREQ:
        for _ in range(num):
            projectiles.add(Projectile(random.randint(0, WIDTH), 0, random.uniform(-.5, .5), 1))
        ticker = 0

controls = {
    pygame.K_w: p1.sprite.up,
    pygame.K_s: p1.sprite.down,
    pygame.K_a: p1.sprite.left,
    pygame.K_d: p1.sprite.right
}





quit_flag = False
while not quit_flag:
    CLOCK.tick(FPS)
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit_flag = True

    pressed = pygame.key.get_pressed() # CANT PRESS MULTIPLE KEYS ASDDSASDASF
    for control in controls.keys():
        if pressed[control]:
            controls.get(control)()
    # Clear the screen (fill with a solid color)
    SCREEN.fill(BLACK)  # Use RGB values for the color


    populate(1)


    p1.update()
    projectiles.update()

    projectiles.draw(SCREEN)
    p1.draw(SCREEN)

    scoreCounter = FONT.render(f'{score}', True, BLUE)
    SCREEN.blit(scoreCounter, (20, 20))

    print(projectiles)
    # Update the display
    pygame.display.flip()


pygame.quit()
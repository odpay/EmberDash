import pygame
import random

## config
WIDTH = 800
HEIGHT = 600
FPS = 60

## Constants

# Colours
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)



SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
CLOCK = pygame.time.Clock()

## Classes
class Player:
    def __init__(self):
        self.x = WIDTH/2
        self.xVel = 0.0
        self.y = HEIGHT/2
        self.yVel = 0.0
        self.speed = 2.5
        self.width = 25
        self.height = 25
        self.colour = WHITE
    

    def draw(self):
        self.tick()
        pygame.draw.rect(SCREEN, self.colour, self.Rect())

    def Rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def up(self):
        self.yVel -= self.speed
    
    def down(self):
        self.yVel += self.speed
    
    def left(self):
        self.xVel -= self.speed
    
    def right(self):
        self.xVel += self.speed
    




    def tick(self):
        self.x += self.xVel
        self.xVel = 0
        self.y += self.yVel
        self.yVel = 0


class Projectile(pygame.sprite.Sprite):
    def __init__(self, x, xVel, y, yVel):
        self.x = x
        self.xVel = xVel
        self.y = y
        self.yVel = yVel
        self.speed = 2.5
        self.width = 8
        self.height = 8
        self.colour = RED
    
    def tick(self):
        self.x += self.xVel
        self.y += self.yVel
    
    def Rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)
    
    def draw(self):
        self.tick()
        pygame.draw.rect(SCREEN, self.colour, self.Rect())

## init
# pygame.init()

pygame.display.set_caption("game")

p1 = Player()

objects = []

def populate(num):
    for _ in range(num):
        objects.append(Projectile(random.randint(0, WIDTH), random.uniform(-.5, .5), 0, 1))

controls = {
    pygame.K_w: p1.up,
    pygame.K_s: p1.down,
    pygame.K_a: p1.left,
    pygame.K_d: p1.right
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
    for obj in objects:
        obj.draw()
    print(len(objects))
    p1.draw()
    # Update the display
    pygame.display.flip()


pygame.quit()
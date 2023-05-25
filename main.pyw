import pygame


## config
WIDTH = 800
HEIGHT = 600
FPS = 60

## Constants

# Colours
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)



SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
CLOCK = pygame.time.Clock()

## Classes
class Player:
    def __init__(self):
        self.x = WIDTH/2
        self.xVel = 0
        self.y = HEIGHT/2
        self.yVel = 0
        self.width = 15
        self.height = 15
        self.colour = WHITE
    

    def draw(self):
        self.tick()
        pygame.draw.rect(SCREEN, self.colour, self.Rect())

    def Rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def up(self):
        self.yVel -= 1
        print("u")
    
    def down(self):
        self.yVel += 1
        print("d")
    
    def left(self):
        self.xVel -= 1
        print("l")
    
    def right(self):
        self.xVel += 1
        print("r")
    




    def tick(self):
        self.x += self.xVel
        self.xVel = 0
        self.y += self.yVel
        self.yVel = 0



## init
# pygame.init()

pygame.display.set_caption("game")

p1 = Player()


controls = {
    pygame.K_UP: p1.up,
    pygame.K_DOWN: p1.down,
    pygame.K_LEFT: p1.left,
    pygame.K_RIGHT: p1.right
}





quit_flag = False
while not quit_flag:
    CLOCK.tick(FPS)
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit_flag = True

    pressed = pygame.key.get_pressed() # CANT PRESS MULTIPLE KEYS ASDDSASDASF
    # print(pressed)
        # if k: print(k)
    for control in controls.keys():
        
        if pressed[control]:
            controls.get(control)()
    # Clear the screen (fill with a solid color)
    SCREEN.fill(BLACK)  # Use RGB values for the color

    p1.draw()
    # Update the display
    pygame.display.flip()


pygame.quit()
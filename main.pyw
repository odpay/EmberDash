import pygame
import random
import json

## config
with open("./cfg/config.json", 'r') as cfgFile:
    cfg = json.loads(cfgFile.read())
    cfgFile.close()

WIDTH = cfg["WIDTH"]
HEIGHT = cfg["HEIGHT"]
FPS = cfg["FPS"]
START_FREQ = cfg["START_FREQ"]
END_FREQ = cfg["END_FREQ"]

## Constants

# Colours
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)


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
        # self.colour = WHITE
        self.flipped = False # Flag indicating if the player sprite is flipped
        # self.image = pygame.Surface((self.width, self.height))
        # self.image.fill(self.colour)
        self.image = pygame.image.load("assets/sprites/wispy/Wispy1.png")
        self.image = pygame.transform.scale(self.image, (self.width*2, self.height*2))
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)
        self.mask = pygame.mask.from_surface(self.image)
        # self.image = self.mask.to_surface()
        self.scoreCooldown = 0

    def update(self): 
        vec = pygame.math.Vector2(self.xVel, self.yVel) # Vectorises velocity each tick
        if vec.x != 0 or vec.y != 0: vec.scale_to_length(self.speed) # Scales vector with speed val if not stationary
        
        # Inflicts vec to positioning
        self.x += vec.x 
        self.y += vec.y

        # Center and screen clamping
        self.rect.center = (round(self.x), round(self.y))
        self.rect.clamp_ip(SCREEN.get_rect())
        self.x = self.rect.centerx
        self.y = self.rect.centery
        
        # Face sprite towards movement direction
        self.face()

        # Reset velocity for this tick
        self.xVel = 0 # make self.speed 'max_speed', have an accel speed for smoother accel & decel <- maybe
        self.yVel = 0

        # Mask collision check with projectiles to kill player
        if pygame.sprite.spritecollideany(self, projectiles, pygame.sprite.collide_mask):
            self.kill()
        
        # Score incriment logic
        else:
            self.scoreCooldown += 1
            if self.scoreCooldown >= 3:
                global score
                score += 1
                self.scoreCooldown = 0

    def face(self): # Flips sprite image (& collision mask) towards velocity direction
        if self.flipped and self.xVel > 0:
            self.image = pygame.transform.flip(self.image, True, False)
            self.flipped = False
        if not self.flipped and self.xVel < 0:
            self.image = pygame.transform.flip(self.image, True, False)
            self.flipped = True
        self.mask = pygame.mask.from_surface(self.image)
    
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
        self.width = 150
        self.height = 150
        self.image = pygame.image.load("assets/sprites/snow/snow.png")
        self.image = pygame.transform.scale(self.image, (self.width/8, self.height/8))
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)
        self.mask = pygame.mask.from_surface(self.image)
        self.outTime = 0

    def update(self):
        # Inflicts velocities to position
        self.x += self.xVel
        self.y += self.yVel
        self.rect.center = (round(self.x), round(self.y))

        # Despawns projectile if out of SCREEN for 100 frames
        if not SCREEN.get_rect().contains(self.rect):
            self.outTime += 1
            if self.outTime > 100:
                self.kill()


## init

# pygame.init()
# ^^ pygame boilerplate init function, commented because i seriously don't think you need it lol
# like it just wastes 4 seconds each launch

def syncHS(s=0): # Sync HI-SCORE with file
    with open("./cfg/hs.txt", 'r+') as hsF:
        hs = int(hsF.read())
        if s > hs:
            # Overly complex overwrite code, thanks python
            hs = s
            hsF.seek(0)
            hsF.write(str(s))
            hsF.truncate()
        hsF.close()
    return hs

## the testcase count number (used for desk check)
# testc = 0

# repeated init (on respawn)
def init():

    # took the init globalisation approach, (yes that's a real thing)
    # i promise i am not being elegantly incompetent, this approach is alot easier to work with in small-scale game dev (without using full OOP)
    global score, p1, projectiles, controls, ticker, populate, processInput, clamp
    
    # global testc, testCase

    # def testCase(s, hs): # Input set: (200, 400, 600, 400, 200, 800)
    #     global testc
    #     testc += 1
    #     print(f"Test Case (#{str(testc)}): Input score: {str(s)}, Output HI-SCORE: {str(hs)}")
    score = 0

    pygame.display.set_caption("Ember Dash")


    p1 = pygame.sprite.GroupSingle()
    p1.add(Player())

    projectiles = pygame.sprite.Group()

    ticker = 0

    # Mapping of keyboard controls to player actions
    controls = {
    pygame.K_w: p1.sprite.up,
    pygame.K_s: p1.sprite.down,
    pygame.K_a: p1.sprite.left,
    pygame.K_d: p1.sprite.right,
    pygame.K_UP: p1.sprite.up,
    pygame.K_DOWN: p1.sprite.down,
    pygame.K_LEFT: p1.sprite.left,
    pygame.K_RIGHT: p1.sprite.right
    }
    
    def populate(num, FREQ): # Projectile population (check pseudocode)
        global ticker
        ticker += 1
        if ticker >= FREQ:
            for _ in range(num):
                projectiles.add(Projectile(random.randint(0, WIDTH), 0, random.uniform(-.5, .5), 1))
            ticker = 0

    def processInput(controlMap):
        pressed = pygame.key.get_pressed() # CANT PRESS MULTIPLE KEYS ASDDSASDASF <- (angry comment translation: pygame keyboard I/O interpreter has a limit of active keypress registrations at once, probably for cross compat, this restricts some movement)
        for control in controlMap.keys():
            if pressed[control]:
                controlMap.get(control)()
    
    def clamp(minimum, x, maximum):
        return max(minimum, min(x, maximum))




def main(): # Main runtime
    HISCORE = syncHS()

    quit_flag = False
    while not quit_flag:
        CLOCK.tick(FPS)
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_flag = True
                pygame.quit()
                # Escapes the While True: loop in the (actual main) main runtime (bottom of file)
                exit()


        processInput(controls)

        # Fills screen to black
        SCREEN.fill(BLACK)

        # Difficulty scaling logic, check config & Data dict
        populate(1, clamp(END_FREQ, START_FREQ-(int(score/150)), START_FREQ)) 

        # Update methods assumed to run every tick/frame
        p1.update()
        projectiles.update()

        # Same logic as from syncHS() without opening & closing a file.... every frame
        if score > HISCORE: HISCORE = score

        # Stop game if player dies (not present in p1)
        if len(p1.sprites()) == 0:
            quit_flag = True

        projectiles.draw(SCREEN)
        p1.draw(SCREEN)

        scoreCounter = FONT.render(f'Score: {score}', True, BLUE)
        hScoreCounter = FONT.render(f'HI-Score: {str(HISCORE)}', True, GREEN)
        SCREEN.blit(scoreCounter, (20, 30))
        SCREEN.blit(hScoreCounter, (19, 10))

        # Update the display
        pygame.display.flip()
    HISCORE = syncHS(score)
    # testCase(score, HISCORE)



if __name__ == "__main__":
    # Check comment @ main() event handling
    while True:
        init()
        main()
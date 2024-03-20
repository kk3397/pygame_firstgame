import pygame

pygame.init()
window = pygame.display.set_mode((500, 500))
pygame.display.set_caption("First Game")

# This goes outside the while loop, near the top of the program
# sets animation to walk left and right as well as the idle animation and background
walkRight = [pygame.image.load('R1.png'), pygame.image.load('R2.png'), pygame.image.load('R3.png'),
             pygame.image.load('R4.png'), pygame.image.load('R5.png'), pygame.image.load('R6.png'),
             pygame.image.load('R7.png'), pygame.image.load('R8.png'), pygame.image.load('R9.png')]
walkLeft = [pygame.image.load('L1.png'), pygame.image.load('L2.png'), pygame.image.load('L3.png'),
            pygame.image.load('L4.png'), pygame.image.load('L5.png'), pygame.image.load('L6.png'),
            pygame.image.load('L7.png'), pygame.image.load('L8.png'), pygame.image.load('L9.png')]
bg = pygame.image.load('bg.jpg')
char = pygame.image.load('standing.png')

clock = pygame.time.Clock()


# Constructor class for the player with all attributes
class player(object):
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 5
        self.isJump = False
        self.left = False
        self.right = False
        self.walkCount = 0
        self.jumpCount = 10
        self.standing = True

    # draw function
    def draw(self, window):
        if self.walkCount + 1 >= 27:
            self.walkCount = 0
        if not (self.standing):
            if self.left:
                window.blit(walkLeft[self.walkCount // 3], (self.x, self.y))
                self.walkCount += 1
            elif self.right:
                window.blit(walkRight[self.walkCount // 3], (self.x, self.y))
                self.walkCount += 1
        else:
            if self.right:
                window.blit(walkRight[0], (self.x, self.y))
            else:
                window.blit(walkLeft[0], (self.x, self.y))


class projectile(object):
    def __init__(self, x, y, radius, color, facing):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.facing = facing
        self.vel = 8 * facing

    def draw(self, window):
        pygame.draw.circle(window, self.color, (self.x, self.y), self.radius)


# update function to update the character
def redrawGameWindow():
    window.blit(bg, (0, 0))
    man.draw(window)
    for bullet in bullets:
        bullet.draw(window)

    pygame.display.update()


man = player(200, 410, 64, 64)
bullets = []

run = True

while run:
    # set fps to 27
    clock.tick(27)
    pygame.time.delay(100)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT] and man.x > man.vel:
        man.x -= man.vel
        man.left = True
        man.right = False
        man.standing = False

    elif keys[pygame.K_RIGHT] and man.x < 500 - man.width - man.vel:
        man.x += man.vel
        man.left = False
        man.right = True
        man.standing = False
    elif keys[pygame.K_SPACE]:
        if man.left:
            facing = -1
        else:
            facing = 1
        if len(bullets) < 5:
            bullets.append(projectile(round(man.x + man.width//2) , round(man.y + man.height // 2), 6, (0, 0, 0),
            facing))
    else:

        man.standing = True
        man.walkCount = 0
    if not (man.isJump):
        if keys[pygame.K_UP]:
            man.isJump = True
            man.left = False
            man.right = False
            man.walkCount = 0
    else:
        if man.jumpCount >= -10:
            man.neg = 1
            if man.jumpCount < 0:
                man.neg = -1
            man.y -= (man.jumpCount ** 2) * 0.5 * man.neg
            man.jumpCount -= 1
        else:
            man.jumpCount = 10
            man.isJump = False
    for bullet in bullets:
        if bullet.x > 0 and bullet.x < 500:
            bullet.x += bullet.vel  # shoots bullets left or right with the speed velocity
        else:
            bullets.pop(bullets.index(bullet))  # erases the bullet when offscreen

    redrawGameWindow()

pygame.quit()

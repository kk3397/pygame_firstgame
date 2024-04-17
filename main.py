import asyncio
import random

import pygame

pygame.init()
window = pygame.display.set_mode((500, 480))
pygame.display.set_caption("First Game")
timer = pygame.time.get_ticks()

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


# bulletSound = pygame.mixer.Sound('bullet.mp3')
# hitSound = pygame.mixer.Sound('hit.mp3')

# bgm = pygame.mixer.music.load('music.mp3')
# pygame.mixer.music.play(-1)  ##keeps the bgm on loop


async def main():
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
            self.health = 100
            self.standing = True
            self.visible = True
            self.hitbox = (self.x + 17, self.y + 11, 29, 52)
            self.gameover=False


        # draw function
        def draw(self, window):
            if self.visible:
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
                # pygame.draw.rect(window, (255, 0, 0), (self.hitbox[0], self.hitbox[1] - 20, 50, 10))  # NEW
                # pygame.draw.rect(window, (0, 128, 0),
                #                  (self.hitbox[0], self.hitbox[1] - 20, 50 - (10  * (50 - self.health)), 10))  # NEW
                self.hitbox = (self.x + 17, self.y + 11, 29, 52)  # redraw hitbox everytime player gets hit
                # draw the hitbox around the player
            #     pygame.draw.rect(window, (255, 0, 0), self.hitbox, 1    )
            else:
                isDead()
                game_over = True

        def hit(self):
            if self.health > 0:
                # hitSound.play()
                self.health -= 1
            if self.health==0:
                self.visible = False
                self.gameover=True




    class enemy(object):
        # set walking animations for the enemy
        walkRight = [pygame.image.load('R1E.png'), pygame.image.load('R2E.png'), pygame.image.load('R3E.png'),
                     pygame.image.load('R4E.png'), pygame.image.load('R5E.png'), pygame.image.load('R6E.png'),
                     pygame.image.load('R7E.png'), pygame.image.load('R8E.png'), pygame.image.load('R9E.png'),
                     pygame.image.load('R10E.png'), pygame.image.load('R11E.png')]
        walkLeft = [pygame.image.load('L1E.png'), pygame.image.load('L2E.png'), pygame.image.load('L3E.png'),
                    pygame.image.load('L4E.png'), pygame.image.load('L5E.png'), pygame.image.load('L6E.png'),
                    pygame.image.load('L7E.png'), pygame.image.load('L8E.png'), pygame.image.load('L9E.png'),
                    pygame.image.load('L10E.png'), pygame.image.load('L11E.png')]

        def __init__(self, x, y, width, height, end):
            self.x = x
            self.y = y
            self.width = width
            self.height = height
            self.path = [x, end]  # determine walk path of enemy
            self.walkCount = 0
            self.vel = 3
            self.health = 10
            self.hitbox = (self.x + 17, self.y + 2, 31, 57)
            self.visible = True

        def draw(self, window):
            self.move()
            if self.visible:
                if self.walkCount + 1 >= 33:
                    self.walkCount = 0

                if self.vel > 0:  # If we are moving to the right we will display our walkRight images
                    window.blit(self.walkRight[self.walkCount // 3], (self.x, self.y))
                    self.walkCount += 1
                else:  # Otherwise we will display the walkLeft images
                    window.blit(self.walkLeft[self.walkCount // 3], (self.x, self.y))
                    self.walkCount += 1
                pygame.draw.rect(window, (255, 0, 0), (self.hitbox[0], self.hitbox[1] - 20, 50, 10))  # NEW
                pygame.draw.rect(window, (0, 128, 0),
                                 (self.hitbox[0], self.hitbox[1] - 20, 50 - (5 * (10 - self.health)), 10))  # NEW
                self.hitbox = (self.x + 17, self.y + 2, 31, 57)  # redraw hitbox everytime player gets hit
                # draw the hitbox around the enemy
            # pygame.draw.rect(window, (255, 0, 0), self.hitbox, 2)

        def move(self):
            if self.vel > 0:
                if self.x < self.path[1] + self.vel:
                    self.x += self.vel
                else:
                    self.vel *= -1
                    self.x += self.vel
                    self.walkCount = 0
            else:
                if self.x > self.path[0] - self.vel:
                    self.x += self.vel
                else:
                    self.vel *= -1
                    self.x += self.vel
                    self.walkCount = 0

        def hit(self):
            if self.health > 0:
                # hitSound.play()
                self.health -= 1
            else:
                self.visible = False
            # print('hit')

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

    def isDead():
            global game_over
            gameOverText = fontSmall.render("GAMEOVER! Press R to Restart", 1, (0, 0, 0))
            window.blit(gameOverText, (100, 240))


    def redrawGameWindow():
        window.blit(bg, (0, 0))
        scoreText = font.render("Score:" + str(score), 1, (0, 0, 0))
        window.blit(scoreText, (370, 10))

        playerHealthText = fontSmall.render("Health:" + str(man.health), 1, (0, 0, 0))
        window.blit(playerHealthText, (30, 10))

        man.draw(window)
        for goblin in goblins:
            goblin.draw(window)
        for bullet in bullets:
            bullet.draw(window)

        pygame.display.update()

    man = player(200, 410, 64, 64)
    bullets = []
    shootRange = 0
    score = 0

    # Timer event constants
    SPAWN_ENEMY_EVENT = pygame.USEREVENT + 1
    ENEMY_SPAWN_INTERVAL = 5000  # milliseconds (2 seconds)

    goblins = []
    pygame.time.set_timer(SPAWN_ENEMY_EVENT, ENEMY_SPAWN_INTERVAL)
    goblin_num = 2

    font = pygame.font.SysFont('comicsans', 30, True)
    fontSmall = pygame.font.SysFont('comicsans', 15, True)

    run = True


    while run:
        # set fps to 27
        clock.tick(27)
        for goblin in goblins:
            if man.hitbox[1] < goblin.hitbox[1] + goblin.hitbox[3] and man.hitbox[1] + man.hitbox[3] > goblin.hitbox[
                1]:  # Checks x coords
                if man.hitbox[0] + man.hitbox[2] > goblin.hitbox[0] and man.hitbox[0] < goblin.hitbox[0] + \
                        goblin.hitbox[
                            2]:  # Checks y coords
                    if man.visible == True:
                        man.hit()

        if shootRange > 0:
            shootRange += 1
        if shootRange > 3:
            shootRange = 0

        pygame.time.delay(100)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == SPAWN_ENEMY_EVENT:  # spawn system
                if len(goblins) < goblin_num:
                    new_goblin = enemy((random.randrange(20, 400)), 410, 64, 64, 450)
                    goblins.append(new_goblin)
                    print(len(goblins))

        keys = pygame.key.get_pressed()
        # all key functunality
        if man.visible:
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

            elif keys[pygame.K_SPACE] and shootRange == 0:
                # bulletSound.play()
                if man.left:
                    facing = -1
                else:
                    facing = 1
                if len(bullets) < 3:
                    bullets.append(
                        projectile(round(man.x + man.width // 2), round(man.y + man.height // 2), 6, (0, 0, 0), facing))
                shootRange = 1
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
        if keys[pygame.K_r] and man.gameover:
            man = player(200, 410, 64, 64)
            bullets = []
            shootRange = 0
            score = 0

            # Timer event constants
            SPAWN_ENEMY_EVENT = pygame.USEREVENT + 1
            ENEMY_SPAWN_INTERVAL = 5000  # milliseconds (2 seconds)

            goblins = []
            pygame.time.set_timer(SPAWN_ENEMY_EVENT, ENEMY_SPAWN_INTERVAL)
            goblin_num = 2
            game_over = False
        for bullet in bullets:
            for goblin in goblins:
                # checks bullet collision to hitbox
                if bullet.y - bullet.radius < goblin.hitbox[1] + goblin.hitbox[3] and bullet.y + bullet.radius > \
                        goblin.hitbox[
                            1]:  # Checks x coords
                    if bullet.x + bullet.radius > goblin.hitbox[0] and bullet.x - bullet.radius < goblin.hitbox[0] + \
                            goblin.hitbox[2]:  # Checks y coords
                        if goblin.visible == True:
                            goblin.hit()  # calls enemy hit method
                            bullets.pop(bullets.index(bullet))  # removes bullet from bullet list
                        else:
                            score += 5
                            goblins.pop(goblins.index(goblin))

            if bullet.x > 0 and bullet.x < 500:
                bullet.x += bullet.vel  # shoots bullets left or right with the speed velocity
            else:
                bullets.pop(bullets.index(bullet))  # erases the bullet when offscreen


        redrawGameWindow()
        await asyncio.sleep(0)


asyncio.run(main())

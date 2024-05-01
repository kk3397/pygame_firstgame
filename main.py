import asyncio
import random
import time

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

healthup = pygame.image.load("potion.png")
moreAmmo = pygame.image.load("ammo.png")
bulletSpeed = pygame.image.load("speedpotion.png")

bulletSound = pygame.mixer.Sound('bullet.ogg')
hitSound = pygame.mixer.Sound('hit.ogg')
hitSound.set_volume(0.3)

pygame.mixer.music.set_volume(0.3)
pygame.mixer.music.load('music.ogg')

pygame.mixer.music.play(-1)  # keeps the bgm on loop


async def main():
    # Constructor class for the player with all attributes
    class Player(object):
        def __init__(self, x, y, width, height):
            self.x = x
            self.y = y
            self.width = width
            self.height = height
            self.vel = 7
            self.isJump = False
            self.left = False
            self.right = False
            self.walkCount = 0
            self.jumpCount = 10
            self.health = 100
            self.bullets = 3
            self.standing = True
            self.visible = True
            self.hitbox = (self.x + 17, self.y + 11, 29, 52)
            self.gameover = False

        # draw function
        def draw(self, window):
            if self.visible:
                if self.walkCount + 1 >= 27:
                    self.walkCount = 0
                if not self.standing:
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
            else:
                isdead()

        def hit(self):
            if self.health > 0:
                # hitSound.play()
                self.health -= 1
            if self.health == 0:
                self.visible = False
                self.gameover = True

    class Enemy(object):
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
            self.vel = 4
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
                self.health -= 1
            else:
                self.visible = False
            # print('hit')

    class Projectile(object):
        def __init__(self, x, y, radius, color, facing):
            self.x = x
            self.y = y
            self.radius = radius
            self.color = color

            self.facing = facing
            self.vel = 7 * facing

        def draw(self, window):
            pygame.draw.circle(window, self.color, (self.x, self.y), self.radius)
        def increaseVelocity(self, bullets, new_speed):
            for bullet in bullets:
                bullet.vel = new_speed


    class Powerup(object):
        def __init__(self, x, y, color):
            self.x = x
            self.y = y
            self.color = color
            self.hitbox = (self.x + 17, self.y + 2, 31, 31)
            self.start_time=0
            self.visible = True

        def drawHealth(self, window):
            if self.visible:
                window.blit(healthup, (self.x, self.y))

                self.hitbox = (self.x + 3, self.y + 2, 30, 30)  # redraw hitbox everytime player gets hit
                # draw the hitbox around the player
            # pygame.draw.rect(window, (255, 0, 0), self.hitbox, 1    )

        def drawAmmo(self, window):
            if self.visible:
                window.blit(moreAmmo, (self.x, self.y))

                self.hitbox = (self.x + 1, self.y + 1, 28, 28)  # redraw hitbox everytime player gets hit
                # draw the hitbox around the player
            # pygame.draw.rect(window, (255, 0, 0), self.hitbox, 1 )

        def drawSpeed(self, window):
            if self.visible:
                window.blit(bulletSpeed, (self.x, self.y))

                self.hitbox = (self.x + 1, self.y + 1, 28, 28)  # redraw hitbox everytime player gets hit
                # draw the hitbox around the player
            # pygame.draw.rect(window, (255, 0, 0), self.hitbox, 1 )

        def recover(self):
            if 0 < man.health < 100:
                man.health += 10
            if man.health > 100:
                man.health = 100

        def increase_bullet(self, duration, new_capacity):
            self.start_time=pygame.time.get_ticks()
            man.bullets += new_capacity
            time.sleep(duration)
            return man.bullets


    def isdead():
        global game_over
        gameOverText = fontSmall.render("GAMEOVER! Press R to Restart", 1, (0, 0, 0))
        window.blit(gameOverText, (100, 240))

    def redrawGameWindow():
        window.blit(bg, (0, 0))
        scoreText = font.render(str(score), 1, (0, 0, 0))
        window.blit(scoreText, (350, 10))

        playerHealthText = fontSmall.render("Health:" + str(man.health), 1, (0, 0, 0))
        window.blit(playerHealthText, (30, 10))

        man.draw(window)
        for goblin in goblins:
            goblin.draw(window)
        for bullet in bullets:
            bullet.draw(window)
        for potion in potions:
            potion.drawHealth(window)
        for ammos in ammo_item:
            ammos.drawAmmo(window)
        for speed in speed_potion:
            speed.drawSpeed(window)

        pygame.display.update()


    man = Player(200, 410, 64, 64)
    bullets = []
    global new_bullet
    shootRange = 0
    score = 0
    goblins = []
    goblin_num = 3

    potions = []
    potions_num = 1

    ammo_item = []
    ammo_num = 1

    speed_potion = []
    speed_potion_num = 1

    # Timer event constants

    SPAWN_ENEMY_EVENT = pygame.USEREVENT + 1
    ENEMY_SPAWN_INTERVAL = 5000  # milliseconds (5 seconds)
    pygame.time.set_timer(SPAWN_ENEMY_EVENT, ENEMY_SPAWN_INTERVAL)

    SPAWN_POTION_EVENT = pygame.USEREVENT + 2
    POTION_SPAWN_INTERVAL = 15000  # milliseconds (10 seconds)
    pygame.time.set_timer(SPAWN_POTION_EVENT, POTION_SPAWN_INTERVAL)

    SPAWN_AMMO_EVENT = pygame.USEREVENT + 3
    AMMO_SPAWN_INTERVAL = 35000  # milliseconds (2 seconds)
    pygame.time.set_timer(SPAWN_AMMO_EVENT, AMMO_SPAWN_INTERVAL)
    ammo_increase_interval = 7000
    ammo_timer_event = pygame.USEREVENT + 4

    SPAWN_SPEED_POTION_EVENT = pygame.USEREVENT + 5
    SPEED_POTION_SPAWN_INTERVAL = 30000  # milliseconds (2 seconds)
    pygame.time.set_timer(SPAWN_SPEED_POTION_EVENT, SPEED_POTION_SPAWN_INTERVAL)
    speed_potion_interval = 5000
    speed_potion_duration_timer = pygame.USEREVENT + 6

    font = pygame.font.SysFont('comicsans', 30, True)
    fontSmall = pygame.font.SysFont('comicsans', 15, True)

    run = True

    while run:
        # set fps to 27
        clock.tick(27)
        for health_potion in potions:
            if man.hitbox[1] < health_potion.hitbox[1] + health_potion.hitbox[3] and man.hitbox[1] + man.hitbox[3] > \
                    health_potion.hitbox[
                        1]:  # Checks x coords
                if man.hitbox[0] + man.hitbox[2] > health_potion.hitbox[0] and man.hitbox[0] < health_potion.hitbox[0] + \
                        health_potion.hitbox[
                            2]:  # Checks y coords
                    if man.visible:
                        health_potion.recover()

                        if health_potion in potions:
                            potions.remove(health_potion)
        for ammos in ammo_item:
            if man.hitbox[1] < ammos.hitbox[1] + ammos.hitbox[3] and man.hitbox[1] + man.hitbox[3] > \
                    ammos.hitbox[
                        1]:  # Checks x coords
                if man.hitbox[0] + man.hitbox[2] > ammos.hitbox[0] and man.hitbox[0] < ammos.hitbox[0] + \
                        ammos.hitbox[
                            2]:  # Checks y coords
                    if man.visible:
                        man.bullets =5
                        pygame.time.set_timer(ammo_timer_event, ammo_increase_interval, 1)

                    if ammos in ammo_item:
                            ammo_item.remove(ammos)


        for speed in speed_potion:
            if man.hitbox[1] < speed.hitbox[1] + speed.hitbox[3] and man.hitbox[1] + man.hitbox[3] > \
                    speed.hitbox[
                        1]:  # Checks x coords
                if man.hitbox[0] + man.hitbox[2] > speed.hitbox[0] and man.hitbox[0] < speed.hitbox[0] + \
                        speed.hitbox[
                            2]:  # Checks y coords
                    if man.visible:
                        for bullet in bullets:
                            bullet.increaseVelocity(bullets, 15)
                            print(bullet.vel)

                        pygame.time.set_timer(speed_potion_duration_timer, speed_potion_interval, 1)

                        if speed in speed_potion:
                                speed_potion.remove(speed)


        for goblin in goblins:
            if man.hitbox[1] < goblin.hitbox[1] + goblin.hitbox[3] and man.hitbox[1] + man.hitbox[3] > goblin.hitbox[
                1]:  # Checks x coords
                if man.hitbox[0] + man.hitbox[2] > goblin.hitbox[0] and man.hitbox[0] < goblin.hitbox[0] + \
                        goblin.hitbox[
                            2]:  # Checks y coords
                    if man.visible == True and goblin.visible == True:
                        hitSound.play()
                        man.hit()

        if shootRange > 0:
            shootRange += 1
        if shootRange >= 3:
            shootRange = 0

        pygame.time.delay(100)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            elif event.type == SPAWN_ENEMY_EVENT:  # spawn system
                if len(goblins) < goblin_num:
                    new_goblin = Enemy((random.randrange(20, 400)), 410, 64, 64, 450)
                    goblins.append(new_goblin)

            elif event.type == SPAWN_POTION_EVENT:  # spawn system
                if len(potions) < potions_num:
                    new_potion = Powerup((random.randrange(20, 350)), (random.randrange(240, 410)), (0, 0, 0))
                    potions.append(new_potion)

            elif event.type == SPAWN_AMMO_EVENT:  # spawn system
                if len(ammo_item) < ammo_num:
                    new_ammo = Powerup((random.randrange(20, 350)), (random.randrange(240, 410)), (0, 0, 0))
                    ammo_item.append(new_ammo)

            # elif event.type == SPAWN_SPEED_POTION_EVENT:  # spawn system
            #     if len(speed_potion) < speed_potion_num:
            #         # new_speed_potion = Powerup((random.randrange(20, 350)), (random.randrange(240, 410)), (0, 0, 0))
            #         # speed_potion.append(new_speed_potion)
            elif event.type == ammo_timer_event:
                man.bullets = 3
            elif event.type == speed_potion_duration_timer:
                for bullet in bullets:
                    bullet.increaseVelocity(bullets, 5)
                    print(bullet.vel)

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
                if man.left:
                    facing = -1
                else:
                    facing = 1
                if len(bullets) < man.bullets:

                    bullets.append(Projectile(round(man.x + man.width // 2), round(man.y + man.height // 2), 6, (0, 0, 0), facing))
                    bulletSound.play()

                shootRange = 0
            else:

                man.standing = True
                man.walkCount = 0

            if not man.isJump:
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
            man = Player(200, 410, 64, 64)
            bullets = []
            shootRange = 0
            score = 0
            goblins = []
            goblin_num = 2

            potions = []
            potions_num = 2

            ammo_item = []
            ammo_num = 1

            # Timer event constants

            SPAWN_ENEMY_EVENT = pygame.USEREVENT + 1
            ENEMY_SPAWN_INTERVAL = 5000  # milliseconds (5 seconds)`
            pygame.time.set_timer(SPAWN_ENEMY_EVENT, ENEMY_SPAWN_INTERVAL)

            SPAWN_POTION_EVENT = pygame.USEREVENT + 2
            POTION_SPAWN_INTERVAL = 10000  # milliseconds (10 seconds)
            pygame.time.set_timer(SPAWN_POTION_EVENT, POTION_SPAWN_INTERVAL)

            SPAWN_AMMO_EVENT = pygame.USEREVENT + 3
            AMMO_SPAWN_INTERVAL = 20000  # milliseconds (2 seconds)
            pygame.time.set_timer(SPAWN_AMMO_EVENT, AMMO_SPAWN_INTERVAL)

            ammo_increase_interval = 5000
            ammo_timer_event = pygame.USEREVENT + 4

            game_over = False
        for bullet in bullets:
            for goblin in goblins:
                # checks bullet collision to hitbox
                if bullet.y - bullet.radius < goblin.hitbox[1] + goblin.hitbox[3] and bullet.y + bullet.radius > \
                        goblin.hitbox[
                            1]:  # Checks x coords
                    if bullet.x + bullet.radius > goblin.hitbox[0] and bullet.x - bullet.radius < goblin.hitbox[0] + \
                            goblin.hitbox[2]:  # Checks y coords
                        if goblin.visible:
                            goblin.hit()  # calls enemy hit method
                            if bullet in bullets:
                                bullets.remove(bullet)
                        else:
                            score += 5
                            if goblin in goblins:
                                goblins.remove(goblin)

            if 0 < bullet.x < 500:
                bullet.x += bullet.vel  # shoots bullets left or right with the speed velocity
            else:
                if bullet in bullets:
                    bullets.remove(bullet)  # erases the bullet when offscreen

        redrawGameWindow()
        await asyncio.sleep(0)

asyncio.run(main())

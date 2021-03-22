import pygame
import os

class Enemy:
    
    def __init__(self, x, y):
        self.IMG = IMGS[2]
        self.x = x
        self.y = y
    
    def move(self, x, y):
        if self.x + x > PADDING:
            if (self.x+self.IMG.get_width()) + x < SIZE[0] - PADDING:
                self.x += x
        
        if self.y + y > PADDING:
            if (self.y+self.IMG.get_height()) + y < SIZE[1] - PADDING:
                self.y += y
    
    def draw(self, win):
        win.blit(self.IMG, (self.x, self.y))


class Player:
    
    def __init__(self, x, y):
        self.IMG = IMGS[0]
        self.x = x
        self.y = y
    
    
    def move(self, x, y=0):
        if self.x + x > PADDING:
            if (self.x+self.IMG.get_width()) + x < SIZE[0] - PADDING:
                self.x += x
        
        if self.y + y > PADDING:
            if (self.y+self.IMG.get_height()) + y < SIZE[1] - PADDING:
                self.y += y

                
    def draw(self, win):
        win.blit(self.IMG, (self.x, self.y))


class Bullet:
    
    def __init__(self, x, y):
        self.IMG = IMGS[1]
        self.x = x
        self.y = y
        self.step = 5
    
    def move(self):
        if self.y - self.step > -(self.IMG.get_height() + 5):
            self.y -= self.step
            return None
        
        else:
            return True
    
    def draw(self, win):
        win.blit(self.IMG, (self.x, self.y))


def collide(bullet, enemy):
    
    colishion = False

    bulletPos = [bullet.x, bullet.y]
    enemyPos = [enemy.x+PADDING, enemy.y]  
    enemyPos.append(enemyPos[1] + pygame.mask.from_surface(enemy.IMG).get_size()[1] - 10)
    enemyPos.append(enemyPos[0] + pygame.mask.from_surface(enemy.IMG).get_size()[0] - 20)
    # enemyPos[1] += int(enemy.IMG.get_height()/2)

    if enemyPos[0] < bulletPos[0] < enemyPos[3]:
        if enemyPos[1] < bulletPos[1] < enemyPos[2]:
            # print(1, bulletPos, enemyPos)
            colishion = True

    bulletPos[0] += bullet.IMG.get_width() 

    if colishion is False:
        if enemyPos[0] < bulletPos[0] < enemyPos[3]:
            if enemyPos[1] < bulletPos[1] < enemyPos[2]:
                # print(2, bulletPos, enemyPos)
                colishion = True
    

    return colishion

def drawWindow(win, player, bullets, enemys):

    # Draw background
    win.fill((255, 0, 0))
    win.blit(IMGS[-1], (0, 0))

    # Draw our player
    player.draw(win)

    # If we have enemys then we draw them
    if len(enemys) != 0:
        for enemy in enemys:
            enemy.draw(win)

    # If we have bullets then we will draw them
    if len(bullets) != 0:
        for bullet in bullets:
            bullet.draw(win)

    # Refresh the screen
    pygame.display.update()

path = __file__.split("\\")[:-1]

end = ""
path[0] = path[0].upper()
path[0] += "\\"
for item in path:
    print(f"end: {end}, item: {item}")
    end = os.path.join(end, item)

print(f"Final path: '{end}'")
path = str(end)


IMGS = [
    pygame.image.load(os.path.join(path, "player.png")),
    pygame.image.load(os.path.join(path, "bullet.png")),
    pygame.image.load(os.path.join(path, "enemy.png")),
    pygame.image.load(os.path.join(path, "background.png"))
]


SIZE = (800, 600)
WIN = pygame.display.set_mode(SIZE)
PADDING = 10
FPS = 60
PlayerStep = 5
BulletDelay = 300


def main():

    prevTime = -float("inf")

    enemys = [Enemy(
        int(SIZE[0]/2),
        int(SIZE[1]/2)
    )]

    bullets = []

    player = Player(
        int((SIZE[0] - PADDING*2)/2), 
        ((SIZE[1]-PADDING) - IMGS[0].get_height())
    )

    right = False
    left = False
    shoot = False

    clock = pygame.time.Clock()

    run = True
    while run:
        clock.tick(FPS)


        # For each event in pygame
        for event in pygame.event.get():

            # If the X button is pressed quit
            if event.type == pygame.QUIT:
                run = False
            

            # If a key is pressed
            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_d:
                    right = True
                
                if event.key == pygame.K_a:
                    left = True
            
                if event.key == pygame.K_SPACE:
                    shoot = True
            


            # If a key is released
            if event.type == pygame.KEYUP:

                if event.key == pygame.K_d:
                    right = False
                
                if event.key == pygame.K_a:
                    left = False
                
                if event.key == pygame.K_SPACE:
                    shoot = False



        # Player movement
        if True:
            if right is True:
                player.move(PlayerStep)

            if left is True:
                player.move(-PlayerStep)

        # If player wants to shoot. 
        if shoot is True:
            currentTime = pygame.time.get_ticks()
            if currentTime - prevTime > BulletDelay:
                prevTime = pygame.time.get_ticks()
                PlayerX = player.x + int(player.IMG.get_width()/4)
                PlayerY = player.y - int(IMGS[-2].get_height()/2)
                bullets.append(Bullet(PlayerX, PlayerY))
                # print((PlayerX, PlayerY))
                # shoot = False



        # Bullet movement
        if True:
            if len(bullets) != 0:
                removeIndexs = []
                for pos, bullet in enumerate(bullets):
                    result = bullet.move()
                    if result is not None:
                        removeIndexs.append(pos)
                
                if len(removeIndexs) != 0:
                    for pos in removeIndexs:
                        bullets.pop(pos)
                        

        if len(bullets) != 0:
            delPosBullet = []
            delPosEnemy = []

            for bPos, bullet in enumerate(bullets):
                for ePos, enemy in enumerate(enemys):
                    result = collide(bullet, enemy)
                    if result is True:
                        delPosBullet.append(bPos)
                        delPosEnemy.append(ePos)
            
            if len(delPosBullet) != 0:
                for pos in delPosBullet:
                    bullets.pop(pos)
            
            if len(delPosEnemy) != 0:
                for pos in delPosEnemy:
                    enemys.pop(pos)

        # Enemy movement
        if True:
            pass

        # Fill the screen with
        # this color \/ 
        WIN.blit(IMGS[-1], (0, 0))

        # Draw the window
        drawWindow(WIN, player, bullets, enemys)
    

    pygame.display.quit()


main()


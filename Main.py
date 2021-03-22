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


def collide(object1, object2):
    MASK1 = pygame.mask.from_surface(object1.IMG)
    MASK2 = pygame.mask.from_surface(object2.IMG)

    OBJ1RECT = MASK1.get_rect()
    OBJ2RECT = MASK2.get_rect()

    offset1_x = OBJ1RECT.x - OBJ2RECT.x
    offset1_y = OBJ1RECT.y - OBJ2RECT.y

    overlap1 = MASK2.overlap(MASK1, (offset1_x, offset1_y))

    offset2_x = OBJ2RECT.x - OBJ1RECT.x
    offset2_y = OBJ2RECT.y - OBJ1RECT.y

    overlap2 = MASK1.overlap(MASK2, (offset2_x, offset2_y))
    print(overlap2)

    # If our two objects overlap then return True else False
    if overlap1 and overlap2:
        print("True", overlap1, overlap2)
        return False

    else:
        # print("False")
        return False

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
PlayerStep = 10

def main():
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
                    result = collide(enemy, bullet)
                    # print(result)
                    if result is True:
                        delPosBullet.append(bPos)
                        delPosEnemy.append(ePos)
            
            if len(delPosBullet) != 0:
                for pos in delPosBullet:
                    del bullets[pos]
            
            if len(delPosEnemy) != 0:
                for pos in delPosEnemy:
                    del delPosEnemy[pos]


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


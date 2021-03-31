import pygame
import random
import os

class Enemy:
    
    # Initalize a class of Enemy
    def __init__(self, x, y):
        # Setup enemy image and other 
        # vairables
        self.IMG = IMGS[2]
        self.x = x
        self.y = y
        self.right = True
        self.left = False
    
    # Check to see if enemy touchs the 
    # side of the screen return
    # False if it is not touching 
    # the side and retrun True if it is
    def touchWall(self):
        x = EnemyStep

        if (self.x+self.IMG.get_width()) + x < SIZE[0] - PADDING and self.right is True:
            return False
        
        elif self.x - x > PADDING and self.left is True:
            return False

        else:
            return True

    # Move the enemy on the x axis the 
    # main program deals with the y axis
    def move(self):
        x = EnemyStep
        
        if (self.x+self.IMG.get_width()) + x < SIZE[0] - PADDING and self.right is True:
            self.x += x
        
        elif self.x - x > PADDING and self.left is True:
            self.x -= x
        
    # Draw the enemy to screen
    def draw(self, win):
        win.blit(self.IMG, (self.x, self.y))


class Player:
    
    # Initalize a class of Player
    def __init__(self, x, y):
        # Set up the players image 
        # and other vairables
        self.IMG = IMGS[0]
        self.x = x
        self.y = y
        self.health = 100
        self.maxHealth = 100
    
    # Moves the player from left to 
    # the right and checks to see 
    # if the move is possible
    def move(self, x, y=0):
        if self.x + x > PADDING:
            if (self.x+self.IMG.get_width()) + x < SIZE[0] - PADDING:
                self.x += x
        
        if self.y + y > PADDING:
            if (self.y+self.IMG.get_height()) + y < SIZE[1] - PADDING:
                self.y += y

    # Draw the player
    def draw(self, win):
        win.blit(self.IMG, (self.x, self.y))


class Bullet:
    
    # Initalize a class of Bullet
    def __init__(self, x, y):
        # Setup the image for the 
        # bullet and other vairables
        self.IMG = IMGS[1]
        self.x = x
        self.y = y
        self.step = BulletMove
    
    # Move the bullet and check if it 
    # hits the top of the screen if so 
    # return True if it can move return None
    def move(self):
        if self.y - self.step > -(self.IMG.get_height() + 5):
            self.y -= self.step
            return None
        
        else:
            return True
    
    # Draw the bullet
    def draw(self, win):
        win.blit(self.IMG, (self.x, self.y))


class Button():
    def __init__(self, color, x, y, width, height, text='', function=None, args=None):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.function = function
        self.args = args

    def draw(self,  win, outline=None):
        #Call this method to draw the button on the screen
        if outline:
            pygame.draw.rect(win, outline, (self.x-2,self.y-2,self.width+4,self.height+4),0)
            
        pygame.draw.rect(win, self.color, (self.x,self.y,self.width,self.height),0)
        
        if self.text != '':
            font = pygame.font.SysFont('comicsans', 30)
            text = font.render(self.text, 1, (0,0,0))
            win.blit(text, (self.x + (self.width/2 - text.get_width()/2), self.y + (self.height/2 - text.get_height()/2)))

    def isOver(self, pos):
        #Pos is the mouse position or a tuple of (x,y) coordinates
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True
            
        return False


def makeRandomWave(enemys, maxNum):
    num = maxNum*10
    minNum = (pygame.mask.from_surface(enemys[-1].IMG).get_size()[1]*3) + (SPACING)
    yPos = random.randint(-num, -minNum)
    newEnemys = spawnEnemys(y=yPos)
    return newEnemys
    

# Check to see if the enemys have been 
# defeated or if they have reached the 
# bottom. If there are no more enemys 
# then return False if there are enemys 
# and at least one has passed the bottom 
# of the screen then return True. If none 
# of these are true then return None
def checkLost(enemys):
    if len(enemys) == 0:
        return False

    else:
        for enemy in enemys:
            if enemy.y + pygame.mask.from_surface(enemy.IMG).get_size()[1] >= SIZE[1] - PADDING:
                return True
    
    return 


# Check to see if there is a collishion 
# between a bullet and an enemy. If there 
# is one then return True if there is no 
# collishion retrun False
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


# Draw the window with everything on it
def drawWindow(win, player, bullets, enemys, end=False):

    # Draw background
    win.fill((255, 0, 0))
    win.blit(IMGS[-1], (0, 0))

    # If we have enemys then we draw them
    if len(enemys) != 0:
        for enemy in enemys:
            if enemy.y > 0:
                enemy.draw(win)

    # If we have bullets then we will draw them
    if len(bullets) != 0:
        for bullet in bullets:
            bullet.draw(win)
    
    # Draw our player
    player.draw(win)

    # Draw the health bar at the top right
    startX = (SIZE[0] - PADDING) - (player.maxHealth)*2
    endX = (SIZE[0] - PADDING) - (player.maxHealth*2 - player.health*2)
    Y = 10

    if player.health <= 0:
        endX = startX + 2

    color = (0, 255, 0)
    if 40 <= player.health <= 70:
        color = (255, 255, 0)
    elif player.health <= 40:
        color = (255, 0, 0)


    pygame.draw.line(win, color, (startX, Y), (endX, Y), 10)

    if end is False:
        # Refresh the screen
        pygame.display.update()


# Draw the end game window. The text 
# depends if they have lost or won
def drawEndGame(win, lost):
    pygame.font.init()

    font = pygame.font.SysFont("comicsans", 60)
    LostText = font.render("You lost!", 1, (255, 255, 255))
    WonText = font.render("Congrats you won!", 1, (255, 255, 255))

    if lost is True:
        win.blit(
            LostText, 
            (
                int(SIZE[0]/2) - int(LostText.get_width()/2),
                int(SIZE[1]/2) - int(LostText.get_height()/2)
            )
        )
    
    else:
        win.blit(
            WonText, 
            (
                int(SIZE[0]/2) - int(WonText.get_width()/2),
                int(SIZE[1]/2) - int(WonText.get_height()/2)
            )
        )

    pygame.display.update()


# Initalize a list of enemys in a 
# grid shape to begin with
def spawnEnemys(ROWS=3, y=0):
    if y == 0:
        y = PADDING

    enemys = []
    enemyImage = IMGS[-2]
    enemyMASK = pygame.mask.from_surface(enemyImage)
    enemySIZE = enemyMASK.get_size()

    COLS = int((SIZE[0]-PADDING*2) / ((enemySIZE[0]) + SPACING))

    x = PADDING + SPACING

    for _ in range(ROWS):
        for _ in range(COLS-2):
            enemys.append(
                Enemy(
                    x,
                    y
                )
            )
            
            x += (enemySIZE[0]) + SPACING
        
        x = PADDING + SPACING
        y += (enemySIZE[1]) + SPACING
    

    return enemys
        

# Get the path for this file
if True:
    path = __file__.split("\\")[:-1]

    end = ""
    path[0] = path[0].upper()
    path[0] += "\\"
    for item in path:
        print(f"end: {end}, item: {item}")
        end = os.path.join(end, item)

    print(f"Final path: '{end}'")
    path = str(end)


# Setup the images list
IMGS = [
    pygame.image.load(os.path.join(path, "player.png")),
    pygame.image.load(os.path.join(path, "bullet.png")),
    pygame.image.load(os.path.join(path, "enemy.png")),
    pygame.image.load(os.path.join(path, "background.png"))
]


# Setup global vairables
SIZE = (800, 600)
WIN = pygame.display.set_mode(SIZE)
SPACING = 10
PADDING = 10 # Padding on all sides
FPS = 30 # Frames per second
PlayerStep = 8 # Pixels per move
EnemyStep = 2 # Pixels per move
BulletMove = 5 # Pixels per move
BulletDelay = 300 # Ms
dmgPerEnemy = 10 # Damage per enemy


def main():
    global EnemyStep
    pygame.font.init()

    buttons = []
    space = 40
    x = int(SIZE[0]/2) - (150+space)
    y = int(SIZE[1]/2) - 20
    clock = pygame.time.Clock()
    

    for i in range(3):
        if i == 0:
            text = "Easy"
        elif i == 1:
            text = "Medium"
        elif i == 2:
            text = "Hard"
        buttons.append(
            Button(
                (255, 255, 255),
                x,
                y,
                100,
                40,
                text

            )
        )

        x += 100+space

    run = True
    while run:
        clock.tick(FPS)

        # For each event in pygame do
        for event in pygame.event.get():

            # If the event is quit then exit
            if event.type == pygame.QUIT:
                quit()
            
            # If the event is a mouse button down then
            if event.type == pygame.MOUSEBUTTONDOWN:

                # Get the mouse position
                mousePos = pygame.mouse.get_pos()

                # For each button in buttons
                for button in buttons:

                    # if the button is clicked then
                    if button.isOver(mousePos):
                        
                        # Check to see what the text is 
                        # then change the diffuculty based 
                        # on that.
                        if button.text.upper() == "EASY":
                            Difficulty = 1

                        elif button.text.upper() == "MEDIUM":
                            Difficulty = 2
                            EnemyStep += 1

                        elif button.text.upper() == "HARD":
                            Difficulty = 3
                            EnemyStep += 1 
                        
                        # Set run to false to exit 
                        # the running loop.
                        run = False
        
        # For each button in buttons 
        # draw the button.
        for button in buttons:
            button.draw(WIN)

        # Update the display
        pygame.display.update()
    
    # Player vairables
    player = Player(
        int((SIZE[0] - PADDING*2)/2), 
        ((SIZE[1]-PADDING) - IMGS[0].get_height())
    )

    right = False
    left = False
    shoot = False
    GameOver = False
    lost = False


    # Enemy vairables
    enemys = spawnEnemys()

    EnemyDown = False
    Amount = 0


    # Bullet vairables
    bullets = []

    prevTime = -float("inf")


    # Get a clock to set the FPS
    clock = pygame.time.Clock()

    run = True
    while run:

        # Run at the game at FPS frames per second
        clock.tick(FPS)

        # For each event in pygame
        for event in pygame.event.get():

            # If the X button is pressed quit
            if event.type == pygame.QUIT:
                run = False


            # If a key is pressed
            if event.type == pygame.KEYDOWN:

                # If the D key is pressed
                if event.key == pygame.K_d:
                    right = True

                # If the A key is pressed
                if event.key == pygame.K_a:
                    left = True

                # If the SPACE BAR is pressed
                if event.key == pygame.K_SPACE:
                    shoot = True



            # If a key is released
            if event.type == pygame.KEYUP:

                # If the D key is pressed
                if event.key == pygame.K_d:
                    right = False

                # If the A key is pressed
                if event.key == pygame.K_a:
                    left = False

                # If the SPACE BAR is pressed
                if event.key == pygame.K_SPACE:
                    shoot = False

        # If the game is not over
        if GameOver is False:

            # Player movement
            if True:

                # If the user wats to move 
                # right then move right
                if right is True:
                    player.move(PlayerStep)

                # If the player wants to move 
                # left then move left
                if left is True:
                    player.move(-PlayerStep)

            # If player wants to shoot. 
            if shoot is True:
                # Get the current time in mili seconds
                currentTime = pygame.time.get_ticks()

                # If the time passed from the last bullet 
                # fired is greater than BulletDelay then
                if currentTime - prevTime >= BulletDelay:
                    prevTime = pygame.time.get_ticks()

                    # Get the player x and y then make a bullet
                    PlayerX = player.x + int(player.IMG.get_width()/4)
                    PlayerY = (player.y - int(IMGS[-2].get_height()/4)) + 20
                    bullets.append(
                        Bullet(PlayerX, PlayerY)
                    )

            # Bullet movement
            if True:
                # If there are bullets to move.
                if len(bullets) != 0:
                    removeIndexs = []

                    # Move the bullet
                    for pos, bullet in enumerate(bullets):
                        result = bullet.move()
                        if result is not None:
                            removeIndexs.append(pos)

                    # If the bullet hit the top of 
                    # the screen delete it
                    if len(removeIndexs) != 0:
                        for pos in removeIndexs:
                            bullets.pop(pos)

            # Check if bullet collided with enemy or wall
            if len(bullets) != 0:
                delPosBullet = []
                delPosEnemy = []

                # Check to see if colishion happens
                for bPos, bullet in enumerate(bullets):
                    for ePos, enemy in enumerate(enemys):
                        result = collide(bullet, enemy)
                        if result is True:
                            delPosBullet.append(bPos)
                            delPosEnemy.append(ePos)

                # Removing the bullet and the enemy
                if len(delPosBullet) != 0:
                    for pos in delPosBullet:
                        try:
                            bullets.pop(pos)
                        except:

                            try:
                                bullets.pop(pos-1)
                            except:

                                try:
                                    bullets.pop(pos+1)
                                except:
                                    pass

                if len(delPosEnemy) != 0:
                    for pos in delPosEnemy:
                        try:
                            enemys.pop(pos)
                        except:

                            try:
                                enemys.pop(pos-1)
                            except:

                                try:
                                    enemys.pop(pos+1)
                                except:
                                    pass

            # Enemy movement
            if True:
                for enemy in enemys:
                    downTF = enemy.touchWall()

                    if downTF is True:
                        EnemyDown = True

                for enemy in enemys:
                    enemy.move()

                    if EnemyDown:
                        enemy.y += int(pygame.mask.from_surface(enemy.IMG).get_size()[0] + SPACING)

                        if enemy.right is True:
                            enemy.left = True
                            enemy.right = False

                        elif enemy.left is True:
                            enemy.left = False
                            enemy.right = True

                EnemyDown = False

                if len(enemys) != 0:
                    Length = pygame.mask.from_surface(enemys[-1].IMG).get_size()[1]*3
                    if enemys[-1].y >= Length:
                        if Amount != Difficulty:
                            newEnemys = makeRandomWave(enemys, 30)
                            for enemy in newEnemys:
                                enemys.append(enemy)
                            Amount += 1
                
                for enemy in enemys:
                    if enemy.y + pygame.mask.from_surface(enemy.IMG).get_size()[1] >= SIZE[1] - PADDING:
                        player.health -= dmgPerEnemy
                        enemy.y = -1000
                        enemys.remove(enemy)



            # Check to see if end of game!
            gameCondition = None
            if player.health > 0:
                if len(enemys) <= 0:
                    gameCondition = False
            else:
                gameCondition = True


            if gameCondition != None:
                GameOver = True
                # print("Game over!", gameCondition)

                if gameCondition == True:
                    lost = True

                else:
                    won = True


            # Fill the screen with
            # this IMG  \/  here \/
            WIN.blit(IMGS[-1], (0, 0))

            # Draw the window
            drawWindow(WIN, player, bullets, enemys)

        # If the game is over then
        else:

            # Move the enemys
            if len(enemys) != 0:
                for enemy in enemys:
                    downTF = enemy.touchWall()

                    if downTF is True:
                        EnemyDown = True

                for enemy in enemys:
                    enemy.move()

                    if EnemyDown:
                        enemy.y += int(pygame.mask.from_surface(enemy.IMG).get_size()[0] + SPACING)

                        if enemy.right is True:
                            enemy.left = True
                            enemy.right = False

                        elif enemy.left is True:
                            enemy.left = False
                            enemy.right = True

                EnemyDown = False

            # Move the bullets
            if len(bullets) != 0:
                removeIndexs = []
                for pos, bullet in enumerate(bullets):
                    result = bullet.move()
                    if result is not None:
                        removeIndexs.append(pos)

                if len(removeIndexs) != 0:
                    for pos in removeIndexs:
                        bullets.pop(pos)

            # Move the player
            if right is True:
                player.move(PlayerStep)

            if left is True:
                player.move(-PlayerStep)

            # Fill the screen with
            # this IMG  \/  here \/
            WIN.blit(IMGS[-1], (0, 0))

            # Draw the window
            drawWindow(WIN, player, bullets, enemys, True)

            # Draw our endgame screen
            drawEndGame(WIN, lost)

        if len(enemys) != 0:
            for enemy in enemys:
                if enemy.y >= SIZE[1]:
                    enemys.remove(enemy)
                elif enemy.y+enemy.IMG.get_height() <= 0:
                    enemys.remove(enemy) 

    # Quit the pygame display
    pygame.display.quit()

# Start the game
main()


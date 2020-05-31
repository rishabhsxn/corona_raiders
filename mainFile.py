# corona raiders

# TODO: when corona hits player add a cross to his face

#------------------------imports------------------------
import turtle
import os
import math
import random
import time

soundFlag = 0
exitFlag = 0

# for cross-platform sound
import platform

if platform.system() == "Windows":
    try:
        import winsound
    except:
        print("Winsound module not available!! Please install.")

WIDTH = 1300
HEIGHT = 1000
NUM_OF_ENEMIES = 15

PLAYER_SPEED = 15
BULLET_SPEED = 20
ENEMY_SPEED_X = 4
ENEMY_SPEED_Y = 2

HOUSE_HEIGHT = 180
HOUSE_WIDTH = 120
LEFT_HOUSE_WALL = -(HOUSE_WIDTH/2)
RIGHT_HOUSE_WALL = HOUSE_WIDTH/2
UPPER_HOUSE_WALL = -400 + HOUSE_HEIGHT

#------------------------Setup screen------------------------
screen = turtle.Screen()
screen.setup(WIDTH, HEIGHT)
screen.bgcolor("black")
screen.title("Corona Raiders")

pen = turtle.Turtle()
pen.speed(0)
pen.color("white")
pen.penup()
pen.setposition(-550, -400)
pen.pendown()
for parallel_sides in range(2):
    pen.fd(1100)
    pen.lt(90)
    pen.fd(800)
    pen.lt(90)
pen.penup()
# make house
pen.fd(550 + HOUSE_WIDTH/2)
pen.pendown()
pen.color("#FAC42F")
pen.lt(90)
pen.fd(HOUSE_HEIGHT)
pen.lt(90)
pen.fd(HOUSE_WIDTH)
pen.lt(90)
pen.fd(HOUSE_HEIGHT)

pen.hideturtle()


#------------------------Register Shapes------------------------
screen.register_shape("corona.gif")
screen.register_shape("deadPlayer2.gif")
screen.register_shape("player2.gif")
screen.register_shape("drop2.gif")

#------------------------Setup Score------------------------
score = 0
scorePen = turtle.Turtle()
scorePen.speed(0)
scorePen.color("white")
scorePen.penup()
scorePen.setposition(-540, 370)
scoreString = "Score: {}".format(score)
scorePen.write(scoreString, False, align="left", font=("Arial", 14, "normal"))
scorePen.hideturtle()


#------------------------Setup Stay Home Message------------------------
messageColor = "green"
messagePen = turtle.Turtle()
messagePen.speed(0)
messagePen.color(messageColor)
messagePen.penup()
messagePen.setposition(0, 420)
message = "STAY HOME - STAY SAFE"
messagePen.write(message, False, align="center", font=("Arial", 20, "bold"))
messagePen.hideturtle()


#------------------------Create main Player------------------------

    #TODO: Make player look like a human being with a hand sanitizer (gun)

player = turtle.Turtle()
player.color("white")
player.shape("player2.gif")
#player.shapesize(2, 2)
player.penup()
player.speed(0)
player.setposition(0, -300)
player.setheading(90)



# Define player movements
playerSpeed = PLAYER_SPEED

def moveLeft():
    global messageColor

    x = player.xcor()
    x -= playerSpeed
    if x > -530:
        player.setx(x)

    if x < LEFT_HOUSE_WALL and messageColor=="green":
        messageColor = "red"
        message = "STAY HOME - STAY SAFE"
        messagePen.color("red")
        messagePen.clear()
        messagePen.write(message, False, align="center", font=("Arial", 20, "bold"))
    elif x < RIGHT_HOUSE_WALL and x > LEFT_HOUSE_WALL and messageColor=="red":
        messageColor = "green"
        message = "STAY HOME - STAY SAFE"
        messagePen.color("green")
        messagePen.clear()
        messagePen.write(message, False, align="center", font=("Arial", 20, "bold"))

def moveRight():
    global messageColor

    x = player.xcor()
    x += playerSpeed
    if x < 530:
        player.setx(x)

    if x > LEFT_HOUSE_WALL and x < RIGHT_HOUSE_WALL and messageColor=="red":
        messageColor = "green"
        message = "STAY HOME - STAY SAFE"
        messagePen.color("green")
        messagePen.clear()
        messagePen.write(message, False, align="center", font=("Arial", 20, "bold"))
    elif x > RIGHT_HOUSE_WALL and messageColor=="green":
        messageColor = "red"
        message = "STAY HOME - STAY SAFE"
        messagePen.color("red")
        messagePen.clear()
        messagePen.write(message, False, align="center", font=("Arial", 20, "bold"))


#------------------------Create Player's Bullet------------------------
bullet = turtle.Turtle()
bullet.hideturtle()
bullet.color("yellow")
bullet.shape("drop2.gif")
#bullet.shapesize(0.5, 0.5)
bullet.penup()
bullet.speed(0)
bullet.setheading(90)
bullet.setposition(-WIDTH, 0)


# Define bullet movement
bulletSpeed = BULLET_SPEED
bulletState = "ready"       # 1. ready - ready to be fired      2. fired - bullet is travelling

def fireBullet():
    global bulletState      # global is used so that we modify the variable globally
    global soundFlag
    global messageColor

    # fire the bullet only when it is in the ready state And Player is not in House
    if bulletState == "ready" and messageColor=="red":
        if soundFlag == 0:
            playSound("corona_go.wav")
            soundFlag = 1
        else:
            playSound("go_corona.wav")
            soundFlag = 0

        bulletState = "fired"
        x = player.xcor()
        y = player.ycor()
        bullet.setposition(x, y+10)
        bullet.showturtle()


# key bindings
screen.listen()
screen.onkeypress(moveLeft, "a")
screen.onkeypress(moveRight, "d")
screen.onkeypress(fireBullet, "space")


#------------------------Sound function------------------------

def playSound(soundFile):
    # Windows
    if platform.system() == "Windows":
        winsound.PlaySound(soundFile, winsound.SND_ASYNC)
    # Linux
    if platform.system() == "Linux":
        os.system("aplay -q {}&".format(soundFile))
    # Mac
    else:
        os.system("afplay {}&".format(soundFile))


#------------------------Define Collision function for 2 objects------------------------

def isCollided(t1, t2):
    distance = math.sqrt(math.pow(t1.xcor() - t2.xcor(), 2) + math.pow(t1.ycor() - t2.ycor(), 2))
    if distance < 15:
        return True
    else:
        return False


#------------------------Create Enemy------------------------

class Enemy:
    def __init__(self, xSpeed, ySpeed):
        self.speedX = xSpeed
        self.speedY = ySpeed
        self.x = random.randint(-520, 520)
        self.y = random.randint(180, 280)
        self.enemyTurtle = turtle.Turtle()
        self.enemyTurtle.color("#43BE31")
        self.enemyTurtle.shape("corona.gif")
        self.enemyTurtle.penup()
        self.enemyTurtle.speed(0)
        self.enemyTurtle.setposition(self.x, self.y)

    def move(self):
        currentX = self.enemyTurtle.xcor()
        currentY = self.enemyTurtle.ycor()

        currentX += self.speedX
        currentY += self.speedY

        self.enemyTurtle.setposition(currentX, currentY)

        # check collisions with Boundaries
        if currentX > 530 or currentX < -530:
            self.speedX *= -1
        if currentY > 380 or currentY < -380:
            self.speedY *= -1

        # check collision with House
        # left wall
        if currentY < UPPER_HOUSE_WALL and abs(LEFT_HOUSE_WALL - currentX) < 15:
            self.speedX *= -1
        # right wall
        elif currentY < UPPER_HOUSE_WALL and abs(RIGHT_HOUSE_WALL - currentX) < 15:
            self.speedX *= -1
        # upper wall
        elif currentX > LEFT_HOUSE_WALL and currentX < RIGHT_HOUSE_WALL and abs(UPPER_HOUSE_WALL - currentY) < 15:
            self.speedY *= -1

# create and store multiple Enemies using List
enemies = []
for i in range(NUM_OF_ENEMIES):

    directions = [-1, 1]
    dirX = random.choice(directions)
    dirY = random.choice(directions)
    enemy = Enemy(dirX*ENEMY_SPEED_X, dirY*ENEMY_SPEED_Y)

    enemies.append(enemy)


#-----------------------More functions-----------------------

def exitGame():
    global exitFlag
    exitFlag = 1

runFlag = 1
while runFlag==1:
    # move all enemies
    for enemy in enemies:
        enemy.move()
            
        if isCollided(enemy.enemyTurtle, bullet):
            playSound("pop.wav")
            # reset bullet
            bullet.hideturtle()
            bulletState = "ready"
            bullet.setposition(0, -420)
            # reset enemy
            x = random.randint(-520, 520)
            y = random.randint(240, 280)
            enemy.enemyTurtle.setposition(x, y)

            # Update the score
            score += 10
            scoreString = "Score: {}".format(score)
            scorePen.clear()
            scorePen.write(scoreString, False, align="left", font=("Arial", 14, "normal"))

        if isCollided(enemy.enemyTurtle, player):
            playSound("coffin_dance.wav")
            player.setposition(0, -300)
            runFlag = 2
            
            # reset keybinds
            screen.onkeypress(None, "a")
            screen.onkeypress(None, "d")
            screen.onkeypress(None, "space")

            
            messagePen.color("white")
            messagePen.setposition(0,20)
            messagePen.write("GAME OVER.", False, align="center", font=("Arial", 50, "bold"))
            messagePen.setposition(-200,-20)
            scoreString = "Score: {}".format(score)
            messagePen.write(scoreString, False, align="left", font=("Arial", 20, "normal"))
            
	    
            player.shape("deadPlayer2.gif")

            break
        

    # move bullet
    if bulletState == "fired":
        bulletY = bullet.ycor()
        bulletNewY = bulletY + bulletSpeed
        bullet.sety(bulletNewY)

        # check if bullet hits top boundary
        if bulletNewY > 380: 
            bullet.hideturtle()
            bulletState = "ready"
            bullet.setposition(0, -420)

    turtle.delay(2)     # this increase or decrease gameplay - Lower is faster

exitPen = turtle.Turtle()
exitPen.hideturtle()
exitPen.penup()
isWhite = False
screen.onkeypress(exitGame, "Return")

while exitFlag==0:
    exitPen.setposition(0, -130)
    if isWhite:
        isWhite = False
        exitPen.color("black")
    else:
        isWhite = True
        exitPen.color("white")

    exitPen.write("Press Enter to exit !", False, align="center", font=("Arial", 16, "normal"))
    time.sleep(1)
    exitPen.clear()


# delay = input("Press Enter to finish!")

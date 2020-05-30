# corona raiders

#------------------------imports------------------------
import turtle
import os
import math
import random

soundFlag = 0

# for cross-platform sound
import platform

if platform.system() == "Windows":
    try:
        import winsound
    except:
        print("Winsound module not available!! Please install.")

WIDTH = 1300
HEIGHT = 1000
NUM_OF_ENEMIES = 5

PLAYER_SPEED = 15
BULLET_SPEED = 20
ENEMY_SPEED = 1


#------------------------Setup screen------------------------
screen = turtle.Screen()
screen.setup(WIDTH, HEIGHT)
screen.bgcolor("black")
screen.title("Corona Raiders")

#------------------------Register Shapes------------------------
# turtle.register_shape("corona.gif")
screen.register_shape("corona.gif")

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
pen.hideturtle()


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

#------------------------Create main Player------------------------

    #TODO: Make player look like a human being

player = turtle.Turtle()
player.color("white")
player.shape("classic")
player.shapesize(2, 2)
player.penup()
player.speed(0)
player.setposition(0, -300)
player.setheading(90)



# Define player movements
playerSpeed = PLAYER_SPEED

def moveLeft():
    x = player.xcor()
    x -= playerSpeed
    if x > -530:
        player.setx(x)

def moveRight():
    x = player.xcor()
    x += playerSpeed
    if x < 530:
        player.setx(x)

#------------------------Create Player's Bullet------------------------
bullet = turtle.Turtle()
bullet.hideturtle()
bullet.color("yellow")
bullet.shape("triangle")
bullet.shapesize(0.5, 0.5)
bullet.penup()
bullet.speed(0)
bullet.setheading(90)


# Define bullet movement
bulletSpeed = BULLET_SPEED
bulletState = "ready"       # 1. ready - ready to be fired      2. fired - bullet is travelling

def fireBullet():
    global bulletState      # global is used so that we modify the variable globally
    global soundFlag
    
    # fire the bullet only when it is in the ready state
    if bulletState == "ready":
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
    #TODO: Make Enemy move in random directions

# create multiple Enemies using List
enemies = []
for i in range(NUM_OF_ENEMIES):
    enemy = turtle.Turtle()
    enemy.color("#43BE31")
    enemy.shape("corona.gif")
    enemy.penup()
    enemy.speed(0)
    x = random.randint(-520, 520)
    y = random.randint(180, 280)
    enemy.setposition(x, y)
    enemies.append(enemy)

# Define Enemy movements
enemySpeed = ENEMY_SPEED

while True:
    # move enemy Left
    for enemy in enemies:
        x = enemy.xcor()
        x += enemySpeed
        enemy.setx(x)

        if x > 530 or x < -530:
            enemySpeed *= -1

            
        if isCollided(enemy, bullet):
            playSound("explosion.wav")
            # reset bullet
            bullet.hideturtle()
            bulletState = "ready"
            bullet.setposition(0, -420)
            # reset enemy
            # TODO: reset enemies in different way - hide or remove
            x = random.randint(-520, 520)
            y = random.randint(240, 280)
            enemy.setposition(x, y)

            # Update the score
            score += 10
            scoreString = "Score: {}".format(score)
            scorePen.clear()
            scorePen.write(scoreString, False, align="left", font=("Arial", 14, "normal"))

        # TODO: check collision between Enemies and Player + Handle GameOver
        

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

    turtle.delay(5)     # this increase or decrease gameplay - Lower is faster





# delay = input("Press Enter to finish!")
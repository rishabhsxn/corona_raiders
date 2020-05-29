# corona raiders

#------------------------imports------------------------
import turtle
import os

WIDTH = 1300
HEIGHT = 1000



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
pen.hideturtle()



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
playerSpeed = 15

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
bulletSpeed = 20
bulletState = "ready"       # 1. ready - ready to be fired      2. fired - bullet is travelling

def fireBullet():
    global bulletState      # global is used so that we modify the variable globally

    # fire the bullet only when it is in the ready state
    if bulletState == "ready":
        bulletState = "fired"
        x = player.xcor()
        y = player.ycor()
        bullet.setposition(x, y+10)
        bullet.showturtle()


# key bindings
turtle.listen()
turtle.onkey(moveLeft, "a")
turtle.onkey(moveRight, "d")
turtle.onkey(fireBullet, "space")



#------------------------Create Enemy------------------------
    #TODO: Make the Enemy look like Corona Virus
    #TODO: Make multiple copies of the Enemy
    #TODO: Make Enemy move in random directions

enemy = turtle.Turtle()
enemy.color("#43BE31")
enemy.shape("circle")
enemy.penup()
enemy.speed(0)
enemy.setposition(0, 280)

# Define Enemy movements
enemySpeed = 1

while True:

    # move enemy Left
    x = enemy.xcor()
    x += enemySpeed
    enemy.setx(x)

    if x > 530 or x < -530:
        enemySpeed *= -1

    if bulletState == "fired":
        bulletY = bullet.ycor()
        bulletNewY = bulletY + bulletSpeed
        bullet.sety(bulletNewY)

        if bulletNewY > 380: 
            bullet.hideturtle()
            bulletState = "ready"






delay = input("Press Enter to finish!")
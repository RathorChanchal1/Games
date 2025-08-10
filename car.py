import turtle
import random
import time

# Setup screen
screen = turtle.Screen()
screen.title("Road Dodge Game")
screen.bgcolor("black")
screen.setup(width=300, height=500)
screen.tracer(0)

# Register image shapes (make sure files are in same directory)
screen.addshape("road.gif")
screen.addshape("red.gif")    # Player car
screen.addshape("white.gif")  # Obstacle cars

# Background setup
background = turtle.Turtle()
background.shape("road.gif")
background.penup()
background.goto(0, 0)

# Player setup
player = turtle.Turtle()
player.shape("red.gif")
player.penup()
player.goto(0, -180)
player.shapesize(stretch_wid=0.05, stretch_len=0.05)  # Scale down car

# Movement controls
def go_left():
    x = player.xcor()
    if x > -80:
        player.setx(x - 80)

def go_right():
    x = player.xcor()
    if x < 80:
        player.setx(x + 80)

screen.listen()
screen.onkey(go_left, "Left")
screen.onkey(go_right, "Right")

# Enemy car logic
enemy_cars = []

def create_enemy():
    enemy = turtle.Turtle()
    enemy.shape("white.gif")
    enemy.penup()
    enemy.speed(0)
    enemy.shapesize(stretch_wid=0.05, stretch_len=0.05)  # Scale down enemy car
    lane = random.choice([-80, 0, 80])
    enemy.goto(lane, 250)
    enemy_cars.append(enemy)

# Game loop variables
score = 0
speed = 4
game_over = False

# Game loop
while not game_over:
    screen.update()
    time.sleep(0.02)

    # Occasionally create enemy cars
    if random.randint(1, 40) == 1:
        create_enemy()

    for enemy in enemy_cars:
        enemy.sety(enemy.ycor() - speed)

        # Collision detection
        if enemy.distance(player) < 30:
            game_over = True

        # Remove enemies that move off-screen
        if enemy.ycor() < -300:
            enemy.hideturtle()
            enemy_cars.remove(enemy)
            score += 1
            if score % 5 == 0:
                speed += 1


# === Game Over Screen ===
end_text = turtle.Turtle()
end_text.hideturtle()
end_text.color("red")
end_text.penup()
end_text.goto(0, 0)
end_text.write(f"💥 GAME OVER 💥\nFinal Score: {score}", align="center", font=("Arial", 18, "bold"))


turtle.done()

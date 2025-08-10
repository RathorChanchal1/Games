import turtle
import time

# === Screen Setup ===
win = turtle.Screen()
win.title("Bouncing Ball Game")
win.bgcolor("black")
win.setup(width=800, height=600)
win.tracer(0)

# === Paddle ===
paddle = turtle.Turtle()
paddle.speed(0)
paddle.shape("square")
paddle.color("white")
paddle.shapesize(stretch_wid=1, stretch_len=5)
paddle.penup()
paddle.goto(0, -250)

# === Ball ===
ball = turtle.Turtle()
ball.speed(1)
ball.shape("circle")
ball.color("red")
ball.penup()
ball.goto(0, 0)
ball.dx = 3
ball.dy = 3

# === Score Display ===
pen = turtle.Turtle()
pen.hideturtle()
pen.color("white")
pen.penup()
pen.goto(0, 260)
pen.write("Score: 0", align="center", font=("Courier", 24, "normal"))

# === Score ===
score = 0
game_running = True
game_over = False

# === Paddle Movement Functions ===
def paddle_left():
    if not game_over:
        x = paddle.xcor()
        if x > -350:
            paddle.setx(x - 40)

def paddle_right():
    if not game_over:
        x = paddle.xcor()
        if x < 350:
            paddle.setx(x + 40)

# === Restart Game ===
def restart_game():
    global score, game_running, game_over
    # Reset game state
    ball.goto(0, 0)
    ball.dx = 3
    ball.dy = 3
    paddle.goto(0, -250)
    score = 0
    pen.clear()
    pen.goto(0, 260)
    pen.write("Score: 0", align="center", font=("Courier", 24, "normal"))
    game_running = True
    game_over = False
    game_loop()

# === Game Loop ===
def game_loop():
    global score, game_running, game_over

    while game_running:
        win.update()

        # Ball Movement
        ball.setx(ball.xcor() + ball.dx)
        ball.sety(ball.ycor() + ball.dy)

        # Border Collisions
        if ball.xcor() > 390:
            ball.setx(390)
            ball.dx *= -1

        if ball.xcor() < -390:
            ball.setx(-390)
            ball.dx *= -1

        if ball.ycor() > 290:
            ball.sety(290)
            ball.dy *= -1

        # Bottom Collision (Game Over)
        if ball.ycor() < -290:
            pen.clear()
            pen.goto(0, 0)
            pen.write(f"GAME OVER\nFinal Score: {score}\nPress SPACE to restart \nSubscribe TeeChungs...", align="center", font=("Courier", 24, "bold"))
            game_running = False
            game_over = True
            break

        # Paddle Collision
        if (
            -260 < ball.ycor() < -240 and
            paddle.xcor() - 50 < ball.xcor() < paddle.xcor() + 50
        ):
            ball.sety(-240)
            ball.dy *= -1
            score += 1
            pen.clear()
            pen.goto(0, 260)
            pen.write(f"Score: {score}", align="center", font=("Courier", 24, "normal"))

        time.sleep(0.01)

# === Keyboard Bindings ===
win.listen()
win.onkeypress(paddle_left, "Left")
win.onkeypress(paddle_right, "Right")
win.onkeypress(restart_game, "space")

# === Start Game Initially ===
game_loop()

win.mainloop()

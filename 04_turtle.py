from turtle import forward, penup, pendown, exitonclick, shape, left

LEN = 100

for _ in range(3):
    for _ in range(4):
        forward(LEN)
        left(90)

    left(20)

exitonclick()

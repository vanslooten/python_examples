# The following code uses tkinter to create a simple catch-a-ball game
# Inspiration:
# https://stackoverflow.com/questions/71460324/python-bounce-ball-game-in-functional-programming

import tkinter as tk
import random

# Constants
screen_width = 1000
screen_height = 800
ball_radius = 10
basket_width = 100
basket_height = 20
ball_speed = 5
basket_speed = 30
update_delay = 10  # milliseconds
speed_increment_interval = 5  # Points interval to increase speed


class CatchTheBallGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Catch the Ball")

        # set up the canvas
        self.canvas = tk.Canvas(root, width=screen_width, height=screen_height, bg="black")
        self.canvas.pack()

        # set up the basket
        self.basket = self.canvas.create_rectangle(0, 0, basket_width, basket_height, fill="white")

        # position the basekt at the bottom of the screen, in the middle)
        self.canvas.move(self.basket, screen_width // 2 - basket_width // 2, screen_height - basket_height - 10)

        # initialise
        self.ball = None
        self.score = 0
        self.ball_speed = ball_speed
        self.score_text = self.canvas.create_text(10, 10, anchor="nw", text=f"Score: {self.score}", fill="white", font=("Arial", 16))

        # associate left and right arrow keys to move the basket
        self.root.bind("<Left>", self.move_left)
        self.root.bind("<Right>", self.move_right)
        self.update_game()

    def move_left(self, event):
        # move the basket left by the basket_speed
        self.canvas.move(self.basket, -basket_speed, 0)

        # prevent the basket from moving off to the left
        x1, y1, x2, y2 = self.canvas.coords(self.basket)
        if x1 < 0:
            self.canvas.move(self.basket, -x1, 0)

    def move_right(self, event):
        # move the basket right
        self.canvas.move(self.basket, basket_speed, 0)
        # prevent the basket from moving off to the right
        x1, y1, x2, y2 = self.canvas.coords(self.basket)
        if x2 > screen_width:
            self.canvas.move(self.basket, screen_width - x2, 0)

    def update_game(self):
        # code in update_game is written by Open AI
        # check if a ball does not exist
        if self.ball is None or self.canvas.coords(self.ball)[1] > screen_height:
            if self.ball is not None:
                # if the ball fell below back to 0
                self.reset_score()
                # remove the ball
                self.canvas.delete(self.ball)
            # new ball at the top of the screen
            self.ball = self.canvas.create_oval(0, 0, ball_radius * 2, ball_radius * 2, fill="white")
            self.canvas.move(self.ball, random.randint(0, screen_width - ball_radius * 2), 0)

        # move the ball downward by the current ball_speed
        self.canvas.move(self.ball, 0, self.ball_speed)
        # check for collisions between the ball and the basket
        self.check_collision()
        # next update
        self.root.after(update_delay, self.update_game)

    def check_collision(self):
        ball_coords = self.canvas.coords(self.ball)
        basket_coords = self.canvas.coords(self.basket)

        # save ball position
        ball_left = ball_coords[0]
        ball_top = ball_coords[1]
        ball_right = ball_coords[2]
        ball_bottom = ball_coords[3]

        # save basket position
        basket_left = basket_coords[0]
        basket_top = basket_coords[1]
        basket_right = basket_coords[2]
        basket_bottom = basket_coords[3]

        # check if the ball is out
        if ball_bottom > basket_bottom:
            self.reset_score()
            self.canvas.delete(self.ball)
            self.ball = None
            return

        # check if the ball's bottom is within the basket's top and bottom bounds
        # check if the ball's horizontal span intersects the basket's horizontal span
        # if statemewnt written is written by Open AI
        if ball_bottom >= basket_top and ball_top <= basket_bottom and \
                (basket_left < ball_right and basket_right > ball_left):
            # ball is caught by the basket
            self.canvas.delete(self.ball)
            self.ball = None
            self.score += 1
            self.update_score()
            self.increase_speed()

    def reset_score(self):
        # reset the score and ball speed
        self.score = 0
        self.ball_speed = ball_speed
        self.canvas.itemconfigure(self.score_text, text=f"Score: {self.score}")

    def update_score(self):
        # update the score display
        self.canvas.itemconfigure(self.score_text, text=f"Score: {self.score}")

    def increase_speed(self):
        # increase the speed
        if self.score % speed_increment_interval == 0:
            self.ball_speed += 1

root = tk.Tk()
game = CatchTheBallGame(root)
root.mainloop()


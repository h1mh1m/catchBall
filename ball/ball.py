import pygame as game
import random

class Ball:
    def __init__(self, screenwidth,screenheight):
        self.widthscreen = screenwidth
        self.heightscreen = screenheight
        self.radius = 15
        self.color = (230, 50, 50)
        self.reset()

    def reset(self):
        self.x = random.randint(self.radius,self.widthscreen - self.radius)
        self.y = 0
        self.speed = 6

    def update(self):
        self.y += self.speed

    def isCaught(self, basket):
        caught = (
            basket.y <= self.y + self.radius <= basket.y + basket.height
        ) and (basket.x <= self.x <= basket.x + basket.width)

        if caught:
            self.y = 0
            self.x = random.randint(
                self.radius, self.widthscreen - self.radius
            )
            self.speed += 0.2
        return caught

    def isOutofField(self):
        if self.y > self.heightscreen :
            self.y = 0
            self.x = random.randint(self.radius,self.widthscreen - self.radius)
            return True
        return False

    def draw(self, surface):
        game.draw.circle(surface,self.color,(int(self.x), int(self.y)),self.radius)
    
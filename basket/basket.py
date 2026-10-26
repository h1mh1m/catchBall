import numpy as np
import pygame as game


class Basket:
    def __init__(self,screenwidth, screenheight):
        self.Screenwidth = screenwidth
        self.width = 125
        self.height = 25
        self.x = screenwidth//2 - self.width//2
        self.y = screenheight - 50
        self.color = (50, 150, 250)

    def updatePosition(self,xRatio):
        if xRatio is not None:
            self.x = int(xRatio * self.Screenwidth) - (self.width // 2)

        self.x = max(0, min(self.Screenwidth - self.width, self.x))

    def draw(self, surface):
        game.draw.rect(
            surface,
            self.color,
            (self.x, self.y, self.width, self.height),
            border_radius= 8
        )

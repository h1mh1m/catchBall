import cv2 
import numpy as np
import pygame as game
import random

class Basket:
    def __init__(self,screenwidth, screenheight):
        self.screenwidth = screenwidth
        self.width = 125
        self.height = 25
        self.x = screenwidth//2 - self.width//2
        self.y = screenheight - 50
        self.color = (50, 150, 250)

    def updatePosition(self,xRatio):
        if xRatio is not None:
            self.x = int(xRatio * self.screenwidth) - (self.width // 2)

        self.x = max(0, min(self.screenwidth - self.width, self.x))

    def draw(self, surface):
        game.draw.rect(
            surface,
            self.color,
            (self.x, self.y, self.width, self.height),
            border_radius= 8
        )

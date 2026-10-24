import cv2 
import numpy as np
import pygame as game
import random

class Ball:
    def __init__(self, screenwidth,screenheight):
        self.widthscreen = screenwidth
        self.heightscreen = screenheight
        self.radius = 15
        self.color = (230, 50, 50)
        self.reset()

    def reset():
        self.x = random.randint(self.radius,self.widthscreen - self.radius)
        self.y = 0
        self.speed = 6
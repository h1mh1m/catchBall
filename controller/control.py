import cv2 
import numpy as np
import pygame as game
import random

#Set surface
WIDTH, HEIGHT = 800, 600
gravitation = 10
Score = 0
level = 1

#Set awal ball
ball = 100
ballradius = 10
ballX = random.randint(ballradius, WIDTH - ballradius)
ballY = 0

#Set awal keranjang
basketWitdh = 100
basketHeight = 30
basketX = WIDTH/2 - basketWitdh/2
basketY = HEIGHT - basketHeight - 40

#Set warna hitam 
LOWER_BLACK = ([0,0,0])
UPPER_BLACK = ([180,255,70])











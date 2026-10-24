import cv2 
import numpy as np
import pygame as game
import random

#Set surface
WIDTH, HEIGHT = 800, 600
screen = game.display.set_mode((WIDTH, HEIGHT))
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

WHITE = (255, 255, 255)
BLACK = (20, 20, 20)
RED = (230, 50, 50)
BLUE = (50, 150, 250)
GREEN = (50, 200, 80)
YELLOW = (255, 215, 0)
GRAY = (100, 100, 100)

#Set warna hitam 
LOWER_BLACK = ([0,0,0])
UPPER_BLACK = ([180,255,70])

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, WIDTH)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, HEIGHT)

font_title = game.font.SysFont(None, 64)
font_btn = game.font.SysFont(None, 36)
font_ui = game.font.SysFont(None, 28)

btn_screen = game.Rect(WIDTH // 2 - 100, 250, 200, 50)

def drawButton(react, text, hover):
    color = GREEN if hover else BLUE
    game.draw.rect(screen, color, react, border_radius=10)
    game.draw.rect(screen, WHITE, react, width=2, border_radius=10)
    btn_text = font_btn.render(text, True, BLACK if hover else WHITE)
    text_rect =  btn_text.get_rect(center=react.center)
    screen.blit(btn_text,text_rect)

def mainScreen():
    game.display.set_caption("Catch WowoBall")
    

    












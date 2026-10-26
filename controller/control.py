import cv2 
import numpy as np
import sys
import pygame as game
import random
from ball import ball as bola
from basket import basket as keranjang
from tracker import tracker as ngetrack

class MainGame:
    def __init__(self, Swidth=800, Sheight=600):
        game.init()
        self.width = Swidth
        self.height = Sheight
        self.screen = game.display.set_mode((Swidth, Sheight))
        game.display.set_caption("CatchWOWOBiji")
        self.clock = game.time.Clock()

        self.tracker = ngetrack.Tracker()
        self.bola = bola.Ball(self.width,self.height)
        self.wadah = keranjang.Basket(self.width,self.height)

        self.WHITE = (255, 255, 255)
        self.BLACK = (20, 20, 20)
        self.YELLOW = (255, 215, 0)
        self.BLUE = (50, 150, 250)
        self.GREEN = (50, 200, 80)

        self.fontTitle = game.font.SysFont(None, 64)
        self.fontBtn = game.font.SysFont(None, 36)
        self.fontUI = game.font.SysFont(None, 28)

        self.state = "MENU"
        self.score = 0
        self.running = True

        self.btnPlayRect = game.Rect(self.width // 2 - 100, 250, 200, 50)
        self.btnQuitRect = game.Rect(self.width // 2 - 100, 330, 200, 50)

    def resetGame(self):
        self.score = 0
        self.bola.reset()

    def drawButton(self, rect, text, isHover):
        color = self.YELLOW if isHover else self.BLUE
        game.draw.rect(self.screen, color, rect, border_radius=10)
        game.draw.rect(self.screen, self.WHITE, rect, width=2, border_radius=10)

        btnText = self.fontBtn.render(
            text, True, self.BLACK if isHover else self.WHITE
        )
        textRect = btnText.get_rect(center=rect.center)
        self.screen.blit(btnText, textRect)

    def HandleEvents(self):
        mousePosition = game.mouse.get_pos()
        for event in game.event.get():
            if event.type == game.QUIT:
                self.running = False
            if event.type == game.MOUSEBUTTONDOWN and event.button == 1:
                if self.state == "MENU":
                    if self.btnPlayRect.collidepoint(mousePosition):
                        self.resetGame()
                        self.state = "PLAY"
                    elif self.btnQuitRect.collidepoint(mousePosition):
                        self.running = False

            if event.type == game.KEYDOWN:
                if event.key == game.K_ESCAPE:
                    if self.state == "PLAY":
                        self.state = "MENU"
                    elif self.state == "MENU":
                        self.running = False

    def renderMenu(self, mousePosition):
        overLay = game.Surface((self.width, self.height))
        overLay.set_alpha(150)
        overLay.fill((0,0,0))
        self.screen.blit(overLay,(0,0))

        TitleSurface = self.fontTitle.render("CATCH WOWO BALL",True,self.GREEN)
        self.screen.blit(TitleSurface,TitleSurface.get_rect(center=(self.width//2, 150)))

        self.drawButton(self.btnPlayRect,"PLAY",self.btnPlayRect.collidepoint(mousePosition))
        self.drawButton(self.btnQuitRect,"QUIT",self.btnQuitRect.collidepoint(mousePosition))

        infoText = self.fontUI.render("Gunakan apapun yang berwarna HITAM untuk mengontrol keranjang",True,self.WHITE)
        self.screen.blit(infoText,infoText.get_rect(center=(self.width//2, self.height - 50)))

    def renderUiPlay(self):
        scoreSurface = self.fontBtn.render(f"Skor:{self.score}",True,self.YELLOW)
        self.screen.blit(scoreSurface,(20,20))

        speedSurface = self.fontBtn.render(f"Speed:{self.bola.speed}", True,self.YELLOW)
        self.screen.blit(speedSurface,(20,40))

        escSurface = self.fontUI.render("Tekan ESC untuk kembali ke MENU", True, self.WHITE)

        game.draw.rect(escSurface,self.BLACK,(15,self.height - 40,escSurface.get_width() + 10, 30))
        self.screen.blit(escSurface,(20, self.height - 35))

    def run(self):
        while self.running:
            mousePosition = game.mouse.get_pos()

            webcamSurface, Xratio = self.tracker.frameProcess(self.width,self.height)

            self.wadah.updatePosition(xRatio=Xratio)

            self.HandleEvents()

            if webcamSurface:
                self.screen.blit(webcamSurface,(0,0))
            else:
                self.screen.fill(self.BLACK)
            if self.state == "MENU":
                self.renderMenu(mousePosition)
            elif self.state == "PLAY":
                self.bola.update()

                if self.bola.isCaught(self.wadah):
                    self.score += 1

                if self.bola.isOutofField():
                    self.score = max(0,self.score - 1)

                self.wadah.draw(self.screen)
                self.bola.draw(self.screen)
                self.renderUiPlay()

            game.display.flip()
            self.clock.tick()

        self.tracker.release()
        game.quit()
        sys.exit()



import pygame
import os
from testgame import Game

pygame.init()
pygame.mixer.init()
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)  # 綠色
RED = (255, 0, 0)  # 紅色
BLUE = (0, 0, 255)  # 藍色
WIDTH, HEIGHT = 1024, 600
FPS = 60


class MainMenu:
    def __init__(self):
        # win
        self.menuwin = pygame.display.set_mode((WIDTH, HEIGHT))
        # background
        self.bg = pygame.image.load(os.path.join("images/Menu.png"))
        self.bg = pygame.transform.scale(pygame.image.load(os.path.join("images", "Menu.png")), (WIDTH, HEIGHT))
        # start button
        self.start_btn = pygame.Rect(349, 315, 338, 101)  # x y 寬 高
        self.start_btn_frame = pygame.Rect(344, 310, 348, 111)
        self.sound_btn = pygame.Rect(725, 525, 90, 70)
        self.sound_btn_frame = pygame.Rect(720, 520, 100, 80)
        self.muse_btn = pygame.Rect(830, 525, 90, 70)
        self.muse_btn_frame = pygame.Rect(820, 520, 100, 80)
        self.buttons = [self.start_btn, self.sound_btn, self.muse_btn]
        self.buttons_frame = [self.start_btn_frame, self.sound_btn_frame, self.muse_btn_frame]
        # music and sound
        self.sound = pygame.mixer.Sound("./sound/sound.flac")
    
    def display(self):
        pygame.display.set_caption("Covid-19 Defense Game")
        self.menuwin.blit(self.bg, (0, 0))
    
    def music(self):
        pygame.mixer.music.load("./sound/menu.wav")
        pygame.mixer.music.set_volume(0.2)
        pygame.mixer.music.play(-1)
        self.sound.set_volume(0.2)

    def menu_run(self):
        run = True
        clock = pygame.time.Clock()
        self.display()
        self.music()
        while run:
            clock.tick(FPS)
            self.menuwin.blit(self.bg, (0, 0))
            for event in pygame.event.get():
                x, y = pygame.mouse.get_pos()
                # quit
                if event.type == pygame.QUIT:
                    run = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    # check if hit start btn
                    if self.start_btn[0] <= x <= self.start_btn[0] + self.start_btn[2] \
                            and self.start_btn[1] <= y <= self.start_btn[1] + self.start_btn[3]:
                        self.sound.play()
                        pygame.mixer.music.pause()
                        g = Game()
                        g.GameRun()
                        run = False
                    elif self.muse_btn[0] <= x <= self.muse_btn[0] + self.muse_btn[2] \
                            and self.muse_btn[1] <= y <= self.muse_btn[1] + self.muse_btn[3]:
                        pygame.mixer.music.pause()
                        self.sound.play()
                    elif self.sound_btn[0] <= x <= self.sound_btn[0] + self.sound_btn[2] \
                            and self.sound_btn[1] <= y <= self.sound_btn[1] + self.sound_btn[3]:
                        pygame.mixer.music.unpause()

            # draw the outer frame of the button
            for btn, btn_frm in zip(self.buttons, self.buttons_frame):
                if btn[0] <= x <= btn[0] + btn[2] and btn[1] <= y <= btn[1] + btn[3]:
                    pygame.draw.rect(self.menuwin, WHITE, btn_frm, 10)

            pygame.display.update()
        pygame.quit()

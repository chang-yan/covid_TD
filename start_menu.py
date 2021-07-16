import pygame
import os
from game import Game

pygame.init()
pygame.mixer.init()
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
WIDTH, HEIGHT = 1024, 600
FPS = 60


class MainMenu:
    def __init__(self):
        # win
        self.menu_win = pygame.display.set_mode((WIDTH, HEIGHT))
        # background
        self.bg = pygame.image.load(os.path.join("images/Menu.png"))
        self.bg = pygame.transform.scale(pygame.image.load(os.path.join("images", "Menu.png")), (WIDTH, HEIGHT))
        # button
        self.start_btn = Buttons(349, 315, 338, 101)  # x, y, width, height
        self.sound_btn = Buttons(725, 525, 90, 70)
        self.muse_btn = Buttons(830, 525, 90, 70)
        self.buttons = {"sound": self.sound_btn,
                        "muse": self.muse_btn,
                        "start": self.start_btn,
                        }
        # music and sound
        self.sound = pygame.mixer.Sound("./sound/sound.flac")
    
    def play_music(self):
        pygame.mixer.music.load("./sound/menu.wav")
        pygame.mixer.music.set_volume(0.2)
        pygame.mixer.music.play(-1)
        self.sound.set_volume(0.2)

    def menu_run(self):
        run = True
        clock = pygame.time.Clock()
        pygame.display.set_caption("Covid-19 Defense Game")
        self.play_music()
        while run:
            clock.tick(FPS)
            self.menu_win.blit(self.bg, (0, 0))
            x, y = pygame.mouse.get_pos()
            for event in pygame.event.get():
                # quit
                if event.type == pygame.QUIT:
                    run = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    # check if hit start btn
                    if self.start_btn.get_touched(x, y):
                        self.sound.play()
                        pygame.mixer.music.pause()
                        g = Game()
                        g.game_run()
                        run = False
                    elif self.muse_btn.get_touched(x, y):
                        pygame.mixer.music.pause()
                        self.sound.play()
                    elif self.sound_btn.get_touched(x, y):
                        pygame.mixer.music.unpause()

            # while cursor is moving
            for name, btn in self.buttons.items():
                btn.create_frame(x, y)
                btn.draw_frame(self.menu_win)

            pygame.display.update()
        pygame.quit()


class Buttons:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.frame = None

    def get_touched(self, x, y):
        """
        if cursor position is on the button, return True
        :param x: int
        :param y: int
        :return: Bool
        """
        if self.x <= x <= self.x + self.width and self.y <= y <= self.y + self.height:
            return True
        return False

    def create_frame(self, x, y):
        """
        if cursor position is on the button, create button frame
        :param x: int
        :param y: int
        :return: None
        """
        if self.get_touched(x, y):
            self.frame = pygame.Rect(self.x - 5, self.y - 5, self.width + 10, self.height + 10)
        else:
            self.frame = None

    def draw_frame(self, win):
        if self.frame:
            pygame.draw.rect(win, WHITE, self.frame, 10)

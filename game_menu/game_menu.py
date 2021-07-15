import pygame
import os
import time
from towers.tower import Pcr, RapidTest, Alcohol

pygame.font.init()
pygame.init()
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
WIDTH = 1024
HEIGHT = 600

class Buttons:
    def __init__(self, x, y, image=None):
        self.x = x
        self.y = y
        self.image = image
        self.width = image.get_width() if image else 70
        self.height = image.get_height() if image else 70
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
        pygame.draw.rect(win, WHITE, self.frame, 10)


class FunctionMenu:
    def __init__(self):
        # images
        self.virus_gray_img = pygame.transform.scale(pygame.image.load("game_menu/images/Virus_gray.png"), (40, 40))
        self.virus_img = pygame.transform.scale(pygame.image.load("game_menu/images/Virus.png"), (40, 40))
        # assets
        self.max_lives = 10
        # buttons
        self.sound_btn = Buttons(695, 5)
        self.muse_btn = Buttons(780, 5)
        self.start_btn = Buttons(860, 5)
        self.stop_btn = Buttons(945, 5)
        self.buttons = {"sound": self.sound_btn,
                        "muse": self.muse_btn,
                        "start": self.start_btn,
                        "stop": self.stop_btn,
                        }
        # font
        self.font_size = 30
        self.font = pygame.font.SysFont("comicsans", self.font_size)
        # menu size
        self.width = WIDTH
        self.height = HEIGHT
        # time
        self.start_time = time.time()

    def draw(self, win, level, tech_level, lives, money):
        """
        show all the information on the function menu
        :param win: window
        :param level: int
        :param tech_level: int
        :param lives: int
        :param money: int
        :return: None
        """
        # level
        text = self.font.render(f"Level: {level}", True, (255, 255, 255))
        win.blit(text, (5, 10))

        # money
        text = self.font.render(f"Money: {money}", True, (255, 255, 255))
        win.blit(text, (5, 35))

        # tech level
        text = self.font.render(f"Technology Level: {tech_level}", True, (255, 255, 255))
        win.blit(text, (5, 60))

        # draw button frame
        for key, btn in self.buttons.items():
            if btn.frame:
                btn.draw_frame(win)

        # draw_lives
        for i in range(self.max_lives):
            win.blit(self.virus_gray_img,
                     (self.width // 2 - self.virus_gray_img.get_width() * (2.5 - i % 5),
                      self.virus_gray_img.get_height() * (i // 5)))
        for i in range(lives):
            win.blit(self.virus_img,
                     (self.width // 2 - self.virus_img.get_width() * (2.5 - i % 5),
                      self.virus_img.get_height() * (i // 5)))

        # draw time
        pygame.draw.rect(win, BLACK, [0, self.height - 40, 80, 40])
        game_time = time.time() - self.start_time
        game_time_sec = int((game_time % 60))
        game_time_min = int(game_time // 60)
        time_text = self.font.render(f"{game_time_min}:{game_time_sec}", True, (255, 255, 255))
        time_Rect = time_text.get_rect()
        time_Rect.center = (40, self.height - 20)
        win.blit(time_text, time_Rect)


class BuildMenu:
    def __init__(self):
        self.item_names = ["alcohol", "rapid test", "pcr"]
        # image
        self.tower_menu_image = pygame.transform.scale(pygame.image.load("game_menu/images/treatment.png"), (100, 350))
        # tower
        self.tower_images = [pygame.transform.scale(pygame.image.load("game_menu/images/alcohol.png"), (20, 60)),
                       pygame.transform.scale(pygame.image.load("game_menu/images/rapid_test.png"), (65, 65)),
                       pygame.transform.scale(pygame.image.load("game_menu/images/pcr.png"), (65, 65)),
                       ]
        self.tower_buttons = {"alcohol": Buttons(960, 160, self.tower_images[0]),
                        "rapid test": Buttons(940, 240, self.tower_images[1]),
                        "pcr": Buttons(940, 330, self.tower_images[2]),
                        }
        self.tower_market_price = {"alcohol": 100,
                             "rapid test": 150,
                             "pcr": 150,
                             }
        # tech
        self.upgrade_image = pygame.transform.scale(pygame.image.load("game_menu/images/upgrade.png"), (100, 45))
        self.upgrade_button = Buttons(920, 440, self.upgrade_image)
        self.upgrade_market_price = [300, 1000, 1500]

    def draw(self, win):
        win.blit(self.tower_menu_image, (920, 100))
        win.blit(self.upgrade_button.image, (self.upgrade_button.x, self.upgrade_button.y))
        for name, btn in self.tower_buttons.items():
            win.blit(btn.image, (btn.x, btn.y))

    def get_items(self, x, y):
        """
        if the cursor is on the tower button (while clicked), select the tower
        :param x: int
        :param y: int
        :return: item object
        """
        for name, btn in self.tower_buttons.items():
            if btn.get_touched(x, y):
                return SelectedItems(x, y, btn.image, name, self.tower_market_price[name])

    def upgrade_tech_level(self, x, y, tech_level, money):
        """
        if the cursor is on the upgrade buttons (while clicked), upgrade the technology level and pay for it
        :param x: int
        :param y: int
        :param tech_level: int
        :param money: int
        :return: (int, int, str)
        """
        notice = None
        if self.upgrade_button.get_touched(x, y):
            if tech_level >= 2:
                notice = f"Already the highest level"
            elif money < self.upgrade_market_price[tech_level]:
                notice = f"{self.upgrade_market_price[tech_level]} is needed for upgrade"
            else:
                money -= self.upgrade_market_price[tech_level]
                notice = f"Pay {self.upgrade_market_price[tech_level]} to upgrade technology level"
                tech_level += 1
        return (tech_level, money, notice)


class SelectedItems:
    def __init__(self, x, y, image, name, market_price):
        self.x = x
        self.y = y
        self.image = image
        self.name = name
        self.market_price = market_price

    def draw(self, win):
        win.blit(self.image, (self.x-self.image.get_width()//2, self.y-self.image.get_height()//2))

    def drop(self, money):
        """
        if the money is enough to build a tower, drop the item (build the tower) and pay for it
        :param money: int
        :return: (int, tower object)
        """
        notice = None
        if money > self.market_price:
            if self.name == "alcohol":
                dropped_item =  Alcohol(self.x, self.y, self.name)
            elif self.name == "rapid test":
                dropped_item = RapidTest(self.x, self.y, self.name)
            else:
                dropped_item = Pcr(self.x, self.y, self.name)

            notice = f"Pay {self.market_price} for {self.name}"
            return (money - self.market_price, dropped_item, notice)
        return(money, None, notice)
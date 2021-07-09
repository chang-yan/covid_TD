import pygame
import time
from towers.tower_main import Tower

alcohol_images = [pygame.transform.scale(pygame.image.load(f"./towers/tower_images/alcohol.png"), (30, 70)) for i in range(3)]
pcr_images = [pygame.transform.scale(pygame.image.load(f"./towers/tower_images/pcr_{i}.png"), (80, 80)) for i in range(3)]
rapid_test_images = [pygame.transform.scale(pygame.image.load(f"./towers/tower_images/rapid_test_{i}.png"), (80, 80)) for i in range(3)]


class Alcohol(Tower):
    def __init__(self, x, y):
        super().__init__(x, y)
        #  tower geometry
        self.images = alcohol_images
        self.width = self.images[0].get_width()
        self.height = self.images[0].get_height()
        # level: 0~2
        self.level = {
            "development": 0,
            "range": 0,
            "damage": 0,
            "cool down": 0,
        }
        # ability: level 0~2
        self.timer = time.time() - 1
        self.ability = {
            "development": [0, 1, 2],
            "range": [90, 100, 120],
            "damage": [1.0, 1.5, 2.0],
            "cool down": [2, 1.6, 1.4]
        }
        # price
        self.upgrade_cost = {
            "development": [250, 350],
            "range": [100, 120],
            "damage": [80, 120],
            "cool down": [80, 100],
        }
        self.selling_price = [130, 350, 700]
        # others
        self.is_selected = False


class Pcr(Tower):
    def __init__(self, x, y):
        super().__init__(x, y)
        #  tower geometry
        self.images = pcr_images
        self.width = self.images[0].get_width()
        self.height = self.images[0].get_height()
        # level: 0~2
        self.level = {
            "development": 0,
            "range": 0,
            "damage": 0,
            "cool down": 0,
        }
        # ability: level 0~2
        self.timer = time.time() - 1
        self.ability = {
            "development": [0, 1, 2],
            "range": [100, 120, 180],
            "damage": [5.0, 6.5, 7.5],
            "cool down": [1.5, 1.0, 0.8]
        }
        # price
        self.upgrade_cost = {
            "development": [300, 400],
            "range": [120, 140],
            "damage": [100, 120],
            "cool down": [120, 150],
        }
        self.selling_price = [300, 500, 750]
        # others
        self.is_selected = False


class RapidTest(Tower):
    def __init__(self, x, y):
        super().__init__(x, y)
        #  tower geometry
        self.images = rapid_test_images
        self.width = self.images[0].get_width()
        self.height = self.images[0].get_height()
        # level: 0~2
        self.level = {
            "development": 0,
            "range": 0,
            "damage": 0,
            "cool down": 0,
        }
        # ability: level 0~2
        self.timer = time.time() - 1
        self.ability = {
            "development": [0, 1, 2],
            "range": [90, 100, 120],
            "damage": [1.5, 2.5, 3.0],
            "cool down": [1.0, 0.8, 0.5]
        }
        # price
        self.upgrade_cost = {
            "development": [250, 350],
            "range": [100, 120],
            "damage": [80, 120],
            "cool down": [80, 100],
        }
        self.selling_price = [130, 350, 700]
        # others
        self.is_selected = False

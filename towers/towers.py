import pygame
import time
from towers.tower_main import Tower

alcohol_images = [pygame.transform.scale(pygame.image.load(f"./towers/tower_images/alcohol.png"), (20, 60)) for i in range(3)]
pcr_images = [pygame.transform.scale(pygame.image.load(f"./towers/tower_images/pcr_{i}.png"), (70, 70)) for i in range(3)]
rapid_test_images = [pygame.transform.scale(pygame.image.load(f"./towers/tower_images/rapid_test_{i}.png"), (70, 70)) for i in range(3)]


class Alcohol(Tower):
    def __init__(self, x, y):
        super().__init__(x, y)
        #  tower geometry
        self.images = alcohol_images
        self.width = self.images[0].get_width()
        self.height = self.images[0].get_height()
        self.price = 100
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
            "range": [90, 110, 130],
            "damage": [1.0, 1.5, 2.0],
            "cool down": [1.5, 1.0, 0.8]
        }
        # price
        self.upgrade_cost = {
            "development": [250, 350],
            "range": [100, 130],
            "damage": [80, 120],
            "cool down": [80, 100],
        }
        self.selling_price = [130, 350, 700]

    def attack(self, enemies):
        """
        AOE attack
        :param enemies: list
        :return: None
        """
        if self.is_cooling_down():
            for en in enemies:
                if self.enemy_in_range(en):
                    en.health -= self.ability["damage"][self.level["damage"]]


class Pcr(Tower):
    def __init__(self, x, y):
        super().__init__(x, y)
        #  tower geometry
        self.images = pcr_images
        self.width = self.images[0].get_width()
        self.height = self.images[0].get_height()
        self.price = 150
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
            "damage": [5.0, 7, 7.5],
            "cool down": [2.0, 1.8, 1.4]
        }
        # price
        self.upgrade_cost = {
            "development": [300, 400],
            "range": [120, 140],
            "damage": [100, 120],
            "cool down": [120, 150],
        }
        self.selling_price = [300, 500, 750]


class RapidTest(Tower):
    def __init__(self, x, y):
        super().__init__(x, y)
        #  tower geometry
        self.images = rapid_test_images
        self.width = self.images[0].get_width()
        self.height = self.images[0].get_height()
        self.price = 150
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
            "damage": [1.5, 2.0, 3.0],
            "cool down": [0.7, 0.5, 0.3]
        }
        # price
        self.upgrade_cost = {
            "development": [250, 350],
            "range": [100, 120],
            "damage": [80, 120],
            "cool down": [80, 100],
        }
        self.selling_price = [130, 350, 700]


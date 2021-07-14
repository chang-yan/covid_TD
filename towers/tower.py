import pygame
from towers.tower_main import Tower

FPS = 60
alcohol_images = [pygame.transform.scale(pygame.image.load(f"./towers/tower_images/alcohol/alcohol.png"), (20, 60)) for i in range(3)]
pcr_images = [pygame.transform.scale(pygame.image.load(f"./towers/tower_images/pcr/pcr_{i}.png"), (70, 70)) for i in range(3)]
rapid_test_images = [pygame.transform.scale(pygame.image.load(f"./towers/tower_images/rapid_test/rapid_test_{i}.png"), (70, 70)) for i in range(3)]

alcohol_proj_images = [[pygame.transform.scale(pygame.image.load(f"./towers/tower_images/alcohol/alcohol_{i}_{j}.png"), (30, 30)) for j in range(3)] for i in range(3)]
pcr_proj_images = [[pygame.transform.scale(pygame.image.load(f"./towers/tower_images/pcr/pcr_{i}_{j}.png"), (70, 70)) for j in range(3)] for i in range(3)]
rapid_test_proj_images = [[pygame.transform.scale(pygame.image.load(f"./towers/tower_images/rapid_test/rapid_test_{i}_{j}.png"), (55, 10)) for j in range(3)] for i in range(3)]


class Alcohol(Tower):
    def __init__(self, x, y, name):
        super().__init__(x, y, name)
        #  tower geometry
        self.images = alcohol_images
        self.width = self.images[0].get_width()
        self.height = self.images[0].get_height()
        self.market_price = 100
        # level: 0~2
        self.level = {
            "range": 0,
            "damage": 0,
            "cool down": 0,
        }
        # ability: level 0~2
        self.ability = {
            "range": [90, 110, 130],
            "damage": [1.0, 1.5, 2.0],
            "cool down": [1.5, 1.0, 0.8]
        }
        # price
        self.upgrade_market_price = {
            "range": [0, 100, 130],
            "damage": [0, 80, 120],
            "cool down": [0, 80, 100],
        }
        self.proj_images = alcohol_proj_images
        self.proj = None

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

    def draw_projectile(self, win, flip):
        """
        draw the projectile
        """
        proj_x = self.x + 40 if flip else self.x - 40
        proj_y = self.y - 10
        if self.proj_count < FPS//2 and self.proj:
            img = self.proj[self.proj_count // 10]
            win.blit(img, (proj_x - img.get_width()//2, proj_y - img.get_height()//2))
            self.proj_count += 1
        else:
            self.proj = []


class Pcr(Tower):
    def __init__(self, x, y, name):
        super().__init__(x, y, name)
        #  tower geometry
        self.images = pcr_images
        self.width = self.images[0].get_width()
        self.height = self.images[0].get_height()
        self.market_price = 150
        # level: 0~2
        self.level = {
            "range": 0,
            "damage": 0,
            "cool down": 0,
        }
        # ability: level 0~2
        self.ability = {
            "range": [100, 120, 180],
            "damage": [5.0, 7, 7.5],
            "cool down": [2.0, 1.8, 1.4]
        }
        # price
        self.upgrade_market_price = {
            "range": [0, 120, 140],
            "damage": [0, 100, 120],
            "cool down": [0, 120, 150],
        }
        self.proj_images = pcr_proj_images
        self.proj = None

    def draw_projectile(self, win, flip):
        """
        draw the projectile
        """
        proj_x = self.x + 50 if flip else self.x - 70
        proj_y = self.y
        if self.proj_count < FPS//2 and self.proj:
            img = self.proj[self.proj_count // 10]
            win.blit(img, (proj_x - img.get_width()//2, proj_y - img.get_height()//2))
            self.proj_count += 1
        else:
            self.proj = []


class RapidTest(Tower):
    def __init__(self, x, y, name):
        super().__init__(x, y, name)
        #  tower geometry
        self.images = rapid_test_images
        self.width = self.images[0].get_width()
        self.height = self.images[0].get_height()
        self.market_price = 150
        # level: 0~2
        self.level = {
            "range": 0,
            "damage": 0,
            "cool down": 0,
        }
        # ability: level 0~2
        self.ability = {
            "range": [90, 100, 120],
            "damage": [1.5, 2.0, 3.0],
            "cool down": [0.7, 0.5, 0.3]
        }
        # price
        self.upgrade_market_price = {
            "range": [0, 100, 120],
            "damage": [0, 80, 120],
            "cool down": [0, 80, 100],
        }
        self.proj_images = rapid_test_proj_images
        self.proj = None

    def draw_projectile(self, win, flip):
        """
        draw the projectile
        """
        proj_x = self.x + 60 if flip else self.x - 60
        proj_y = self.y + 20
        if self.proj_count < FPS//2 and self.proj:
            img = self.proj[self.proj_count // 10]
            win.blit(img, (proj_x - img.get_width()//2, proj_y - img.get_height()//2))
            self.proj_count += 1
        else:
            self.proj = []

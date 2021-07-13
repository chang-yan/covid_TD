import pygame
import time
import math
from towers.upgrade_menu import UpgradeMenu


class Tower:
    def __init__(self, x, y):
        #  tower geometry
        self.x = x
        self.y = y
        self.images = [None, None, None]
        self.width = 0
        self.height = 0
        self.market_price = 0
        self.upgrade_cost = 0
        # level: 0~2
        self.level = {
            "range": 0,
            "damage": 0,
            "cool down": 0,
        }
        # ability: level 0~2
        self.cooling_timer = time.time() - 1
        self.ability = {
            "range": [0, 0, 0],
            "damage": [0, 0, 0],
            "cool down": [0, 0, 0],
        }
        # price
        self.upgrade_market_price = {
            "range": [0, 0, 0],
            "damage": [0, 0, 0],
            "cool down": [0, 0, 0],
        }
        # others
        self.menu = None
        self.announcement = None


    def upgrade(self, x, y, tech_level, money):
        """
        if the button is clicked, upgrade the corresponding ability and return the cost
        :param x: int
        :param y: int
        :param tech_level: int
        :param money: int
        :return: int
        """
        if self.menu:
            option = self.menu.get_items(x, y)
            if option and option != "selling":
                if self.level[option] >= tech_level:
                    pass
                elif money < self.upgrade_market_price[option][self.level[option]+1]:
                    pass
                else:
                    money -= self.upgrade_market_price[option][self.level[option]+1]
                    self.level[option] += 1
        return money

    def sells(self, x, y, money):
        """
        if "selling" button is clicked, return the selling price and the status
        :param x: int
        :param y: int
        :param money: int
        :return: (int, Bool)
        """
        if self.menu:
            option = self.menu.get_items(x, y)
            if option == "selling":
                selling_price = self.market_price
                for name, price in self.upgrade_market_price.items():
                    selling_price += price[self.level[name]]
                money += selling_price*0.9
                return (int(money//10)*10, True)
        return (money, False)

    def call_menu(self, x, y):
        """
        if the tower is selected, call the upgrade menu
        :param x: int
        :param y: int
        :return: None
        """
        if self.is_clicked(x, y):
            self.menu = UpgradeMenu(self.x-5, self.y-10)
        else:
            self.menu = None

    def attack(self, enemies):
        """
        detect the enemies in range and drop their health
        :param enemies: list
        :return: None
        """
        if self.is_cooling_down():
            for en in enemies:
                if self.enemy_in_range(en):
                    en.health -= self.ability["damage"][self.level["damage"]]
                    break  # single attack

    def enemy_in_range(self, enemy):
        """
        return whether the enemy is in the range
        :param enemy: obj
        :return: Bool
        """
        x = enemy.x
        y = enemy.y
        distance = math.sqrt((x-self.x)**2 + (y-self.y)**2)
        if distance <= self.ability["range"][self.level["range"]]:
            return True
        return False

    def is_cooling_down(self):
        """
        return whether the tower is cooling down
        :return: Bool
        """
        cd_time = self.ability["cool down"][self.level["cool down"]]
        if time.time() - self.cooling_timer >= cd_time:
            self.cooling_timer = time.time()
            return True
        return False

    def is_clicked(self, x, y):
        """
        return whether the tower get clicked
        :param x: int
        :param y: int
        :return: Bool
        """
        if (self.x - self.width // 2) < x < (self.x + self.width // 2) \
                and (self.y - self.height // 2) < y < (self.y + self.height // 2):
            return True
        if self.menu and self.menu.is_clicked(x, y):
            return True
        return False

    def draw(self, win, tech_level):
        """
        draw the tower and other stuffs if the tower is selected
        :param win: obj
        :return: None
        """
        if self.menu:
            self.draw_range(win)
            self.menu.draw(win)
        self.draw_tower(win, tech_level)

    def draw_tower(self, win, tech_level):
        """
        draw the tower itself
        :param win: game window
        :return: None
        """
        win.blit(self.images[tech_level],
                 (self.x - self.width//2, self.y - self.height//2),
                 )

    def draw_range(self, win):
        """
        draw the attack range of tower
        :param win: window
        :return:  None
        """
        tw_range = self.ability["range"][self.level["range"]]
        surface = pygame.Surface((tw_range * 2, tw_range * 2), pygame.SRCALPHA)
        pygame.draw.circle(surface, (128, 128, 128, 120), (tw_range, tw_range), tw_range)
        win.blit(surface, (self.x - tw_range, self.y - tw_range))







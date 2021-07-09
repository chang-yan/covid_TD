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
        # level: 0~2
        self.level = {
            "development": 0,   
            "range": 0,
            "damage": 0,
            "cool down": 0,
        }
        # ability: level 0~2
        self.time = time.time() - 1
        self.ability = {
            "development": [0, 1, 2],
            "range": [0, 0, 0],
            "damage": [0, 0, 0],
            "cool down": [0, 0, 0]
        }
        # price
        self.upgrade_cost = {
            "development": [0, 0],
            "range": [0, 0],
            "damage": [0, 0],
            "cool down": [0, 0],
        }
        self.selling_price = [0, 0, 0]
        # others
        self.is_selected = False
        self.menu = UpgradeMenu(self.x-5, self.y-10)
        self.warning_text = None
        self.warning_time = time.time()

    def cooling_down(self):
        """
        return whether the tower is cooling down
        :return: Bool
        """
        cd_time = self.ability["cool down"][self.level["cool down"]]
        if time.time() - self.time >= cd_time:
            self.time = time.time()
            return True
        return False

    def upgrade(self, mouse_pos):
        """
        upgrade the tower level
        :param mouse_pos: (x, y)
        :return: None
        """
        option = self.menu.get_items(mouse_pos)
        if option:
            if self.level[option] <= self.level["development"]:
                if self.level[option] < 2:
                    self.level[option] += 1
                else:
                    self.warning_text = f"The {option} is the highest level"
                    self.warning_time = time.time()
            else:
                self.warning_text = f"You have to upgrade your medical development to unlock greater ability"
                self.warning_time = time.time()

    def attack(self, enemies):
        """
        detect the enemies in range and drop their health
        :param enemies: list
        :return: None
        """
        for en in enemies:
            if self.enemy_in_range(en):
                if self.cooling_down():
                    en.health -= self.ability["damage"][self.level["damage"]]
                if en.health < 0:
                    enemies.remove(en)

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

    def get_clicked(self, mouse_pos):
        """
        update the status of whether the tower is selected
        :param mouse_pos: (x, y)
        :return: None
        """
        x, y = mouse_pos
        if (self.x - self.width // 2) < x < (self.x + self.width // 2) \
                and (self.y - self.height // 2) < y < (self.y + self.height // 2):
            self.menu.is_selected = True
            self.is_selected = True
        else:
            if self.is_selected:
                self.menu.get_clicked(mouse_pos)
                if not self.menu.is_selected:
                    self.is_selected = False
            else:
                self.menu.is_selected = False

    def draw(self, win):
        """
        draw the tower and other stuffs if the tower is selected
        :param win: obj
        :return: None
        """
        if self.is_selected:
            self.draw_range(win)
            self.menu.draw(win)
            for btn in self.menu.buttons:
                btn.draw(win)
        self.draw_tower(win)

    def draw_tower(self, win):
        win.blit(self.images[self.level["development"]],
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
        pygame.draw.circle(surface, (128, 128, 128, 70), (tw_range, tw_range), tw_range)
        win.blit(surface, (self.x - tw_range, self.y - tw_range))

    def show_warning(self, win):
        """
        show the warning message on the window
        :param win: obj
        :return: None
        """
        if time.time() - self.warning_time <= 1:
            warning = pygame.font.SysFont("comicsans", 25)
            text_surface = warning.render(self.warning_text, True, (255, 255, 255))
            win.blit(text_surface, (win.get_width() // 2 - text_surface.get_width() // 2, 100))






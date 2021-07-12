#!/usr/bin/env python
# coding: utf-8

# In[2]:


import pygame
import os
import time
import random
from towers.towers import Pcr, RapidTest, Alcohol
from enemies.virus import Virus

pygame.mixer.init()
pygame.font.init()
pygame.init()
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)  # 綠色
RED = (255, 0, 0)  # 紅色
BLUE = (0, 0, 255)  # 藍色
FPS = 60
start_time = 0


class Game:
    def __init__(self):
        # image
        self.width, self.height = 1024, 600
        self.win = pygame.display.set_mode((self.width, self.height))
        self.gamebg = pygame.transform.scale(pygame.image.load(os.path.join("images", "Map.png")), (self.width, self.height))
        self.virus_gray_img = pygame.transform.scale(pygame.image.load("images/Virus_gray.png"), (40, 40))
        self.virus_img = pygame.transform.scale(pygame.image.load("images/Virus.png"), (40, 40))
        # game button
        self.game_sound_btn = Buttons(695, 5, 70, 70)  # x y 寬 高
        self.game_muse_btn = Buttons(780, 5, 70, 70)
        self.game_start_btn = Buttons(860, 5, 70, 70)
        self.game_stop_btn = Buttons(945, 5, 70, 70)
        self.buttons = [self.game_start_btn, self.game_stop_btn, self.game_sound_btn, self.game_muse_btn]
        # font
        self.score_size = 32
        self.set_font = pygame.font.Font(None, self.score_size)
        self.warning_text = None
        # player
        self.start_time = 0
        self.money = 100
        self.sound = pygame.mixer.Sound("./sound/sound.flac")
        self.virus_limit = 10
        self.virus_num = 6
        self.base = pygame.Rect(430, 90, 195, 130)
        # enemy
        self.enemies = []
        self.gen_enemy_time = time.time() - 1
        # tower
        self.tower_menu = TowerMenu()
        self.selected_item = None
        self.towers = [Pcr(100, 500), RapidTest(400, 420), Alcohol(300, 250)]

    def game_screen(self):
        self.win.blit(self.gamebg, (0, 0))
        pygame.display.set_caption("Covid-19 Defense Game")

    def game_music(self):
        pygame.mixer.music.load("./sound/menu.wav")
        pygame.mixer.music.set_volume(0.2)
        self.sound.set_volume(0.2)
        pygame.mixer.music.play(100)

    def generate_enemies(self):
        if time.time() - self.gen_enemy_time >= 2:  # wave interval
            self.gen_enemy_time = time.time()
            self.enemies.append(random.choice([Virus()]))

    def draw(self):
        """
        all that related to drawing the images work in this function
        :return:
        """
        # base
        pygame.draw.rect(self.gamebg, BLACK, pygame.Rect(430, 90, 195, 130), 5)

        # timer
        pygame.draw.rect(self.win, BLACK, [0, self.height - 40, 80, 40])
        count_time = pygame.time.get_ticks() - self.start_time
        count_sec = int((count_time % 60000)/1000)
        count_min = int(count_time//60000)
        time_text = self.set_font.render(str(count_min)+':'+str(count_sec), True, (255, 255, 255))
        time_Rect = time_text.get_rect()
        time_Rect.center = (40, self.height-20)
        self.win.blit(time_text, time_Rect)

        # level
        level_num = count_min+1
        level_text = self.set_font.render(f"level: {level_num}", True, (255, 255, 255))
        self.win.blit(level_text, (5, 10))
        
        # money
        money_text = self.set_font.render(f"money: {self.money}", True, (255, 255, 255))
        self.win.blit(money_text, (5, 50))

        # draw_Virus
        for i in range(self.virus_limit):
            self.win.blit(self.virus_gray_img,
                          (self.width//2 - self.virus_gray_img.get_width() * (2.5 - i % 5), self.virus_gray_img.get_height()*(i // 5)))
        for i in range(self.virus_num):
            self.win.blit(self.virus_img,
                          (self.width//2 - self.virus_img.get_width() * (2.5 - i % 5), self.virus_img.get_height()*(i // 5)))

        # draw tower
        for tw in self.towers:
            tw.draw(self.win)

        # draw enemy
        for en in self.enemies:
            en.draw(self.win)

        # draw button frame
        for btn in self.buttons:
            if btn.frame:
                btn.draw_frame(self.win)

        # draw tower menu
        self.tower_menu.draw(self.win)
        for name in self.tower_menu.item_names:
            if self.tower_menu.buttons[name].frame:
                self.tower_menu.buttons[name].draw_frame(self.win)

        # draw selected item
        if self.selected_item:
            self.selected_item.draw(self.win)

        pygame.display.update()

    def raise_warning(self, text):
        text_surface = pygame.font.SysFont("comicsans", 25).render(text, True, (255, 255, 255))
        self.win.blit(text_surface, (self.win.get_width() // 2 - text_surface.get_width() // 2, 100))

        #
        for tw in self.towers:
            tw.raise_warning(self.win)

    def GameRun(self):
        # initialization
        run = True
        paused = False
        clock = pygame.time.Clock()
        self.start_time = pygame.time.get_ticks()
        self.game_screen()
        self.game_music()
        while run:
            clock.tick(FPS)
            self.win.blit(self.gamebg, (0, 0))
            x, y = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        run = False
                    if event.key == pygame.K_SPACE:
                        paused = not paused

                if event.type == pygame.MOUSEBUTTONDOWN:  # every action related to "click"
                    # turn on/off the music
                    if self.game_muse_btn.get_touched(x, y):
                        pygame.mixer.music.pause()
                    elif self.game_sound_btn.get_touched(x, y):
                        pygame.mixer.music.unpause()

                    # click the tower
                    for tw in self.towers:
                        tw.call_menu(x, y)
                        tw.upgrade(x, y, self.money)
                        self.money -= tw.cost
                        tw.cost = 0
                    # click the tower menu
                    if event.button == 3:
                        self.selected_item = None
                    if self.selected_item:
                        new_tower = self.selected_item.drop(x, y)
                        if self.money >= new_tower.price:
                            self.money -= new_tower.price
                            self.towers.append(new_tower)
                        else:
                            self.warning_text = f"You don't have enough money to pay for the tower({new_tower.price})"
                    self.selected_item = self.tower_menu.get_items(x, y)

            # generate monster
            if not paused:
                self.generate_enemies()

            # button loop
            for btn in self.buttons:
                btn.create_frame(x, y)
            for name in self.tower_menu.item_names:
                self.tower_menu.buttons[name].create_frame(x, y)

            # tower loop
            for tw in self.towers:
                tw.attack(self.enemies)

            # enemy loop
            for en in self.enemies:
                en.move()
                if en.y < 160:
                    self.enemies.remove(en)
                    self.virus_num -= 1
                if en.health <= 0:
                    self.money += 10
                    self.enemies.remove(en)

            # selected item
            if self.selected_item:
                self.selected_item.x, self.selected_item.y = x, y

            # draw all the stuff
            self.raise_warning(self.warning_text)
            self.draw()
        pygame.quit()


class TowerMenu:
    def __init__(self):
        self.item_names = ["alcohol", "rapid test", "pcr"]
        # image
        self.tower_menu_image = pygame.transform.scale(pygame.image.load("images/treatment.png"), (100, 300))
        self.images = {"alcohol": pygame.transform.scale(pygame.image.load("images/alcohol.png"), (20, 60)),
                       "rapid test": pygame.transform.scale(pygame.image.load("images/rapid_test.png"), (65, 65)),
                       "pcr": pygame.transform.scale(pygame.image.load("images/pcr.png"), (65, 65)),
                       }
        # button
        self.buttons = {"alcohol": Buttons(960, 150, self.images["alcohol"].get_width(), self.images["alcohol"].get_height()),
                        "rapid test": Buttons(940, 230, self.images["rapid test"].get_width(), self.images["rapid test"].get_height()),
                        "pcr": Buttons(940, 320, self.images["pcr"].get_width(), self.images["pcr"].get_height()),
                        }

    def draw(self, win):
        win.blit(self.tower_menu_image, (920, 100))
        for name in self.item_names:
            win.blit(self.images[name], (self.buttons[name].x, self.buttons[name].y))

    def get_items(self, x, y):
        for name in self.item_names:
            if self.buttons[name].get_touched(x, y):
                return SelectedItems(x, y, self.images[name], name)


class Buttons:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.surface = pygame.Rect(x, y, width, height)
        self.frame = None

    def get_touched(self, x, y):
        if self.x <= x <= self.x + self.width and self.y <= y <= self.y + self.height:
            return True
        return False

    def create_frame(self, x, y):
        if self.get_touched(x, y):
            self.frame = pygame.Rect(self.x-5, self.y-5, self.width+10, self.height+10)
        else:
            self.frame = None

    def draw_frame(self, win):
        pygame.draw.rect(win, WHITE, self.frame, 10)


class SelectedItems:
    def __init__(self, x, y, image, name):
        self.x = x
        self.y = y
        self.image = image
        self.name = name

    def draw(self, win):
        win.blit(self.image, (self.x-self.image.get_width()//2, self.y-self.image.get_height()//2))

    def drop(self, x, y):
        if self.name == "alcohol":
            return Alcohol(x, y)
        elif self.name == "rapid test":
            return RapidTest(x, y)
        elif self.name == "pcr":
            return Pcr(x, y)



















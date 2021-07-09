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
        self.width, self.height = 1024, 600
        self.win = pygame.display.set_mode((self.width, self.height))
        self.gamebg = pygame.image.load(os.path.join("images/Map.png"))
        self.gamebg = pygame.transform.scale(pygame.image.load(os.path.join("images", "Map.png")), (self.width, self.height))
        self.virus_gray_img = pygame.transform.scale(pygame.image.load("images/Virus_gray.png"), (40, 40))
        self.virus_img = pygame.transform.scale(pygame.image.load("images/Virus.png"), (40, 40))
        # game button
        self.gamesound_btn = pygame.Rect(695, 5, 70, 70)  # x y 寬 高
        self.gamesound_out = pygame.Rect(690, 0, 80, 80)
        self.gamemuse_btn = pygame.Rect(780, 5, 70, 70)
        self.gamemuse_out = pygame.Rect(775, 0, 80, 80)
        self.gamestart_btn = pygame.Rect(860, 5, 70, 70)
        self.gamestart_out = pygame.Rect(855, 0, 80, 80)
        self.gamestop_btn = pygame.Rect(945, 5, 70, 70)
        self.gamestop_out = pygame.Rect(940, 0, 80, 80)
        self.buttons = [self.gamestart_btn, self.gamestop_btn, self.gamesound_btn, self.gamemuse_btn]
        self.buttons_out = [self.gamestart_out, self.gamestop_out, self.gamesound_out, self.gamemuse_out]
        self.score_size = 32
        self.set_font = pygame.font.Font(None, self.score_size)
        # sound
        self.sound = pygame.mixer.Sound("./sound/sound.flac")
        # live 
        self.virus_limit = 10
        self.virus_num = 6
        # base
        self.base = pygame.Rect(430, 90, 195, 130)
        # tower
        self.towers = [Pcr(100, 500), RapidTest(400, 420), Alcohol(300, 250)]
        # enemy
        self.enemies = []
        self.gen_enemy_time = time.time() - 1
        # delete
        self.clicks = []

    def game_screen(self):
        self.win.blit(self.gamebg, (0, 0))
        pygame.display.set_caption("Covid-19 Defense Game")

    def gamemusic(self):
        pygame.mixer.music.load("./sound/menu.wav")
        pygame.mixer.music.set_volume(0.2)
        self.sound.set_volume(0.2)
        pygame.mixer.music.play(100)

    def generate_enemies(self):
        """
        generate the next enemy
        :return: None
        """
        if time.time() - self.gen_enemy_time >= 2:  # wave interval
            self.gen_enemy_time = time.time()
            self.enemies.append(random.choice([Virus()]))
    
    def draw(self):
        # base
        pygame.draw.rect(self.gamebg, BLACK, self.base, 5)
        
        #timer
        pygame.draw.rect(self.win, BLACK, [0, self.height - 40, 80, 40])
        count_time = pygame.time.get_ticks() - self.start_time
        count_sec = int((count_time % 60000)/1000)
        count_min = int(count_time//60000)
        time_text = self.set_font.render(str(count_min)+':'+str(count_sec), True, (255, 255, 255))
        time_Rect = time_text.get_rect()
        time_Rect.center = (40, self.height-20)
        self.win.blit(time_text, time_Rect)

        #level 
        level_num = count_min+1
        lv_center_move = len(str(level_num))-1
        level_text = self.set_font.render('level: '+str(level_num), True, (255,255,255))
        level_Rect = level_text.get_rect()
        pygame.draw.rect(self.win, 0, [0, 0, 160, 40])
        level_Rect.center = (40+lv_center_move*7.5, 20)
        self.win.blit(level_text, level_Rect)
        
        #money
        money_num = int(count_time/100)
        mr_center_move = len(str(money_num))-1
        money_text = self.set_font.render('money:', True, (255, 255, 255))
        money_Rect = money_text.get_rect()
        pygame.draw.rect(self.win, 0, [0, 40, 80, 40])
        money_Rect.center = (40, 60)
        self.win.blit(money_text, money_Rect)
        
        money_num_text = self.set_font.render(str(money_num), True, (255, 255, 255))
        money_num_Rect = money_num_text.get_rect()
        pygame.draw.rect(self.win, 0, [80, 40, 80, 40])
        money_num_Rect.center = (91+mr_center_move*7.5, 60)
        self.win.blit(money_num_text, money_num_Rect)
        
        # draw_Virus
        for i in range(self.virus_limit):
            if i < 5:
                if i < self.virus_limit-self.virus_num:
                    self.win.blit(self.virus_gray_img, (int(self.width / 2) +
                                                        2.5 * self.virus_gray_img.get_width() -
                                                        (i+1) * self.virus_gray_img.get_width(),
                                                        self.virus_gray_img.get_width()))
                if i < self.virus_num:
                    self.win.blit(self.virus_img, (int(self.width / 2) -
                                                   2.5 * self.virus_img.get_width() +
                                                   i * self.virus_img.get_width(), 0))
            else:
                j = i-5
                if i < self.virus_limit-self.virus_num:
                    self.win.blit(self.virus_gray_img, (int(self.width / 2) +
                                                        2.5 * self.virus_gray_img.get_width() -
                                                        (j+1) * self.virus_gray_img.get_width(), 0))
                if i < self.virus_num:
                    self.win.blit(self.virus_img, (int(self.width / 2) -
                                                   2.5 * self.virus_img.get_width() +
                                                   j * self.virus_img.get_width(),
                                                   self.virus_img.get_width()))
        # draw tower
        for tw in self.towers:
            tw.show_warning(self.win)
            tw.draw(self.win)
        # draw enemy
        for en in self.enemies:
            en.draw(self.win)

        pygame.display.update()                 

    def game_run(self):
        run = True
        paused = False
        clock = pygame.time.Clock()
        self.start_time = pygame.time.get_ticks()
        self.game_screen()
        self.gamemusic()
        while run:
            clock.tick(FPS)
            self.win.blit(self.gamebg, (0, 0))
            for event in pygame.event.get():
                x, y = pygame.mouse.get_pos()

                if event.type == pygame.QUIT:
                    run = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        run = False
                    if event.key == pygame.K_SPACE:
                        paused = not paused

                if event.type == pygame.MOUSEBUTTONDOWN:
                    # turn on/off the music
                    if self.gamemuse_btn[0] <= x <= self.gamemuse_btn[0] + self.gamemuse_btn[2] and self.gamemuse_btn[1] <= y <= self.gamemuse_btn[1] + self.gamemuse_btn[3]:
                        pygame.mixer.music.pause()
                    elif self.gamesound_btn[0] <= x <= self.gamesound_btn[0] + self.gamesound_btn[2] and self.gamesound_btn[1] <= y <= self.gamesound_btn[1] + self.gamesound_btn[3]:
                        pygame.mixer.music.unpause()
                    # click the tower
                    for tw in self.towers:
                        tw.get_clicked((x, y))
                        tw.upgrade((x, y))

            # generate monster
            if not paused:
                self.generate_enemies()

            # enemy loop
            for en in self.enemies:
                if en.y > 150:
                    en.move()
                else:
                    self.enemies.remove(en)
                    self.virus_num -= 1

            # tower loop
            for tw in self.towers:
                tw.attack(self.enemies)

            # draw outer frame of the buttons
            for btn, btn_out in zip(self.buttons, self.buttons_out):
                if btn[0] <= x <= btn[0] + btn[2] and btn[1] <= y <= btn[1] + btn[3]:
                    pygame.draw.rect(self.win, WHITE, btn_out, 10)
                    break
            self.draw()
        pygame.quit()

                    





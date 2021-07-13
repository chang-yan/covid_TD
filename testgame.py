import pygame
import os
import time
import random
from game_menu.game_menu import FunctionMenu, TowerMenu
from enemies.virus import Virus

pygame.mixer.init()
pygame.font.init()
pygame.init()
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
FPS = 60


class Game:
    def __init__(self):
        # image
        self.width, self.height = 1024, 600
        self.win = pygame.display.set_mode((self.width, self.height))
        self.gamebg = pygame.transform.scale(pygame.image.load(os.path.join("images", "Map.png")), (self.width, self.height))
        # attribute
        self.money = 2000
        self.lives = 6
        self.level = 1
        self.tech_level = 0
        # base
        self.base = pygame.Rect(430, 90, 195, 130)
        # enemy
        self.wave = 0
        self.enemies = []
        self.enemy_generator = EnemyGenerator()
        # tower
        self.tower_menu = TowerMenu()
        self.selected_item = None
        self.towers = []
        # main menu
        self.func_menu = FunctionMenu()
        # sound
        self.sound = pygame.mixer.Sound("./sound/sound.flac")
        # announcement
        self.announcement = None
        self.announcement_time = time.time() - 1

    def game_screen(self):
        self.win.blit(self.gamebg, (0, 0))
        pygame.display.set_caption("Covid-19 Defense Game")

    def game_music(self):
        pygame.mixer.music.load("./sound/menu.wav")
        pygame.mixer.music.set_volume(0.2)
        self.sound.set_volume(0.2)
        pygame.mixer.music.play(-1)

    def raise_announcement(self):
        font = pygame.font.SysFont("comicsans", 25)
        text_surface = font.render(self.announcement, True, WHITE)
        self.win.blit(text_surface, (self.width//2 - text_surface.get_width()//2, 550))

    def draw(self):
        # base
        pygame.draw.rect(self.gamebg, BLACK, pygame.Rect(430, 90, 195, 130), 5)
        # function menu
        self.func_menu.draw(self.win, self.level, self.tech_level, self.lives, self.money)
        # draw tower menu
        self.tower_menu.draw(self.win)
        if self.tower_menu.upgrade_button.frame:
            self.tower_menu.upgrade_button.draw_frame(self.win)
        for name, btn in self.tower_menu.tower_buttons.items():
            if btn.frame:
                btn.draw_frame(self.win)
        # draw selected item
        if self.selected_item:
            self.selected_item.draw(self.win)
        # draw tower
        for tw in self.towers:
            tw.draw(self.win, self.tech_level)
        # draw enemy
        for en in self.enemies:
            en.draw(self.win)


    def GameRun(self):
        # initialization
        run = True
        game_paused = False
        wave_paused = False
        clock = pygame.time.Clock()
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
                        game_paused = not game_paused
                    if event.key == pygame.K_y:
                        wave_paused = False

                if event.type == pygame.MOUSEBUTTONDOWN:  # every action related to "click"
                    # turn on/off the music
                    if self.func_menu.buttons["muse"].get_touched(x, y):
                        pygame.mixer.music.pause()
                    elif self.func_menu.buttons["sound"].get_touched(x, y):
                        pygame.mixer.music.unpause()

                    # click the tower
                    for tw in self.towers:
                        tw.call_menu(x, y)
                        self.money = tw.upgrade(x, y, self.tech_level, self.money)
                        (self.money, tower_is_sell) = tw.sells(x, y, self.money)
                        if tower_is_sell:
                            self.towers.remove(tw)

                    # click the upgrade button
                    self.tech_level, self.money = self.tower_menu.upgrade_tech_level(x, y, self.tech_level, self.money)

                    # click the items
                    if event.button == 3:
                        self.selected_item = None
                    if self.selected_item:
                        self.money, new_tower = self.selected_item.drop(self.money)
                        self.towers.append(new_tower)
                    self.selected_item = self.tower_menu.get_items(x, y)

            # generate monster
            if not wave_paused:
                self.enemy_generator.generate(self.enemies, self.wave)
                if self.enemy_generator.enemy_nums[self.wave] == 0:
                    print("next wave")
                    self.wave += 1
                    wave_paused = True

            # function menu loop
            for name, btn in self.func_menu.buttons.items():
                btn.create_frame(x, y)
            for name, btn in self.tower_menu.tower_buttons.items():
                btn.create_frame(x, y)
            self.tower_menu.upgrade_button.create_frame(x, y)

            # tower loop
            for tw in self.towers:
                tw.attack(self.enemies)

            # enemy loop
            for en in self.enemies:
                en.move()
                if self.base[0] < en.x < self.base[0]+self.base[2] and self.base[1] < en.y < self.base[1]+self.base[3]:
                    self.enemies.remove(en)
                    self.lives -= 1
                if en.health <= 0:
                    self.money += 10
                    self.enemies.remove(en)

            # selected item
            if self.selected_item:
                self.selected_item.x, self.selected_item.y = x, y

            # draw all the stuff
            self.draw()
            # self.raise_announcement()
            pygame.display.update()
        pygame.quit()


class EnemyGenerator:
    random.seed()
    def __init__(self):
        self.enemy_nums = [10, 20, 30, 40, 50]
        self.enemy_health = [10, 12, 14, 15, 15]
        self.gen_enemy_time = time.time() - 1
        self.period = [2, 2, 1, 1, 0.6]
        self.mutation_probability = [0.1, 0.15, 0.3, 0.4, 0.4]

    def generate(self, enemies, wave):
        """
        generate the enemy to the enemy list according to the given wave
        :param enemies: list
        :param wave: int
        :return: None
        """
        if time.time() - self.gen_enemy_time >= self.period[wave] and self.enemy_nums[wave] > 0:  # wave interval
            self.gen_enemy_time = time.time()
            self.enemy_nums[wave] -= 1
            if random.random() < self.mutation_probability[wave]:
                enemies.append(random.choice([Virus(True, self.enemy_health[wave])]))
            else:
                enemies.append(random.choice([Virus(False, self.enemy_health[wave])]))


















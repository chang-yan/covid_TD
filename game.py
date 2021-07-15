import pygame
import os
import time
import random
from game_menu.game_menu import FunctionMenu, BuildMenu
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
PATH_0 = [(22, 308), (52, 283), (84, 283), (110, 305), (116, 341),
          (115, 375), (112, 405), (116, 433), (135, 455), (159, 475),
          (188, 480), (217, 481), (243, 474), (267, 463), (291, 454),
          (315, 441), (334, 423), (343, 398), (339, 368), (328, 345),
          (305, 331), (282, 322), (264, 303), (255, 283), (259, 259),
          (274, 239), (294, 225), (318, 214), (347, 212), (373, 217),
          (394, 230), (410, 250), (429, 266), (446, 282), (465, 295),
          (483, 310), (502, 321), (523, 309), (535, 282), (535, 254),
          (533, 230), (532, 196)]
PATH_1 = [(574, 585), (581, 559), (600, 534), (621, 514), (645, 500), (668, 488), (693, 492), (716, 500),
          (742, 501), (769, 501), (796, 502), (823, 501), (848, 495), (868, 475), (887, 453), (874, 426),
          (851, 408), (828, 396), (801, 382), (779, 364), (763, 342), (775, 313), (800, 294), (827, 276),
          (845, 248), (835, 222), (812, 209), (785, 200), (757, 206), (727, 207), (701, 220), (680, 233),
          (653, 245), (630, 262), (611, 280), (585, 302), (558, 318), (530, 324), (523, 294), (533, 262),
          (541, 230), (543, 189)]
WIDTH = 1024
HEIGHT = 600


class Game:
    def __init__(self):
        # screen
        self.win = pygame.display.set_mode((WIDTH, HEIGHT))
        self.gamebg = pygame.transform.scale(pygame.image.load(os.path.join("images", "Map.png")), (WIDTH, HEIGHT))
        # attribute
        self.money = 2000
        self.lives = 1
        self.level = 1
        self.tech_level = 0
        # base
        self.base = pygame.Rect(430, 90, 195, 130)
        # enemy
        self.wave = 0
        self.enemies = []
        self.enemy_generator = EnemyGenerator()
        # tower
        self.build_menu = BuildMenu()
        self.selected_item = None
        self.towers = []
        # main menu
        self.func_menu = FunctionMenu()
        # sound
        self.sound = pygame.mixer.Sound("./sound/sound.flac")
        # announcement
        self.bulletin_board = BulletinBoard()
        #
        self.game_paused = False
        self.wave_paused = True
        self.is_game_over =  False

    def game_music(self):
        pygame.mixer.music.load("./sound/menu.wav")
        pygame.mixer.music.set_volume(0.2)
        self.sound.set_volume(0.2)
        pygame.mixer.music.play(-1)

    def click_action(self, event, x, y):
        """
        run all that related to "click" action
        """
        if self.func_menu.buttons["muse"].get_touched(x, y):
            pygame.mixer.music.pause()
            self.bulletin_board.receive("MUSIC OFF!")
        elif self.func_menu.buttons["sound"].get_touched(x, y):
            pygame.mixer.music.unpause()
            self.bulletin_board.receive("MUSIC ON!")

        if not self.game_paused:
            # click the tower
            for tw in self.towers:
                tw.call_menu(x, y)
                # upgrade tower
                self.money, tower_upgrade_text = tw.upgrade(x, y, self.tech_level, self.money)
                if tower_upgrade_text:
                    self.bulletin_board.receive(tower_upgrade_text)

                # sell tower
                self.money, selling_text = tw.sells(x, y, self.money)
                if selling_text:
                    self.towers.remove(tw)
                    self.bulletin_board.receive(selling_text)

            # click the upgrade button
            self.tech_level, self.money, tech_upgrade_text = self.build_menu.upgrade_tech_level(x, y, self.tech_level, self.money)
            if tech_upgrade_text:
                self.bulletin_board.receive(tech_upgrade_text)

            # click the build menu
            if event.button == 3:
                self.selected_item = None
            if self.selected_item:
                self.money, new_tower, drop_text = self.selected_item.drop(self.money)
                if drop_text:
                    self.towers.append(new_tower)
                    self.bulletin_board.receive(drop_text)
            self.selected_item = self.build_menu.get_items(x, y)

    def game_processing(self, x, y):
        # generate monster
        if not self.wave_paused and self.wave < 5:
            self.enemy_generator.generate(self.enemies, self.wave)
            if self.enemy_generator.enemy_nums[self.wave] == 0:
                self.wave += 1
                self.wave_paused = True

        # function menu loop
        for name, btn in self.func_menu.buttons.items():
            btn.create_frame(x, y)
        for name, btn in self.build_menu.tower_buttons.items():
            btn.create_frame(x, y)
        self.build_menu.upgrade_button.create_frame(x, y)

        # tower loop
        for tw in self.towers:
            tw.attack(self.enemies)
            tw.throw(self.enemies, self.tech_level)

        # enemy loop
        for en in self.enemies:
            en.move()
            if self.base[0] < en.x < self.base[0] + self.base[2] and self.base[1] < en.y < self.base[1] + self.base[3]:
                self.enemies.remove(en)
                self.lives -= 1
            if en.health <= 0:
                self.money += 10
                self.enemies.remove(en)

        # base
        if self.lives <= 0:
            self.bulletin_board.receive("GAME OVER")
            self.is_game_over = True

        # selected item
        if self.selected_item:
            self.bulletin_board.receive("Press RIGHT click to cancel")
            self.selected_item.x, self.selected_item.y = x, y

    def draw(self):
        # base
        pygame.draw.rect(self.gamebg, BLACK, pygame.Rect(430, 90, 195, 130), 5)
        # function menu
        self.func_menu.draw(self.win, self.level, self.tech_level, self.lives, self.money)
        # draw tower menu
        self.build_menu.draw(self.win)
        if self.build_menu.upgrade_button.frame:
            self.build_menu.upgrade_button.draw_frame(self.win)
        for name, btn in self.build_menu.tower_buttons.items():
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

    def game_run(self):
        # initialization
        run = True
        clock = pygame.time.Clock()
        pygame.display.set_caption("Covid-19 Defense Game")
        self.game_music()
        while run:
            clock.tick(FPS)
            self.win.blit(self.gamebg, (0, 0))
            x, y = pygame.mouse.get_pos()

            if self.game_paused:
                self.bulletin_board.receive("press SPACE to continue")
            elif self.wave_paused:
                self.bulletin_board.receive("Press y for next wave")

            for event in pygame.event.get():
                # quit game
                if event.type == pygame.QUIT:
                    run = False

                # press action
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        run = False
                    if event.key == pygame.K_SPACE:
                        self.game_paused = not self.game_paused
                    if event.key == pygame.K_y:
                        self.wave_paused = False

                # click action
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.click_action(event, x, y)

            if self.is_game_over:
                continue

            # processing
            if not self.game_paused:
                self.game_processing(x, y)

            # draw all the stuff
            self.draw()

            # post announcement
            self.bulletin_board.post(self.win)
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
        self.path = [PATH_0, PATH_1]

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
                enemies.append(random.choice([Virus(True, self.enemy_health[wave], self.path[wave % 2])]))
            else:
                enemies.append(random.choice([Virus(False, self.enemy_health[wave], self.path[wave % 2])]))


class BulletinBoard:
    def __init__(self):
        self.font_size = 25
        self.font = pygame.font.SysFont("comicsans", self.font_size)
        self.time = time.time() - 1
        self.duration = 1.5
        self.text = ""

    def receive(self, text):
        self.text = text
        self.time = time.time()

    def post(self, win):
        """
        post the announcement until times up
        :param win: window
        :return: None
        """
        if time.time() - self.time < self.duration:
            text_surface = self.font.render(self.text, True, WHITE)
            win.blit(text_surface, (WIDTH//2 - text_surface.get_width()//2, 550))

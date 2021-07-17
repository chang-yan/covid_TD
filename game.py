import pygame
import os
import time
from game_menu.game_menu import FunctionMenu, BuildMenu
from enemies.generator import EnemyGenerator
from towers.builder import VacantLot

pygame.mixer.init()
pygame.font.init()
pygame.init()
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
FPS = 60
WIDTH = 1024
HEIGHT = 600


class Game:
    def __init__(self):
        # screen
        self.win = pygame.display.set_mode((WIDTH, HEIGHT))
        self.gamebg = pygame.transform.scale(pygame.image.load(os.path.join("images", "Map.png")), (WIDTH, HEIGHT))
        # information
        self.money = 2000
        self.lives = 10
        self.tech_level = 0
        self.game_time = time.time()
        self.start_time = time.time()
        # base
        self.base = pygame.Rect(430, 90, 195, 130)
        # main menu
        self.func_menu = FunctionMenu()
        # enemy
        self.wave = 0
        self.enemies = []
        self.enemy_generator = EnemyGenerator()
        # tower
        self.build_menu = BuildMenu()
        self.selected_building= None
        self.towers = []
        self.vacant_lots = [VacantLot(50, 350), VacantLot(180, 250), VacantLot(200, 420), VacantLot(340, 270),
                            VacantLot(400, 450), VacantLot(860, 340), VacantLot(660, 570), VacantLot(680, 330),
                            VacantLot(870, 140)]
        # sound
        self.sound = pygame.mixer.Sound("./sound/sound.flac")
        # announcement
        self.bulletin_board = BulletinBoard()
        # status
        self.game_paused = False
        self.wave_paused = True
        self.is_game_over =  False

    def play_music(self):
        pygame.mixer.music.load("./sound/menu.wav")
        pygame.mixer.music.set_volume(0.2)
        self.sound.set_volume(0.2)
        pygame.mixer.music.play(-1)

    def get_click(self, event, x, y):
        """
        run all that related to "click" action
        """
        if self.func_menu.buttons["muse"].get_touched(x, y):
            pygame.mixer.music.pause()
            self.bulletin_board.receive("MUSIC OFF!")
        elif self.func_menu.buttons["sound"].get_touched(x, y):
            pygame.mixer.music.unpause()
            self.bulletin_board.receive("MUSIC ON!")
        elif self.func_menu.buttons["continue"].get_touched(x, y):
            self.game_paused = False
        elif self.func_menu.buttons["pause"].get_touched(x, y):
            self.game_paused = True

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
                    self.vacant_lots.append(VacantLot(tw.x, tw.y))
                    self.bulletin_board.receive(selling_text)

            # click the upgrade button
            self.tech_level, self.money, tech_upgrade_text = self.build_menu.upgrade_tech_level(x, y, self.tech_level, self.money)
            if tech_upgrade_text:
                self.bulletin_board.receive(tech_upgrade_text)

            # click the build menu
            if event.button == 3:
                self.selected_building = None
            if self.selected_building:
                for vacant in self.vacant_lots:
                    if vacant.in_range(self.selected_building):
                        self.money, new_tower, build_text = self.selected_building.build(self.money, vacant.x, vacant.y)
                        self.towers.append(new_tower)
                        self.bulletin_board.receive(build_text)
                        self.vacant_lots.remove(vacant)
                        break
            self.selected_building = self.build_menu.get_items(x, y)

    def execute(self, x, y):
        # time
        self.game_time = int(time.time() - self.start_time)
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
        if self.selected_building:
            self.bulletin_board.receive("Press RIGHT click to cancel")
            self.selected_building.x, self.selected_building.y = x, y

        #

    def draw(self):
        # base
        pygame.draw.rect(self.gamebg, BLACK, pygame.Rect(430, 90, 195, 130), 5)
        # function menu
        self.func_menu.draw(self.win, self.wave+1, self.tech_level, self.lives, self.money, self.game_time)

        # draw tower menu
        self.build_menu.draw(self.win)
        if self.build_menu.upgrade_button.frame:
            self.build_menu.upgrade_button.draw_frame(self.win)
        for name, btn in self.build_menu.tower_buttons.items():
            if btn.frame:
                btn.draw_frame(self.win)

        # draw selected item
        if self.selected_building:
            self.selected_building.draw(self.win)

        # draw tower
        for tw in self.towers:
            tw.draw(self.win, self.tech_level)

        # draw enemy
        for en in self.enemies:
            en.draw(self.win)

        for v_lot in self.vacant_lots:
            v_lot.draw(self.win)

    def game_run(self):
        # initialization
        run = True
        clock = pygame.time.Clock()
        pygame.display.set_caption("Covid-19 Defense Game")
        self.play_music()
        while run:
            clock.tick(FPS)
            self.win.blit(self.gamebg, (0, 0))
            x, y = pygame.mouse.get_pos()

            if self.wave_paused:
                self.bulletin_board.receive("Press Y for next wave")

            # player action
            for event in pygame.event.get():
                # quit game
                if event.type == pygame.QUIT:
                    run = False
                # press action
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        run = False
                    if event.key == pygame.K_y:
                        self.wave_paused = False
                # click action
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.get_click(event, x, y)

            # computer action
            if self.is_game_over:
                continue
            if not self.game_paused:
                self.execute(x, y)
                # draw all the stuff
                self.draw()
                # post announcement
                self.bulletin_board.post(self.win)
                pygame.display.update()
        pygame.quit()


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

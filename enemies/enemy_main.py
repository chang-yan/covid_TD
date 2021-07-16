import pygame
import math
import os
import time
import random

random.seed()
virus_img1 = pygame.transform.scale(pygame.image.load("./enemies/images/Virus1.png"), (20, 20))
virus_img2 = pygame.transform.scale(pygame.image.load("./enemies/images/Virus.png"), (20, 20))

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
PATH = [PATH_0, PATH_1]


class Enemy:
    def __init__(self, is_mutation, max_health, path_num):
        self.width = 40
        self.height = 48
        self.animation_count = 0
        self.max_health = max_health if is_mutation else max_health//2
        self.health = self.max_health
        self.path = PATH[path_num]
        self.x = self.path[0][0]
        self.y = self.path[0][1]
        self.image = None
        self.images = []
        self.path_pos = 0
        self.money = 0
        self.move_count = 0
        self.is_mutation = is_mutation

    def draw(self, win):
        """
        Draws the enemy with the given images
        :param win: surface
        :return: None
        """
        self.image = self.images[self.animation_count - 1]
        win.blit(self.image, (self.x - self.width//2, self.y - self.height//2))
        self.draw_health_bar(win)
        self.draw_virus_icon(win)

    def move(self):
        """
        Move enemy
        :return: None
        """
        x1, y1 = self.path[self.path_pos]
        if self.path_pos+1 >= len(self.path):
            x2, y2 = self.path[-1][0], self.path[-1][1]-50
        else:
            x2, y2 = self.path[self.path_pos+1]

        # compute the moving direction and steps needed from 1 to 2
        dis = math.sqrt((x2-x1)**2 + (y2-y1)**2)
        dir_x, dir_y = (x2-x1) / dis, (y2-y1) / dis
        count = int(dis)

        # update the new position
        if self.move_count >= count:
            self.move_count = 0
            self.path_pos += 1
            self.x, self.y = self.path[self.path_pos]
        else:
            self.x, self.y = self.x + dir_x, self.y + dir_y
            self.move_count += 1

        # update the animation count
        if self.animation_count >= len(self.images) - 1:
            self.animation_count = 0
        else:
            self.animation_count += 1

    def draw_health_bar(self, win):
        """
        draw health bar above enemy
        :param win: surface
        :return: None
        """
        total_length = 40
        section_length = total_length / self.max_health
        health_bar = section_length * self.health
        pygame.draw.rect(win, (255, 0, 0), [self.x - total_length // 2, self.y - self.height // 2 - 5, total_length, 5], 0)
        if self.is_mutation:
            pygame.draw.rect(win, (147, 0, 147), [self.x - total_length//2, self.y - self.height//2 - 5, health_bar, 5], 0)
        else:
            pygame.draw.rect(win, (0, 255, 0), [self.x - total_length//2, self.y - self.height//2 - 5, health_bar, 5], 0)

    def draw_virus_icon(self, win):
        """
        draw the virus icon above enemy
        :param win: surface
        :return: None
        """
        if self.is_mutation:
            win.blit(virus_img1, (self.x - virus_img1.get_width()//2, self.y - 50))
        else:
            win.blit(virus_img2, (self.x - virus_img2.get_width()//2, self.y - 50))



            
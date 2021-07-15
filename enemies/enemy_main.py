import pygame
import math
import os
import time
import random

random.seed()
virus_img1 = pygame.transform.scale(pygame.image.load("./enemies/images/Virus1.png"), (20, 20))
virus_img2 = pygame.transform.scale(pygame.image.load("./enemies/images/Virus.png"), (20, 20))


class Enemy:
    def __init__(self, is_mutation, max_health, path):
        self.width = 40
        self.height = 48
        self.animation_count = 0
        self.max_health = max_health if is_mutation else max_health//2
        self.health = self.max_health
        self.path = path
        self.x = self.path[0][0]
        self.y = self.path[0][1]
        self.image = None
        self.images = []
        self.path_pos = 0
        self.money = 0
        self.move_count = 0
        self.start_time = 0
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



            
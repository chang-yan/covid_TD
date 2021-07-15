import pygame
import os
from enemies.enemy_main import Enemy
import random 
import time

normal_file_path = "./enemies/images"
mutation_file_path = "./enemies/images/mutation"
normal_images = [pygame.transform.scale(pygame.image.load(os.path.join(normal_file_path, f"{i}.png")), (30, 36)) for i in range(2)]
mutation_images = [pygame.transform.scale(pygame.image.load(os.path.join(mutation_file_path, f"{i}.png")), (30, 36)) for i in range(2, 4)]


class Virus(Enemy):
    def __init__(self, is_mutation, max_health, path):
        super().__init__(is_mutation, max_health, path)
        self.name = "normal_virus"
        self.money = 15
        self.start_time = 0
        self.images = mutation_images[:] if is_mutation else normal_images[:]


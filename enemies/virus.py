import pygame
import os
from enemies.enemy_main import Enemy
import random 
import time

normal_file_path = "./enemies/images"
mutation_file_path = "./enemies/images/mutation"
normal_images = [pygame.transform.scale(pygame.image.load(os.path.join(normal_file_path, f"{i}.png")), (40, 48)) for i in range(2)]
mutation_images = [pygame.transform.scale(pygame.image.load(os.path.join(mutation_file_path, f"{i}.png")), (40, 48)) for i in range(2, 4)]


class Virus(Enemy):
    def __init__(self):
        super().__init__()
        self.name = "normal_virus"
        self.money = 15
        #self.max_health = 5
        self.vel = 100
        self.start_time = 0
        
        count_time = pygame.time.get_ticks() - self.start_time
        
        a = random.random()
        if a <= 0.1:
            self.mutation = 1
            self.max_health = 12 + (count_time//60000)
            self.images = mutation_images[:]
        else: 
            self.mutation = 0
            self.max_health = 7 + (count_time//60000)
            self.images = normal_images[:]
            
        self.health = self.max_health

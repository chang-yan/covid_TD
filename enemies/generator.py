import random
import time
from enemies.virus import Virus

random.seed()


class EnemyGenerator:
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
                enemies.append(Virus(True, self.enemy_health[wave], wave % 2))
            else:
                enemies.append(Virus(False, self.enemy_health[wave], wave % 2))
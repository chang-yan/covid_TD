import pygame
from towers.tower import Pcr, RapidTest, Alcohol



class TowerBuilder:
    def __init__(self, x, y, image, name, market_price):
        self.x = x
        self.y = y
        self.image = image
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.name = name
        self.market_price = market_price

    def draw(self, win):
        win.blit(self.image, (self.x - self.width//2, self.y - self.height//2))

    def build(self, money, x, y):
        """
        if the money is enough to build a tower, build the tower and pay for it
        :param money: int
        :return: (int, tower object)
        """
        notice = None
        if money > self.market_price:
            if self.name == "alcohol":
                built_item = Alcohol(x, y, self.name)
            elif self.name == "rapid test":
                built_item = RapidTest(x, y, self.name)
            else:
                built_item = Pcr(x, y, self.name)

            notice = f"Pay {self.market_price} for {self.name}"
            return money - self.market_price, built_item, notice
        return money, None, notice


class VacantLot:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 30
        self.height = 30
        self.image = pygame.transform.scale(pygame.image.load("towers/tower_images/vacant_lot.png"), (self.width, self.height))

    def in_range(self, building):
        if self.x - self.width//2 < building.x < self.x + self.width//2 \
                and self.y - self.height//2 < building.y < self.y + self.height//2:
            return True
        return False

    def draw(self, win):
        win.blit(self.image, (self.x-self.width//2, self.y-self.height//2))
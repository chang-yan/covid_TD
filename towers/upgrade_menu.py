import pygame

btn_image = {
    "selling": pygame.transform.scale(pygame.image.load("./towers/tower_images/upgrade.png"), (70, 35)),
    "range": pygame.transform.scale(pygame.image.load("./towers/tower_images/range.png"), (30, 30)),
    "damage": pygame.transform.scale(pygame.image.load("./towers/tower_images/damage.png"), (20, 30)),
    "cool down": pygame.transform.scale(pygame.image.load("./towers/tower_images/cool_down.png"), (30, 30)),
}
menu_image = pygame.transform.scale(pygame.image.load("./towers/tower_images/upgrade_menu.png"), (200, 200))


class UpgradeMenu:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.image = menu_image
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.buttons = [Button(self.x, self.y+75, "selling"),
                        Button(self.x, self.y-70, "range"),
                        Button(self.x+69, self.y+6, "damage"),
                        Button(self.x-69, self.y+6, "cool down"),
                        ]

    def is_clicked(self, x, y):
        if (self.x - self.width // 2) < x < (self.x + self.width // 2) \
                and (self.y - self.height // 2) < y < (self.y + self.height // 2):
            return True
        return False

    def draw(self, win):
        win.blit(self.image, (self.x - self.width // 2, self.y - self.height // 2))
        for btn in self.buttons:
            btn.draw(win)

    def get_items(self, x, y):
        for btn in self.buttons:
            if btn.is_clicked(x, y):
                return btn.name


class Button:
    def __init__(self, x, y, name):
        self.x = x
        self.y = y
        self.name = name
        self.image = btn_image[self.name]
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.is_selected = False

    def is_clicked(self, x, y):
        if (self.x - self.width // 2) < x < (self.x + self.width // 2) \
                and (self.y - self.height // 2) < y < (self.y + self.height // 2):
            return True
        return False

    def draw(self, win):
        win.blit(self.image, (self.x - self.width // 2, self.y - self.height // 2))





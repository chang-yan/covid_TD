import pygame

btn_image = {
    "development": pygame.transform.scale(pygame.image.load("./towers/tower_images/upgrade.png"), (70, 35)),
    "range": pygame.transform.scale(pygame.image.load("./towers/tower_images/range.png"), (25, 25)),
    "damage": pygame.transform.scale(pygame.image.load("./towers/tower_images/damage.png"), (15, 25)),
    "cool down": pygame.transform.scale(pygame.image.load("./towers/tower_images/cool_down.png"), (25, 25)),
}
menu_image = pygame.transform.scale(pygame.image.load("./towers/tower_images/upgrade_menu.png"), (150, 150))


class UpgradeMenu:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.image = menu_image
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.is_selected = False
        self.buttons = [Button(self.x, self.y-90, "development"),
                        Button(self.x+1, self.y-52, "range"),
                        Button(self.x+51, self.y+50, "damage"),
                        Button(self.x-49, self.y+50, "cool down"),
                        ]

    def get_clicked(self, mouse_pos):
        x, y = mouse_pos
        if (self.x - self.width // 2) < x < (self.x + self.width // 2) \
                and (self.y - self.height // 2) < y < (self.y + self.height // 2):
            self.is_selected = True
        else:
            self.is_selected = False

    def draw(self, win):
        win.blit(self.image,
                 (self.x - self.width // 2, self.y - self.height // 2))

    def get_items(self, mouse_pos):
        for btn in self.buttons:
            btn.get_clicked(mouse_pos)
            if btn.is_selected:
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

    def get_clicked(self, mouse_pos):
        x, y = mouse_pos
        if (self.x - self.width // 2) < x < (self.x + self.width // 2) \
                and (self.y - self.height // 2) < y < (self.y + self.height // 2):
            self.is_selected = True
        else:
            self.is_selected = False

    def draw(self, win):
        win.blit(self.image,
                 (self.x - self.width // 2, self.y - self.height // 2))





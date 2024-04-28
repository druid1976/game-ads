CELL_SIZE = 25

import pygame


class Mob(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((CELL_SIZE, CELL_SIZE))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def move_towards_player(self, player_rect):
        dx = player_rect.x - self.rect.x
        dy = player_rect.y - self.rect.y
        distance = math.sqrt(dx ** 2 + dy ** 2)
        if distance != 0:
            dx = dx / distance
            dy = dy / distance
        self.rect.x += int(dx * CELL_SIZE)
        self.rect.y += int(dy * CELL_SIZE)
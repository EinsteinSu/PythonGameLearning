import pygame
from pygame.sprite import Sprite


class Bullet(Sprite):
    def __init__(self, mi_settings, screen, ship):
        super(Bullet, self).__init__()
        self.screen = screen
        self.image = pygame.image.load('images\heart.bmp')
        self.rect = self.image.get_rect()
        self.rect.centerx = ship.rect.centerx
        self.rect.top = ship.rect.top

        self.y = float(self.rect.y)
        self.speed_factor = mi_settings.bullet_speed_factor

    def update(self):
        self.y -= self.speed_factor
        self.rect.y = self.y

    def blitme(self):
        self.screen.blit(self.image, self.rect)


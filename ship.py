import pygame
from pygame.sprite import Sprite


class Ship(Sprite):
    def __init__(self, mi_settings, screen):
        super(Ship, self).__init__()
        self.screen = screen
        self.image = pygame.image.load('images/ship.bmp')
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()
        self.mi_settings = mi_settings

        self.rect.centerx = self.screen_rect.centerx
        self.rect.centery = self.screen_rect.centery
        self.rect.bottom = self.screen_rect.bottom
        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False
        self.center = float(self.rect.centerx)
        self.vertical = float(self.rect.centery)

    def blitme(self):
        self.screen.blit(self.image, self.rect)

    def update(self):
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.center += self.mi_settings.ship_speed_factor
        if self.moving_left and self.rect.left > 0:
            self.center -= self.mi_settings.ship_speed_factor
        if self.moving_up and self.rect.top > 0:
            self.vertical -= self.mi_settings.ship_speed_factor
        if self.moving_down and self.rect.bottom < self.screen_rect.bottom:
            self.vertical += self.mi_settings.ship_speed_factor
        self.rect.centerx = self.center
        self.rect.centery = self.vertical

    def center_ship(self):
        self.center = self.screen_rect.centerx
        self.vertical = self.screen_rect.bottom

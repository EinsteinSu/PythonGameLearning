import pygame.font


class StatsBoard():
    def __init__(self, mi_settings, screen):
        self.mi_settings = mi_settings
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.text_color = (40, 40, 40)

        self.font = pygame.font.SysFont(None, 24)
        self.prep_stats()

    def prep_stats(self):
        stats = "ship: " + str(self.mi_settings.ship_speed_factor)
        stats += "; bullet: " + str(self.mi_settings.bullet_speed_factor)
        stats += "; monster: " + str(self.mi_settings.monster_speed_factor)
        self.stats_image = self.font.render(stats, True, self.text_color, self.mi_settings.bg_color)
        self.stats_rect = self.stats_image.get_rect()
        self.stats_rect.left = self.screen_rect.left + 20
        self.stats_rect.top = 20

    def show_stats(self):
        self.screen.blit(self.stats_image, self.stats_rect)

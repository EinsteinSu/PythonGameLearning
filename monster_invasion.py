import pygame
from settings import Settings
from ship import Ship
import game_functions as gf
from pygame.sprite import Group
from gameStats import GameStats
from button import Button
from scoreboard import Scoreboard
from stats_board import StatsBoard


def run_game():
    pygame.init()
    mi_settings = Settings()
    screen = pygame.display.set_mode((mi_settings.screen_width, mi_settings.screen_height))
    ship = Ship(mi_settings, screen)
    stats = GameStats(mi_settings)
    bullets = Group()
    monsters = Group()
    gf.create_fleet(mi_settings, screen, ship, monsters)
    pygame.display.set_caption("Monster Invasion")
    py_button = Button(mi_settings, screen, "Play")
    score_board = Scoreboard(mi_settings, screen, stats)

    while True:
        gf.check_events(mi_settings, stats, screen, ship, monsters, bullets, py_button, score_board)
        if stats.game_active:
            ship.update()
            gf.update_bullets(mi_settings, stats, screen, ship, monsters, bullets, score_board)
            gf.update_monsters(mi_settings, stats, screen, ship, monsters, bullets, score_board)
        gf.update_screen(mi_settings, stats, screen, ship, monsters, bullets, py_button, score_board)


run_game()

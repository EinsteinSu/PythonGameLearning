import sys
import pygame
from bullet import Bullet
from monster import Monster


def keyup_events(event, ship):
    if event.key == pygame.K_UP:
        ship.moving_up = False
    if event.key == pygame.K_DOWN:
        ship.moving_down = False
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False


def keydown_events(event, ai_settings, screen, ship, bullets):
    if event.key == pygame.K_UP:
        ship.moving_up = True
    if event.key == pygame.K_DOWN:
        ship.moving_down = True
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings, screen, ship, bullets)
    elif event.key == pygame.K_q:
        sys.exit()


def fire_bullet(ai_settings, screen, ship, bullets):
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullets = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullets)


def check_events(ai_settings, screen, ship, bullets):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            keydown_events(event, ai_settings, screen, ship, bullets)
        elif event.type == pygame.KEYUP:
            keyup_events(event, ship)


def update_bullets(bullets):
    bullets.update()
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)


def update_screen(ai_settings, screen, ship, monsters, bullets):
    screen.fill(ai_settings.bg_color)
    for bullet in bullets.sprites():
        bullet.blitme()
    ship.blitme()
    monsters.draw(screen)
    # this is important to update the blits
    pygame.display.flip()


def get_number_monsters_x(ai_settings, monster_width):
    available_space_x = ai_settings.screen_width - 2 * monster_width
    number_monsters_x = int(available_space_x / (2 * monster_width))
    return number_monsters_x


def create_monster(ai_settings, screen, monsters, number, row_number):
    monster = Monster(ai_settings, screen)
    monster_width = monster.rect.width
    monster.x = monster_width + 2 * monster_width * number
    monster.rect.x = monster.x
    monster.rect.y = monster.rect.height + 2 * monster.rect.height * row_number
    monsters.add(monster)


def create_fleet(ai_settings, screen, ship, monsters):
    monster = Monster(ai_settings, screen)
    number_monsters_x = get_number_monsters_x(ai_settings, monster.rect.width)
    number_rows = get_number_rows(ai_settings, ship.rect.height, monster.rect.height)
    for row in range(number_rows):
        for number in range(number_monsters_x):
            create_monster(ai_settings, screen, monsters, number, row)


def get_number_rows(ai_settings, ship_height, monster_height):
    available_space_y = (ai_settings.screen_height - (3 * monster_height) - ship_height)
    number_rows = int(available_space_y / (2 * monster_height))
    return number_rows


def update_monsters(monsters):
    monsters.update()

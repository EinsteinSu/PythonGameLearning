import sys
import pygame
from bullet import Bullet
from monster import Monster
from time import sleep


def keyup_events(event, ship):
    if event.key == pygame.K_UP:
        ship.moving_up = False
    if event.key == pygame.K_DOWN:
        ship.moving_down = False
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False


def keydown_events(event, mi_settings, screen, ship, bullets):
    if event.key == pygame.K_UP:
        ship.moving_up = True
    if event.key == pygame.K_DOWN:
        ship.moving_down = True
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(mi_settings, screen, ship, bullets)
    elif event.key == pygame.K_q:
        sys.exit()


def check_play_button(stats, play_button, mouse_x, mouse_y, mi_settings, screen, ship, monsters, bullets, score_board):
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        mi_settings.initialize_dynamic_settings()
        pygame.mouse.set_visible(False)
        stats.reset_stats()
        stats.game_active = True
        monsters.empty()
        bullets.empty()

        score_board.prep_score()
        score_board.prep_high_score()
        score_board.prep_level()
        score_board.prep_ships()
        create_fleet(mi_settings, screen, ship, monsters)
        ship.center_ship()


def fire_bullet(mi_settings, screen, ship, bullets):
    if len(bullets) < mi_settings.bullets_allowed:
        new_bullets = Bullet(mi_settings, screen, ship)
        bullets.add(new_bullets)


def check_events(mi_settings, stats, screen, ship, monsters, bullets, button, score_board):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            keydown_events(event, mi_settings, screen, ship, bullets)
        elif event.type == pygame.KEYUP:
            keyup_events(event, ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(stats, button, mouse_x, mouse_y, mi_settings, screen, ship, monsters, bullets, score_board)


def update_bullets(mi_settings, stats, screen, ship, monsters, bullets, score):
    bullets.update()
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    check_bullets_monster_collisions(mi_settings, stats, screen, ship, monsters, bullets, score)


def check_high_score(stats, score):
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        score.prep_high_score()


def check_bullets_monster_collisions(mi_settings, stats, screen, ship, monsters, bullets, score):
    collisions = pygame.sprite.groupcollide(bullets, monsters, True, True)
    if collisions:
        for monster in collisions.values():
            stats.score += mi_settings.monster_points * len(monster)
            score.prep_score()
        check_high_score(stats, score)
    if len(monsters) == 0:
        # stats_board.prep_stats()
        stats.level += 1
        score.prep_level()
        mi_settings.increase_speed()
        bullets.empty()
        create_fleet(mi_settings, screen, ship, monsters)


def update_screen(mi_settings, stats, screen, ship, monsters, bullets, button, score):
    screen.fill(mi_settings.bg_color)
    if not stats.game_active:
        button.draw_button()
    score.show_score()
    # statsBoard.show_stats()
    for bullet in bullets.sprites():
        bullet.blitme()
    ship.blitme()
    monsters.draw(screen)
    # this is important to update the blits
    pygame.display.flip()


def get_number_monsters_x(mi_settings, monster_width):
    available_space_x = mi_settings.screen_width - 2 * monster_width
    number_monsters_x = int(available_space_x / (2 * monster_width))
    return number_monsters_x


def create_monster(mi_settings, screen, monsters, number, row_number):
    monster = Monster(mi_settings, screen)
    monster_width = monster.rect.width
    monster.x = monster_width + 2 * monster_width * number
    monster.rect.x = monster.x
    monster.rect.y = monster.rect.height + 2 * monster.rect.height * row_number
    monsters.add(monster)


def create_fleet(mi_settings, screen, ship, monsters):
    monster = Monster(mi_settings, screen)
    number_monsters_x = get_number_monsters_x(mi_settings, monster.rect.width)
    number_rows = get_number_rows(mi_settings, ship.rect.height, monster.rect.height)
    for row in range(number_rows):
        for number in range(number_monsters_x):
            create_monster(mi_settings, screen, monsters, number, row)


def get_number_rows(mi_settings, ship_height, monster_height):
    available_space_y = (mi_settings.screen_height - (3 * monster_height) - ship_height)
    number_rows = int(available_space_y / (2 * monster_height))
    return number_rows


def update_monsters(mi_settings, stats, screen, ship, monsters, bullets, score_board):
    check_fleet_edeges(mi_settings, monsters)
    monsters.update()
    if pygame.sprite.spritecollideany(ship, monsters):
        ship_hit(mi_settings, stats, screen, ship, monsters, bullets, score_board)
    check_monster_bottom(mi_settings, stats, screen, ship, monsters, bullets, score_board)


def check_fleet_edeges(mi_settings, monsters):
    for monster in monsters.sprites():
        if monster.check_edges():
            change_fleet_direction(mi_settings, monsters)
            break


def check_monster_bottom(mi_settings, stats, screen, ship, monsters, bullets, score_board):
    screen_rect = screen.get_rect()
    for monster in monsters.sprites():
        if monster.rect.bottom >= screen_rect.bottom:
            ship_hit(mi_settings, stats, screen, ship, monsters, bullets, score_board)
            break


def change_fleet_direction(mi_settings, monsters):
    for monster in monsters.sprites():
        monster.rect.y += mi_settings.fleet_drop_speed
    mi_settings.fleet_direction *= -1


def ship_hit(mi_settings, stats, screen, ship, monsters, bullets, score_board):
    if stats.ship_left > 0:
        stats.ship_left -= 1
        monsters.empty()
        bullets.empty()
        print(stats.ship_left)
        create_fleet(mi_settings, screen, ship, monsters)
        ship.center_ship()
        score_board.prep_ships()
        sleep(0.5)
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)

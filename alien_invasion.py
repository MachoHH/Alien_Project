import pygame

import game_function as gf
from ship import Ship
from settings import Settings
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard
from pygame.sprite import Group


def run_game():
    pygame.init()             #初始化背景设置
    ai_settings = Settings()

    screen = pygame.display.set_mode(
        (ai_settings.screen_width,ai_settings.screen_height))   #设置背景色
    pygame.display.set_caption("Alien Invasion")                #设置游戏名

    play_button = Button(ai_settings, screen, "Play")
    stats = GameStats(ai_settings)
    sb = Scoreboard(ai_settings, screen, stats)
    ship = Ship(ai_settings, screen)
    aliens = Group()                    #创建外星人编组
    bullets = Group()                   #创建子弹编组

    gf.create_fleet(ai_settings, screen, ship, aliens)

    while True:
        gf.check_events(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets)   #鼠标和按键行为
        if stats.game_active:       #游戏开始
            ship.update()                                                                     #更新飞船
            gf.update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets)          #更新子弹
            gf.update_aliens(ai_settings, screen, stats, sb, ship, aliens, bullets)           #更新外星人
        gf.update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets, play_button)  #更新屏幕


run_game()
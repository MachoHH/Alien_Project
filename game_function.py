import sys
import pygame

from time import sleep
from bullet import Bullet
from alien import Alien


def check_keydown_events(event, ai_settings, screen, ship, bullets):   #检测按下按键
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_UP:
        ship.moving_up = True
    elif event.key == pygame.K_DOWN:
        ship.moving_down = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings, screen, ship, bullets)
    elif event.key == pygame.K_q:
        sys.exit()


def check_keyup_events(event, ship):                    #检测松开按键
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False
    elif event.key == pygame.K_UP:
        ship.moving_up = False
    elif event.key == pygame.K_DOWN:
        ship.moving_down = False


def check_events(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets):  #检测按键行为
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y, = pygame.mouse.get_pos()
            check_play_button(ai_settings, screen, stats, sb, play_button, ship,
                              aliens, bullets, mouse_x, mouse_y)
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, ship, bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)


def check_play_button(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets, mouse_x, mouse_y):
        button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)    #True or False
        if button_clicked and not stats.game_active:    #当点击了Play且游戏处于非活动状态时，才重新开始
            ai_settings.initialize_dynamic_settings()   #重置速度
            pygame.mouse.set_visible(False)             #隐藏光标
            stats.reset_stats()        #重置游戏信息
            stats.game_active = True
            sb.prep_score()            #重置记分牌
            sb.prep_high_score()
            sb.prep_level()
            sb.prep_ships()
            aliens.empty()             #清空
            bullets.empty()
            create_fleet(ai_settings, screen, ship, aliens)
            ship.center_ship()


def update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets, play_button):
    screen.fill(ai_settings.bg_color)   #背景色填充
    for bullet in bullets.sprites():    #绘制子弹
        bullet.draw_bullet()
    ship.blitme()                       #绘制飞船
    aliens.draw(screen)                 #绘制外星人
    sb.show_score()                     #显示得分
    if not stats.game_active:           #绘制按钮
        play_button.draw_button()
    pygame.display.flip()               #更新屏幕


def fire_bullet(ai_settings, screen, ship, bullets):
    if len(bullets) < ai_settings.bullets_allowed:       #限制子弹数，小于限制数才会创建新子弹
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)


def check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens, bullets):
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)  #检测子弹和外星人碰撞
    if collisions:
        for aliens in collisions.values():
            stats.score += ai_settings.alien_points * len(aliens)
            sb.prep_score()
        check_high_score(stats, sb)
    if len(aliens) == 0:                                 #若外星人消灭完了
        bullets.empty()                                  #删除现有的子弹
        ai_settings.increase_speed()                     #加速
        stats.level += 1                                 #升级
        sb.prep_level()
        create_fleet(ai_settings, screen, ship, aliens)  #重新创建一批外星人


def check_high_score(stats, sb):
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()


def update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets):
    bullets.update()
    for bullet in bullets.copy():              #遍历编组的副本，在循环中修改bullets
        if bullet.rect.bottom <= 0:            #若子弹移出屏幕
            bullets.remove(bullet)             #将其从编组中删除
    check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens, bullets)


def check_fleet_edges(ai_settings, aliens):
    for alien in aliens.sprites():
        if alien.check_edges():                 #若外星人到达左右边缘，下移并改变运动方向
            change_fleet_direction(ai_settings, aliens)
            break                               #退出for循环


def change_fleet_direction(ai_settings, aliens):
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed        #外星人下移
    ai_settings.fleet_direction *= -1                       #改变移动方向


def update_aliens(ai_settings, screen, stats, sb, ship, aliens, bullets):
    check_fleet_edges(ai_settings, aliens)              #检测是否有外星人到达边缘
    aliens.update()                                     #更新外星人位置
    if pygame.sprite.spritecollideany(ship, aliens):    #若外星人撞到飞船
        ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets)
    check_aliens_bottom(ai_settings, screen, stats, sb, ship, aliens, bullets)


def check_aliens_bottom(ai_settings, screen, stats, sb, ship, aliens, bullets):
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:     #若外星人到达底部
            ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets)
            break


def ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets):
    if stats.ships_left > 0:
        stats.ships_left -= 1                           #飞船数减1
        sb.prep_ships()
        aliens.empty()                                  #清空外星人
        bullets.empty()                                 #清空子弹
        create_fleet(ai_settings, screen, ship, aliens) #重新创建一批外星人
        ship.center_ship()                              #将飞船置于屏幕底端中央
        sleep(0.5)                                      #暂停
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)          #游戏结束，显示光标


def get_number_aliens_x(ai_settings, alien_width):
    available_space_x = ai_settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x        #返回每行外星人数


def get_number_rows(ai_settings, ship_height, alien_height):
    available_space_y = (ai_settings.screen_height - (3 * alien_height) - ship_height)
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows            #返回外星人行数


def create_fleet(ai_settings, screen, ship, aliens):
    alien = Alien(ai_settings, screen)
    number_alien_x = get_number_aliens_x(ai_settings, alien.rect.width)
    number_rows = get_number_rows(ai_settings, ship.rect.height, alien.rect.height)
    for row_number in range(number_rows):
        for alien_number in range(number_alien_x):
            create_alien(ai_settings, screen, aliens, alien_number, row_number)


def create_alien(ai_settings, screen, aliens, alien_number, row_number):
    alien = Alien(ai_settings, screen)                        #创建一个外星人
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number    #计算各外星人x坐标
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number   #计算各行外星人y坐标
    aliens.add(alien)                                                       #加入编组
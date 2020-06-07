import pygame.font
from pygame.sprite import Group

from ship import Ship


class Scoreboard():
    def __init__(self, ai_settings, screen, stats):
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.ai_settings = ai_settings
        self.stats = stats

        self.text_color = (30, 30, 30)              #得分颜色
        self.font = pygame.font.SysFont(None, 48)   #默认字体，48字号

        self.prep_score()       #当前得分
        self.prep_high_score()  #最高分
        self.prep_level()       #等级
        self.prep_ships()       #剩余飞船

    def prep_score(self):
        rounded_score = int(round(self.stats.score, -1))    #将分数圆整到最近的10的倍数
        score_str = "{:,}".format(rounded_score)            #将数字转化为字符串时在其中插入逗号
        self.score_image = self.font.render(score_str, True, self.text_color, self.ai_settings.bg_color)
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20     #距离右边缘20像素
        self.score_rect.top = 20                                #距离上边缘20像素

    def prep_high_score(self):
        high_score = int(round(self.stats.high_score, -1))
        high_score_str = "{:,}".format(high_score)
        self.high_score_image = self.font.render(high_score_str, True, self.text_color, self.ai_settings.bg_color)
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.score_rect.top

    def prep_level(self):
        self.level_image = self.font.render(str(self.stats.level), True, self.text_color, self.ai_settings.bg_color)
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.score_rect.right
        self.level_rect.top = self.score_rect.bottom + 10

    def prep_ships(self):
        self.ships = Group()
        for ship_number in range(self.stats.ships_left):
            ship = Ship(self.ai_settings, self.screen)
            ship.rect.x = 10 + ship_number * ship.rect.width
            ship.rect.y = 10
            self.ships.add(ship)

    def show_score(self):
        self.screen.blit(self.score_image, self.score_rect)             #显示得分
        self.screen.blit(self.high_score_image, self.high_score_rect)   #显示最高分
        self.screen.blit(self.level_image, self.level_rect)             #显示等级
        self.ships.draw(self.screen)
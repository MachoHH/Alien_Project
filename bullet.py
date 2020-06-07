import pygame

from pygame.sprite import Sprite


class Bullet(Sprite):
    def __init__(self, ai_settings, screen, ship):
        super(Bullet, self).__init__()           #super()继承Sprite
        self.screen = screen
        self.rect = pygame.Rect(0, 0, ai_settings.bullet_width,   #从空白创建一个矩形
                                ai_settings.bullet_height)
        self.rect.centerx = ship.rect.centerx       #子弹初始位置取决于飞船位置
        self.rect.top = ship.rect.top

        self.color = ai_settings.bullet_color                #子弹颜色
        self.speed_factor = ai_settings.bullet_speed_factor  #子弹速度
        self.y = float(self.rect.y)                          #子弹y坐标

    def update(self):
        self.y -= self.speed_factor                          #子弹移动
        self.rect.y = self.y

    def draw_bullet(self):
        pygame.draw.rect(self.screen,self.color,self.rect)   #绘制子弹
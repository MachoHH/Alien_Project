import pygame
from pygame.sprite import Sprite


class Ship(Sprite):
    def __init__(self, ai_settings, screen):
        super(Ship, self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings

        self.image = pygame.image.load('images/ship.bmp')    #加载图像
        self.rect = self.image.get_rect()                    #获取飞船相应属性
        self.screen_rect = self.screen.get_rect()            #获取屏幕相应属性
        self.rect.centerx = self.screen_rect.centerx         #飞船中心设置为屏幕中心
        self.rect.bottom = self.screen_rect.bottom          #飞船下边缘设置为屏幕属性bottom

        self.centerxx = float(self.rect.centerx)
        self.centeryy = float(self.rect.bottom)

        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False

    def update(self):
        if self.moving_right and self.rect.right < self.screen_rect.right: #右方向键按下且未触及屏幕右边缘
            self.centerxx += self.ai_settings.ship_speed_factor            #向右移
        if self.moving_left and self.rect.left > 0:                        #左方向键按下且未触及屏幕左边缘
            self.centerxx -= self.ai_settings.ship_speed_factor            #向左移
        if self.moving_up and self.rect.top > 0:                           #上方向键按下且未触及屏幕上边缘
            self.centeryy -= self.ai_settings.ship_speed_factor            #向上移
        if self.moving_down and self.rect.bottom < self.screen_rect.bottom:#下方向键按下且未触及屏幕下边缘
            self.centeryy += self.ai_settings.ship_speed_factor            #向下移
        self.rect.centerx = self.centerxx
        self.rect.bottom = self.centeryy

    def blitme(self):
        self.screen.blit(self.image,self.rect)      #将飞船图像绘制到屏幕上

    def center_ship(self):
        self.centerxx = self.screen_rect.centerx
        self.centeryy = self.screen_rect.bottom       #将飞船置于底部中央
class Settings():
    def __init__(self):
        self.screen_width = 1200          #设置屏幕大小
        self.screen_height = 800
        self.bg_color = (230, 230, 230)   #设置屏幕背景色
        self.ship_limit = 2               #飞船数
        self.bullet_width = 10             #子弹设置
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)
        self.bullets_allowed = 5
        self.fleet_drop_speed = 10        #外星人向下移动速度
        self.speedup_scale = 1.1          #加快游戏速度
        self.score_scale = 1.5            #外星人点数加倍
        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        self.ship_speed_factor = 1.5      #飞船移动速度
        self.bullet_speed_factor = 3      #子弹速度
        self.alien_speed_factor = 1       #外星人左右移动速度
        self.fleet_direction = 1          #1代表向右移，-1代表向左移
        self.alien_points = 50            #外星人点数

    def increase_speed(self):    #提高速度
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale
        self.alien_points = int(self.alien_points * self.score_scale)
        print(self.alien_points)    #终端窗口显示点数值

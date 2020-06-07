import pygame.font


class Button():
    def __init__(self, ai_settings, screen, msg):
        self.screen = screen
        self.screen_rect = screen.get_rect()

        self.width, self.height = 200, 50                       #按钮尺寸
        self.button_color = (0, 255, 0)                         #按钮颜色
        self.text_color = (255, 255, 255)                       #文字颜色
        self.font = pygame.font.SysFont(None, 48)               #默认字体，48字号
        self.rect = pygame.Rect(0, 0, self.width, self.height)  #按钮属性
        self.rect.center = self.screen_rect.center

        self.prep_msg(msg)                                      #将字符串渲染为图像

    def prep_msg(self, msg):                    #布尔参数True开启反锯齿功能
        self.msg_image = self.font.render(msg, True, self.text_color, self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        self.screen.fill(self.button_color, self.rect)          #绘制按钮矩形
        self.screen.blit(self.msg_image, self.msg_image_rect)   #绘制文本图像
class GameStats():
    def __init__(self,ai_settings):
        self.ai_settings = ai_settings
        self.reset_stats()          #初始化游戏信息
        self.game_active = False    #飞船用完后变为False
        self.high_score = 0         #最高分，不重置

    def reset_stats(self):
        self.ships_left = self.ai_settings.ship_limit
        self.score = 0      #初始分数
        self.level = 1      #初始等级
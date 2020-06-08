class Player:
    def __init__(self, uuid, hypixel_id, display_name, first_login, last_login, last_logout, xp, stats, achievements,
                 one_time_achievements):
        self.UUID = uuid
        self.HYPIXEL_ID = hypixel_id
        self.DISPLAY_NAME = display_name
        self.FIRST_LOGIN = first_login
        self.LAST_LOGIN = last_login
        self.LAST_LOGOUT = last_logout
        self.XP = xp
        self.STATS = stats
        self.ACHIEVEMENTS = achievements
        self.ONE_TIME_ACHIEVEMENTS = one_time_achievements


class Player:

    def __init__(self, uuid, hypixel_id, display_name, first_login, last_login, last_logout, exp, stats, achievements,
                 one_time_achievements, karma, prefix, rank, time_playing, guild):
        """A base class for a hypixel player that contains only the most important data"""
        self.UUID = uuid
        self.HYPIXEL_ID = hypixel_id
        self.DISPLAY_NAME = display_name
        self.FIRST_LOGIN = first_login
        self.LAST_LOGIN = last_login
        self.LAST_LOGOUT = last_logout
        self.EXP = exp
        self.STATS = stats
        self.ACHIEVEMENTS = achievements
        self.ONE_TIME_ACHIEVEMENTS = one_time_achievements
        self.KARMA = karma
        self.PREFIX = prefix
        self.RANK = rank
        self.TIME_PLAYING = time_playing
        self.GUILD = guild

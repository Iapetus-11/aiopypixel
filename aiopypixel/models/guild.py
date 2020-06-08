
class Guild:

    def __init__(self, id, name, coins, created, exp, description, preferred_games, tag, members):
        """Base class for the most import guild data"""
        self.ID = id
        self.NAME = name
        self.COINS = coins
        self.CREATED = created
        self.EXP = exp
        self.DESCRIPTION = description
        self.PREFERRED_GAMES = preferred_games
        self.TAG = tag
        self.MEMBERS = members

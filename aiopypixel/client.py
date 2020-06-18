from .exceptions.exceptions import *
from .models.player import Player
from .models.guild import Guild
from random import choice
from typing import Union
import aiohttp
import asyncio


class Client:

    def __init__(self, api_keys: Union[list, str]):
        """basic initialization of the hypixel API client"""

        # Handles the instance of a singular key
        if not isinstance(api_keys, list):
            api_keys = [api_keys]

        self.API_KEYS = api_keys

        self.BASE_URL = 'https://api.hypixel.net/'

        self.session = aiohttp.ClientSession()

    async def close(self):
        """used for safe client cleanup and stuff"""
        await self.session.close()

    async def get(self, url: str) -> dict:
        """base method to fetch a response from hypixel"""

        response = await self.session.get(f"{self.BASE_URL}" + url.replace("api_key", choice(self.API_KEYS)))

        if response.status == 429:
            raise RateLimitError("Hypixel")

        return await response.json()

    async def usernameToUUID(self, username: str) -> str:
        """takes in an mc username and tries to convert it to a mc uuid"""

        response = await self.session.post("https://api.mojang.com/profiles/minecraft", json=[username])

        data = await response.json()

        if response.status == 204 or data == []:
            raise InvalidPlayerError("Invalid username was supplied!")

        return data[0]["id"]

    async def UUIDToUsername(self, uuid: str) -> str:
        """takes in a minecraft UUID and converts it to a minecraft username"""

        data = await self.session.get(f"https://api.mojang.com/user/profiles/{uuid}/names")

        if data.status == 204:
            raise InvalidPlayerError("Invalid UUID was supplied!")

        data = await data.json()

        data = data.get(len(data) - 1)

        if data is None:
            raise InvalidPlayerError("Something went wrong!")

        return data["name"]

    async def getKeyData(self, key: str = None) -> dict:
        """fetches information from the api about the key used
        uses a random key if none is specified"""

        if key is None:
            key = choice(self.API_KEYS)

        data = await self.get(f"key?key={key}")

        if not data["status"]:
            raise Error(f"An error occurred while fetching information on a key! ({data.get('cause')})")

        return data

    async def getPlayerRaw(self, player) -> dict:
        """returns a player's data from the api"""

        if len(player) <= 16:
            player = await self.usernameToUUID(player)

        data = await self.get(f"player?key=api_key&uuid={player}")

        if not data["success"]:
            raise Error(f"An error occurred while fetching a player from the api! ({data.get('cause')})")

        if data["player"] is None:
            raise NullPlayerError

        return data["player"]

    async def getPlayer(self, player) -> Player:
        """returns a player object"""

        raw_player = await self.getPlayerRaw(player)

        return Player(
            raw_player["uuid"],
            raw_player["_id"],
            raw_player["displayname"],
            raw_player["firstLogin"],
            raw_player["lastLogin"],
            raw_player["lastLogout"],
            raw_player["networkExp"],
            raw_player["stats"],
            raw_player["achievements"],
            raw_player["achievementsOneTime"],
            await self.getPlayerGuild(player)
        )

    async def getPlayerFriends(self, player: str) -> list:
        """returns the friends list of the provided player (list of uuids)
        if the user doesn't have any friends, returns an empty list"""

        if len(player) < 17:
            player = await self.usernameToUUID(player)

        data = await self.get(f"friends?key=api_key&uuid={player}")

        if not data["success"]:
            raise Error(f"Error while getting player friends! ({data.get('cause')})")

        uuids = []

        for record in data["records"]:
            if record["uuidSender"] != player:
                uuids.append(record["uuidSender"])
            else:
                uuids.append(record["uuidReceiver"])
        return uuids

    async def getPlayerGuild(self, player: str) -> str:
        """returns the guild id (if any) of that which the provided player is in
        returns None if the user doesn't have a guild"""

        if len(player) <= 16:
            player = await self.usernameToUUID(player)

        data = await self.get(f"findGuild?key=api_key&byUuid={player}")

        if not data["success"]:
            raise InvalidGuildError(data.get('cause'))

        return data["guild"]

    async def getGuildIDByName(self, guild_name: str) -> str:
        """fetches a hypixel guild id based on the given guild name"""

        data = await self.get(f"guild?key=api_key&name={guild_name}")

        if not data["success"]:
            raise InvalidGuildError(data.get('cause'))

        if data["guild"] is None:
            raise InvalidGuildError("Guild not found!")

        return data["guild"]["_id"]

    async def getGuildNameByID(self, guild_id: str) -> str:
        """fetches a hypixel guild name based on the given guild id"""

        data = await self.get(f"guild?key=api_key&id={guild_id}")

        if not data["success"]:
            raise InvalidGuildError(data.get('cause'))

        if data["guild"] is None:
            raise InvalidGuildError("Guild not found!")

        return data["guild"]["name"]

    async def getGuildDataRaw(self, guild_id: str) -> dict:
        """fetches a hypixel guild based on the given guild id"""

        data = await self.get(f"guild?key=api_key&id={guild_id}")

        if not data["success"]:
            raise InvalidGuildError(data.get('cause'))

        if data["guild"] is None:
            raise InvalidGuildError("Guild not found!")

        return data["guild"]

    async def getGuildData(self, guild_id: str) -> Guild:
        """returns a guild object"""

        raw_guild = await self.getGuildDataRaw(guild_id)

        return Guild(
            raw_guild.get('_id'),
            raw_guild.get('name'),
            raw_guild.get('coins'),
            raw_guild.get('created'),
            raw_guild.get('exp'),
            raw_guild.get('description'),
            raw_guild.get('preferredGames'),
            raw_guild.get('tag'),
            raw_guild.get('members')
        )

    async def getGameCounts(self) -> dict:
        """fetches the player counts for every game on hypixel"""

        data = await self.get(f"gameCounts?key=api_key")

        if not data["success"]:
            raise Error(data.get('cause'))

        return data

    async def getLeaderboard(self) -> dict:
        data = await self.get('leaderboards?key=api_key')

        return data

    async def getWatchdogStats(self) -> dict:
        data = await self.get(f"watchdogstats?key=api_key")

        return data

    async def calcPlayerLevel(self, xp) -> int:
        return int(1 + (-8750. + (8750 ** 2 + 5000 * xp) ** .5) / 2500)

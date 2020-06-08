from .exceptions.exceptions import *
from random import choice
from typing import Union
import aiohttp
import asyncio
import time


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

    async def UsernameToUUID(self, username: str) -> str:
        """takes in an mc username and tries to convert it to a mc uuid"""

        response = await self.session.get(
            f"https://api.mojang.com/users/profiles/minecraft/{username}?at={int(time.time())}")
        data = await response.json()

        if response.status == 204:
            raise InvalidPlayerError("Invalid username was supplied!")

        return data["id"]

    async def UUIDToUsername(self, uuid: str) -> str:
        """takes in a minecraft UUID and converts it to a minecraft username"""

        data = await self.session.get(f"https://api.mojang.com/user/profiles/{uuid}")

        if data.status == 400:
            raise InvalidPlayerError("Invalid UUID was supplied!")

        return (await data.json())["name"]

    async def getKeyData(self, key: str = None) -> dict:
        """fetches information from the api about the key used
        uses a random key if none is specified"""

        if key is None:
            key = choice(self.API_KEYS)

        data = await self.get(f"key?key={key}")

        if not data["success"]:
            raise Error(f"An error occured while fetching information on a key! ({data.get('cause')})")

        return data

    async def getPlayerRaw(self, player) -> dict:
        """returns a player object"""

        data = await self.get(f"player?key=api_key&uuid=")

    async def getPlayerFriends(self, player: str) -> list:
        """returns the friends list of the provided player (list of uuids)
        if the user doesn't have any friends, returns an empty list"""

        if len(player) < 17:
            player = await self.UsernameToUUID(player)

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
        """returns the guild id (if any) of that which the provided player is in"""

        if len(player) <= 16:
            player = await self.UsernameToUUID(player)

        data = await self.get(f"findGuild?key=api_key&byUuid={player}")

        if not data["success"]:
            raise Error(f"Error while getting player guild! ({data.get('cause')})")

        return data["guild"]

    async def getGuildID(self, guild_name: str) -> str:
        """fetches a hypixel guild id based on the given guild name"""

        data = await self.get(f"guild?key=api_key&name={guild_name}")

        if not data["success"]:
            raise Error(f"An unknown error occurred! ({data.get('cause')})")

        if data["guild"] is None:
            raise Error("Guild not found!")

        return data["guild"]["_id"]

    async def getGuildName(self, guild_id: str) -> str:
        """fetches a hypixel guild name based on the given guild id"""

        data = await self.get(f"guild?key=api_key&name={guild_id}")

        if not data["success"]:
            raise Error(f"An unknown error occurred ({data.get('cause')})!")

        if data["guild"] is None:
            raise Error("Guild not found!")

        return data["guild"]["name"]

    async def getGuildData(self, guild_id: str) -> dict:
        """fetches a hypixel guild based on the given guild id"""

        data = await self.get(f"guild?key=api_key&name={guild_id}")

        if not data["success"]:
            raise Error(data.get('cause'))

        if data["guild"] is None:
            raise Error("Guild not found!")

        return data["guild"]

    async def getGameCounts(self) -> dict:
        """fetches the player counts for every game on hypixel"""

        data = await self.get(f"gameCounts?key=api_key")

        if not data["success"]:
            raise Error(data.get('cause'))

        return data

    async def getRank(self, player: str) -> dict:
        """returns the provided player's hypixel rank"""

        if len(player) < 16:
            player = await self.UsernameToUUID(player)

        data = await self.get(f"{self.BASE_URL}/player?key={{api_key}}&name={player}")

        return data

    async def getLeaderboard(self) -> dict:

        data = await self.get('leaderboards?key=api_key')

        return data

    async def getWatchdogStats(self) -> dict:

        data = await self.get(f"watchdogstats?key=api_key")

        return data

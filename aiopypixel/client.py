from .exceptions.exceptions import *
import aiohttp
import asyncio
from random import choice


class Client:
    def __init__(self, api_keys):
        # Handles the instance of a singular key
        if not isinstance(api_keys, list):
            api_keys = [api_keys]

        self.API_KEYS = api_keys

        self.BASE_URL = 'https://api.hypixel.net/'

        self.session = aiohttp.ClientSession()

    async def close(self):
        """Used for safe client cleanup and stuff"""
        await self.session.close()

    async def get(self, url: str) -> dict:
        """base method to fetch a response from hypixel"""

        response = await self.session.get(f"{self.BASE_URL}" + url.replace("api_key", choice(self.API_KEYS)))

        if response.status == 429:
            raise RateLimited("Hypixel")

        return await response.json()

    async def GamertagToUUID(self, gamertag) -> str:
        """takes in an mc gamertag and tries to convert it to a mc uuid"""

        response = await self.session.get("https://api.mojang.com/profiles/minecraft", json=[gamertag])
        data = await response.json()

        if response.status == 204:
            raise InvalidPlayerError("Invalid gamertag was supplied!")

        return j[0]["id"]

    async def UUIDToGamertag(self, uuid) -> str:
        """takes in an mc uuid and converts it to an mc gamertag"""

        data = await self.session.get(f"https://api.mojang.com/user/profiles/{uuid}")

        if data.status == 400:
            raise InvalidPlayerError("Invalid uuid was supplied!")

        return (await data.json())["name"]

    async def getKeyData(self, key=None):
        """fetches information from the api about the key used
        uses a random key if none is specified"""

        if key is None:
            key = choice(self.API_KEYS)

        data = await self.get(f"key?key={key}")

        if not data["status"]:
            raise Error(f"An error occured while fetching information on a key! ({data.get('cause')})")

    async def getPlayerFriends(self, player) -> list:
        """returns the friends list of the provided player (list of uuids)
        if the user doesn't have any friends, returns an empty list"""

        if len(player) < 17:
            player = await self.GamertagToUUID(player)

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

    async def getPlayerGuild(self, player) -> str:
        """returns the guild id (if any) of that which the provided player is in"""

        if len(player) < 17:
            player = await self.GamertagToUUID(player)

        data = await self.get(f"findGuild?key=api_key&byUuid={player}")

        if not data["success"]:
            raise Error(f"Error while getting player guild! ({data.get('cause')})")

        return data["guild"]

    async def getGuildID(self, guild_name):
        """fetches a hypixel guild id based on the given guild name"""

        data = await self.get(f"guild?key=api_key&name={guild_name}")

        if not data["success"]:
            raise Error(f"An unknown error occurred! ({data.get('cause')})")

        if data["guild"] is None:
            raise Error("Guild not found!")

        return data["guild"]["_id"]

    async def getGuildName(self, guild_id):
        """fetches a hypixel guild name based on the given guild id"""

        data = await self.get(f"guild?key=api_key&name={guild_id}")

        if not data["success"]:
            raise Error(f"An unknown error occurred ({data.get('cause')})!")

        if data["guild"] is None:
            raise Error("Guild not found!")

        return data["guild"]["_id"]

    async def getGuildData(self, guild_id):
        """fetches a hypixel guild based on the given guild id"""

        data = await self.get(f"guild?key=api_key&name={guild_id}")

        if not data["success"]:
            raise Error(f"An unknown error occurred! ({data.get('cause')})")

        if data["guild"] is None:
            raise Error("Guild not found!")

        return data["guild"]

    async def getPlayerCounts(self):
        """fetches the player counts for every game on hypixel"""

        data = await self.get(f"gameCounts?key=api_key")

        if not data["success"]:
            raise Error(f"An unknown error occurred! ({data.get('cause')})")

        return data

    async def getRank(self, player):  # still a wip
        """returns the provided player's hypixel rank"""

        if len(player) < 16:
            player = await self.name_to_uuid(player)

        data = await (await self.get(f"{self.BASE_URL}/player?key=api_key&name={player}")).json()

        return data

from typing import Union
import aiohttp
import asyncio
from random import choice


class RateLimited(Exception):
    def __init__(self, specifics, message="You're being rate limited! ({0})"):
        self.message = message.format(specifics)
        super().__init__(self.message)

    def __str__(self):
        return self.message


class Error(Exception):
    def __init__(self, message="An error occurred!", cause="unknown"):
        self.message = message + "\nCause: " + str(cause)
        super().__init__(self.message)

    def __str__(self):
        return self.message


class Client:
    def __init__(self, api_keys):
        # Handles the instance of a singular key
        if not isinstance(api_keys, list):
            api_keys = [api_keys]

        self.API_KEYS = api_keys

        self.BASE_URL = 'https://api.hypixel.net/'

        self.session = aiohttp.ClientSession()

    async def close(self):
        # Safe client cleanup and exit
        await self.session.close()

    async def get(self, url: str) -> dict:
        """base method to fetch api response"""

        response = await self.session.get(f"{self.BASE_URL}" + url.replace("api_key", choice(self.API_KEYS)))

        if response.status == 429:
            raise RateLimited("Hypixel")

        return await response.json()

    async def GamertagToUUID(self, gamertag) -> str:
        """takes in an mc gamertag and tries to convert it to a mc uuid"""

        data = await self.session.get("https://api.mojang.com/profiles/minecraft", json=[gamertag])
        data = await data.json()

        if not data:
            raise Error("An error occurred while converting gamertag to uuid!", "User couldn't be found!")

        return j[0]["id"]

    async def UUIDToGamertag(self, uuid) -> str:
        """takes in an mc uuid and converts it to an mc gamertag"""

        data = await self.session.get(f"https://api.mojang.com/user/profiles/{uuid}/names")

        if data.status == 204:
            raise Error("An error occurred while converting uuid to gamertag!", "User couldn't be found!")

        return (await data.json())[len(j) - 1]["name"]

    async def getKeyData(self, key=None):
        """fetches information from the api about the key used
        uses a random key if none is specified"""

        if key is None:
            key = choice(self.API_KEYS)

        data = await self.get(f"key?key={key}")

        if not data["status"]:
            raise Error("An error occured while fetching information on a key!", data.get("cause"))

    async def getPlayerFriends(self, player) -> list:
        """returns the friends list of the provided player (list of uuids)
        if the user doesn't have any friends, returns an empty list"""

        if len(player) < 17:
            player = await self.GamertagToUUID(player)

        data = await self.get(f"friends?key=api_key&uuid={player}")

        if not data["success"]:
            raise Error("Error while getting player friends!", data.get("cause"))

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
            raise Error("Error while getting player guild!", data.get("cause"))

        return data["guild"]

    async def getGuildID(self, guild_name):
        """fetches a hypixel guild id based on the given guild name"""

        data = await self.get(f"guild?key=api_key&name={guild_name}")

        if not data["success"]:
            raise Error("An unknown error occurred!", data.get("cause"))

        if data["guild"] is None:
            raise Error("Guild not found!", "The API returned null!")

        return data["guild"]["_id"]

    async def getGuildName(self, guild_id):
        """fetches a hypixel guild name based on the given guild id"""

        data = await self.get(f"guild?key=api_key&name={guild_id}")

        if not data["success"]:
            raise Error("An unknown error occurred!", data.get("cause"))

        if data["guild"] is None:
            raise Error("Guild not found!", "The API returned null!")

        return data["guild"]["_id"]

    async def getGuildData(self, guild_id):
        """fetches a hypixel guild based on the given guild id"""

        data = await self.get(f"guild?key=api_key&name={guild_id}")

        if not data["success"]:
            raise Error("An unknown error occurred!", data.get("cause"))

        if data["guild"] is None:
            raise Error("Guild not found!", "The API returned null!")

        return data["guild"]

    async def getPlayerCounts(self):
        """fetches the player counts for every game on hypixel"""

        data = await self.get(f"gameCounts?key=api_key")

        if not data["success"]:
            raise Error("An unknown error occurred!", data.get("cause"))

        return data

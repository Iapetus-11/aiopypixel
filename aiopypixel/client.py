from typing import Union
import aiohttp
import asyncio
import random


class RateLimited(Exception):
    def __init__(self, message="[429] You're being rate limited!"):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return self.message


class PlayerNotFound(Exception):
    def __init__(self, specifics, message="That player couldn't be found! ({0})"):
        self.message = message.format(specifics)
        super().__init__(self.message)

    def __str__(self):
        return self.message


class Client:
    def __init__(self, api_keys):
        # Handles the instance of a singular key
        if not isinstance(api_keys, list):
            api_keys = [api_keys]

        self.API_KEYS = api_keys

        self.BASE_URL = 'https://api.hypixel.net'

        self.session = aiohttp.ClientSession()

    async def close(self):
        # Safe client cleanup and exit
        await self.session.close()

    async def get(self, url: str) -> dict:
        """base method to fetch api response"""

        response = await self.session.get(url.replace("api_key", random.choice(self.API_KEYS)))

        if response.status == 429:
            raise RateLimited

        return await response.json()

    async def GamertagToUUID(self, gamertag) -> str:
        """takes in an mc gamertag and tries to convert it to a mc uuid"""
        data = await self.session.get("https://api.mojang.com/profiles/minecraft", json=[gamertag])
        data = await data.json()

        if not data:
            raise PlayerNotFound("Error while converting gamertag to uuid!")

        return j[0]["id"]

    async def UUIDToGamertag(self, uuid) -> str:
        """takes in an mc uuid and converts it to an mc gamertag"""
        data = await self.session.get(f"https://api.mojang.com/user/profiles/{uuid}/names")

        if data.status == 204:
            raise PlayerNotFound("Error while converting uuid to gamertag!")

        return (await data.json())[len(j) - 1]["name"]

    async def getFriends(self, player) -> list:
        """returns the friends list of the provided player (list of uuids)
        if the user doesn't have any friends, returns an empty list"""

        if len(player) < 16:

        data = await self.get(f"{self.BASE_URL}/friends?key=api_key&uuid={player}")

        if not data["success"]:
            return False  # raise error later

        uuids = []

        for record in data["records"]:
            if record["uuidSender"] != player:
                uuids.append(record["uuidSender"])
            else:
                uuids.append(record["uuidReceiver"])
        return uuids

    async def getGuildFromID(self, guild_id):
        data = await self.get(f"{self.BASE_URL}/friends?key=api_key&id={guild_id}")

    async def getRank(self, player):
        return await self.get(f"{self.BASE_URL}/player?key=api_key&name={player}")

from .exceptions.exceptions import *
from typing import Union
import aiohttp
import asyncio
import random


class Client:

    def __init__(self, api_keys):
        """basic initalization of the Hypixel API Client"""

        # Handles the instance of a singular key
        if not isinstance(api_keys, list):
            api_keys = [api_keys]

        self.API_KEYS = api_keys
        self.session = aiohttp.ClientSession()
        self.BASE_URL = 'https://api.hypixel.net'

    async def exit(self):
        """safe cleanup and exit"""
        await self.session.close()

    async def get(self, url: str) -> list:
        """base method to fetch api response"""
        response = await self.session.get(url.replace("api_key", random.choice(self.API_KEYS)))

        if response.status == 429:
            raise RateLimitError

        return [response.status, await response.json()]

    async def uuid_name_converter(self, player):
        """converts name to uuid and uuid to name depending on input"""
        if len(player) < 16:  # provided data is uuid
            data = await self.get(f'https://sessionserver.mojang.com/session/minecraft/profile/{player}')
            if data[0] == 400 or data[1]["error"] == "Bad Request":
                raise InvalidPlayer


    async def getFriends(self, player) -> Union[bool, list]:

        """returns the friends list of the provided player (list of uuids)
        if the user doesn't have any friends, returns an empty list"""

        if len(player) < 16:
            pass  # replace name with uuid

        data = await self.get(f"{self.BASE_URL}/friends?key=api_key&uuid={player}")
        data = data[1]

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
        data = data[1]

    async def getRank(self, player):
        """returns the provided player's hypixel rank"""
        data = await self.get(f"{self.BASE_URL}/player?key=api_key&name={player}")
        data = data[1]

        return data

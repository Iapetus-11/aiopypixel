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

    async def get(self, url: str):
        """base method to fetch api response"""

        response = await self.session.get(url.replace("api_key", random.choice(self.API_KEYS)))

        if response.status == 429:
            raise RateLimitError

        return response

    async def uuid_to_name(self, uuid: str):

        if len(uuid) > 16:  # provided data is uuid
            response = await self.get(f'https://sessionserver.mojang.com/session/minecraft/profile/{uuid}')
            if response.status == 400:
                raise InvalidPlayerError
            else:
                data = await response.json()
                return data["name"]

    async def name_to_uuid(self, name: str) -> str:

        response = await self.get(f'https://api.mojang.com/users/profiles/minecraft/{name}')
        if response.status == 204:
            raise InvalidPlayerError
        else:
            data = await response.json()
            return data["id"]

    async def getFriends(self, player: str) -> Union[bool, list]:
        """returns the friends list of the provided player (list of uuids)
        if the user doesn't have any friends, returns an empty list"""

        if len(player) < 16:
            player = await self.name_to_uuid(player)

        data = await (await self.get(f"{self.BASE_URL}/friends?key=api_key&uuid={player}")).json()

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
        """gets hypixel guild data from the provided ID"""

        data = await (await self.get(f"{self.BASE_URL}/friends?key=api_key&id={guild_id}")).json()

    async def getRank(self, player):
        """returns the provided player's hypixel rank"""

        if len(player) < 16:
            player = await self.name_to_uuid(player)

        data = await (await self.get(f"{self.BASE_URL}/player?key=api_key&name={player}")).json()

        return data

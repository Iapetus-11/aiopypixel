import aiohttp
import asyncio
import random


class Client:

    def __init__(self, api_keys):

        # Handles the instance of a singular key
        if not isinstance(api_keys, list):
            api_keys = [api_keys]

        self.API_KEYS = api_keys

        self.BASE_URL = 'https://api.hypixel.net'

        self.session = aiohttp.ClientSession()

    async def exit(self):

        # Safe client cleanup and exit
        await self.session.close()

    async def get(self, url: str) -> dict:

        """base method to fetch api response"""

        response = await self.session.get(url.replace("api_key", random.choice(self.API_KEYS)))

        if response.status == 429:
            pass  # raise errors here

        return await response.json()

    # Returns list of the uuids for the players who are friends with the specified player
    # Returns an empty list if the user is not found.
    async def getFriends(self, player) -> list:

        """returns the friends list of the provided player (list of uuids)
        if the user doesn't have any friends, returns an empty list"""

        if len(player) < 16:
            pass  # replace name with uuid

        data = await self.get(f"{self.BASE_URL}/friends?key=api_key&uuid={player}")

        if not data["success"]:
            pass  # raise error later

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

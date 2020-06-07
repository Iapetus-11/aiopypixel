import aiohttp
import asyncio
from random import choice


class Client:

    def __init__(self, api_keys):
        # Handle using a singular key
        if not isinstance(api_keys, list):
            api_keys = [api_keys]

        self.API_KEYS = api_keys

        self.BASE_URL = 'https://api.hypixel.net'

        self.session = aiohttp.ClientSession()

    async def close(self):
        # Do any cleanup here ig
        await self.session.close()

    async def get(self, url, json=True):
        response = await self.session.get(url.replace("api_key", choice(self.API_KEYS)))
        failed = 0
        while response.status == 429 and failed <= 121:  # 121 to give just a little bit of extra leeway
            await asyncio.sleep(.5)
            response = await self.session.get(url.replace("api_key", choice(self.API_KEYS)))

        if failed > 120:
            # RAISE AN EXCEPTION HERE!
            pass

        if json:
            return await response.json()
        else:
            return response

    # Returns list of the uuids for the players who are friends with the specified player
    async def getFriends(self, player_uuid):
        data = await self.get(f"{self.BASE_URL}/friends?key=api_key&uuid={player_uuid}")
        uuids = []
        for record in data["records"]:
            if record["uuidSender"] != player_uuid:
                uuids.append(record["uuidSender"])
            else:
                uuids.append(record["uuidReceiver"])
        return uuids

    async def getRank(self, player):
        return await self.get(f"{self.BASE_URL}/player?key=api_key&name={player}")

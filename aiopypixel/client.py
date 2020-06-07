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

    async def get(self, url):
        response = await self.session.get(url.replace("api_key", choice(self.API_KEYS)))
        failed = 0
        while response.status == 429 and failed <= 50:
            await asyncio.sleep(.5 + (.05 * failed))  # Will take a total of 86.25 seconds to reach this
            response = await self.session.get(url.replace("api_key", choice(self.API_KEYS)))
        if failed > 50:
            # RAISE AN EXCEPTION HERE!
            pass
        return response

    async def getRank(self, player):
        data = await self.session.get(f'{self.BASE_URL}/player?key=api_key&name={player}')
        data = await data.json()
        print(data)

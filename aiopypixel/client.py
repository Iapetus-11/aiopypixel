import asyncio
import aiohttp


class Client:

    def __init__(self, api_key):
        self.API_KEY = api_key
        self.BASE_URL = 'https://api.hypixel.net'
        self.session = aiohttp.ClientSession()

    async def getRank(self, player):

        data = await self.session.get(f'{self.BASE_URL}/player?key={self.API_KEY}&name={player}')
        data = await data.json()
        print(data)

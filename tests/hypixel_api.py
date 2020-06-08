import os
import random
import dotenv
import asyncio
import aiopypixel

dotenv.load_dotenv()
api_key = os.getenv('api_key')
api_key = random.choice(api_key.split(',')).replace(',', '')
print(api_key)


async def leaderboard():
    client = aiopypixel.Client(api_key)
    print(await client.getLeaderboard())
    await client.close()


async def test_get_friends():
    client = aiopypixel.Client(api_key)
    print(await client.getPlayerFriends("TrustedMercury"))
    await client.close()


async def rank():
    client = aiopypixel.Client(api_key)
    print(await client.getRank("Iapetus11"))
    await client.close()


async def getKeyData():
    client = aiopypixel.Client(api_key)
    await client.getKeyData()
    await client.close()


async def getPlayerGuild():
    client = aiopypixel.Client(api_key)
    await client.getPlayerGuild("TrustedMercury")
    await client.close()


async def getGuildID():
    client = aiopypixel.Client(api_key)
    await client.getGuildID("Iapetus11")
    await client.close()


async def getGuildName():
    client = aiopypixel.Client(api_key)
    await client.getGuildName("TrustedMercury")
    await client.close()


async def getGuildData():
    client = aiopypixel.Client(api_key)
    await client.getGuildName("Iapetus11")
    await client.close()


async def getGameCounts():
    client = aiopypixel.Client(api_key)
    await client.getGameCounts()
    await client.close()

asyncio.get_event_loop().run_until_complete(leaderboard())


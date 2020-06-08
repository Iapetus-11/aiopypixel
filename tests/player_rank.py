import asyncio
import aiopypixel


async def rank():
    client = aiopypixel.Client("a8965b71-df11-468e-8be2-9ec64e56adf0")
    await client.getRank("Iapetus11")
    await client.exit()


asyncio.get_event_loop().run_until_complete(rank())

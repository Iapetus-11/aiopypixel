import asyncio
import aiopypixel


async def test_get_friends():
    client = aiopypixel.Client(["a8965b71-df11-468e-8be2-9ec64e56adf0"])  # Brackets are there for testing
    print(await client.getFriends("cbcfa252867d4bdaa214776c881cf370"))
    await client.close()


asyncio.get_event_loop().run_until_complete(test_get_friends())

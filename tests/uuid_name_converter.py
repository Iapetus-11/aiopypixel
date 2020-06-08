import aiopypixel
import asyncio


async def test_uuid_name_converter():
    client = aiopypixel.Client("a8965b71-df11-468e-8be2-9ec64e56adf0")  # Brackets are there for testing
    print(await client.uuid_name_converter('TrustedMercury'))
    await client.exit()

asyncio.get_event_loop().run_until_complete(test_uuid_name_converter())

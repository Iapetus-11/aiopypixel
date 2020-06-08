import asyncio
import aiopypixel


async def leaderboard():
    client = aiopypixel.Client("a8965b71-df11-468e-8be2-9ec64e56adf0")
    lb = await client.getLeaderboard()

    print(lb)


asyncio.get_event_loop().run_until_complete(leaderboard())

import asyncio
import aiohttp


class AsyncClass:
    def __init__(self):
        self.client = None

    @classmethod
    async def create(cls):
        self = cls()
        async with aiohttp.ClientSession() as session:
            self.client = session
        return self


async def abv():
    obj = await AsyncClass.create()
    print(obj.client)

asyncio.run(abv())

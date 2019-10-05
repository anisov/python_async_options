import asyncio
import aiohttp
import aiofiles
from time import time
import os


async def write_image(data):
    if not os.path.exists('files'):
        os.makedirs('files')
    filename = 'files/file-{}.jpeg'.format(int(time() * 1000))
    async with aiofiles.open(filename, mode='wb') as f:
        await f.write(data)


async def fetch_content(url, session):
    async with session.get(url, allow_redirects=True) as response:
        data = await response.read()
        await write_image(data)


async def main():
    url = 'https://loremflickr.com/320/240'
    tasks = []
    async with aiohttp.ClientSession() as session:
        for _ in range(10):
            task = asyncio.create_task(fetch_content(url, session))
            tasks.append(task)
        await asyncio.gather(*tasks)


if __name__ == '__main__':
    t0 = time()
    asyncio.run(main())
    print(time()-t0)


import os
import uuid
import time

import asyncio
import aiofiles
from aiohttp import ClientSession

url = 'https://loremflickr.com/1920/1080'


async def get_image():
    print('start routine')
    async with ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                f = await aiofiles.open('{}/media/{}.jpg'.format(os.getcwd(), uuid.uuid4()), mode='wb')
                await f.write(await response.read())
                await f.close()


async def run_tasks():
    tasks = [asyncio.ensure_future(get_image()) for _ in range(10)]
    await asyncio.wait(tasks)


ioloop = asyncio.get_event_loop()
start = time.time()
ioloop.run_until_complete(run_tasks())
end = time.time()
print(end - start)
ioloop.close()

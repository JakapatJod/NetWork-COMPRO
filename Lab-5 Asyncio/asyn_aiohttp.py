import aiohttp
import asyncio

async def ioioio():
    async with aiohttp.ClientSession() as ses:
        url = 'http://siamchart.com/stock-chart/itd'
        async with ses.get(url) as r:
            print('url:', r.url)
            print('status:', r.status)
            print('content_type:', r.content_type)

asyncio.run(ioioio())

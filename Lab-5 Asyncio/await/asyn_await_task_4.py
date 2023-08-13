import asyncio 

async def buaklek(a,b):
    c = a+b
    print('====== เริ่มทำงาน ======')
    return c


async def main():
    coru = buaklek(13,10)
    task = asyncio.create_task(coru)
    phonbuak = await task
    print('ได้ผลบวก %s'%phonbuak)

maincoru = main()
asyncio.run(maincoru)
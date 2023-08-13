import asyncio

async def hanlek(a,b):
    print('%s/%s'%(a,b))
    return a/b

loop = asyncio.get_event_loop() # สร้าง loop
phonhan = loop.run_until_complete(hanlek(7,6)) # เอา loop มา run
print('result : %.3f'%phonhan)
import asyncio

async def main():
    print('watcharachai')
    await foo('text')
    print('finished')
    
async def foo(text):
    print(text)
    await asyncio.sleep(5)


asyncio.run(main())
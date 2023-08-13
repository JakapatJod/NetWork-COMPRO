import asyncio

async def main():
    print('watcharachai')
    task = asyncio.create_task(foo('text'))
    print('finished')

async def foo(text):
    print(text)
    await asyncio.sleep(5)

asyncio.run(main())
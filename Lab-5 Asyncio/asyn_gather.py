import asyncio,time

async def ioioio(wela,chue_ngan):
    print('เริ่ม %s เวลาผ่านไปแล้ว %.5f วินาที'%(chue_ngan,time.time()-t0))
    await asyncio.sleep(wela)
    print('%s เสร็จแล้ว เวลาผ่านไปแล้ว %.5f วินาที'%(chue_ngan,time.time()-t0))
    return

async def main():
    cococoru = [ioioio(2, 'เต้าหู้'), ioioio(3.5, 'เค้ก'), ioioio(3, 'ไส้กรอก'), ioioio(1, 'ครัวซอง')]
    phonlap = await asyncio.gather(*cococoru)
    print(phonlap)
t0 = time.time()
asyncio.run(main())
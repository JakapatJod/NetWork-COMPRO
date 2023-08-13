import asyncio,time

async def ioioio(wela,chue_ngan):
    print('เริ่ม %s เวลาผ่านไปแล้ว %.5f วินาที'%(chue_ngan,time.time()-t0))
    await asyncio.sleep(wela)
    print('%s เสร็จแล้ว เวลาผ่านไปแล้ว %.5f วินาที'%(chue_ngan,time.time()-t0))
    return

async def main():
    print('เริ่มต้นฟังก์ชัน')
    phara1 =  asyncio.create_task(ioioio(1.5,'โหลดเพลง'))
    phara2 =  asyncio.create_task(ioioio(1.5,'โหลดอนิเมะ'))
    phara3 =  asyncio.create_task(ioioio(1.5,'โหลดหนัง'))
    print('สร้างภารกิจเสร็จแล้ว')
    await phara2
    print('สิ้นสุดฟังก์ชัน')

t0 = time.time()
asyncio.run(main())

    
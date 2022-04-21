import asyncio

async def firstWorker():
    while True:
        await asyncio.sleep(0.5)
        print("First Worker Executed")

async def secondWorker():
    x=1
    while x<=2:
        x+=1
        await asyncio.sleep(1.5)
        print("Second Worker Executed")
    print(x)

loop = asyncio.get_event_loop()

try:
    asyncio.ensure_future(firstWorker())
    asyncio.ensure_future(secondWorker())
    loop.run_forever()
except KeyboardInterrupt:
    pass
finally:
    print("Closing Loop")
    loop.close()
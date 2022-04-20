import asyncio

async def main():
    print("will sleep")
    await asyncio.sleep(100)
    print("done sleep")

asyncio.run(main())

print("this is async")
import asyncio

# This method represents your blocking code
def blocking(loop, queue):
    import time
    while True:
        loop.call_soon_threadsafe(queue.put_nowait, 'Blocking A')
        time.sleep(2)
        loop.call_soon_threadsafe(queue.put_nowait, 'Blocking B')
        time.sleep(2)

# This method represents your async code
async def nonblocking(queue):
    await asyncio.sleep(1)
    while True:
        queue.put_nowait('Non-blocking A')
        await asyncio.sleep(0.5)
        queue.put_nowait('Non-blocking B')
        await asyncio.sleep(0.5)

# The main sets up the queue as the communication channel and synchronizes them
async def main():
    queue = asyncio.Queue()
    loop = asyncio.get_running_loop()

    blocking_fut = loop.run_in_executor(None, blocking, loop, queue)
    nonblocking_task = loop.create_task(nonblocking(queue))

    running = True  # use whatever exit condition
    while running:
        # Get messages from both blocking and non-blocking in parallel
        message = await queue.get()
        # You could send any messages, and do anything you want with them
        print(message)

asyncio.run(main())

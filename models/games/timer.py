import threading
import time
import asyncio

class Timer(object):

    def __init__(self, seconds, end_method,loop ):
        self.seconds = seconds
        self.start_time = time.time()
        self.finished = False
        self.loop = loop
        self.end_method = end_method

        # file deepcode ignore MissingAPI: <please specify a reason of ignoring this>
        thread = threading.Thread(target=self.run, args=[self.loop])

        thread.daemon = True
        thread.start()

    def run(self,loop):
        while not self.finished :
            if time.time() - self.start_time >= self.seconds:
                self.finished = True
        asyncio.run_coroutine_threadsafe(self.end(), loop)

    async def end(self):
        await self.end_method()

    def stop(self):
        self.finished = True
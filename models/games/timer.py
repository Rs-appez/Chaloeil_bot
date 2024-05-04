import threading
import time
import asyncio
import math
class Timer(object):

    def __init__(self, seconds, end_method, time_msg ,loop ):
        self.seconds = seconds
        self.start_time = time.time()
        self.finished = False
        self.loop = loop
        self.end_method = end_method
        self.time_msg = time_msg

        self.last_second = 0

        # file deepcode ignore MissingAPI: <please specify a reason of ignoring this>
        thread = threading.Thread(target=self.run, args=[self.loop])

        thread.daemon = True
        thread.start()

    def run(self,loop):
        while not self.finished :
            if time.time() - self.start_time >= self.seconds:
                self.finished = True
            if math.floor(time.time() - self.start_time) != self.last_second:
                self.last_second = math.floor(time.time() - self.start_time)
                asyncio.run_coroutine_threadsafe(self.edit(), loop)

        asyncio.run_coroutine_threadsafe(self.end(), loop)

    async def end(self):
        await self.end_method()
    
    async def edit(self):
        s_text = "secondes" if self.seconds - self.last_second > 1 else "seconde"
        await self.time_msg.edit(content=f"‎ ‎\n**Temps restant : {self.seconds - self.last_second} {s_text}**")

    def stop(self):
        self.finished = True
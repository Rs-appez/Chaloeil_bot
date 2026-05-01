import threading
import time
import asyncio
import math


class Timer(object):
    def __init__(self, seconds, end_method, time_msg, loop=None):
        self.seconds = seconds
        self.end_method = end_method
        self.time_msg = time_msg
        self.finished = False
        self._editing = False
        self._task = asyncio.create_task(self.run())

    async def run(self):
        start = time.monotonic()
        last_displayed = self.seconds + 1

        while not self.finished:
            elapsed = time.monotonic() - start
            remaining = max(0, self.seconds - elapsed)
            remaining_int = int(remaining) + (1 if remaining % 1 > 0 else 0)

            if remaining_int < last_displayed:
                last_displayed = remaining_int
                if not self._editing:
                    _ = asyncio.create_task(self._edit(remaining_int))

            if elapsed >= self.seconds:
                break

            await asyncio.sleep(0.3)

        if not self.finished:
            self.finished = True
            await self.end_method()

    async def _edit(self, remaining):
        self._editing = True
        s_text = "seconde" if remaining <= 1 else "secondes"
        try:
            await self.time_msg.edit(
                content=f"‎ ‎\n**Temps restant : {remaining} {s_text}**"
            )
        except Exception:
            pass
        finally:
            self._editing = False

    def stop(self):
        if not self.finished:
            self.finished = True
            self._task.cancel()
            asyncio.create_task(self.end_method())

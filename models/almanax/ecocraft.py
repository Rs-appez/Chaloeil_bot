import httpx
from httpx import Timeout

import config


class EcoCraft:
    api_url: str = config.BACKEND_URL + "almanax/api/economy-entries/"

    headers: dict[str, str] = {"Authorization": config.BACKEND_TOKEN}

    timeout = Timeout(30.0, connect=10.0)

    def __init__(self, job: str):
        self.job = job

    async def get_date(self) -> tuple[int, int]:
        async with httpx.AsyncClient(
            headers=self.headers, timeout=self.timeout
        ) as client:
            res = await client.get(self.api_url + "get_job/", params={"job": self.job})
            res.raise_for_status()
            data = res.json()
        return (data.get("day"), data.get("month"))

    @staticmethod
    async def get_all_dates() -> list[tuple[str, int, int]]:
        data = []
        async with httpx.AsyncClient(
            headers=EcoCraft.headers, timeout=EcoCraft.timeout
        ) as client:
            url: str | None = EcoCraft.api_url
            while url:
                res = await client.get(url)
                res.raise_for_status()
                res_json = res.json()
                data.extend(res_json.get("results", []))
                url = res_json.get("next")
        return [
            (entry.get("bonus"), entry.get("day"), entry.get("month")) for entry in data
        ]
